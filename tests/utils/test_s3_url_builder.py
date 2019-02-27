# -*- coding: utf-8 -*-

import pytest
from s3iotools.utils.s3_url_builder import s3_url_builder


class TestS3UrlBuilder(object):
    def test_build_url_by_key(self):
        assert s3_url_builder.build_url_by_key("test", "/test.txt") \
            == "https://s3.amazonaws.com/test/test.txt"

    def test_build_s3_uri_by_key(self):
        assert s3_url_builder.build_s3_uri_by_key("test", "/test.txt") \
            == "s3://test/test.txt"

    def test_build_key_by_parts(self):
        assert s3_url_builder.build_key_by_parts("a", "b", "c") == "a/b/c"
        assert s3_url_builder.build_key_by_parts("/a", "b", "c") == "a/b/c"
        assert s3_url_builder.build_key_by_parts("a", "/b", "c") == "a/b/c"
        assert s3_url_builder.build_key_by_parts("a", "b", "/c") == "a/b/c"
        assert s3_url_builder.build_key_by_parts(
            "/a/", "/b/", "/c/") == "a/b/c"

        assert s3_url_builder.build_key_by_parts("/", "a", "/", "b") == "a/b"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
