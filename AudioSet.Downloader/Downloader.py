import csv
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import asyncio
from aiofiles import open as aio_open
from typing import Union

try:
    from downloader_configs import *
except ImportError:
    sys.stderr.write("!Panic!: Config file not found.")
    exit(-1)

try:
    import pytube
except ImportError:
    print("Trying to install pytube.")
    subprocess.run([sys.executable, "-m", "pip", "install", "pytube"])
    import pytube

VERSION = [1, 0, 2]


async def run_subprocess(cmd):
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f'Command failed with exit code {
                      proc.returncode}\n{stderr.decode()}')
    return proc.returncode == 0


async def convert_to_wav(filename: str, save_dir: str) -> Union[str, None]:
    basename = os.path.basename(filename)
    name, _ = os.path.splitext(basename)
    output_name = os.path.join(save_dir, f"{name}.wav")
    success = await run_subprocess([
        "ffmpeg",
        "-i", filename,
        output_name
    ])
    if not success:
        return None
    return output_name


async def splits_audio(filename: str, start_sec: int, end_sec: int, save_dir: str) -> Union[str, None]:
    basename = os.path.basename(filename)
    name, _ = os.path.splitext(basename)
    output_name = os.path.join(save_dir, f"{name}.wav")
    success = await run_subprocess([
        "ffmpeg",
        "-ss", str(start_sec),
        "-i", filename,
        "-t", str(end_sec - start_sec),
        output_name
    ])
    if not success:
        return None
    return output_name


async def download_video(url: str, youtube_id: str, save_dir: str, highest_quality=False, only_audio=False) -> Union[str, None]:
    try:
        if only_audio:
            download_file_name = pytube.YouTube(
                url).streams.get_audio_only().download()
        elif highest_quality:
            download_file_name = pytube.YouTube(url).streams.filter(
                progressive=True).order_by('resolution').desc().first().download()
        else:
            download_file_name = pytube.YouTube(url).streams.first().download()
        _, ext_name = os.path.splitext(download_file_name)
        moved_name = os.path.join(save_dir, f"{youtube_id}{ext_name}")
        pathlib.Path(download_file_name).rename(moved_name)
        return moved_name
    except Exception as e:
        logging.error(f"Download failed for {url}: {e}")
        return None


async def process_video(url, ytid, dl_video_save_dir, wav_temps_dir, splits_dir, start_sec, end_sec, only_audio, highest_quality, delete_video, delete_wav):
    moved_name = await download_video(url, ytid, dl_video_save_dir, highest_quality, only_audio)
    if moved_name:
        logging.info(f"Converting file<{moved_name}> to .wav format.")
        wave_name = await convert_to_wav(moved_name, wav_temps_dir)
        if wave_name:
            logging.info(f"Splitting file<{wave_name}>, from {
                         start_sec} to {end_sec}")
            split_name = await splits_audio(wave_name, start_sec, end_sec, splits_dir)
            if split_name:
                if delete_video:
                    logging.info(f"Deleting video file<{moved_name}>")
                    os.remove(moved_name)
                if delete_wav:
                    logging.info(f"Deleting wave file<{wave_name}>")
                    os.remove(wave_name)
                return split_name
    return None


async def main(csv_file: str, timer: int, remove_exist: bool, youtube_url_fmt: str, only_audio=False, highest_quality=False, delete_video=False, delete_wav=False) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s - pid:%(process)d", handlers=[
                        logging.FileHandler(filename=f"{csv_file}_dl.log", mode="w"), logging.StreamHandler(stream=sys.stdout)])
    dl_video_save_dir = f"./{csv_file}.download/"
    wav_temps_dir = f"./{csv_file}.waves/"
    splits_dir = f"./{csv_file}.splits/"
    if not os.path.exists(dl_video_save_dir):
        os.makedirs(dl_video_save_dir)
    else:
        if remove_exist:
            shutil.rmtree(dl_video_save_dir)
            os.makedirs(dl_video_save_dir)
    if not os.path.exists(wav_temps_dir):
        os.makedirs(wav_temps_dir)
    else:
        if remove_exist:
            shutil.rmtree(wav_temps_dir)
            os.makedirs(wav_temps_dir)
    if not os.path.exists(splits_dir):
        os.makedirs(splits_dir)
    else:
        if remove_exist:
            shutil.rmtree(splits_dir)
            os.makedirs(splits_dir)

    tasks = []
    async with aio_open(f"{csv_file}.split-pos.csv", "w") as split_audio_positive_label:
        async with aio_open(csv_file, "r") as csv_fin:
            reader = csv.reader(await csv_fin.readlines())
            for i, line in enumerate(reader):
                if 0 < timer == i:
                    break
                raw = {"YTID": line[0], "start_sec": int(float(line[1].replace(" ", ""))), "end_sec": int(
                    float(line[2].replace(" ", ""))), "positive_labels": line[3:]}
                url = youtube_url_fmt.format(YTID=raw["YTID"])
                task = asyncio.create_task(process_video(url, raw["YTID"], dl_video_save_dir, wav_temps_dir, splits_dir,
                                           raw["start_sec"], raw["end_sec"], only_audio, highest_quality, delete_video, delete_wav))
                tasks.append(task)

            for future in asyncio.as_completed(tasks):
                split_name = await future
                if split_name:
                    await split_audio_positive_label.write(f'{split_name}, {"{}".format(",".join(raw["positive_labels"]))}\n')
                    await split_audio_positive_label.flush()


if __name__ == "__main__":
    if DEBUG:
        asyncio.run(main(csv_file=CSV_FILE_NAMES[0], timer=TIMER, remove_exist=REMOVE_EXIST_DOWNLOADS, youtube_url_fmt=YTB_URL_FORMAT,
                    only_audio=ONLY_AUDIO, highest_quality=DOWN_HIGHEST_QUALITY, delete_video=DELETE_DOWNLOADED_VIDEO, delete_wav=DELETE_WAVE_FILE))
    else:
        tasks = [main(csv_file=csv_file, timer=TIMER, remove_exist=REMOVE_EXIST_DOWNLOADS, youtube_url_fmt=YTB_URL_FORMAT, only_audio=ONLY_AUDIO,
                      highest_quality=DOWN_HIGHEST_QUALITY, delete_video=DELETE_DOWNLOADED_VIDEO, delete_wav=DELETE_WAVE_FILE) for csv_file in CSV_FILE_NAMES]
        asyncio.run(asyncio.gather(*tasks))
        print("All subprocesses done.")
