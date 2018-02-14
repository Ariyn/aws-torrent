import boto3
import re

s3 = boto3.client("s3")
files = [i for i in re.sub("(.+     \d+ )", "", open("test.log","r").read()).split('\n') if i]

for index in range(0, len(files), 30):
  s3.delete_objects(
    Bucket='videos.ismin.uk',
      Delete={
          'Objects': [ {'Key':i} for i in files[index:index+30]]
      }
  )
