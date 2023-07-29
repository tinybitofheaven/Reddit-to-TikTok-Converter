import random
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from settings import *

# Get background video.
def clip_background_video(submission, clip_length):
    # Start at 3 minutes to prevent issues.
    initial_value = 180
    background_video = VideoFileClip(f"{BACKGROUND_VIDEO_PATH}minecraft.mp4")
    start_time = random.randrange(initial_value, int(background_video.duration) - int(clip_length))
    end_time = start_time + clip_length
    
    ffmpeg_extract_subclip(
            f"{BACKGROUND_VIDEO_PATH}minecraft.mp4",
            start_time,
            end_time,
            targetname=f"{ASSETS_PATH}{submission.id}/{VIDEO_PATH}background.mp4",
        )