import os, sys
sys.path.insert(0, "/home/wssh/torrents/script")

import unittest
import transmission as tr
import random

class Tester(unittest.TestCase):
  testMagnets = [
    "magnet:?xt=urn:btih:25ce3e50163c01dc2df3a5fa3a47e674d765e8bb&dn=%5BOhys-Raws%5D+Karakai+Jouzu+no+Takagi-san+-+03+%28MX+1280x720+x264+AAC%29.mp4&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannonuce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce",
    "magnet:?xt=urn:btih:99F18A4390E6DFC006D58A34FAFABF0EB5B8B914",
    "magnet:?xt=urn:btih:DF47CCF0B8EBE2EC7FF8AAF6ADC4CC5136E5C7A3",
    "magnet:?xt=urn:btih:8A29DD7CFD7DABD3763D4A8BA48867D005169CE1",
    "magnet:?xt=urn:btih:7F407721BAF879DA28EFE1943C4CC56ED14922A4",
    "magnet:?xt=urn:btih:9F2F83683D3BB35ACA0532D6B54F20601F7AF3F1",
    "magnet:?xt=urn:btih:4497DE805F7C6EEF66F5EE2732FB9FDCC1D02192"
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
      if x[i]["hash"] == "7F407721BAF879DA28EFE1943C4CC56ED14922A4":
        target = x[i]
        
    tr.reallocTorrent(target["id"], target["magnet"], target["path"], "/mnt/newVolume/torrent/test/")
    
if __name__ == "__main__":
  unittest.main()