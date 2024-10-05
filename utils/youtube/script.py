import os
from pytube import YouTube
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import wave

def download_youtube_audio(youtube_url, download_path='downloads'):
    """
    Downloads the audio from a YouTube video.

    Args:
        youtube_url (str): URL of the YouTube video.
        download_path (str): Directory where the audio will be saved.

    Returns:
        str: Path to the downloaded audio file.
    """
    try:
        yt = YouTube(youtube_url)
        print(f"Title: {yt.title}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio streams available for this video.")

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        downloaded_file = audio_stream.download(output_path=download_path)
        print(f"Downloaded audio to: {downloaded_file}")
        return downloaded_file
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def convert_to_wav(input_file, output_file):
    """
    Converts an audio file to WAV format.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path where the WAV file will be saved.
    """
    try:
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1)  # Mono
        audio = audio.set_frame_rate(44100)  # 44.1kHz
        audio.export(output_file, format="wav")
        print(f"Converted to WAV: {output_file}")
    except Exception as e:
        print(f"Error converting to WAV: {e}")

def reduce_noise(input_wav, output_wav):
    """
    Performs noise reduction on a WAV file.

    Args:
        input_wav (str): Path to the input WAV file.
        output_wav (str): Path where the cleaned WAV file will be saved.
    """
    try:
        # Read the WAV file
        with wave.open(input_wav, 'rb') as wf:
            rate = wf.getframerate()
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            n_frames = wf.getnframes()
            audio_data = wf.readframes(n_frames)
            audio_np = np.frombuffer(audio_data, dtype=np.int16)

        # If stereo, take one channel
        if n_channels > 1:
            audio_np = audio_np[::n_channels]

        # Perform noise reduction
        reduced_noise = nr.reduce_noise(y=audio_np, sr=rate)

        # Save the cleaned audio
        with wave.open(output_wav, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sampwidth)
            wf.setframerate(rate)
            wf.writeframes(reduced_noise.astype(np.int16).tobytes())

        print(f"Noise reduced WAV saved as: {output_wav}")
    except Exception as e:
        print(f"Error reducing noise: {e}")

def main():
    # Replace this URL with any YouTube Shorts or regular video URL
    youtube_url = "https://www.youtube.com/shorts/kCyX3MeHBaw"
    download_path = 'downloads'

    # Step 1: Download the audio
    raw_audio = download_youtube_audio(youtube_url, download_path)
    if not raw_audio:
        print("Failed to download audio. Exiting.")
        return

    # Step 2: Convert the audio to WAV
    wav_file = os.path.splitext(raw_audio)[0] + ".wav"
    convert_to_wav(raw_audio, wav_file)

    # Step 3: Perform noise reduction
    cleaned_wav = os.path.splitext(raw_audio)[0] + "_clean.wav"
    reduce_noise(wav_file, cleaned_wav)

    # Optional: Cleanup intermediate files
    # os.remove(raw_audio)
    # os.remove(wav_file)

    print("Processing complete. Clean WAV file is ready.")

if __name__ == "__main__":
    main()
