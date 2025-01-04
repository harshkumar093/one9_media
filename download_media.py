import requests
import os
# Downloads file from source URL, and saves it to the given path
def download_media(url, save_path):
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # Open a file in binary write mode to save the MP4 video
        with open(save_path, 'wb') as video_file:
            # Iterate over the response content and write it to the file
            for chunk in response.iter_content(chunk_size=1024):
                video_file.write(chunk)

        print("Media downloaded successfully! :: download_url: {url}, save_location: {save_path}")
    else:
        print(f"Failed to download media :: status_code: {response.status_code}")