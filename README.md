YouTube Playlist Downloader
===========================

A Python script to download all videos from a YouTube playlist to your local drive. The script uses the `pytube` library to fetch and download the videos.

Requirements
------------

-   Python 3.x
-   pytube library

Installation
------------

To install the required library, run the following command in your terminal or command prompt:


`pip install pytube`

Usage
-----

The script requires a configuration file in YAML format that specifies the YouTube playlist ID, the target directory for the downloaded videos, and other options.

Here is a sample configuration file:

yamlCopy code

```
playlist_id: PLlFmjZCvV7Wct4gx4VdO4zXk3B8hcQQSQ
target_dir: ~/Downloads/Youtube
start: 0
end: 1000
audio_stream: False
```

In this configuration file, `playlist_id` is the ID of the YouTube playlist you want to download videos from, `target_dir` is the directory where the downloaded videos will be saved, `start` and `end` are optional parameters that specify the range of videos to download (for example, you can download only the first 100 videos by setting `start` to 0 and `end` to 100), and `audio_stream` is an optional parameter that determines whether to download only the audio stream of the videos or not.

To run the script, use the following command:

cssCopy code

```
python youtube_playlist_downloader.py --config <configuration_file>`
```
where `<configuration_file>` is the path to the configuration file.

Note
----

The script downloads the highest resolution video stream by default, or the audio-only stream if the `audio_stream` option is set to `True`. If there are any errors during the download process, the script will retry the download up to 10 times.

