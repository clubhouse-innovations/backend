import boto3

from settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, S3_DOCS_BUCKET, DEFAULT_REGION_S3
from transcribe import TranscriptionResult


def upload_to_s3(data, dir_name, file_name, extension, is_public=False):
    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=DEFAULT_REGION_S3)

    file_name = f'{dir_name}/{file_name}.{extension}'
    try:
        if is_public:
            s3.put_object(Body=data, Bucket=S3_DOCS_BUCKET, Key=file_name, ACL='public-read')
        else:
            s3.put_object(Body=data, Bucket=S3_DOCS_BUCKET, Key=file_name)
    except Exception as ex:
        print(f'Error when uploading {file_name}. Error [{ex}]')


def upload_transcription(session_name, transcription_results: TranscriptionResult):
    upload_to_s3(transcription_results.full_text, session_name, 'full_text', 'txt', True)
    upload_to_s3(transcription_results.speakers_json, session_name, 'transcription_speakers', 'json', True)
