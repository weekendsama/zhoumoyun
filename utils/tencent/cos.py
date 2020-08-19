from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings


def create_bucket(bucket, region='ap-chengdu'):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)
    client.create_bucket(
        Bucket=bucket,
        ACL='public-read'
    )


def upload_file(bucket, region, file_object, key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_COS_ID, SecretKey=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)

    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key=key
    )
    return 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, key)


def delete_file(bucket, region, key):
    config = CosConfig(Region=region, Secret_key=settings.TENCENT_COS_KEY, Secret_id=settings.TENCENT_COS_ID)
    client = CosS3Client(config)

    client.delete_object(
        Bucket=bucket,
        Key=key
    )


def delete_file_list(bucket, region, key_list):
    config = CosConfig(Region=region, Secret_id=settings.TENCENT_COS_ID, Secret_key=settings.TENCENT_COS_KEY)
    client = CosS3Client(config)
    objects = {
        'Quiet': 'true',
        'Object': key_list
    }
    client.delete_objects(
        Bucket=bucket,
        Delete=objects
    )
