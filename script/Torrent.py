from random import sample

from urllib.request import Request, urlopen
from urllib.error import HTTPError

import json, base64
import sys, os, subprocess, time

class Transmission:
	tag = int("".join([str(v) for v in sample([0,1,2,3,4,5,6,7,8,9], 6)]))
	
	def __init__(self, server="127.0.0.1", port=9091, id="transmission", passwd="pw4transmission", https=False, pathToRPC="transmission/rpc"):
		self.server = "http%s://%s:%s/%s"%("s" if https else "", server, str(port), pathToRPC)
		self.sessionId = ""
		self.id, self.passwd = id, passwd
		self.authInfo = "%s:%s"%(id, passwd)
		self.bAuthInfo = base64.b64encode(self.authInfo.encode("utf-8")).decode("utf-8")
		
	def auth(f):
		def _(*args, **kwargs):
			req = Request(url=tr.server, headers = {
				"X-Transmission-Session-Id":tr.sessionId,
				"Authorization":"Basic %s"%tr.bAuthInfo
			})
			
			try:
				res = urlopen(req)
			except HTTPError as e:
				if e.code == 401:
					#this means wrong id or password
					pass
				elif e.code == 409:
					tr.sessionId = e.headers.get("X-Transmission-Session-Id")
			
			return f(*args, **kwargs)
		return _
	
	def fields(*args):
		def _(f):
			def __(self, *_args, **kwargs):
				if "arguments" not in kwargs:
					kwargs["arguments"] = {}
				kwargs["arguments"]["fields"] = args
				return f(self, *_args, **kwargs)
			return __
		return _

	def input(*args, **kwargs):
		def _(f):
			def __(*_args, **_kwargs):
				if "arguments" not in _kwargs:
					_kwargs["arguments"] = {}
				for i in args:
					if i in _kwargs:
						_kwargs["arguments"][i.replace("_", "-")] = _kwargs[i]
				return f(*_args, **_kwargs)
			return __
		return _

	def ids(f):
		def _(self, *args, **kwargs):
			if "arguments" not in kwargs:
				kwargs["arguments"] = {}
			kwargs["arguments"]["ids"] = [self.id]
# 			kwargs["ids"]
			return f(self, *args, **kwargs)
		return _
	
	def deleteLocalData(f):
		def _(self, *args, **kwargs):
			if "arguments" not in kwargs:
				kwargs["arguments"] = {}
			kwargs["arguments"]["delete-local-data"] = True
			return  f(self, *args, **kwargs)
		return _
	
	def arguments(**kwargs):
		def _(f):
			def __(*args, **_kwargs):
				if "arguments" not in _kwargs:
					_kwargs["arguments"] = {}
				for i in kwargs:
					_kwargs["arguments"][i] = kwargs[i]
			
				return  f(*args, **_kwargs)
			return __
		return _
		
	def invoke(method):
		def _(f):
			def __(*args, arguments = {}, **kwargs):
				req = Request(url = tr.server, headers = {
					"X-Transmission-Session-Id":tr.sessionId,
					"Authorization":"Basic %s"%tr.bAuthInfo
				}, data = json.dumps({
					"arguments": {
						i : v for i,v in arguments.items()
					}, "method": method,
					"tag":tr.tag
				}).encode("utf-8"))
				
				res = urlopen(req)
				data = json.loads(res.read().decode("utf-8"))
				
				if method == "torrent-set-location":
					print(req.data)
# 				print(len(args), args)
				return f(*args, data=data, **kwargs)
			return __
		return _

tr = Transmission(port=8080)

class Torrent:
	B, KB, MB, GB = 1024, 1024*1024, 1024*1024*1024, 1024*1024*1024*1024
	statusKey = {
		0		:"PAUSED",  # Torrent is stopped
		1		:"CHECK_WAIT",  # Queued to check files
		2		:"CHECK",  # Checking files
		3 	:"DOWNLOAD_WAIT",  # Queued to download
		4		:"DOWNLOAD",  # Downloading
		5		:"SEED_WAIT",  # Queued to seed
		6		:"SEED",  # Seeding
		7		:"ISOLATED",  # Torrent can't find peers
		8		:"STOPPED" # for dev
	}
	
	def __init__(self, **kwargs):
		self.__info__(**kwargs)
		
	def __info__(self, magnetLink=None, tFile = None, hashString=None, name=None, id=-1, totalSize=0, status="stopped", percentDone=0, files=[], downloadDir="", **kwargs):
		self.magnetLink, self.hash = magnetLink, magnetLink.split("btih:")[1].split("&")[0] if not hashString else hashString
		self.name, self.id = name, id
		self.totalSize, self.status, self.statusString, self.percentDone = totalSize, status, self.statusKey[status], round(percentDone*100,1)
		self.files, self.downloadDir = files, downloadDir if (downloadDir and downloadDir[-1] != "/") else downloadDir[:-1]

		self.readableUnit = "B" if totalSize < self.B else "KB" if totalSize < self.KB else "MB" if totalSize < self.MB else "GB"
		self.readableSize = round(totalSize /(1 if totalSize < self.B else self.B if totalSize < self.KB else self.KB if totalSize<self.MB else self.MB if totalSize<self.GB else self.GB), 1)
		self.gigaSize = self.readableSize / (1 if self.readableUnit == "GB" else 1024 if self.readableUnit == "MB" else 1024*1024 if self.readableUnit == "KB" else 1024*1024*1024)

		if self.status == 0 and self.percentDone == 1:
			self.status, self.statusString = 8, self.statusKey[8]
			
	def __str__(self):
		return "%d) %s - %.1lf%s %.1lf%% done @%s\t\t:%s"%(self.id, self.name, self.readableSize, self.readableUnit, self.percentDone, self.statusString, self.hash)
	
	def waitAdd(self):
		added, count = False, 0

		while (not added) and count < 20:
			self.update()
			if self.totalSize != 0:
				added = True
				
			count = count + 1
			time.sleep(2)

		return added
	
	@staticmethod
	@Transmission.auth
	@Transmission.arguments(fields=["error", "errorString", "eta", "id", "isFinished", "leftUntilDone", "name", "rateDownload", "sizeWhenDone", "status", "hashString", "magnetLink", "totalSize", "percentDone", "downloadDir", "files"])
	@Transmission.invoke("torrent-get")
	def get(id=None, hash=None, data=[]):
		data = data["arguments"]["torrents"]
		retVal = []
		for i in data:
			if id and i["id"] == id:
				retVal.append(Torrent(**i))
			elif hash and hash in i["magnetLink"]:
				retVal.append(Torrent(**i))
			elif not hash and not id and i:
				retVal.append(Torrent(**i))

		if retVal and (hash or id):
			retVal = retVal[0]
		
		return retVal if retVal else None
	
	@Transmission.auth
	@Transmission.arguments(fields=["error", "errorString", "eta", "id", "isFinished", "leftUntilDone", "name", "rateDownload", "sizeWhenDone", "status", "hashString", "magnetLink", "totalSize", "percentDone", "downloadDir", "files"])
	@Transmission.invoke("torrent-get")
	def update(self, data=[]):
		data = data["arguments"]["torrents"]
		retVal = []
		for i in data:
			if self.id and i["id"] == self.id:
				retVal.append(i)
				
		retVal = retVal[0]
		self.__info__(**retVal)
	
	@Transmission.auth
	@Transmission.ids
	@Transmission.invoke("torrent-stop")
	def stop(self, data=None, **kwargs):
		return data
	
	@Transmission.auth
	@Transmission.ids
	@Transmission.invoke("torrent-start")
	def start(self, data=None, **kwargs):
		return data
	
	@Transmission.auth
	@Transmission.ids
	@Transmission.input("location")
	@Transmission.arguments(move=True)
	@Transmission.invoke("torrent-set-location")
	def moveTo(self, *arg, data=None, **kwargs):
		self.update()
		return data
	
	@staticmethod
	@Transmission.auth
	@Transmission.input("cookies","download_dir","filename","metainfo","paused","peer_limit","bandwidthPriority","files_wanted","files_unwanted","priority_high","priority_low","priority_normal")
	@Transmission.invoke("torrent-add")
	def add(*args, data=None, **kwargs):
		data = data["arguments"]
		if "torrent-added" in data:
			return Torrent.get(id=data["torrent-added"]["id"])
		else:
			return None
	
	@Transmission.ids
	@Transmission.deleteLocalData
	@Transmission.invoke("torrent-remove")
	def removeTorrentAndFile(self, *args, data, **kwargs):
		return data

	@Transmission.ids
	@Transmission.input("location")
	@Transmission.arguments(move=False)
	@Transmission.invoke("torrent-set-location")
	def setLocation(self, *args, data, **kwargs):
		print("removing")
		return data