# -*- coding: utf-8 -*-

from s3iotools import config

config.aws_profile = "sanhe"
config.bucket_name = "python-s3iotools"

from s3iotools.tests import s3
from s3iotools.tests.io_dataframe import df_customers
from s3iotools.io.dataframe import S3Dataframe


def run():
    # csv
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

    # json
    s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name)
    s3df.df = df_customers
    s3df.to_json(key="customers.json")
    s3df.to_json(key="customers.json.gz", gzip_compressed=True)

    s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name, key="customers.json")
    assert s3df.df is None
    s3df.read_json()
    assert s3df.df.shape == (91, 7)

    s3df = S3Dataframe(s3_resource=s3, bucket_name=config.bucket_name, key="customers.json.gz")
    assert s3df.df is None
    s3df.read_json(gzip_compressed=True)
    assert s3df.df.shape == (91, 7)


if __name__ == "__main__":
    run()
