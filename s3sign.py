#!/usr/bin/python

import sys,argparse,logging,re, urllib
import boto
from boto.exception import S3ResponseError

__author__ = 'stormacq'
__version__ = 1.1

'''
Usage : s3sign  --bucket <bucket_name>
                --key <key_name>
                --expire <seconds to expiration> (default 24h)

Generate a signed URL to access the object identified by bucket_name and key_name
Signed URL expires after 'seconds'.  You can pass an expression like 60*60*24 for one day

Example : s3sign --bucket my_bucket --key test.txt --expire 60*60*24
'''

logger = None

def extractBucketAndKeyNameFromURL(url, format) :
        p = re.compile(format)
        m = p.match(urllib.unquote(url))
        bucket = m.group(1)
        key    = urllib.unquote_plus(m.group(2))
        return bucket, key

def main(parser, **kwargs):

    logger.debug('Parameter url    = %s' % kwargs['url'])
    logger.debug('Parameter bucket = %s' % kwargs['bucket'])
    logger.debug('Parameter key    = %s' % kwargs['key'])
    logger.debug('Parameter expire = %s' % kwargs['expire'])

    url    = kwargs['url']
    bucket = kwargs['bucket']
    key    = kwargs['key']

    if url is None and bucket is None and key is None:
        parser.print_help()
        exit(-1)


    if url is not None:
        logger.debug('Going to parse URL')

        # URL format https://bucket_name.s3.amazonaws.com/key_name
        bucket, key = extractBucketAndKeyNameFromURL(url, '^http[s]?:\/\/(.*?)\..*?\/(.*)$')


    logger.debug('bucket = %s' % bucket)
    logger.debug('key    = %s' % key)

    s3conn = boto.connect_s3()

    try:
        s3bucket = s3conn.get_bucket(bucket)
    except S3ResponseError as e:

        if url is not None:
            # maybe user passed a different URL format, let's try
            # https://region_name.s3.amazonaws/bucket_name/key_name
            bucket, key = extractBucketAndKeyNameFromURL(url, '^http[s]?:\/\/.*?\/(.*?)/(.*)$')
            logger.debug('bucket = %s' % bucket)
            logger.debug('key    = %s' % key)
            try:
                s3bucket = s3conn.get_bucket(bucket)
            except S3ResponseError as e:
                print 'Error : invalid bucket name : %s' % bucket
                exit(-1)
        else:
            print 'Error : invalid bucket name : %s' % bucket
            exit(-1)

    s3key = s3bucket.get_key(key)
    if s3key is None:
        print 'Error : key name : %s' % key
        exit(-1)

    seconds=60*60*24 if kwargs['expire'] is None else eval(kwargs['expire']) #default to one day
    print s3key.generate_url(expires_in=seconds)

if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('s3sign')

    if sys.version_info < (2, 7):
        logger.info('Using Python < 2.7')
        parser = argparse.ArgumentParser(description='Generate Signed S3 URL')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v' +
        str(__version__))
    else:
        parser = argparse.ArgumentParser(description='Generate Signed S3 URL', version='%(prog)s v' +
                                                                                            str(__version__))
    parser.add_argument('-b', '--bucket', type=str, help='Bucket name')
    parser.add_argument('-k', '--key', type=str, help='Key Name')
    parser.add_argument('-u', '--url', type=str, help='S3 URL to sign.  When this parameter is given, \'bucket\' and \'key\' parameters are ignored')
    parser.add_argument('-e', '--expire', type=str, default='60*60*24', help='Seconds before expiration (default one day)')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debugging information', default=False)
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    main(parser, **vars(args))
