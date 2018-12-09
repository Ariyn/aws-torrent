import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

from adder import *
import unittest
import json

testMagnets = ["magnet:?","magnet:?"]

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
