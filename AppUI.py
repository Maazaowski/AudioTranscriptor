import this
import tkinter as tk
import tkinter.font as tkFont
from api_communication import *
from functools import partial
from threading import *

URLLink = ""


def CreateUI(root):
    root.title("Audio Transcriber")
    width = 592
    height = 334
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    titleLabel = tk.Label(root)
    titleLabel["disabledforeground"] = "#9a1b1b"
    ft = tkFont.Font(family='Times', size=23)
    titleLabel["font"] = ft
    titleLabel["fg"] = "#333333"
    titleLabel["justify"] = "center"
    titleLabel["text"] = "Audio Transcriber"
    titleLabel["relief"] = "flat"
    titleLabel.place(x=180, y=10, width=250, height=41)

    linkLabel = tk.Label(root)
    ft = tkFont.Font(family='Times', size=13)
    linkLabel["font"] = ft
    linkLabel["fg"] = "#333333"
    linkLabel["justify"] = "center"
    linkLabel["text"] = "Enter YouTube URL"
    linkLabel.place(x=30, y=130, width=147, height=30)

    textBoxLink = tk.Entry(root)
    textBoxLink["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    textBoxLink["font"] = ft
    textBoxLink["fg"] = "#333333"
    textBoxLink["justify"] = "center"
    textBoxLink["text"] = "Entry"
    textBoxLink.place(x=200, y=130, width=357, height=30)

    statusLabel = tk.Label(root)
    ft = tkFont.Font(family='Times', size=13)
    statusLabel["font"] = ft
    statusLabel["fg"] = "#333333"
    statusLabel["justify"] = "center"
    statusLabel["text"] = ""
    statusLabel.place(x=180, y=300, width=220, height=30)

    buttonSubmit = tk.Button(root)
    buttonSubmit["bg"] = "#55a1d9"
    ft = tkFont.Font(family='Times', size=10)
    buttonSubmit["font"] = ft
    buttonSubmit["fg"] = "#000000"
    buttonSubmit["justify"] = "center"
    buttonSubmit["text"] = "Transcribe!"
    buttonSubmit.place(x=250, y=220, width=70, height=25)
    buttonSubmit["command"] = partial(buttonSubmit_command, textBoxLink, statusLabel)


def buttonSubmit_command(textBoxLink, statusLabel):
    this.URLLink = textBoxLink.get()
    t1 = Thread(target=StartProcess, args=(statusLabel,))
    t1.start()


def StartProcess(statusLabel):
    statusLabel["text"] = "Downloading file..."
    filename = downloadYouTubeAsMp3(this.URLLink)
    statusLabel["text"] = "Transcribing..."
    audio_url = upload(filename)
    statusLabel["text"] = "Saving Transcript..."
    save_transcript(audio_url, filename)
    statusLabel["text"] = "Finished!"
