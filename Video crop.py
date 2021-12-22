import moviepy.editor as mpy


vcodec = "libx264"

videoquality = "24"

# slow, ultrafast, super fast, very fast, faster, fast, medium, slow, slower, veryslow
compression = "slow"

title = "A:/Trell Scraping/SECRET vs TUNDRA"
loadtitle = title + '.mp4'
savetitle = title + 'scraped' + '.mp4'

# 0:0-0:5,21:0-21:05  # example time frame
# ------------------------------------------------------------------------------------------
# modify these start and end times for your sub clips


def time_frame(a):
    split = a.split(',')
    cuts = []

    for i, j in enumerate(split):
        # print(i,j)
        temp = tuple(j.split('-'))
        # print(temp)
        cuts.append(temp)
    return cuts


cuts = time_frame("0:0-0:5, 0:35-0:40")
# cuts = [('0:0', '0:5'), (' 0:35', '0:40'), (' 1:10', '1:13'), (' 3:23', '3:30'), (' 18:21', '18:26'), (' 21:0', '21:05')]
# -------------------------------------------------------------------------------------------------------------


def edit_video(loadtitle, savetitle, cuts):
    # load file
    video = mpy.VideoFileClip(loadtitle)

    # cut file
    clips = []
    for i, cut in enumerate(cuts):
        clip = video.subclip(cut[0], cut[1])
        clips.append(clip)

    final_clip = mpy.concatenate_videoclips(clips)


    # CROPPING A RECTANGLE OUT OF A CLIP
    final = final_clip.crop(x1=622, width=400) # Need to fix this

    # save file
    final.write_videofile(savetitle, threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf", videoquality])

    video.close()


if __name__ == '__main__':
    edit_video(loadtitle, savetitle, cuts)
