import urllib.error

from pytube import Playlist
import os

import os
import yaml
import time
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # option that takes a value
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:
        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)

            playlist_id = conf_info["playlist_id"]

            target_dir = conf_info["target_dir"]
            start = conf_info.get("start", 0)
            end = conf_info.get("end", 1000)
            audio_stream = conf_info.get("audio_stream", False)
            playlist_dir = os.path.join(target_dir, playlist_id)
            os.makedirs(playlist_dir, exist_ok=True)
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            playlist = Playlist(playlist_url)
            videos = playlist.videos

            for index, video in enumerate(videos):
                 video_id = video.video_id
                 if start <= index+1 <= end:
                     print(f"Downloading {index+1}_{video_id} to {playlist_dir}")
                     if not audio_stream:
                         video_streams = video.streams
                         downl_stream = video_streams.get_highest_resolution()
                     else:
                         audio_streams = video.streams.filter(only_audio=True)
                         downl_stream = audio_streams.get_audio_only()

                     #video_to_download.on_progress()
                     max_tries = 10
                     successful = False
                     while max_tries > 0 and not successful:
                         try:
                             downl_stream.download(output_path=playlist_dir,
                                                     filename=f'{video_id}.mp4',
                                                     filename_prefix=str(index+1)+'_',
                                                     skip_existing=True,
                                                     max_retries=3, timeout=600)
                             successful = True
                             print(f"Sucessfully downloaded {index + 1}_{video_id} to {playlist_dir}")

                         except Exception as httpe:
                             print("Error while trying to download, retrying")
                             max_tries -= 1

                 else:
                     print(f"Skipping {video_id} to {playlist_dir}")
