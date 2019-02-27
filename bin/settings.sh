#!/bin/bash
# -*- coding: utf-8 -*-
#
# This script should be sourced to use.


# GitHub
github_account="MacHu-GWU"
github_repo_name="s3iotools-project"


# Python
package_name="s3iotools"
py_ver_major="2"
py_ver_minor="7"
py_ver_micro="13"
use_pyenv="Y" # "Y" or "N"
supported_py_versions="2.7.13 3.4.6 3.5.3 3.6.2" # e.g: "2.7.13 3.6.2"


#--- Doc Build

rtd_project_name="s3iotools"

# AWS profile name for hosting doc on S3
# should be defined in ~/.aws/credentials
# read https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html for more information
aws_profile_doc_host="an-aws-profile-name"

# html doc will be upload to:
# "s3://${S3_BUCKET_DOC_HOST}/docs/${PACKAGE_NAME}/${PACKAGE_VERSION}"
s3_bucket_doc_host="a-s3-bucket-name"


