#!/usr/bin/env python
# coding=utf-8

# PiPresenter - Turning your Raspberry Pi into a presenter!
# Copyright (C) {2017}  {Tilman Hoffbauer}
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>. 


import subprocess
import signal
import pygame
import os
import threading
import moodle
import time
import stat

USBCONNECT_EVENT = pygame.USEREVENT + 1
USBDISCONNECT_EVENT = pygame.USEREVENT + 2

usb_mount = "/media/usb"
superlevel = "Übergeordneter Ordner"
supported = ["odp", "ppt", "pptx",
             "pdf", 
             "jpg", "png", "svg", "gif", "tiff", "xpm", "bmp", "ico", "pcx", "wmf",
             "mp4", "h264"]
workdir = "work/"

proc = None
showing_video = False

def is_supporting(filename):
    return filename[filename.rfind(".") + 1:] in supported


def open_file_async(e, state, current_dir):
    if "$" in e:
        # Block these evil hackers trying to do bash injection ;)
        return
    thread = threading.Thread(target=open_file, args=(e, state, current_dir,))
    thread.start()
    return thread


def open_file(e, state, current_dir):
    global showing_video
    showing_video = False
    path = None
    if state == "usb":
        path = usb_mount + "/" + current_dir + e
    elif state == "moodle":
        path = moodle.download(e)
    directory = path[:path.rfind("/")]
    filename = path[path.rfind("/") + 1:]
    extension = path[path.rfind(".") + 1:].lower()
    if extension == "odp" or extension == "ppt" or extension == "pptx":
        startx("libreoffice --norestore --nofirststartwizard --show \"" + path + "\"")
    elif extension == "pdf":
        startx("pdfpc --switch-screens \"" + path + "\"")
    elif extension in ["jpg", "png", "svg", "gif", "tiff", "xpm", "bmp", "ico", "pcx", "wmf"]:
        f = open(workdir + "qivlist.txt", "w")
        l = None
        if state == "usb":
            l = os.listdir(directory)
        elif state == "moodle":
            l = moodle.list()
        l = [e for e in l if is_supporting(e)]
        l.sort()
        start = l.index(filename)
        for i in range(start, start + len(l)):
            e_path = None
            index = i % len(l)
            if state == "usb":
                e_path = os.path.join(directory, l[index])
            elif state == "moodle":
                e_path = moodle.download(l[index])
            f.write(e_path + "\n")
        f.close()
        startx("qiv --maxpect --scale_down --fullscreen --slide --delay 360000 --no_sort --no_statusbar --file " + workdir + "qivlist.txt")
    elif extension in ["mp4", "h264"]:
        showing_video = True
        thread = threading.Thread(target=pipe_later)
        thread.start()
        startx("omxplayer \"" + path + "\" < /tmp/keyboarder")


def pipe_later():
    time.sleep(2)
    press_key("a") # harmles key ;)


def startx(cmd):
    global proc
    write_script(cmd)
    subprocess.call(["startx", "/usr/bin/xterm", "-e", "/opt/pipresenter/work/xstart.sh"])


def write_script(cmd):
    f = open(workdir + "xstart.sh", "w")
    f.write("#!/bin/bash\n")
    f.write("unclutter -idle 1 &\n")
    if showing_video:
        f.write("mkfifo /tmp/keyboarder\n")
    else:
        f.write("/opt/pipresenter/keyboarder.sh &\n")
    f.write(cmd)
    f.write("\n")
    if showing_video:
        f.write("rm /tmp/keyboarder\n")
    f.close()
    subprocess.call(["chmod", "+x", "work/xstart.sh"])


def is_pipe(path):
    return stat.S_ISFIFO(os.stat(path).st_mode)


def on_sigusr1(signum, frame):
    pygame.event.post(pygame.event.Event(USBCONNECT_EVENT))


def on_sigusr2(signum, frame):
    pygame.event.post(pygame.event.Event(USBDISCONNECT_EVENT))


def init():
    # Register signal listeners
    signal.signal(signal.SIGUSR1, on_sigusr1)
    signal.signal(signal.SIGUSR2, on_sigusr2)
    # Save PID
    f = open(workdir + "pid", "w")
    f.write(str(os.getpid()))
    f.close()


def list(directory=""):
    entries = []
    if directory != "":
        entries.append(superlevel)
    path = os.path.join(usb_mount, directory)
    raw = os.listdir(path)
    for e in raw:
        if os.path.isfile(os.path.join(path, e)):
            if is_supporting(e):
                entries.append(e)
        else:
            entries.append(e + "/")
    
    def key(s):
        if s == superlevel:
            return ".."
        elif s[-1] == "/":
            return "." + s.lower()
        else:
            return s.lower()
    
    entries.sort(key=key)
    return entries


def press_key(key):
    pipe = open("/tmp/keyboarder", "w")
    pipe.write(key)
    if not showing_video:
        pipe.write("\n")
    pipe.close()


def shutdown():
    subprocess.call(["systemctl", "poweroff", "-i"])
