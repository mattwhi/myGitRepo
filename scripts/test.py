#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from datetime import datetime
from time import strftime

import pytz
import json
from boto3 import Session
from botocore.exceptions import ClientError
from collections import Counter

import test_config
from utils import get_ec2_instance_tags

timestamp = strftime("%Y%m%d-%H%M%S")
xlsx_filename = 'aws_account_report_{0}.xlsx'.format(timestamp)
workbook = xlsxwriter.Workbook(xlsx_filename)

row_title = workbook.add_format({'bold': 1})

instance_summary = list()
for config in test_config.accounts:
    worksheet = workbook.add_worksheet(config.get('friendly_name'))
    worksheet.write('A1', 'id', row_title)
    worksheet.write('B1', 'name', row_title)
    worksheet.write('C1', 'state', row_title)
    worksheet.write('D1', 'type', row_title)
    worksheet.write('E1', 'image', row_title)
    worksheet.write('F1', 'public ip', row_title)
    worksheet.write('G1', 'private ip', row_title)
    worksheet.write('H1', 'running time (hours)', row_title)
    worksheet.write('I1', '$ hour', row_title)
    print('Getting session for: {0}'.format(config.get('friendly_name')))
    try:
        session = Session(aws_access_key_id=config.get('access_key_id'),
                          aws_secret_access_key=config.get('secret_access_key'), region_name=config.get('region'))
        ec2_client = session.client('ec2')
        instances_req = ec2_client.describe_instances()
        reservations = instances_req.get('Reservations')
        all_instances = list()
        instances = sorted(all_instances, key=lambda k: get_ec2_instance_tags(ec2_instance=k, tag_key='Name'))
        row_num = 1
        for reservation in reservations:
            for instance in reservation.get('Instances'):
                instance_id = instance.get('InstanceId')
                instance_state = instance.get('State').get('Name')
                instance_type = str(instance.get('InstanceType'))
                image_id = instance.get('ImageId')
                public_ip = instance.get('PublicIpAddress')
                private_ip = instance.get('PrivateIpAddress')
                launch_time_raw = instance.get('LaunchTime')
                running_time_delta = datetime.now(pytz.UTC) - launch_time_raw
                days, seconds = running_time_delta.days, running_time_delta.seconds
                hours = days * 24 + seconds // 3600
                instance_name = get_ec2_instance_tags(ec2_instance=instance, tag_key='Name')

                instance_summary.append({'account_alias': config.get('friendly_name'), 'instance_id': instance_id,
                                         'instance_name': instance_name, 'instance_type': instance_type})

                worksheet.write(row_num, 0, instance_id)
                worksheet.write(row_num, 1, instance_name)
                worksheet.write(row_num, 2, instance_state)
                worksheet.write(row_num, 3, instance_type)
                worksheet.write(row_num, 4, image_id)
                worksheet.write(row_num, 5, public_ip)
                worksheet.write(row_num, 6, private_ip)
                worksheet.write(row_num, 7, hours)
                row_num += 1
    except ClientError:
        print('Unable to connect to query account: {0}'.format(config.get('friendly_name')))
    worksheet.set_column('A:A', 13)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:G', 13)
    worksheet.set_column('H:H', 17)

# Add summary sheet
print('Writing ec2 summary sheet')
worksheet = workbook.add_worksheet('ec2_summary')
worksheet.write('A1', 'account alias', row_title)
worksheet.write('B1', 'instance id', row_title)
worksheet.write('C1', 'instance name', row_title)
worksheet.write('D1', 'instance type', row_title)
summary_row_no = 1
type_list = list()
for instance in instance_summary:
    worksheet.write(summary_row_no, 0, instance.get('account_alias'))
    worksheet.write(summary_row_no, 1, instance.get('instance_id'))
    worksheet.write(summary_row_no, 2, instance.get('instance_name'))
    worksheet.write(summary_row_no, 3, instance.get('instance_type'))
    type_list.append(instance.get('instance_type'))
    summary_row_no += 1
type_count = Counter(type_list)
worksheet.write('F1', 'instance type', row_title)
worksheet.write('G1', 'count', row_title)
type_summary_row_no = 1
for itype, count in type_count.iteritems():
    worksheet.write(type_summary_row_no, 5, itype)
    worksheet.write(type_summary_row_no, 6, count)
    type_summary_row_no += 1
workbook.close()
