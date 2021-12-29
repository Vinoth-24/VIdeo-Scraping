# from future import Tkinter
# top = Tkinter.Tk()
# # Code to add widgets will go here...
# top.mainloop()
from tkinter import *
import pandas as pd
from tkinter import filedialog
from prac_gui import main

root = Tk()
root.title("Trell's Video editor")
root.iconbitmap("Logo/red-box.ico")
root.geometry("700x500")

# Create Frame:
my_frame = Frame(root)
my_frame.pack(pady=20)


def open():
    global my_label
# Create a label
    filename = filedialog.askopenfilename(initialdir="save_path/Output", title=" Select a file", filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))

    if filename:
        try:
            my_label = Label(root, text=("File path: ", filename)).pack()
            filename = r"{}".format(filename)
            data = pd.read_excel(filename)
            my_label = Label(root, text="Editing has Begun.. Grab a coffee..!", font=("fixedsys", 16)).pack(pady=20)
            errors, total_videos = main(data)
            my_label = Label(root, text=("Total no. of errors occured: ", errors), font=("Helvetica", 18)).pack(pady=20)
            my_label = Label(root, text=("Total no. of videos processed: ", total_videos), font=("Helvetica", 18)).pack(pady=20)

        except:
            pass
        # return errors


my_button = Button(root, text="Open File", command=open).pack()
# my_button.pack(pady=20)

root.mainloop()
