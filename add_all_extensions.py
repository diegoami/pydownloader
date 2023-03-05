import urllib.error

from pytube import Playlist
import os

import os
import yaml
import time
import argparse
import shutil

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
            for playlist_id in os.listdir(target_dir):
                playlist_dir = os.path.join(target_dir, playlist_id)
                for file_name in os.listdir(playlist_dir):
                    if not file_name.endswith('.mp4'):
                        src = os.path.join(playlist_dir, file_name)
                        dest = os.path.join(playlist_dir, file_name+'.mp4')
                        shutil.move(src, dest)