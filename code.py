import moviepy.editor as mpy
import pandas as pd
from pytube import YouTube
from moviepy.editor import VideoFileClip, CompositeVideoClip
import os.path

# Video qualities for our output file
vcodec = "libx264"
videoquality = "24"
# slow, ultrafast, super fast, very fast, faster, fast, medium, slow, slower, veryslow
compression = "medium"

# ----------------------------------------------------------------------------------------------------------
# This is the main function
# First It downloads the original video from youtube
# Then it defines the Trimming time
# Then It trims the video and
# Sends that video for cropping
# Then adds Watermark to the video, then
# Final video is saved in a folder
# Then next video link is used


def video_processing(video_link, counter):
    link = video_link

    # Saving name for the video
    file_name = "video" + str(x) + ".mp4"
    a_path = "C:\\Users\\new\\VideoScraping\\save_path"
    final_path = os.path.join(a_path, file_name)
    print("Downloading file: %s" % file_name)

    youtube = YouTube(link)
    video = youtube.streams.get_highest_resolution().download(a_path)  # We can change resolution if we want
    if os.path.exists(final_path):
        os.remove(final_path)      # if video already exists, then delete the old file
    os.rename(video, final_path)

    print("%s is downloaded!\n" % file_name)

    # Allocating paths for loading the downloaded video and saving the processed video
    loadtitle = final_path
    savetitle = a_path + '\\' + "scraped" + "\\" + "scraped_video" + str(x) + '.mp4'

    # Processing counter into required time frame
    full_clip = VideoFileClip(final_path)
    # END = full_clip.duration
    # START = 0.0

    cuts = time_frame(counter)

    # Trimming and Cropping Done
    edit_video(loadtitle, savetitle, cuts, full_clip)

    return savetitle  # For remembering the saved location of video


# 0:0-0:5,21:0-21:05  # example time frame
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
            # print(i,j)
            temp = tuple(j.split('-'))
            # print(temp)
            cuts.append(temp)
            # print(cuts)
        return cuts

# -------------------------------------------------------------------------------------------------------------
# Trimming, Cropping video and Saving it in destination folder is done sequentially in this Function


def edit_video(loadtitle, savetitle, cuts, full_clip):
    ## print(cuts)
    # load file
    video = mpy.VideoFileClip(loadtitle)

    # Trimming video
    # No trimming done for "NIL" or "NR"
    if cuts == 0:
        final_clip = full_clip

    # Creating sub clips from video and joining them
    else:
        clips = []
        for i, cut in enumerate(cuts):
            # print(cut[0],cut[1])
            clip = video.subclip(cut[0], cut[1])
            clips.append(clip)

        final_clip = mpy.concatenate_videoclips(clips)


    # CROPPING THE TRIMMED VIDEO into a RECTANGULAR SHAPE
    final = final_clip.crop(x1=324, width=576)  # Fixed to 9:16

    # Watermarking Trell Logo
    logo = (mpy.ImageClip("C:\\Users\\new\\VideoScraping\\Logo\\red-box.png")
          .set_duration(final.duration)
          .resize(height=50) # if you need to resize...
          .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
          .set_pos(("right","top")))
    result = CompositeVideoClip([final, logo])


    # Saving Video
    result.write_videofile(savetitle, threads=4, fps=24,
                          codec=vcodec,
                          preset=compression,
                          ffmpeg_params=["-crf", videoquality])

    video.close()


# Program Starts here

if __name__ == '__main__':
    data = pd.read_csv("Master_ PUGC Supply Generation Pipeline - November - Tamil-Demand.csv")
    input_data = data[['Sourced Ref Video Link', 'Counter']]
    final_data = data[['Sourced Ref Video Link', 'Counter']]
    final_data['Final Saved File Link'] = ''

    x = 1  # For naming file
    error_count = 0
    # iterating over rows using iterrows() function
    for i, j in input_data.iterrows():

        counter = j[1]
        video_link = j[0]

        # Calling the main func with try except blocks
        try:
            savetitle = video_processing(video_link, counter)

        except:
            error_count += 1
            savetitle = "Error while processing video"
            print(savetitle, x)
        x = x+1

        final_data['Final Saved File Link'][i] = savetitle  # New column with processed video location
    print("All videos processed!")
    print(final_data)
    print("Total errors occured = ", error_count)
