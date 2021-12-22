from pytube import YouTube
import os


def download_video_series(video_links):
    x = 1
    for link in video_links:

        file_name = "video" + str(x) + ".mp4"
        a_path = "C:\\Users\\new\\VideoScraping\\save_path"
        final_path = os.path.join(a_path, file_name)
        print("Downloading file:%s" % file_name)

        youtube = YouTube(link)
        video = youtube.streams.get_highest_resolution().download('C:\\Users\\new\\VideoScraping\\save_path')
        os.rename(video, final_path)

        print("%s downloaded!\n" % file_name)
        x = x+1
    print("All videos downloaded!")
    return


video_links = ["https://www.youtube.com/watch?v=d95PPykB2vE", "https://www.youtube.com/watch?v=kLGaoYbR7LA"]
download_video_series(video_links)
