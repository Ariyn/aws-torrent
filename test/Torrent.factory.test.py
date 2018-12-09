import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Torrent_refctory import Torrent
import datetime, time, subprocess

class moduleTest(unittest.TestCase):
	def test_get(self):
		t = Torrent
		results = t.get()
		for i in results:
			print(i)
# 			print(i.id, i.name, i.readableSize, i.readableUnit, i.statusString)

		self.assertNotEqual(results, [])

	@unittest.skip("")
	def test_delete(self):
		t = Torrent.get(hash="8e85a4")
		if t:
			x = t.removeTorrentAndFile()
			print(x)

	@unittest.skip("")
	def test_stop(self):
		t = Torrent.get()
		if t:
			data = t.stop()
			print(data)
# 		self.assertNotEqual(result, [])

# 	@unittest.skip("")
	def test_move(self):
		t = Torrent.get(hash="4c776cf936de1a0a415786e25fefb9375f63909f")
		if t:
			t.moveTo(location="/mnt/fa20d3")
			print(t.downloadDir)

	@unittest.skip("")
	def test_add(self):
		magnetHash = "magnet:?xt=urn:"
		t = Torrent.add(filename=magnetHash, download_dir="/mnt/torrent-temp/")
		t.waitAdd()
		print(t)

if __name__ == "__main__":
	moduleSuite = unittest.TestSuite()
	moduleSuite.addTest(unittest.makeSuite(moduleTest))


	runner=unittest.TextTestRunner()
	runner.run(moduleSuite)
