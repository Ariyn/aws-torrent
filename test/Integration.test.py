import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Volume import Volume
from Torrent import Torrent
import Controller as ctrl
import datetime, time, subprocess

datas = {
	"name":"TR_TORRENT_NAME",
	"hash":"TR_TORRENT_HASH",
	"dir":"TR_TORRENT_DIR"
}
magnet = "magnet:?"
magnets = ["magnet:?"]
instanceId = "i-"

class integTest(unittest.TestCase):
	def test_calculateTorrentSize(self):
		results = Torrent.get()
		torrentSize = {}
		for i in results:
			if i.downloadDir not in torrentSize:
				torrentSize[i.downloadDir] = []
			torrentSize[i.downloadDir].append(i)

		torrentSize = {i:sum([j.gigaSize for j in v]) for i,v in torrentSize.items()}
# 		print(torrentSize)

	def test_calculateVolumeSize(self):
		volumes = Volume.get(volumeFilter = [{
			"Name":"attachment.instance-id",
			"Values":[instanceId]
		}])
		volumeSize = {}

		for i in volumes:
			if i.mountPath not in volumeSize:
				volumeSize[i.mountPath] = []
			volumeSize[i.mountPath].append(i)

		volumeSize = {i:sum([j.size for j in v]) for i,v in volumeSize.items()}
# 		print(volumeSize)

	def test_ctrlSummLeftSize(self):
		result = ctrl.summLeftSize()
		print(result)

	def test_releaseCheck(self):
		ctrl.releaseCheck()

	@unittest.skip("skipping")
	def test_done(self):
		torrents = Torrent.get()
		for t in torrents:
			os.environ[datas["hash"]] = t.hash
			os.environ[datas["name"]] = t.name
			os.environ[datas["dir"]] = t.downloadDir

			ctrl.done()

	@unittest.skip("skipping")
	def test_newTorrent(self):
		for m in magnets:
			ctrl.newTorrent(m)

	@unittest.skip("skipping")
	def test_mountAndDelete(self):
		v = Volume.create(1, tags = [("Debug","true")])
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

		print(open("/etc/fstab","r").read())

		open(path+"/sample.text","w").write("hi! it's an test sample")

		self.assertEqual(path, "%s/%s"%(Volume.mountPoint, v.uid))
		print("Path = %s"%path)
		print(open(path+"/sample.text","r").read())

		x = Volume.get(uid)
		self.assertNotEqual(x, [])

		v.umount()
		v.detach()
		v.waitDetach()
		v.delete()
		v.waitDelete()

		x = Volume.get(uid)
		self.assertEqual(x, [])

if __name__ == "__main__":
	integSuite = unittest.TestSuite()
	integSuite.addTest(unittest.makeSuite(integTest))

	runner=unittest.TextTestRunner()
	runner.run(integSuite)
