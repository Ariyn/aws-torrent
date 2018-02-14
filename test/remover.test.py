import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from Torrent import Transmission
from DB import *
import json

import Remover as rm

class Test(unittest.TestCase):
	def setUp(self):
		self.t = Transmission(server="13.124.14.192", port=8080, passwd="pw4transmission")
		# x = self.t.list()[4]

		# print(x.name, x.hash, x.downloadDir)
		# os.environ["TR_TORRENT_NAME"] = x.name
		# os.environ["TR_TORRENT_HASH"] = x.hash
		# os.environ["TR_TORRENT_DIR"] = x.downloadDir

	def test_remover(self):
		x = self.t.list()
		for i in x:
			if i.percentDone == 100:
				os.environ["TR_TORRENT_NAME"] = i.name
				os.environ["TR_TORRENT_HASH"] = i.hash
				os.environ["TR_TORRENT_DIR"] = i.downloadDir
				rm.done()
			else:
				print(i)

	def test_compress(self):
		return True
		s3Bucket = "videos.ismin.uk"
		name, hash = os.environ["TR_TORRENT_NAME"], os.environ["TR_TORRENT_HASH"]
		path = os.environ["TR_TORRENT_DIR"]

		filePath = path+"/"+name
		fileList = list(os.listdir(filePath))
		fileList = [rm.compress(path, name, fileList)]
		filePath = path

		rm.upload(s3Bucket, filePath, fileList)

	def test_release(self):
		rm.releaseCheck()

	def test_nonCompress(self):
		return True
		s3Bucket = "videos.ismin.uk"
		name, hash = os.environ["TR_TORRENT_NAME"], os.environ["TR_TORRENT_HASH"]
		path = os.environ["TR_TORRENT_DIR"]

		filePath = path+"/"+name
		fileList = list(os.listdir(filePath))
		# filePath = path

		# rm.upload(s3Bucket, path, [name+"/"+i for i in fileList])

if __name__ == "__main__":
	# print(os.environ)
	unittest.main()
