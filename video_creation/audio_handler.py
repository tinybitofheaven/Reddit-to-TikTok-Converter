from gtts import gTTS
import re
from mutagen.mp3 import MP3

from settings import *

# Clean text for better TTS and no directory errors.
def sanitize_text(text: str) -> str:
    r"""Sanitizes the text for tts.
        What gets removed:
     - following characters`^_~@!&;#:-%“”‘"%*/{}[]()\|<>?=+`
     - any http or https links

    Args:
        text (str): Text to be sanitized

    Returns:
        str: Sanitized text
    """

    # remove any urls from the text
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    result = re.sub(regex_urls, " ", text)

    # note: not removing apostrophes
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!&;#:\-%—“”‘\"%\*/{}\[\]\(\)\\|<>=+]"
    result = re.sub(regex_expr, " ", result)
    result = result.replace("+", "plus").replace("&", "and")

    # emoji removal if the setting is enabled
    # if settings.config["settings"]["tts"]["no_emojis"]:
    #     result = clean(result, no_emoji=True)

    # remove extra whitespace
    return " ".join(result.split())

def split_thread_text(text: str):
    text_list = text.split(".")
    while("" in text_list):
        text_list.remove("")
    return text_list

# Returns a list of strings from the subreddit submission
def save_text_to_mp3(submission) -> list[str]:
    mp3_file_path = ASSETS_PATH + submission.id + "/" + MP3_PATH
    
    # Make tts for title
    tts = gTTS(text=submission.title, lang="en")
    tts.save(f"{mp3_file_path}/0.mp3")
    
    length_of_mp3_files = 0
    length_of_mp3_files += MP3(f"{mp3_file_path}/0.mp3").info.length
    
    txt = sanitize_text(submission.selftext)
    split_txt = split_thread_text(txt)
    
    # make tts for each line in the thread
    count = 1
    for line in split_txt:
        #IMPORTANT: PUTS LIMIT ON HOW MUCH TEXT IS SPOKEN, CHANGE THIS FOR TESTING
        if length_of_mp3_files > 10:
            break

        if line == "":
            continue
        tts = gTTS(text=line, lang="en")
        tts.save(f"{mp3_file_path}/{count}.mp3")
        length_of_mp3_files += MP3(f"{mp3_file_path}/{count}.mp3").info.length
        count += 1
    return split_txt