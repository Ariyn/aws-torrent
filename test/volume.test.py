import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Volume import *
import datetime

resultSample = {'State': 'creating', 'Iops': 100, 'CreateTime': datetime.datetime(2018, 1, 31, 7, 51, 55, 401000), 'VolumeId': 'vol-0c1369454803ca3aa', 'AvailabilityZone': 'ap-northeast-2c', 'Tags': [{'Value': 'torrent', 'Key': 'type'}, {'Value': 'torrent-2be50b', 'Key': 'name'}, {'Value': 'aty6ep', 'Key': 'hash'}], 'Encrypted': False, 'SnapshotId': '', 'ResponseMetadata': {'RequestId': '6f37e7f2-5375-4e6e-a41f-9d8038a822f5', 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'vary': 'Accept-Encoding', 'server': 'AmazonEC2', 'transfer-encoding': 'chunked', 'date': 'Wed, 31 Jan 2018 07:51:54 GMT'}, 'RetryAttempts': 0, 'HTTPStatusCode': 200}, 'VolumeType': 'gp2', 'Size': 10, "DeviceName":"/dev/xvdk"}

class Test(unittest.TestCase):
	def setUp(self):
		self.v = Volume("e408cc", "vol-051ca250b25bc990b", DeviceName="/dev/xvdk")

	def test_Volume(self):
		self.assertIsNotNone(self.v)

	def test_VolumeIsAttached(self):
		x = self.v.isAttached()

	def test_VolumeState(self):
		status, ret = self.v.state()

	def test_VolumeAllocate(self):
		return True
		x = VM.allocNewVolume(resultSample)
		print(x.size, x.deviceName)

	def test_VolumeAttach(self):
		x = self.v.attach(VM.instance["id"])
		print("attach", x)

	def test_detachVolume(self):
		x = self.v.detach()
		print("detach", x)

	def test_deleteVolume(self):
		self.v.detach()
		print("detaching!!")
		VM.waitDetach(self.v)
		x = self.v.delete()
		print("delete", x)

if __name__ == "__main__":
	unittest.main()
