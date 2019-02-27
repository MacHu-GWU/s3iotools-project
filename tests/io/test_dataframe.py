# -*- coding: utf-8 -*-

import pytest
from s3iotools import config

config.bucket_name = "test-bucket"

from s3iotools.tests import moto_compat
from s3iotools.tests.io_dataframe import df_customers
from s3iotools.io.dataframe import S3Dataframe

import boto3
from moto import mock_s3


class TestS3Dataframe(object):
    @mock_s3
    def test(self):
        s3 = boto3.resource("s3", region_name='us-east-1')
        s3.create_bucket(Bucket=config.bucket_name)

        s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name)
        s3df.df = df_customers
        s3df.to_csv(key="customers.csv")
        s3df.to_csv(key="customers.csv.gz", gzip_compressed=True)

        s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name, key="customers.csv")
        assert s3df.df is None
        s3df.read_csv()
        assert s3df.df.shape == (91, 7)

        s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name, key="customers.csv.gz")
        assert s3df.df is None
        s3df.read_csv(gzip_compressed=True)
        assert s3df.df.shape == (91, 7)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
