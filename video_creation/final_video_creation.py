import os
from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeAudioClip, CompositeVideoClip, TextClip, ImageClip
from moviepy.video.tools.subtitles import SubtitlesClip

import reddit_scraper

import audio_handler
import background_handler
import image_handler
from settings import *
from utils import create_folders, clear_folders


def create_final_video(submission):
    # audio & subtitles
    subtitles_list = audio_handler.save_text_to_mp3(submission)
    mp3_file_path = ASSETS_PATH + submission.id + "/" + MP3_PATH
    audio = []
    subtitles = []
    timer = 0
    start_time = 0
    counter = 0
    for audio_file in os.listdir(mp3_file_path):
        audioClip = AudioFileClip(f"{mp3_file_path}/{audio_file}")
        # skip title timing
        if(audio_file == "0.mp3"):
            audio.append(audioClip)
            timer += audioClip.duration
            start_time = timer
        else:
            audio.append(audioClip)
            subtitles.append(((timer, timer + audioClip.duration), subtitles_list[counter]))
            counter += 1
            timer += audioClip.duration
            
    # background
    background_handler.clip_background_video(submission, clip_length=timer + 1)
    videoClip = VideoFileClip(f"{ASSETS_PATH}{submission.id}/{VIDEO_PATH}background.mp4")
        
    # generate subtitles
    generator = lambda txt: TextClip(txt, font='Verdana-Bold', fontsize=100, color='white', stroke_color='black', stroke_width=6, method='caption', size=videoClip.size)
    subtitles = SubtitlesClip(subtitles, generator)
    subtitles.set_position(('center','middle'))
    
    audio_concat = concatenate_audioclips(audio)
    final_audio = CompositeAudioClip([audio_concat])
    videoClip.audio = final_audio
    
    # screenshot
    # image_handler.take_screenshot_of_entire_post(submission)
    # title = ImageClip(f"{ASSETS_PATH}{submission.id}/{IMG_PATH}title.png").set_start(0).set_duration(start_time).set_position(("center","center"))
    
    # fake screenshot
    title = ImageClip(f"{POST_BG_IMG_PATH}bg.png").set_start(0).set_duration(start_time).set_position(("center", 720)).resize(width=videoClip.size[0] - 50)
    size = [videoClip.size[0] - 100, videoClip.size[1]]
    title_generator = lambda txt: TextClip(txt, font='Verdana-Bold', fontsize=42, color='white', align="West", method='caption', size=size)
    title_text = SubtitlesClip([((0, start_time), submission.title)], title_generator).set_position((50, "center"))
    author_generator = lambda txt: TextClip(txt, font='Verdana-Bold', fontsize=38, color='white', align="West", method='caption', size=size)
    author_text = SubtitlesClip([((0, start_time), submission.author.name)], author_generator).set_position((210, -180))
    
    final_video = CompositeVideoClip([videoClip, title, author_text, title_text, subtitles])
    
    # final composite
    final_video.write_videofile(f"{FINAL_VIDEOS_PATH}/{submission.id}.mp4")
    
#-----------------TESTING-----------------#

# Uncomment to generate a video.

threads = reddit_scraper.get_threads_from_subreddit(reddit_scraper.SUBREDDIT, reddit_scraper.POST_LIMIT)
clear_folders(threads[0])
create_folders(threads[0])
create_final_video(threads[0])