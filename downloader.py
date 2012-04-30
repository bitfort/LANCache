import os
import threading
import urllib
import os.path as path
import api.S3 as s3

gm = s3.AWSAuthConnection("AKIAI5C3B4IPLZDLBPKA", "QAzLIUIATfMX3JnxzrKm5Xd3YWB6k5tTxle0U22B")
BUCKET = "capel_bittorf"


class CloudDownloader(threading.Thread):
  def __init__(self, name):
    super(CloudDownloader, self).__init__()
    self.name = name

  def run(self):
    filename = self.name
    target = os.path.join(os.path.dirname(__file__), "data", filename)
    obj = gm.get(BUCKET, filename)
    if obj.message != "200 OK":
      print "Bad filename, message:"
      print obj.message
      return
    with open(target, 'w') as f:
      f.write(obj.object.data)


class Downloader(threading.Thread):
  def __init__(self, url):
    super(Downloader, self).__init__()
    self.url = url

  def run(self):
    dir_ = path.dirname(__file__)
    base = path.basename(self.url)
    target = path.join(dir_, 'data', base)
    print 'Downloading ', self.url, ' to', target
    urllib.urlretrieve(self.url, target)
