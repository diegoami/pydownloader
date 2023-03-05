
from pytube import Playlist

import os
import yaml
import argparse


def compare_videos_from_playlist(playlist_url, playlist_dir):


    playlist = Playlist(playlist_url)
    videos = playlist.videos
    videos_len = len(videos)
    files_amount = len(os.listdir(playlist_dir))
    print(f"There are {files_amount} files and {videos_len} videos in the playlist {playlist_dir}")
    if videos_len > files_amount:
        for index in range(files_amount, videos_len):
            video = videos[index]
            video_id = video.video_id
            print(f"Downloading {index + 1}_{video_id} to {playlist_dir}")
            video_streams = video.streams
            downl_stream = video_streams.get_highest_resolution()
            max_tries = 10
            successful = False
            while max_tries > 0 and not successful:
                try:
                    downl_stream.download(output_path=playlist_dir,
                                          filename=f'{video_id}.mp4',
                                          filename_prefix=str(index + 1) + '_',
                                          skip_existing=True,
                                          max_retries=3, timeout=600)
                    successful = True
                    print(f"Sucessfully downloaded {index + 1}_{video_id} to {playlist_dir}")

                except Exception as httpe:
                    print("Error while trying to download, retrying")
                    max_tries -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # option that takes a value
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:
        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)
            target_dir = conf_info["target_dir"]
            monitored_playlists = conf_info["monitored_playlists"]
            for playlist_id in monitored_playlists:
                playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
                playlist_dir = os.path.join(target_dir, playlist_id)
                compare_videos_from_playlist(playlist_url, playlist_dir)