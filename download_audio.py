#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2021 Apple Inc. All Rights Reserved.
#

"""
For each podcast episode:
* Download the raw mp3/m4a file
* Convert it to a 16k mono wav file
* Remove the original file

Changed from the original script to read the csv with pandas, download with requests instead
of wget (so it works on Windows), and skip an episode instead of crashing when its link is dead
or ffmpeg fails.
"""

import argparse
import pathlib
import subprocess

import pandas as pd
import requests
from tqdm import tqdm

AUDIO_TYPES = ['.mp3', '.m4a', '.mp4']

parser = argparse.ArgumentParser(
    description='Download raw audio files for SEP-28k-Extended and convert to 16kHz mono wavs.')
parser.add_argument('--episodes', required=True,
                    help='Path to the episodes csv (e.g. SEP-28k-Extended_episodes.csv)')
parser.add_argument('--wavs', default='wavs',
                    help='Directory where converted wav files will be saved')
args = parser.parse_args()

episodes = pd.read_csv(args.episodes)
episodes['url'] = episodes['url'].str.strip()
episodes['Show'] = episodes['Show'].str.strip()


def download(url, path):
    """Stream url to path in 64 KB chunks, with a progress bar."""
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    size = int(response.headers.get('content-length', 0))
    with open(path, 'wb') as f, tqdm(total=size, unit='B', unit_scale=True,
                                     desc=f'  {path.name}', leave=False) as bar:
        for chunk in response.iter_content(chunk_size=65536):
            f.write(chunk)
            bar.update(len(chunk))


for _, row in tqdm(episodes.iterrows(), total=len(episodes), desc='Episodes'):
    show, ep_id, url = row['Show'], row['EpId'], row['url']

    episode_dir = pathlib.Path(args.wavs) / show
    episode_dir.mkdir(parents=True, exist_ok=True)
    wav_path = episode_dir / f'{ep_id}.wav'
    if wav_path.exists():
        continue

    # Name the download after its file type (defaults to .mp4, as the original loop did)
    ext = next((e for e in AUDIO_TYPES if e in url), AUDIO_TYPES[-1])
    raw_path = episode_dir / f'{ep_id}{ext}'
    print(f'\nProcessing {show} ep{ep_id}')

    if not raw_path.exists():
        try:
            download(url, raw_path)
        except requests.exceptions.RequestException as e:
            print(f'  download error for {url}:\n  {e}')
            raw_path.unlink(missing_ok=True)  # don't leave a half-downloaded file behind
            continue

    # Convert to mono (-ac 1) at 16 kHz (-ar 16000)
    result = subprocess.run(['ffmpeg', '-i', str(raw_path), '-ac', '1', '-ar', '16000', str(wav_path)],
                            capture_output=True)
    if result.returncode != 0:
        print(f'  ffmpeg error for {raw_path.name}:\n{result.stderr.decode()}')
        continue

    raw_path.unlink()
