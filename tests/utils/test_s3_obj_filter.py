# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from s3iotools.utils.s3_obj_filter import filter_constructor
from s3iotools.tests.fake_s3_obj import FakeS3Object


class TestFilterConstructor(object):
    def run_test(self, filters_factory_func, base_kwargs, s3_obj, returned_flag):
        kwargs_classmethod = {"is_classmethod": True}
        kwargs_classmethod.update(base_kwargs)
        kwargs_staticmethod = {"is_staticmethod": True}
        kwargs_staticmethod.update(base_kwargs)
        kwargs_regularmethod = {"is_regularmethod": True}
        kwargs_regularmethod.update(base_kwargs)

        class MyClass(object):
            filter_classmethod = filters_factory_func(**kwargs_classmethod)
            filter_staticmethod = filters_factory_func(**kwargs_staticmethod)
            filter_regularmethod = filters_factory_func(**kwargs_regularmethod)

        my_class = MyClass()

        assert MyClass.filter_classmethod(s3_obj) is returned_flag
        assert MyClass.filter_staticmethod(s3_obj) is returned_flag
        assert my_class.filter_staticmethod(s3_obj) is returned_flag
        assert my_class.filter_regularmethod(s3_obj) is returned_flag
        assert filters_factory_func(**base_kwargs)(s3_obj) is returned_flag

    def test_by_extension(self):
        s3_obj = FakeS3Object(key="test.py")

        run_test_args_list = [
            (filter_constructor.by_extension, dict(ext=".py", case_sensitive=True), s3_obj, True),
            (filter_constructor.by_extension, dict(ext=".PY", case_sensitive=True), s3_obj, False),
            (filter_constructor.by_extension, dict(ext=".PY", case_sensitive=False), s3_obj, True),
        ]
        for run_test_args in run_test_args_list:
            self.run_test(*run_test_args)

    def test_by_basename(self):
        s3_obj = FakeS3Object(key="scripts/Test.py")

        run_test_args_list = [
            (
                filter_constructor.by_basename,
                dict(basename="Test.py", case_sensitive=True),
                s3_obj,
                True
            ),
            (
                filter_constructor.by_basename,
                dict(basename="st.py", case_sensitive=True),
                s3_obj,
                True
            ),
            (
                filter_constructor.by_basename,
                dict(basename="run.py", case_sensitive=True),
                s3_obj,
                False
            ),
            (
                filter_constructor.by_basename,
                dict(basename="scripts", case_sensitive=True),
                s3_obj,
                False
            ),
            (
                filter_constructor.by_basename,
                dict(basename="TEST.py", case_sensitive=True),
                s3_obj,
                False
            ),
            (
                filter_constructor.by_basename,
                dict(basename="TEST.py", case_sensitive=False),
                s3_obj,
                True
            ),
        ]
        for run_test_args in run_test_args_list:
            self.run_test(*run_test_args)

    def test_by_last_modified(self):
        obj = FakeS3Object(last_modified=datetime(2000, 6, 1))
        assert filter_constructor.by_last_modified_after(
            datetime(2000, 1, 1))(obj) is True
        assert filter_constructor.by_last_modified_after(
            datetime(2000, 12, 1))(obj) is False

        assert filter_constructor.by_last_modified_before(
            datetime(2000, 1, 1))(obj) is False
        assert filter_constructor.by_last_modified_before(
            datetime(2000, 12, 1))(obj) is True

        assert filter_constructor \
                   .by_last_modified_between(datetime(2000, 1, 1), datetime(2000, 12, 1))(obj) is True
        assert filter_constructor \
                   .by_last_modified_between(datetime(2010, 1, 1), datetime(2010, 12, 1))(obj) is False

    def test_by_size(self):
        obj = FakeS3Object(content_length=500)
        assert filter_constructor.by_size()(obj) is True
        assert filter_constructor.by_size(min_size_in_bytes=1000)(obj) is False
        assert filter_constructor.by_size(max_size_in_bytes=100)(obj) is False
        assert filter_constructor.by_size(
            min_size_in_bytes=100, max_size_in_bytes=1000)(obj) is True


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
