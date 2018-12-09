#! /usr/bin/python3

import os
import json
import boto3
import time
from zipfile import ZipFile
from datetime import datetime

from Volume import Volume
from Torrent import Torrent

instanceId = "i-"
defaultSIZE = 10
datas = {
	"name":"TR_TORRENT_NAME",
	"hash":"TR_TORRENT_HASH",
	"dir":"TR_TORRENT_DIR"
}
maxSize = 400*1024*1024


#### USER debian-transmission
#### add s3 region

def summTorrentSize(target=None):
	torrentSize = {}

	for i in Torrent.get():
		if i.downloadDir not in torrentSize:
			torrentSize[i.downloadDir] = []
		torrentSize[i.downloadDir].append(i)

	torrentSize = {i:sum([j.gigaSize for j in v]) for i,v in torrentSize.items() if (target and i == target) or not target}
	return torrentSize

def summVolumeSize(target=None):
	volumes = Volume.get(volumeFilter = [{
		"Name":"attachment.instance-id",
		"Values":[instanceId]
	}])
	volumeSize = {i.mountPath:i.size for i in volumes if (target and i == target) or not target}

	return volumeSize

def summLeftSize(target=None):
	vs, ts = summVolumeSize(target), summTorrentSize(target)
	leftSize = {i:(v,0) if i=="/mnt/torrent-temp" else (v, v-ts[i]) if i in ts else (v, v) for i,v in vs.items()}
# 	leftSize["/mnt/torrent-temp"] = (leftSize["/mnt/torrent-temp"][0], leftSize["/mnt/torrent-temp"][0])
	return leftSize[target] if target else leftSize

def allocateNewVolume(size):
	size = max(size, defaultSIZE)
	v = Volume.create(size, tags = [("Debug","false")])
	print("created %s(%s) @ %s-%d GB"%(
		v.volumeId,
		v.uid,
		v.deviceId,
		v.size
	))

	v.waitCreate()
	v.attach(instanceId)
	v.waitAttach()
	path = v.mount()

	return path

def newTorrent(magnet):
	t = Torrent.add(filename=magnet, download_dir="/mnt/torrent-temp/")
	t.waitAdd()
	print(t)

	x = summLeftSize()
	volumeSize = x[t.downloadDir]

	if volumeSize[1] <= 0:
		t.stop()
		moved=False
		for i,v in x.items():
			if t.gigaSize <= v[1]:
				moved, path = True, i
		if not moved:
			path = allocateNewVolume(t.gigaSize)

		t.moveTo(location=path)
		time.sleep(2)
		t.start()

	if 5 < len(Torrent.get()):
		t.stop()

def done():
	s3Bucket = "videos.ismin.uk"
	name, hash = os.environ[datas["name"]], os.environ[datas["hash"]]
	path = os.environ[datas["dir"]]

	torrent = Torrent.get(hash=hash)
# 	print(torrent)
	fileList = torrent.files
# 	print(torrent.totalSize, len(torrent.files))
	if (torrent.totalSize < maxSize or 50 <= len(torrent.files)) and len(torrent.files) != 1:
		fileList = [compress(path, name, fileList)]
	else:
		fileList = [i["name"] for i in fileList]

	upload(s3Bucket, path, fileList)

	torrent.removeTorrentAndFile()
	tList = Torrent.get()
	runningList, stopList = [i for i in tList if i.statusString == "DOWNLOAD"], [i for i in tList if i.statusString == "PAUSED"]
	if len(runningList)<5:
		for i in range(0,min(len(stopList), 5-len(runningList))):
			stopList[i].start()

	releaseCheck()

def compress(path, name, fileList):
	fileName = "%s/%s.zip"%(path, name)

	z = ZipFile(fileName, "w")

	for i in fileList:
		z.write(path+"/"+i["name"], i["name"])

	ret = z.testzip()
	if ret is not None:
		print("File error")
	z.close()

	return "%s.zip"%name

def upload(bucket, path, fileList):
	s3 = boto3.client("s3")
	for i in fileList:
		print("uploading %s"%i)
		s3.upload_file(path+"/"+i, bucket, i)

def releaseCheck():
	volumes = summLeftSize()
	print(volumes)
	emptyVolumes = [(i, v) for i, v in volumes.items() if v[1] == v[0]]
	for i in emptyVolumes:
		v = Volume.get(uid=i[0][5:])
		if not v:
			continue

		v.umount()
		v.detach()
		v.waitDetach()
		v.delete()
# 		v.waitDelete()

if __name__ == "__main__":
	done()
