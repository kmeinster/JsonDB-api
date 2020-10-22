import boto3
# import datetime
import json
import time
from calendar import timegm
from datetime import datetime, tzinfo, timedelta

from minio import Minio

mc = Minio('127.0.0.1:9000',
           access_key='minio',
           secret_key='minio123',
           secure=False)

s3 = boto3.client('s3',
                  endpoint_url='http://localhost:9000',
                  aws_access_key_id='minio',
                  aws_secret_access_key='minio123',
                  region_name='us-east-1')


def search_all_objects(metric):
    objects = mc.list_objects_v2(bucket_name=metric,
                                 prefix=None,
                                 recursive=True,
                                 include_user_meta=True)
    return objects


def search_all_objects_within_time_range(metric, start_time, end_time):
    converted_date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    return converted_date


def search_all_objects_within_raw_time_range(metric, start_time, end_time):
    pass


def generate_datapoints_from_metrics(metric):
    datapoints = []
    objects = search_all_objects(metric)
    for obj in objects:
        obj_json = json.load(mc.get_object(bucket_name=metric,
                                           object_name=obj.object_name))
        epoch_time = timegm(time.strptime(obj_json['ingest_timestamp'], "%H:%M:%S.%f - %b %d %Y"))
        datapoint = [obj_json['value'], epoch_time]
        datapoints.append(datapoint)
        # target = {'target': obj_json['name'], 'datapoints': [obj_json['value'], epoch_time]}
    return datapoints


def time_test():
    # now = datetime.now()  # current date and time
    # year = now.strftime("%Y")
    # month = now.strftime("%m")
    # day = now.strftime("%d")
    # hour = now.strftime("%H")
    # minute = now.strftime("%M")
    current_utc = datetime.utcnow().isoformat()
    return current_utc

# print(generate_datapoints_from_metrics('humidity'))
print(time_test())