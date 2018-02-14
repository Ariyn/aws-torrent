import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

from adder import *
import unittest
import json

testMagnets = ["magnet:?xt=urn:btih:7a5db698cf186a505965cf1165a70251a8dbd010&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+02+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:8949bf4ff5d492c650b397d05d8a6a68f7f07855&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+03+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:339f8617d1aff230773329462d098db779ced233&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+04+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:77dd3a58aa7007b4d64fd197c235dd5140bb7cc8&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+05+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:5192e565830aff78d9267454b6c7517830379041&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+07+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:f82f425ff4c174c3ffd38d65b07dc47088655548&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+08+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:2fd1e06e4ab8ee9c0ba8ed49b977a343d21bc094&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+09+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:d144efe55a183b9b2c7c3ae30c621561f463e155&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+10+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Frntracker.ohys.net%3A80%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:8462d47be23565048b771edd504e8fc84a9d3672&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+11+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:9606234d30e3a2de5c40532a80766e0f24038c9d&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+12+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:9606234d30e3a2de5c40532a80766e0f24038c9d&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+12+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:945df9a5b87a8c1fe09441f5deb3d0345db6a817&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+13+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:f2cf682f76fb146e9c7c014aa8d4901979aef275&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+14+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:bd0f2e10b7638b088a130c3cc0056ff4f12ead8b&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+15+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:b61ae6b12f75df7aa5ee6741dd853a911cbc0808&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+16+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
"magnet:?xt=urn:btih:3c62e5769bc550d0a59373d3876ba9c63661b559&dn=%5BOhys-Raws%5D+Osomatsu-san+2+-+17+%28TX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce"]

class Test(unittest.TestCase):
	def setUp(self):
		# self.t = Transmission(server="13.124.193.22", port=8080, id="Aladdin", passwd="open sesame")
		self.t = Transmission(server="127.0.0.1", port=8080, passwd="pw4transmission")

	def test_t__invoke(self):
		req, res, data = self.t.__invoke__("torrent-get", {"fields":["id"]})
		# print(data)

	def test_TransmissionTorrentData(self):
		x = self.t.list()
		for i in x:
			print(json.dumps(str(i))+"\t\t"+i.downloadDir)

	def test_TransmissionTorrentStop(self):
		response, data = self.t.stop(ids=2)
		self.assertEqual(data["result"], "success")

	def test_TransmissionTorrentStart(self):
		response, data = self.t.start(ids=1)
		self.assertEqual(data["result"], "success")

	def test_TransmissionTorrentVerify(self):
		response, data = self.t.verify(ids=1)
		self.assertEqual(data["result"], "success")

	def test_TransmissionTorrentRemove(self):
		self.assertTrue(True)
		response, data = self.t.remove(ids=25)
		self.assertEqual(data["result"], "success")

	def test_transmissionTorrentMove(self):
		self.assertTrue(True)
		response, data = self.t.move(ids=13, location="/mnt/newVolume/torrent/test", debug=True)
		self.assertEqual(data["result"], "success")

	def test_transmissionTorrentAdd(self):
		response, data = self.t.add(filename="magnet:?xt=urn:btih:C56EED4D416E61DC75AFB07D7A650DF1F99C14AC")
		self.assertEqual(data["result"], "success")

if __name__ == "__main__":
	t = Transmission(server="127.0.0.1", port=8080, passwd="pw4transmission")
	print("test",testMagnets)
	for i in testMagnets:
		print(i)
		t.add(filename=i)

	# unittest.main()
