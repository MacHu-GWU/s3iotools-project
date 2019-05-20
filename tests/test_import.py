# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import s3iotools

    s3iotools.S3FileObject
    s3iotools.S3Dataframe

    s3iotools.select_from
    s3iotools.Filters
    s3iotools.filter_constructor

    s3iotools.s3_url_builder


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
