from PIL import Image
import os
from time import time
from subprocess import run as srun, check_output
from json import loads as jsonloads

def take_ss(video_file, duration):
    des_dir = 'Thumbnails'
    if not os.path.exists(des_dir):
        os.mkdir(des_dir)
    des_dir = os.path.join(des_dir, f"{time()}.jpg")
    if duration is None:
        duration = get_media_info(video_file)[0]
    if duration == 0:
        duration = 3
    duration = duration // 2

    status = srun(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(duration),
                   "-i", video_file, "-frames:v", "1", des_dir])

    if status.returncode != 0 or not os.path.lexists(des_dir):
        return None
    with Image.open(des_dir) as img:
        img.convert("RGB").save(des_dir, "JPEG")

    return des_dir


def get_media_info(path):
    try:
        result = check_output(["ffprobe", "-hide_banner", "-loglevel", "error", "-print_format",
                               "json", "-show_format", "-show_streams", path]).decode('utf-8')
    except Exception as e:
        print(f'{e}. Mostly file not found!')
        return 0, None, None

    fields = jsonloads(result).get('format')
    if fields is None:
        print(f"get_media_info: {result}")
        return 0, None, None

    duration = round(float(fields.get('duration', 0)))

    return duration


def allinfo(file,thumb=None):
    duration = get_media_info(file)
    if thumb is None:
        thumb = take_ss(file, duration)
    if thumb is not None:
        with Image.open(thumb) as img:
            width, height = img.size
    else:
        width = 480
        height = 320

    return thumb,duration,width,height
