from moviepy.editor import VideoFileClip
import os
from vosk import Model, KaldiRecognizer
import wave
import json
import subprocess


def ap(video_file):
    wav_file = "audio.wav" #wav file needed for speech to text conversion
    output_text_file = "atext.txt"
    model_path = "model"  # Put vosk model folder here (like 'vosk-model-small-en-us-0.15')

    #Extract audio from video
    video_clip = VideoFileClip(video_file)
    video_clip.audio.write_audiofile("temp_audio.mp3")
    video_clip.close()

    #Convert to mono WAV with ffmpeg
    ffmpeg_path = r"D:\EasyMeet\ffmpeg\bin\ffmpeg.exe" #converts mp3 o wav file
    command = [
        ffmpeg_path, "-y",
        "-i", "temp_audio.mp3",
        "-ac", "1",  # mono
        "-ar", "16000",  # 16kHz sample rate
        "-sample_fmt", "s16",  # 16-bit signed PCM
        wav_file
    ]
    subprocess.run(command, shell=True)

    #delete temp mp3
    os.remove("temp_audio.mp3")

    #Speech-to-text using Vosk
    model = Model(model_path)
    wf = wave.open(wav_file, "rb")

    # Confirm format
    #if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        #raise ValueError("Audio must be WAV format PCM mono.")

    rec = KaldiRecognizer(model, wf.getframerate()) #speech to text process
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result())["text"])

    results.append(json.loads(rec.FinalResult())["text"])

    #Save output to text file
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    wf.close()
    os.remove(wav_file)
