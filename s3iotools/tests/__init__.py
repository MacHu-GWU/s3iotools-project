# -*- coding: utf-8 -*-

import boto3
from .. import config

print(config.aws_profile)
ses = boto3.Session(profile_name=config.aws_profile)
s3 = ses.resource("s3")
