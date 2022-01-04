import sys

import pandas as pd
from pytube import YouTube
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
import os.path
import xlsxwriter

# Video qualities for our output file
vcodec = "libx264"
videoquality = "24"
# slow, ultrafast, super fast, very fast, faster, fast, medium, slow, slower, veryslow
compression = "medium"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
# ----------------------------------------------------------------------------------------------------------
# This is the main function
# First It downloads the original video from youtube
# Then it defines the Trimming time
# Then It trims the video and
# Sends that video for cropping
# Then adds Watermark to the video, then
# Final video is saved in a folder
# Then next video link is used


def video_processing(video_link, counter, error_count):
    link = video_link
    try:
        video, final_path, a_path = download_yt_video(link)  # downloading youtube video function
        print("downloaded")
    except:

        error = "Error in downloading from youtube"
        print(error)
        error_count += 1
        return error, error_count

    # Allocating paths for loading the downloaded video and saving the processed video
    loadtitle = final_path
    savetitle = a_path + '\\' + "scraped" + "\\" + "scraped_video" + str(x) + '.mp4'

    # Processing counter into required time frame
    full_clip = VideoFileClip(final_path)
    # END = full_clip.duration

    cuts = time_frame(counter)  # processing counter time to required format function

    # Trimming and Cropping Done here
    # try:
    edit_video(loadtitle, savetitle, cuts, full_clip)  # Editing function
    #except:
    #    error = "Error in Counter timings"
    #     print(error)
    #     error_count += 1
    #     return error, error_count
    return savetitle, error_count  # For remembering the saved location of video and error count


# -------------------------------------------------------------------------------------------------------
# Downloading Youtube video function

def download_yt_video(link):
    # Saving name for the video
    file_name = "video" + str(x) + ".mp4"
    a_path = "C:\\Users\\new\\VideoScraping\\save_path"
    final_path = os.path.join(a_path, file_name)
    print("Downloading file: %s" % file_name)

    youtube = YouTube(link)
    video = youtube.streams.get_highest_resolution().download(a_path)  # We can change resolution if we want
    if os.path.exists(final_path):
        os.remove(final_path)  # if video already exists, then delete the old file
    os.rename(video, final_path)

    print("%s is downloaded!\n" % file_name)
    return video, final_path, a_path


# 0:0-0:5,21:0-21:05  # example counter time frame
# ------------------------------------------------------------------------------------------
# Function to define the time frame for trimming video

def time_frame(counter):
    # If Trimming Not required(for skipping Trimming process)
    if counter == 'NIL' or counter == "NR":
        cuts = 0
        return cuts

    # Processing Timeframe for trimming
    else:
        split = counter.split(',')
        cuts = []

        for i, j in enumerate(split):
            temp = tuple(j.split('-'))
            cuts.append(temp)
        return cuts


# -------------------------------------------------------------------------------------------------------------
# Trimming, Cropping video and Saving it in destination folder is done sequentially in this Function


def edit_video(loadtitle, savetitle, cuts, full_clip):
    # load file
    video = VideoFileClip(loadtitle)

    # Trimming video
    # No trimming done for "NIL" or "NR"
    if cuts == 0:
        final_clip = full_clip

    # Creating sub clips from video and joining them
    else:
        clips = []
        for i, cut in enumerate(cuts):
            clip = video.subclip(cut[0], cut[1])
            clips.append(clip)

        final_clip = concatenate_videoclips(clips)

    # CROPPING THE TRIMMED VIDEO into a RECTANGULAR SHAPE
    final = final_clip.crop(x1=324, width=576)  # Fixed to 9:16

    Logo = resource_path("C:\\Users\\new\\VideoScraping\\red-box.png")
    # Watermarking Trell Logo
    print(Logo)
    logo = (ImageClip(Logo)
            .set_duration(final.duration)
            .resize(height=50)  # if you need to resize...
            .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            .set_pos(("right", "top")))
    result = CompositeVideoClip([final, logo])

    # Saving Video
    print("Writing edited video%d .. ..." %x)
    result.write_videofile(savetitle, threads=4, fps=24,
                           codec=vcodec, logger=None,
                           preset=compression,
                           ffmpeg_params=["-crf", videoquality])

    video.close()
    print("Editing done on video%d." %x)
    print('─' * 15)
# -------------------------------------------------------------------------------------------------------------------
# For .exe file (Adding Logo to video)
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)


# -------------------------------------------------------------------------------------------------------------------

# Program Starts here

def main(data):

    global x
    # data = pd.read_excel("C:\\Users\\new\\VideoScraping\\save_path\\Output\\Master_ PUGC Supply Generation Pipeline - November - Tamil-Demand.xlsx", sheet_name="Master_ PUGC Supply Generation ")
    input_data = data[['Sourced Ref Video Link', 'Counter']]
    final_data = data[['Sourced Ref Video Link', 'Counter']]
    final_data['Final Saved File Link'] = ''

    x = 1  # For naming file
    error_count = 0
    # iterating over rows using iterrows() function
    for i, j in input_data.iterrows():

        counter = j[1]
        video_link = j[0]
        #try:
        savetitle, error_count = video_processing(video_link, counter, error_count)
        # except Exception:
        #     error_count += 1
        #     error = "Some error has been occurred"
        #     print(error)
        #     savetitle = error
        x = x + 1

        final_data['Final Saved File Link'][i] = savetitle  # New column with processed video location
    print("All videos processed!")
    print(final_data)
    total_revised_videos = x-1

    # Saving the final_data dataframe into an Excel File - Scraped_Sheet.xlsx
    writer = pd.ExcelWriter('C:\\Users\\new\\VideoScraping\\save_path\\Output\\Scraped_Sheet.xlsx', engine='xlsxwriter')
    final_data.to_excel(writer, sheet_name='Scraping output', index=False)
    writer.save()
    return error_count, total_revised_videos
