import os, sys
sys.path.insert(0, "/home/wssh/torrents/script")

import unittest
import adder, transmission as tr
import random

class Tester(unittest.TestCase):
  magnet = "magnet:?xt=urn:btih:0f516cc42cf4f8ddf6fa2dbebee9f76fd9feae50&dn=%5BOhys-Raws%5D+Girls+und+Panzer+%28BD+1280x720+x264+AAC%29&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F208.67.16.113%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker.swateam.org.uk%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.skyts.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.pomf.se%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.kuroy.me%3A5944%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=http%3A%2F%2Fleechers-paradise.org%3A6969%2Fannounce&tr=http%3A%2F%2F184.105.214.73%3A6969%2Fannounce&tr=http%3A%2F%2Fopen.nyaatorrents.info%3A6544%2Fannounce"
  
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