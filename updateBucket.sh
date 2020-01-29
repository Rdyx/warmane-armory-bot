#/bin/sh
# This bot is hosted on a GCP compute engine, data files are stored on a bucket to ensure
# that it would not be lost if CE got a hard crash and can't be accessed

# Clean bucket to remove any file that should not be there anymore
# Don't forget to set bucket name as env var
gsutil rm -r gs://$bucketName/*
# Copy files to bucket
# Don't forget to set bot directory path as env var
gsutil cp -r $botDirPath/data/ gs://$bucketName