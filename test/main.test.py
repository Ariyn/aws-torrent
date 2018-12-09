import os, sys
sys.path.insert(0, "/home/wssh/torrents/script")

import unittest
import adder, transmission as tr
import random

class Tester(unittest.TestCase):
  magnet = "magnet:?"

  def test_moveTest(self):
    return True
    target = tr.addToTransmission(self.magnet, "/mnt/newVolume/torrent")
    print(target["path"]+"/"+target["name"])

    targetPath = "/mnt/28efd5/"
    cmd = tr.reallocTorrent(target["id"], target["magnet"], target["path"]+"/"+target["name"], targetPath)

    print(cmd)

  def test_updateTorrent(self):
    hash = tr.parseHash(self.magnet)
    self.assertEqual(hash, "0f516cc42cf4f8ddf6fa2dbebee9f76fd9feae50".upper())
    torrentId = adder.getTorrentId(hash)
    targetPath = "/mnt/84900c/"
    disk = adder.getDisk(18)
    adder.updateTorrentRow(torrentId, targetPath, disk[0])

if __name__ == "__main__":
  unittest.main()
