#!/usr/bin/python

import sys,argparse,logging
import boto

__author__ = 'stormacq'
__version__ = 1.0

'''
Usage : s3sign  --bucket <bucket_name>
                --key <key_name>
                --expire <seconds to expiration> (default 24h)

Generate a signed URL to access the object identified by bucket_name and key_name
Signed URL expires after 'seconds'.  You can pass an expression like 60*60*24 for one day

Example : s3sign --bucket my_bucket --key test.txt --expire 60*60*24
'''

logger = None

def main(**kwargs):

    logger.debug('Parameter bucket = %s' % kwargs['bucket'])
    logger.debug('Parameter key    = %s' % kwargs['key'])
    logger.debug('Parameter expire = %s' % kwargs['expire'])


    s3conn = boto.connect_s3()
    bucket = s3conn.get_bucket(kwargs['bucket'])
    key = bucket.get_key(kwargs['key'])
    seconds=60*60*24 if kwargs['expire'] is None else eval(kwargs['expire']) #default to one day
    print key.generate_url(expires_in=seconds)

if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('s3sign')
    #logger.setLevel(logging.DEBUG)

    if sys.version_info < (2, 7):
        logger.info('Using Python < 2.7')
        parser = argparse.ArgumentParser(description='Generate Signed S3 URL')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v' +
        str(__version__))
    else:
        parser = argparse.ArgumentParser(description='Generate Signed S3 URL', version='%(prog)s v' +
                                                                                            str(__version__))
    parser.add_argument('-b', '--bucket', type=str, help='Bucket name', required=True)
    parser.add_argument('-k', '--key', type=str, help='Key Name', required=True)

    parser.add_argument('-e', '--expire', type=str, default='60*60*24', help='Seconds before expiration (default one '
                                                                             'day)')
    args = parser.parse_args()
    main(**vars(args))
