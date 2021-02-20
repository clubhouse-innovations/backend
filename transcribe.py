import json
import os
import uuid
from dataclasses import dataclass
from time import sleep
from typing import Optional

from rev_ai import JobStatus
from rev_ai.apiclient import RevAiAPIClient

import settings

MAX_RETRIES = 5


@dataclass
class TranscriptionResult:
    full_text: str
    speakers_json: str


def wait_for_job_finish(client, job_id):
    retries = 0
    job_details = client.get_job_details(job_id)
    while job_details.status == JobStatus.IN_PROGRESS and retries < MAX_RETRIES:
        sleep(5)
        job_details = client.get_job_details(job_id)
        retries += 1

    if retries == MAX_RETRIES and job_details.status == JobStatus.IN_PROGRESS:
        raise Exception('Maximum retries for RAV AI reached')


def transcribe_rev_ai(file_obj) -> Optional[TranscriptionResult]:
    client = RevAiAPIClient(settings.REV_AI_ACCESS_KEY)
    temp_file_name = f'{str(uuid.uuid4())}.wav'
    try:
        file_obj.save(temp_file_name)
        job = client.submit_job_local_file(temp_file_name)
        wait_for_job_finish(client, job.id)

        transcript_text = client.get_transcript_text(job.id)
        transcript_json = json.dumps(client.get_transcript_json(job.id))
        os.remove(temp_file_name)
        return TranscriptionResult(transcript_text, transcript_json)
    except Exception as ex:
        os.remove(temp_file_name)
        raise
