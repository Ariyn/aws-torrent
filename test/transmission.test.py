import os, sys
sys.path.insert(0, "/home/wssh/torrents/script")

import unittest
import transmission as tr
import random

class Tester(unittest.TestCase):
  testMagnets = [
    "magnet:?xt=urn:btih:",
    "magnet:?xt=urn:btih:",
    "magnet:?xt=urn:btih:",
    "magnet:?xt=urn:btih:"
  ]


  def test_collectTorrents(self):
    x = tr.collectTorrents()
#     print(x)
#     for i in x:
#       print(i)
  def test_addTorrent(self):

    tr.addToTransmission(self.testMagnets[4], "/mnt/newVolume/torrent")
    pass

  def test_realloc(self):
    x = tr.collectTorrents()
    target = None
    for i in x:
      if x[i]["hash"] == "7F4":
        target = x[i]

    tr.reallocTorrent(target["id"], target["magnet"], target["path"], "/mnt/newVolume/torrent/test/")

if __name__ == "__main__":
  unittest.main()
