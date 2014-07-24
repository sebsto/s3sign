s3sign is a very simple script to generate S3 Signed URL.

s3sign uses AWS Python SDK (aka boto) to generate the signature.
Learn more about [boto](http://aws.amazon.com/sdkforpython/) and [how to configure boto](http://aws.amazon.com/developers/getting-started/python/) on your machine.

#Usage

```
usage: s3sign [-h] [-v] [-b BUCKET] [-k KEY] [-u URL] [-e EXPIRE] [-d]

Generate Signed S3 URL

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -b BUCKET, --bucket BUCKET
                        Bucket name
  -k KEY, --key KEY     Key Name
  -u URL, --url URL     S3 URL to sign. When this parameter is given, 'bucket'
                        and 'key' parameters are ignored
  -e EXPIRE, --expire EXPIRE
                        Seconds before expiration (default one day)
  -d, --debug           Print debugging information
```

