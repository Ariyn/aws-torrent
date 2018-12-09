import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Volume import *
import datetime

class Test(unittest.TestCase):
	def setUp(self):
		self.v = Volume("e408cc", "vol-051ca250b25bc990b", DeviceName="/dev/xvdk")

	def test_Volume(self):
		self.assertIsNotNone(self.v)

	def test_VolumeIsAttached(self):
		x = self.v.isAttached()

	def test_VolumeState(self):
		status, ret = self.v.state()

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
