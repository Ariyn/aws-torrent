
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError

from random import shuffle, sample
import string
import math
import hashlib
import json
import time
import os
import subprocess

os.environ["HOME"] = "/home/wssh/"
ec2 = boto3.client("ec2")
ec2Methods = {i:ec2.__getattribute__(i) for i in [
		"describe_volumes",
		"describe_volume_status",
		"create_volume",
		"attach_volume",
		"detach_volume",
		"delete_volume"
	]}
class Volume:
	mountPoint, deviceNames, defaultSize = "/mnt", "fghijklmnopqrstuvwxyz", 10
	defaultTags = [
		{
			'Key': 'Name',
			'Value': ''
		},
		{
			'Key': 'Hash',
			'Value': ''
		},
		{
			'Key': 'Type',
			'Value': ''
		}
	]
	randomString = lambda:sample(string.ascii_lowercase+string.digits, 6)
	availabilityZone, instanceId = "ap-northeast-2c", ""
	
	def invoke(method):
		method = ec2Methods[method]
		def _(f):
			def __(*args, **kwargs):
				return method(**f(*args, **kwargs))
			return __
		return _
	
	def waiter(name, delay=5, maxAttempts=6):
		waiter = ec2.get_waiter(name)
		def _(f):
			def __(*args, **kwargs):
				kwargs = f(*args, **kwargs) 
				kwargs["WaiterConfig"] = {
					"Delay":delay,
					"MaxAttempts":maxAttempts
				}
				return waiter.wait(**kwargs)
			return __
		return _
	
	def __init__(self, uid=None, **kwargs):
		self.volumeId, self.size = "", 0
		self.tags, self.hash, self.uid = {}, "", ""
		self.mountPath, self.deviceId, self.instanceId = "", "", ""
		self.attachment, self.state = {}, "Unallocated"
		self.createdTime = ""
		kwargs["uid"] = uid
		
		self.__allocInfo__(kwargs)
		self.__mountInfo__()
	
	def __mountInfo__(self):
		mounts = subprocess.check_output(["mount"]).decode("utf-8").split("\n")
		mounts = [i for i in mounts if self.deviceId and i.startswith(self.deviceId)]
		if mounts:
			self.mountPath = mounts[0].replace(self.deviceId+" on ", "").split(" ")[0]
			
			
	def __allocInfo__(self, kwargs):
		if "VolumeId" in kwargs:
			self.volumeId = kwargs["VolumeId"]
		
		if "Tags" in kwargs:
			self.tags = {i["Key"]:i["Value"] for i in kwargs["Tags"]}
			self.hash, self.uid = self.tags["Hash"], self.tags["Hash"][:6]
		
		if "Size" in kwargs:
			self.size = kwargs["Size"]
			
		if "Hash" in kwargs:
			self.hash, self.uid = kwargs["Hash"], kwargs["Hash"][:6]
			
		if "Attachments" in kwargs:
			attach = {}
			for i in kwargs["Attachments"]:
				if i["InstanceId"] not in attach:
					attach[i["InstanceId"]] = []
				attach[i["InstanceId"]].append(i)
				self.deviceId = i["Device"]
				self.instanceId = i["InstanceId"]
			
			self.attachment = attach
		
		if "State" in kwargs:
			self.state = kwargs["State"]
			
		if "CreatedTime" in kwargs:
			self.createdTime = kwargs["CreatedTime"]
		
	@waiter("volume_available", delay=5, maxAttempts=6)
	def waitCreate(self):
		return {
			"VolumeIds":[self.volumeId]
		}
	@waiter("volume_available", delay=10, maxAttempts=6)
	def waitDetach(self):
		return {
			"VolumeIds":[self.volumeId]
		}
	 
	@waiter("volume_deleted", delay=5, maxAttempts=6)
	def waitDelete(self):
		return {
			"VolumeIds":[self.volumeId]
		}
	
	@waiter("volume_in_use", delay=5, maxAttempts=6)
	def waitAttach(self):
		return {
			"VolumeIds":[self.volumeId],
			"Filters":[{
				"Name":"attachment.status",
				"Values":["attached"]
			}]
		}
	
	@invoke("delete_volume")
	def delete(self):
		kwargs = {
			"VolumeId":self.volumeId
		}
		return kwargs
	
	@invoke("attach_volume")
	def attach(self, instanceId, deviceId=None):
		self.instanceId = instanceId		
		if not deviceId:
			deviceId = Volume.getFreeDeviceName(instanceId)
			
		self.deviceId = deviceId
		
		kwargs = {
			"Device":deviceId,
			"InstanceId":instanceId,
			"VolumeId":self.volumeId
		}
		return kwargs
	
	def isAttached(self):
		return self.attachment != {}
	
	@invoke("detach_volume")
	def detach(self):
		kwargs = {
			"VolumeId":self.volumeId,
			"Device":self.deviceId,
			"InstanceId":self.instanceId,
			"Force":True
		}
		return kwargs

	@staticmethod
	def staticInvoke(method, kwargs):
		return ec2Methods[method](**kwargs)
	
	@staticmethod
	def get(uid=None, volumeId=None, volumeFilter=[]):
		kwargs = {
			"Filters":[{
				"Name":"tag:Type",
				"Values":["torrent"]
			}]
		}
		if uid:
			kwargs["Filters"].append({
				"Name":"tag:Name",
				"Values":["torrent-%s"%uid]
			})
		if volumeId:
			kwargs["VolumeIds"] = [volumeId]
		if volumeFilter:
			kwargs["Filters"] = kwargs["Filters"]+volumeFilter

		retVal = [Volume(**i) for i in Volume.staticInvoke("describe_volumes", kwargs)["Volumes"]]
		
		if retVal and uid:
			retVal = retVal[0]
			
		return retVal if retVal else []
	
	@staticmethod
	def getFreeDeviceName(instanceId=instanceId):
		import functools
		retVal = Volume.get(volumeFilter = [{
			"Name":"attachment.instance-id",
			"Values":[instanceId]
		}])

		retVal = [[j["Device"] for j in i.attachment[instanceId]] for i in retVal]
		retVal = map(lambda x:x[-1], functools.reduce(lambda x,y :x+y, retVal))
		retVal = sample(set(Volume.deviceNames) - set(retVal), 1)[0]
		return "/dev/xvd"+retVal
	
	@staticmethod
	def create(size, hash=None, tags=[]):
		if not hash:
			sha, rs = hashlib.sha256(), Volume.randomString()
			shuffle(rs)
			sha.update("".join(rs).encode("utf-8"))
			hash = sha.hexdigest()
		
		
		tags = [{"Key":i[0],"Value":i[1]} for i in tags]
		uid = hash[:6]
		kwargs = {
			"AvailabilityZone":Volume.availabilityZone,
			"Size":size,
			"VolumeType":"gp2",
			"TagSpecifications":[{
				"ResourceType":"volume",
				"Tags": [{
					"Key":"Type",
					"Value":"torrent"
				}, {
					"Key":"Name",
					"Value":"torrent-%s"%uid,
				}, {
					"Key":"Hash",
					"Value":hash
				}]+tags
			}]
		}
		
		retVal = Volume(**Volume.staticInvoke("create_volume", kwargs))
		return retVal
	
	def popFstab(self):
		if self.deviceId != "":
			fstab = open("/etc/fstab","r").read().split("\n")
			fstab = [v for v in fstab if self.deviceId not in v]
			x = open("/etc/fstab","w").write("\n".join(fstab))

	def appendFstab(self):
		if self.deviceId != "":
			x = open("/etc/fstab","a")
			x.write("\n%s %s %s %s %d %d"%(self.deviceId, self.mountPath, "ext4", "defaults", 0, 0))
			x.close()

	def mount(self):
		deviceName = self.deviceId
		mountPath = "%s/%s"%(self.mountPoint, self.uid)
		x = subprocess.check_output(["sudo", "file", "-s", deviceName]).decode("utf-8")
		
		if ("%s: data"%deviceName) in x:
			p = subprocess.Popen(("sudo mkfs -t ext4 %s"%deviceName).split(" "))
			p.wait()

		p = subprocess.Popen(("sudo mkdir %s"%mountPath).split(" "))
		p.wait()

		
		p = subprocess.Popen(("sudo mount -t ext4 %s %s"%(deviceName, mountPath)).split(" "))
		p.wait()
		
		subprocess.Popen(("sudo chmod 777 %s"%mountPath).split(" "))
		p.wait()
		
		self.mountPath = mountPath
		self.appendFstab()

		return self.mountPath

	def umount(self):
		mountPath = self.mountPath
		self.mountPath = ""
		print(mountPath)
		subprocess.check_output(("sudo umount %s"%mountPath).split(" "))
# 		time.sleep(1)
		self.popFstab()
		
	def isMounted(self):
		return self.mountPath != ""

	
	
# default form
# {
# 	'Attachments': [
# 			{
# 					'AttachTime': datetime(2015, 1, 1),
# 					'Device': 'string',
# 					'InstanceId': 'string',
# 					'State': 'attaching'|'attached'|'detaching'|'detached'|'busy',
# 					'VolumeId': 'string',
# 					'DeleteOnTermination': True|False
# 			},
# 	],
# 	'AvailabilityZone': 'string',
# 	'CreateTime': datetime(2015, 1, 1),
# 	'Encrypted': True|False,
# 	'KmsKeyId': 'string',
# 	'Size': 123,
# 	'SnapshotId': 'string',
# 	'State': 'creating'|'available'|'in-use'|'deleting'|'deleted'|'error',
# 	'VolumeId': 'string',
# 	'Iops': 123,
# 	'Tags': [
# 			{
# 					'Key': 'string',
# 					'Value': 'string'
# 			},
# 	],
# 	'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1'
# },