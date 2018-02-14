import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Volume_refactory import Volume
from Torrent_refctory import Torrent
import Controller as ctrl
import datetime, time, subprocess

datas = {
	"name":"TR_TORRENT_NAME",
	"hash":"TR_TORRENT_HASH",
	"dir":"TR_TORRENT_DIR"
}
magnet = "magnet:?xt=urn:btih:7dc2a8f2cad9623c1fb5264a5395f075e66f62af&dn=Fap+Hero+-+Futa+Dream+%5BUC+3D+Hentai%5D+%5BHD+720P%5D+-+BH7.MP4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2Feddie4.nl%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2740%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.vanitycore.co%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=http%3A%2F%2F82.209.230.66%2Fannounce&tr=http%3A%2F%2Fretracker.mgts.by%3A80%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&tr=http%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=http%3A%2F%2F163.172.180.68%2Fannounce&tr=http%3A%2F%2Fipv4.tracker.harry.lu%2Fannounce"
magnets = ["magnet:?xt=urn:btih:9ea38b6daadbe34e20ef156958eff55e338e4d67&dn=%5B141108%5D+%5B%E3%81%93%E3%82%8D%E3%81%BD%E3%81%A3%E3%81%A8%5D+%E3%83%AA%E3%82%B9%E3%83%8A%E3%81%A8%E6%82%AA%E5%A4%A2%E3%82%92%E5%AD%95%E3%81%BF%E3%81%97%E6%9D%91+Ver.1.2&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.doko.moe%3A6969&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce", "magnet:?xt=urn:btih:25d38ca46a68d8a05b2e7f824fbcc55f7f7f1edd&dn=%5BBH7+Uncensored+JAV%5D+Maid%2C+You+Are+Hired+%5BSD+480P%5D.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Fretracker.mgts.by%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A80%2Fannounce&tr=http%3A%2F%2F82.209.230.66%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&tr=http%3A%2F%2Fretracker.mgts.by%3A80%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&tr=http%3A%2F%2Fopen.kickasstracker.com%3A80%2Fannounce"]
instanceId = "i-0d95f7b47ba724311"

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
		
	def test_ctrlerLeftSize(self):
		result = ctrl.summLeftSize()
# 		print(result)

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
	
# 	@unittest.skip("skipping")
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