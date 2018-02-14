import os, sys
sys.path.insert(0, str(os.path.abspath("script")))

import unittest
from DB import *

class Test(unittest.TestCase):
	def setUp(self):
		path = os.path.abspath("torrent")
		self.db = DB
		self.db.connect(dbPath=path)

	def test_DB(self):
		self.assertIsNotNone(self.db)

	def test_getDeviceNames(self):
		x = self.db.getDeviceNames()
		print(x)

if __name__ == "__main__":
	unittest.main()
