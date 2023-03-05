
from pytube import Playlist

import os
import yaml
import argparse


def download_videos_from_playlist(playlist_url,  playlist_dir, audio_stream, start, end):
    """
    This method download_videos_from_playlist downloads videos from a given playlist URL. The method takes the following parameters:

    playlist_url: the URL of the playlist from which videos will be downloaded.
    audio_stream: a boolean indicating whether to download audio-only streams (if True) or the highest resolution video stream (if False).
    start: an integer indicating the index of the first video to be downloaded.
    end: an integer indicating the index of the last video to be downloaded.
    target_dir: the target directory where the downloaded videos will be stored.
    The method starts by creating a Playlist object from the playlist_url and retrieving all the videos in the playlist. Then, it loops through the videos and downloads each video if its index (index + 1) is within the start and end range.

    If audio_stream is True, it selects the audio-only stream for each video, otherwise it selects the highest resolution video stream. The video is then downloaded using the download method of the selected stream. The method uses a loop with a maximum of 10 tries and retries downloading if an exception occurs. The downloaded video is stored in the target directory with a filename that includes the index and the video ID of the video.

    If the video index is outside the start and end range, the method simply skips downloading that video and prints a message indicating that it has been skipped.
    """


    playlist = Playlist(playlist_url)
    videos = playlist.videos
    for index, video in enumerate(videos):
        video_id = video.video_id
        if start <= index + 1 <= end:
            print(f"Downloading {index + 1}_{video_id} to {playlist_dir}")
            if not audio_stream:
                video_streams = video.streams
                downl_stream = video_streams.get_highest_resolution()
            else:
                audio_streams = video.streams.filter(only_audio=True)
                downl_stream = audio_streams.get_audio_only()

            # video_to_download.on_progress()
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

        else:
            print(f"Skipping {video_id} to {playlist_dir}")


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
            download_videos_from_playlist(playlist_url, playlist_dir, audio_stream, start, end)
