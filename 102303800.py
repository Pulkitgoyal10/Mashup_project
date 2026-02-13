import sys
import os
import shutil
import warnings
import yt_dlp
from pydub import AudioSegment

# Suppress warnings for a clean CLI output
warnings.filterwarnings("ignore", category=SyntaxWarning)

def create_mashup(singer_name, n_videos, duration, output_filename):
    # Validation
    if n_videos <= 10:
        print("Error: Number of videos must be greater than 10.")
        return
    if duration <= 20:
        print("Error: Audio duration must be greater than 20.")
        return

    temp_dir = "temp_download_folder"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # yt-dlp options: searching, downloading, and converting to mp3
    # We use 'ytsearchN:' to search directly within yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'noprogress': True,
    }

    try:
        print(f"--- Searching and Downloading {n_videos} videos of {singer_name} ---")
        search_query = f"ytsearch{n_videos}:{singer_name}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # This searches and downloads in one step
            result_info = ydl.extract_info(search_query, download=True)
            
        # Get list of downloaded mp3 files
        downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
        
        final_mashup = AudioSegment.empty()

        print(f"--- Trimming and Merging Audios ---")
        for i, file in enumerate(downloaded_files):
            file_path = os.path.join(temp_dir, file)
            audio = AudioSegment.from_file(file_path)
            
            # Logic: Remove first 30s, take the next 'duration' seconds
            start_point = 30 * 1000 
            end_point = start_point + (duration * 1000)
            
            trimmed = audio[start_point:end_point]
            final_mashup += trimmed
            print(f"Processed file {i+1} of {len(downloaded_files)}")

        if len(final_mashup) > 0:
            final_mashup.export(output_filename, format="mp3")
            print("-" * 40)
            print(f"DONE! Final mashup saved as: {output_filename}")
            print("-" * 40)
        else:
            print("Error: Mashup could not be created.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Appropriate Message: Wrong number of inputs.")
        print("Usages: python 102303800.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    try:
        singer = sys.argv[1]
        n = int(sys.argv[2])
        y = int(sys.argv[3])
        output = sys.argv[4]
        create_mashup(singer, n, y, output)
    except ValueError:
        print("Appropriate Message: N and Y must be integers.")
