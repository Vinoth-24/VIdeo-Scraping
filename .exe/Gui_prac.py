
from tkinter import *
import pandas as pd
from tkinter import filedialog
from prac_gui import main
import time
import os
import sys


root = Tk()
root.title(" Video editor")
img = PhotoImage(file='C:\\Users\\new\\VideoScraping\\red-box.png')
root.tk.call('wm', 'iconphoto', root._w, img)
root.geometry("700x500")

# Create Frame:
my_frame = Frame(root)
my_frame.pack(pady=20)


def open():
    global my_label
# Create a label
    filename = filedialog.askopenfilename(initialdir="C:\\Users\\new\\VideoScraping\\save_path\\Output", title=" Select a file", filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))

    if filename:
        try:
            my_label = Label(root, text=("File path: ", filename)).pack()
            filename = r"{}".format(filename)
            data = pd.read_excel(filename)
            my_label = Label(root, text="Editing has Begun.. Grab a coffee..!", font=("fixedsys", 16)).pack(pady=20)
            start = time.time()
            # Logo = resource_path("C:\\Users\\new\\VideoScraping\\red-box.png")
            errors, total_videos = main(data)
            end = time.time()
            error = ("Total no. of errors occurred: ", str(errors))
            error = " ".join(error)
            my_label = Label(root, text=error, font=("Helvetica", 18)).pack(pady=20)
            total = ("Total no. of videos processed: ", str(total_videos))
            total = " ".join(total)
            my_label = Label(root, text=total, font=("Helvetica", 18)).pack(pady=20)
            time_taken = ("Runtime of the program is: ", str(end - start),"seconds")
            time_taken = " ".join(time_taken)
            my_label = Label(root, text=time_taken, font=("fixedsys", 15)).pack(pady=20)

        except:
            pass
        # return errors


my_button = Button(root, text="Open File", command=open).pack()
# my_button.pack(pady=20)

root.mainloop()
