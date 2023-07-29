import os, shutil
from settings import *

def create_folders(reddit_id):
    try:
        if not os.path.exists(f"{ASSETS_PATH}{reddit_id}/"):
            os.makedirs(f"{ASSETS_PATH}{reddit_id}/{MP3_PATH}")
            os.makedirs(f"{ASSETS_PATH}{reddit_id}/{IMG_PATH}")
            os.makedirs(f"{ASSETS_PATH}{reddit_id}/{VIDEO_PATH}")
    except OSError:
        print("Error: creating directory." + reddit_id)
        
def clear_folders(reddit_id):
    if os.path.exists(f"{ASSETS_PATH}{reddit_id}/"):
        delete_files(f"{ASSETS_PATH}{reddit_id}/{MP3_PATH}")
        delete_files(f"{ASSETS_PATH}{reddit_id}/{IMG_PATH}")
        delete_files(f"{ASSETS_PATH}{reddit_id}/{VIDEO_PATH}")
                
def delete_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
