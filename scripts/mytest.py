#!/usr/bin/env python
import boto3

#from boto3 import session

# import config

# try:
# 	session = Session(aws_access_key_id=config.get('access_key_id'),
# 	                  aws_secret_access_key=config.get('secret_access_key'), region_name=config.get('region'))
#         ec2_client = session.client('ec2')
#         instances_req = ec2_client.describe_instances()
# print('aws_access_key_id')
# ec2 = boto3.client('ec2')

# # Retrieves all regions/endpoints that work with EC2
# response = ec2.describe_regions()
# print('Regions:', response['Regions'])

# # Retrieves availability zones only for region of the ec2 object
# response = ec2.describe_availability_zones()
# print('Availability Zones:', response['AvailabilityZones'])