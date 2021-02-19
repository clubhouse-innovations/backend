
from google.cloud import speech_v1p1beta1 as speech
import soundfile as sf
from datetime import timedelta

def convert_time_delta(td):
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

client = speech.SpeechClient()

speech_file = "./clubhouse_chat.wav"

f = sf.SoundFile(speech_file)
print('samples = {}'.format(len(f)))
sample_rate = f.samplerate
print('sample rate = {}'.format(sample_rate))
channel_count = f.channels
print('audio channel count = {}'.format(channel_count))
total_time = len(f) / f.samplerate
print('Total seconds = {}'.format(total_time))

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=sample_rate,
    language_code="en-US",
    enable_speaker_diarization=True,
    audio_channel_count=channel_count,
    # diarization_speaker_count=channel_count,
)
# print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)
# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
confidence_value = float(response.results[0].alternatives[0].confidence)

print("response list:")
response_list_1 = response.results[-1].alternatives[0].words
speaker_set_1 = set()
prev_speaker_1 = response_list_1[0].speaker_tag
speaker_dict_1 = {}
speaker_start_time = response_list_1[0].start_time.total_seconds()
speaker_end_time = response_list_1[0].end_time.total_seconds()
speaker_set_1.add(prev_speaker_1)
for i,val in enumerate(response_list_1):
	if i == 0:
		continue
	if val.speaker_tag not in speaker_set_1:
		speaker_set_1.add(val.speaker_tag)

	if prev_speaker_1 != val.speaker_tag:
		if prev_speaker_1 not in speaker_dict_1:
			speaker_dict_1[prev_speaker_1] = [(speaker_start_time,speaker_end_time)]
		else:
			speaker_dict_1[prev_speaker_1].append((speaker_start_time,speaker_end_time))
		prev_speaker_1 = val.speaker_tag
		speaker_start_time = val.start_time.total_seconds()

	elif i == len(response_list_1)-1:
		if prev_speaker_1 not in speaker_dict_1:
			final_end_time = val.end_time.total_seconds()
			speaker_dict_1[prev_speaker_1] = [(speaker_start_time,final_end_time)]
		else:
			final_end_time = val.end_time.total_seconds()
			speaker_dict_1[prev_speaker_1].append((speaker_start_time,final_end_time))
	else:
		speaker_end_time = val.end_time.total_seconds()



response_list_2 = response.results[0].alternatives[0].words
speaker_set_2 = set()
prev_speaker_2 = response_list_2[0].speaker_tag
speaker_dict_2 = {}
speaker_start_time_2 = response_list_2[0].start_time.total_seconds()
speaker_end_time_2 = response_list_2[0].end_time.total_seconds()
speaker_set_2.add(prev_speaker_2)

for i,val in enumerate(response_list_2):
	if i == 0:
		continue
	if val.speaker_tag not in speaker_set_2:
		speaker_set_2.add(val.speaker_tag)

	if prev_speaker_2 != val.speaker_tag:
		if prev_speaker_2 not in speaker_dict_2:
			speaker_dict_2[prev_speaker_2] = [(speaker_start_time_2,speaker_end_time_2)]
		else:
			speaker_dict_2[prev_speaker_2].append((speaker_start_time_2,speaker_end_time_2))
		prev_speaker_2 = val.speaker_tag
		speaker_start_time_2 = val.start_time.total_seconds()

	elif i == len(response_list_2)-1:
		if prev_speaker_2 not in speaker_dict_2:
			final_end_time = val.end_time.total_seconds()
			speaker_dict_2[prev_speaker_2] = [(speaker_start_time_2,final_end_time)]
		else:
			final_end_time = val.end_time.total_seconds()
			speaker_dict_2[prev_speaker_2].append((speaker_start_time_2,final_end_time))
	else:
		speaker_end_time_2 = val.end_time.total_seconds()

# i have created a dict for both alternative transcriptions
# transcriptions 2 seems to be working better
print(speaker_set_1)
print(speaker_dict_1)
print(speaker_set_2)
print(speaker_dict_2)
# print("condience value: "+str(confidence_value))

