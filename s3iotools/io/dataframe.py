# -*- coding: utf-8 -*-

"""
s3 IO tools.
"""

import attr
import pandas as pd
from six import string_types, StringIO

from ..compat import gzip_compress, gzip_decompress


@attr.s
class S3Dataframe(object):
    """
    S3 object backed pandas DataFrame.
    """
    s3_resource = attr.ib(default=None)
    bucket_name = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(string_types)
        ),
        default=None,
    )
    _bucket = attr.ib(default=None)
    key = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(string_types)
        ),
        default=None,
    )
    _object = attr.ib(default=None)
    df = attr.ib(
        validator=attr.validators.optional(
            attr.validators.instance_of(pd.DataFrame)
        ),
        default=None,
    )

    @property
    def bucket(self):
        """
        access the ``s3.Bucket`` instance.

        Ref: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#bucket
        """
        if self._bucket is None:
            self._bucket = self.s3_resource.Bucket(self.bucket_name)
        return self._bucket

    @property
    def object(self):
        """
        access the ``s3.Object`` instance.

        Ref: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#object
        """
        if self._object is None:
            self._object = self.bucket.Object(self.key)
        return self._object

    def read_csv(self, bucket=None, gzip_compressed=False, **read_csv_kwargs):
        """
        Read dataframe data from a s3 object in csv format.

        :param s3_bucket: :class:`s3.Bucket`
        :param gzip_compressed: bool
        :param read_csv_kwargs: key word arguments for :meth:`pandas.read_csv`
        :return:
        """
        if bucket is None:
            bucket = self.bucket

        obj = bucket.Object(self.key)
        response = obj.get()
        body = response["Body"].read()
        if gzip_compressed:
            body = gzip_decompress(body)

        self.df = pd.read_csv(
            StringIO(body.decode("utf-8")),
            **read_csv_kwargs)

        return response

    def to_csv(self, bucket=None, key=None, gzip_compressed=False, **to_csv_kwargs):
        """
        Save a dataframe to a s3 object in csv format.
        It will overwrite existing one.

        :param s3_bucket: :class:`s3.Bucket`
        :param gzip_compressed: bool
        :param to_csv_kwargs: key word arguments for :meth:`pandas.DataFrame.to_csv`
        :return:
        """
        if bucket is None:
            bucket = self.bucket
        if key is None:
            key = self.key

        buffer = StringIO()
        self.df.to_csv(buffer, index=False, **to_csv_kwargs)

        body = buffer.getvalue().encode("utf-8")
        if gzip_compressed is True:
            body = gzip_compress(body)

        response = bucket.put_object(Body=body, Key=key)
        return response