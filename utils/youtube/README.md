# Downloads a YouTube video (including Shorts) from a given URL

1. **Downloads a YouTube video (including Shorts) from a given URL.**
2. **Extracts and converts the audio to a WAV file.**
3. **Performs basic noise reduction to ensure the WAV file is clean.**

### **Prerequisites**

Before running the script, ensure you have the following installed:

1. **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).
2. **FFmpeg**: This is required by `pydub` for audio processing.
   - **Installation:**
     - **Windows:** Download from [FFmpeg Windows Builds](https://www.gyan.dev/ffmpeg/builds/) and follow the installation instructions.
     - **macOS:** Use Homebrew:

       ```bash
       brew install ffmpeg
       ```

     - **Linux:** Use your distribution’s package manager, e.g.,

       ```bash
       sudo apt-get install ffmpeg
       ```

3. **Python Libraries**: Install the necessary libraries using `pip`. You can do this by running the following command in your terminal or command prompt:

   ```bash
   pip install pytube pydub noisereduce numpy scipy
   ```

### **The Complete Python Script**

```python
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
```

### **How the Script Works**

1. **Downloading the Audio:**
   - The script uses `pytube` to download the audio stream from the provided YouTube URL.
   - It saves the downloaded audio in the `downloads` directory (created if it doesn't exist).

2. **Converting to WAV:**
   - Using `pydub`, the script converts the downloaded audio to a WAV file.
   - The audio is set to mono and a sample rate of 44.1kHz for consistency and quality.

3. **Noise Reduction:**
   - The `noisereduce` library is employed to perform basic noise reduction on the WAV file.
   - The cleaned audio is saved with a `_clean.wav` suffix.

4. **Cleanup (Optional):**
   - The script includes commented lines that can delete the original downloaded file and the intermediate WAV file if you wish to save space.

### **Running the Script**

1. **Save the Script:**
   - Save the above Python code in a file named, for example, `download_clean_wav.py`.

2. **Run the Script:**
   - Open your terminal or command prompt.
   - Navigate to the directory containing `download_clean_wav.py`.
   - Execute the script using Python:

     ```bash
     python download_clean_wav.py
     ```

   - The script will display progress messages and save the cleaned WAV file in the `downloads` directory.

3. **Customizing the YouTube URL:**
   - To process a different YouTube video or Short, replace the `youtube_url` variable in the `main()` function with your desired URL.

### **Additional Notes**

- **FFmpeg Requirement:**
  - Ensure FFmpeg is correctly installed and added to your system’s PATH. You can verify this by running `ffmpeg -version` in your terminal or command prompt. If it returns version information, it's correctly installed.

- **Noise Reduction Limitations:**
  - The `noisereduce` library provides basic noise reduction. For more advanced audio cleaning, consider using more sophisticated tools or algorithms.

- **Error Handling:**
  - The script includes basic error handling to inform you if something goes wrong during downloading, conversion, or noise reduction.

- **Extending Functionality:**
  - You can enhance the script by adding features like batch processing multiple URLs, a graphical user interface (GUI), or more advanced audio processing techniques.

### **Troubleshooting**

- **Pytube Errors:**
  - If you encounter issues with `pytube`, ensure you have the latest version installed:

    ```bash
    pip install --upgrade pytube
    ```

  - Sometimes, YouTube updates can break `pytube`. Check the [pytube GitHub repository](https://github.com/pytube/pytube) for updates or patches.

- **FFmpeg Issues:**
  - If `pydub` cannot find FFmpeg, ensure that FFmpeg is installed and its executable is in your system’s PATH.

- **Permission Errors:**
  - If you encounter permission-related errors while saving files, ensure you have the necessary write permissions for the target directory.

