import boto3
import sys
import os
import pandas as pd
import argparse
import argcomplete
import logging
boto3.set_stream_logger('botocore', logging.INFO)

def get_access_creds(credentials_csv):
    df = pd.read_csv(credentials_csv, sep=',')
    return str(df['Access key ID']), str(df['Secret access key'])

''' this will help you if you want to pay Amazon for a high powered computer that you 
    can't afford unless you save up...I guess it makes sense...kinda '''
def main():
    parser = argparse.ArgumentParser(description='Upload or download files/directories to or from an S3 bucket')
    subparsers = parser.add_subparsers(dest='mode')

    upload_file_parser = subparsers.add_parser('up_file', help='Upload individual file to S3 bucket')
    upload_file_parser.add_argument('-f', '--file_loc', required=True, action='store', dest='file_loc', help='Full path to filename')
    upload_file_parser.add_argument('-b', '--bucket', required=True, action='store', dest='bucket_name', help='Name of the S3 bucket')
    upload_file_parser.add_argument('-fs', '--file_store', required=True, action='store', dest='file_store', help='How the file will be named in S3 bucket')

    upload_dir_parser = subparsers.add_parser('up_dir', help='Upload directory to S3 bucket')
    upload_dir_parser.add_argument('-d', '--dir_loc', required=True, action='store', dest='dir_loc', help='Full path to directory')
    upload_dir_parser.add_argument('-b', '--bucket', required=True, action='store', dest='bucket_name', help='Name of the S3 bucket')

    dnload_file_parser = subparsers.add_parser('dn_file', help='Download individual file from S3 bucket')
    dnload_file_parser.add_argument('-b', '--bucket', required=True, action='store', dest='bucket_name', help='Name of the S3 bucket')
    dnload_file_parser.add_argument('-f', '--file_name', required=True, action='store', dest='file_name', help='Name of file in S3 bucket')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    
    s3 = boto3.resource('s3')

    if args.mode == 'up_file':
        print('Uploading: ' + args.file_loc)
        s3.Bucket(args.bucket_name).put_object(Key=args.file_store, Body=open(args.file_loc))

    if args.mode == 'up_dir':
        for path, dirs, files in os.walk(args.dir_loc):
            for filename in files:
                print('Uploading: ' + (path + filename))
                s3.Bucket(args.bucket_name).put_object(Key=filename, Body=open(path + filename, 'rb'))

    if args.mode == 'dn_file':
        s3.meta.client.download_file(args.bucket_name, args.file_name, './' + args.file_name)

if __name__ == '__main__':
    sys.exit(main())
