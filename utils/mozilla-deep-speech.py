import requests
import os

def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        print(f"Downloading {filename}...")
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=block_size):
                size = f.write(chunk)
                downloaded += size
                done = int(50 * downloaded / total_size)
                print(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes", end='', flush=True)
    print("\nDownload complete!")

# DeepSpeech model URLs (update these if there's a newer version)
model_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
scorer_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"

# Set the specific download path
download_path = "/Users/admin/Desktop/earnings-transcription-api"

# Create the directory if it doesn't exist
os.makedirs(download_path, exist_ok=True)

# Download the files
model_filename = os.path.join(download_path, "deepspeech-0.9.3-models.pbmm")
scorer_filename = os.path.join(download_path, "deepspeech-0.9.3-models.scorer")

download_file(model_url, model_filename)
download_file(scorer_url, scorer_filename)

print("Both model files have been downloaded successfully to:")
print(download_path)