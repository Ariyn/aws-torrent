import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Volume_refactory import Volume
import datetime, time, subprocess

instanceId = "i-0d95f7b47ba724311"
class moduleTest(unittest.TestCase):
	def test_staticMethod(self):
		x = Volume()
		
	def test_volumeInitialze(self):
		x = Volume("615a3f")
		
	def test_getFalse(self):
		x = Volume.get(uid="ec2800")
		self.assertEqual(x,[])
		
	def test_attach(self):
		x = Volume.get(uid="615a3f")

		if x and not x.isAttached():
			x.attach(instanceId)
	
	def test_detach(self):
		x = Volume.get("615a3f")
#		 print(x.deviceId, x.)
		if x and x.isAttached():
			ret = x.detach()
			print(ret)
#		 self.assertFalse(x.isAttached())
#		 print(x.volumeId, x.size, x.uid)

	def test_delete(self):
		x = Volume.get("615a3f")
		if x:
			x.remove_test()
	
	def test_release(self):
		for i in ["134545", "1584f2"]:
			x = Volume.get(uid=i)
			if x:
				if x.isAttached():
					x.detach()
					x.waitDetach()
				x.delete()
		
#	 def test_createAndRelease(self):
#		 x = Volume.create(1)
#		 result = x.release()
#		 print(result)

	def test_getFreeDeviceName(self):
		deviceName = Volume.getFreeDeviceName(instanceId)
		self.assertNotEqual(deviceName, "")
		
		self.assertEqual("".join(set("abcd")-set("abcd")), "")

class IntegrationTest(unittest.TestCase):
	def tearDown(self):
		x = Volume.get(volumeFilter=[{
			"Name":"tag:Debug",
			"Values":["true"]
		}])
		for i in x:
			if i.isMounted():
				i.umount()
				
			if i.isAttached():
				i.detach()
				i.waitDetach()
				
			i.delete()
			
	def test_pass(self):
		pass
	
	def test_mountInfo(self):
		v = Volume.get("bf5a6a")
		self.assertEqual(v.mountPath, "%s/%s"%(Volume.mountPoint, v.uid))
# 		print(v.mountPath, v.isMounted())
	
	@unittest.skip("skipping")
	def test_mount(self):
		v = Volume.create(1, tags = [("Debug","false")])
		uid = v.uid
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
		
if __name__ == "__main__":

	moduleSuite = unittest.TestSuite()
	moduleSuite.addTest(unittest.makeSuite(moduleTest))
	
	integSuite = unittest.TestSuite()
	integSuite.addTest(unittest.makeSuite(IntegrationTest))
	
	runner=unittest.TextTestRunner()
	runner.run(integSuite)