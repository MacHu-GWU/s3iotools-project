# -*- coding: utf-8 -*-

import pytest
from pathlib_mate import PathCls as Path
from s3iotools.io.file_object import S3FileObject

from s3iotools.tests import moto_compat # create fake ~/.aws/credential file
import boto3
from moto import mock_s3

bucket_name = "my_bucket"


class TestS3FileObject(object):
    @classmethod
    def setup_class(cls):
        p = Path(__file__).change(new_basename="downloaded_test_file_object.py")
        if p.exists():
            p.remove()

    @classmethod
    def teardown_class(cls):
        cls.setup_class()

    @mock_s3
    def test_use_case(self):
        # setup_class with @classmethod decorator can't use with @mock_s3
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)
        bucket.create()

        s3_obj = S3FileObject(
            bucket_name=bucket_name,
            key=Path(__file__).basename,
        )
        assert s3_obj.exists_on_s3() is False

        s3_obj.path = __file__
        assert s3_obj.exists_on_local() is True

        s3_obj.copy_to_s3()
        assert s3_obj.exists_on_s3() is True

        s3_obj.path = Path(__file__).change(new_basename="downloaded_test_file_object.py")
        assert s3_obj.path_obj.exists() is False

        s3_obj.copy_to_local()
        assert s3_obj.path_obj.exists() is True


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
