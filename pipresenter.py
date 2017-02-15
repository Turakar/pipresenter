#! /usr/bin/env python
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



import pygame
import os
import hardware
from virtualKeyboard import VirtualKeyboard
import moodle

# Config
width = 480
height = 320
imgsdir = "imgs/"

# Setup touchscreen
os.environ['SDL_FBDEV'] = '/dev/fb1'
os.environ['FRAMEBUFFER'] = '/dev/fb1'
os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
os.environ['SDL_MOUSEDRV'] = 'TSLIB'

# Init
pygame.init()
hardware.init()
screen = pygame.display.set_mode((width, height))
pygame.mouse.set_visible(False)

# Design
default_entries = ["Bitte USB-Stick einstecken"]

primary_color = (59, 78, 223)
background_color = (247, 251, 254)
seperator_color = (230, 233, 255)
#button_color = (235, 243, 255)
button_color = background_color
button_border_color = (59, 78, 223)
text_color = (60, 60, 60)
title_color = seperator_color

font_big = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

margin_top = 5
banner_height = margin_top + 40
list_margin_top = banner_height + 10
button_margin_top = banner_height + 20
margin = 20
entry_size = 30
entry_margin = 3
scroll_button_width = 30
control_button_size = 140
button_margin = 10
home_button_size = 37
error_text_margin = 50

list_left = margin
list_top = list_margin_top
list_width = width - 2 * margin - scroll_button_width
list_height = height - margin - list_margin_top
list_height -= list_height % entry_size
list_items = int(list_height / entry_size)
list_entry_max_width = list_width - entry_margin * 2

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(background_color)

banner_rect = pygame.Rect(0, 0, width, banner_height)

# General
home_button_rect = pygame.Rect(width - home_button_size, 0, home_button_size, home_button_size)
img_home = pygame.image.load(imgsdir + 'home.png')
img_home_pos = img_home.get_rect()
img_home_pos.centerx = home_button_rect.centerx
img_home_pos.centery = home_button_rect.centery


# Welcome Screen
text_welcome = font_big.render('PiPresenter (T. Hoffbauer)', 1, title_color)
text_welcome_pos = text_welcome.get_rect()
text_welcome_pos.x = margin
text_welcome_pos.y = margin_top

usb_button_rect = pygame.Rect(margin, button_margin_top, control_button_size, control_button_size)
img_usb = pygame.image.load(imgsdir + 'usb.png')
img_usb_pos = img_usb.get_rect()
img_usb_pos.centerx = usb_button_rect.centerx
img_usb_pos.centery = usb_button_rect.centery

moodle_button_rect = pygame.Rect(margin + control_button_size + button_margin, button_margin_top, control_button_size, control_button_size)
img_moodle = pygame.image.load(imgsdir + 'moodle.png')
img_moodle_pos = img_moodle.get_rect()
img_moodle_pos.centerx = moodle_button_rect.centerx
img_moodle_pos.centery = moodle_button_rect.centery

shutdown_button_rect = pygame.Rect(margin + control_button_size * 2 + button_margin * 2, 
                                 button_margin_top, control_button_size, control_button_size)
img_shutdown = pygame.image.load(imgsdir + 'shutdown.png')
img_shutdown_pos = img_shutdown.get_rect()
img_shutdown_pos.centerx = shutdown_button_rect.centerx
img_shutdown_pos.centery = shutdown_button_rect.centery

# Moodle login
text_moodle_login = font_big.render('Moodle Login', 1, title_color)
text_moodle_login_pos = text_moodle_login.get_rect()
text_moodle_login_pos.x = margin
text_moodle_login_pos.y = margin_top

username_button_rect = pygame.Rect(margin, button_margin_top, control_button_size, control_button_size)
text_username = font_small.render('Name', 1, text_color)
text_username_pos = text_username.get_rect()
text_username_pos.centerx = username_button_rect.centerx
text_username_pos.centery = username_button_rect.centery

password_button_rect = pygame.Rect(margin + control_button_size + button_margin, button_margin_top, control_button_size, control_button_size)
text_password = font_small.render('Passwort', 1, text_color)
text_password_pos = text_password.get_rect()
text_password_pos.centerx = password_button_rect.centerx
text_password_pos.centery = password_button_rect.centery

login_button_rect = pygame.Rect(margin + control_button_size * 2 + button_margin * 2, 
                                 button_margin_top, control_button_size, control_button_size)
text_login = font_small.render('Login', 1, text_color)
text_login_pos = text_login.get_rect()
text_login_pos.centerx = login_button_rect.centerx
text_login_pos.centery = login_button_rect.centery

text_error = font_small.render('Fehler!', 1, text_color)
text_error_pos = text_error.get_rect()
text_error_pos.centerx = password_button_rect.centerx
text_error_pos.y = password_button_rect.y + password_button_rect.height + error_text_margin


# List View
text_plsselect = font_big.render('Wählen Sie ihre Datei aus:', 1, title_color)
text_plsselect_pos = text_plsselect.get_rect()
text_plsselect_pos.x = margin
text_plsselect_pos.y = margin_top

img_arrow_up = pygame.image.load(imgsdir + 'arrowup.png')
img_arrow_up_pos = img_arrow_up.get_rect()
img_arrow_up_pos.centery = list_top + list_height / 4
img_arrow_up_pos.centerx = list_left + list_width + scroll_button_width / 2
img_arrow_down = pygame.image.load(imgsdir + 'arrowdown.png')
img_arrow_down_pos = img_arrow_down.get_rect()
img_arrow_down_pos.centery = list_top + list_height / 4 + list_height / 2
img_arrow_down_pos.centerx = list_left + list_width + scroll_button_width / 2

top_button_rect = pygame.Rect(list_left + list_width, list_top,
                              scroll_button_width, list_height / 2)
bottom_button_rect = pygame.Rect(list_left + list_width, list_top + list_height / 2,
                                 scroll_button_width, list_height / 2)

# Presentation Overlay
text_presentation = font_big.render('Präsentationsmodus', 1, title_color)
text_presentation_pos = text_presentation.get_rect()
text_presentation_pos.x = margin
text_presentation_pos.y = margin_top

left_button_rect = pygame.Rect(margin, button_margin_top, control_button_size, control_button_size)
img_arrow_left = pygame.image.load(imgsdir + 'arrowleft.png')
img_arrow_left_pos = img_arrow_left.get_rect()
img_arrow_left_pos.centerx = left_button_rect.centerx
img_arrow_left_pos.centery = left_button_rect.centery

right_button_rect = pygame.Rect(margin + control_button_size + button_margin, button_margin_top, control_button_size, control_button_size)
img_arrow_right = pygame.image.load(imgsdir + 'arrowright.png')
img_arrow_right_pos = img_arrow_right.get_rect()
img_arrow_right_pos.centerx = right_button_rect.centerx
img_arrow_right_pos.centery = right_button_rect.centery

escape_button_rect = pygame.Rect(margin + control_button_size * 2 + button_margin * 2, 
                                 button_margin_top, control_button_size, control_button_size)
img_escape = pygame.image.load(imgsdir + 'escape.png')
img_escape_pos = img_escape.get_rect()
img_escape_pos.centerx = escape_button_rect.centerx
img_escape_pos.centery = escape_button_rect.centery


# Runtime variables
state = None
prior_state = None
scroll = 0
current_dir = ""
presentation_thread = None
moodle_username = None
moodle_password = None
login_error = False


def change_state(new_state, *args):
    global state, prior_state, entries, moodle_username, moodle_password, login_error, entries, presentation_thread, scroll, current_dir
    if new_state == "usb":
        scroll = 0
        current_dir = ""
        entries = hardware.list()
        if len(entries) == 0:
            entries = default_entries
    elif new_state == "moodlelogin":
        moodle_username = None
        moodle_password = None
        login_error = False
    elif new_state == "moodle":
        entries = [e for e in moodle.list() if hardware.is_supporting(e)]
    elif new_state == "presentation":
        presentation_thread = hardware.open_file_async(args[0], state, args[1])
    
    prior_state = state
    state = new_state


def draw():
    # Draw Background
    background.fill(background_color)
    
    if state == "welcome":
        draw_welcome()
    elif state == "moodlelogin":
        draw_moodle_login()
    elif state == "usb" or state == "moodle":
        draw_list()
    elif state == "presentation":
        draw_presentation()
    
    # Draw to Display
    screen.blit(background, (0, 0))
    pygame.display.flip()


def draw_button(rect):
    pygame.draw.rect(background, button_color, rect)
    pygame.draw.rect(background, button_border_color, rect, 3)


def draw_button_content(rect, content, content_pos):
    draw_button(rect)
    background.blit(content, content_pos)


def draw_home_button():
    background.blit(img_home, img_home_pos)


def draw_welcome():
    # Title
    pygame.draw.rect(background, primary_color, banner_rect)
    background.blit(text_welcome, text_welcome_pos)
    
    # Buttons
    draw_button_content(usb_button_rect, img_usb, img_usb_pos)
    draw_button_content(moodle_button_rect, img_moodle, img_moodle_pos)
    draw_button_content(shutdown_button_rect, img_shutdown, img_shutdown_pos)


def draw_moodle_login():
    # Title
    pygame.draw.rect(background, primary_color, banner_rect)
    background.blit(text_moodle_login, text_moodle_login_pos)
    
    # Buttons
    draw_button_content(username_button_rect, text_username, text_username_pos)
    draw_button_content(password_button_rect, text_password, text_password_pos)
    draw_button_content(login_button_rect, text_login, text_login_pos)
    
    # Error
    if login_error:
        background.blit(text_error, text_error_pos)
    
    # Home button
    draw_home_button()


def draw_list():
    
    # Title
    pygame.draw.rect(background, primary_color, banner_rect)
    background.blit(text_plsselect, text_plsselect_pos)

    # List
    for i, entry in enumerate(entries):
        if i < scroll:
            continue

        offset = i - scroll

        if font_small.size(entry)[0] > list_entry_max_width:
            suffix = "..."
            if entry[-1] == "/":
                entry = entry[:-1]
                suffix += "/"
            while font_small.size(entry + suffix)[0] > list_entry_max_width:
                entry = entry[:-1]
            entry += suffix
        text_entry = font_small.render(entry, 1, text_color)
        text_entry_pos = text_entry.get_rect()
        text_entry_pos.x = list_left + entry_margin
        text_entry_pos.y = list_top + offset * entry_size + entry_margin
        background.blit(text_entry, text_entry_pos)

        if i - scroll + 1 == list_items:
            break

        pygame.draw.line(background, seperator_color,
                         (list_left, list_top + (offset + 1) * entry_size),
                         (list_left + list_width, list_top + (offset + 1) * entry_size))

    pygame.draw.rect(background, primary_color,
                     pygame.Rect(list_left, list_top, list_width, list_height),
                     3)
    
    # Scroll Buttons
    draw_button_content(top_button_rect, img_arrow_up, img_arrow_up_pos)
    draw_button_content(bottom_button_rect, img_arrow_down, img_arrow_down_pos)
    
    # Home button
    draw_home_button()


def draw_presentation():
    # Title
    pygame.draw.rect(background, primary_color, banner_rect)
    background.blit(text_presentation, text_presentation_pos)
    
    # Buttons
    draw_button_content(left_button_rect, img_arrow_left, img_arrow_left_pos)
    draw_button_content(right_button_rect, img_arrow_right, img_arrow_right_pos)
    draw_button_content(escape_button_rect, img_escape, img_escape_pos)


def on_touch(x, y):
    if state == "welcome":
        on_touch_welcome(x, y)
    elif state == "moodlelogin":
        on_touch_moodle_login(x, y)
    elif state == "usb" or state == "moodle":
        on_touch_list(x, y)
    elif state == "presentation":
        on_touch_presentation(x, y)


def on_touch_welcome(x, y):
    global state
    if usb_button_rect.collidepoint(x, y):
        change_state("usb")
    elif moodle_button_rect.collidepoint(x, y):
        change_state("moodlelogin")
        moodle_username = None
        moodle_password = None
    elif shutdown_button_rect.collidepoint(x, y):
        hardware.shutdown()


def on_touch_moodle_login(x, y):
    global state, moodle_username, moodle_password, login_error, entries
    if username_button_rect.collidepoint(x, y):
        keyboard = VirtualKeyboard(screen)
        userinput = keyboard.run(text=moodle_username if moodle_username != None else "")
        moodle_username = userinput
    elif password_button_rect.collidepoint(x, y):
        keyboard = VirtualKeyboard(screen)
        moodle_password = keyboard.run(password=True)
    elif login_button_rect.collidepoint(x, y):
        if moodle_username == None or moodle_password == None:
            login_error = True
            return
        try:
            moodle.connect(moodle_username, moodle_password)
        except Exception as exc:
            if len(exc.args) == 1 and exc.args[0] == "invalidlogin":
                login_error = True
            else:
                raise
        else:
            change_state("moodle")
    elif home_button_rect.collidepoint(x, y):
        change_state("welcome")


def on_touch_list(x, y):
    global scroll, entries, current_dir, presentation_thread, state, prior_state
    if top_button_rect.collidepoint(x, y):
        if scroll > 0:
            scroll -= 1
    elif bottom_button_rect.collidepoint(x, y):
        if scroll < len(entries) - list_items:
            scroll += 1
    elif list_left <= x < list_left + list_width and list_top <= y < list_top + list_height:
        # Inside the List
        i = int((y - list_top) / entry_size) + scroll
        if i >= len(entries):
            return
        e = entries[i]
        if e == default_entries[0]:
            return
        elif i == 0 and current_dir != "":
            last_index = current_dir[0:-1].rfind('/')
            if last_index == -1:
                current_dir = ""
            else:
                current_dir = current_dir[0:last_index + 1]
            entries = hardware.list(current_dir)
            scroll = 0
        elif e[-1] == "/":
            current_dir += e
            entries = hardware.list(current_dir)
            scroll = 0
        else:
            # A file
            change_state("presentation", e, current_dir)
    elif home_button_rect.collidepoint(x, y):
        change_state("welcome")


def on_touch_presentation(x, y):
    if left_button_rect.collidepoint(x, y):
        hardware.press_key("Page_Up")
    elif right_button_rect.collidepoint(x, y):
            hardware.press_key("Page_Down")
    elif escape_button_rect.collidepoint(x, y):
        if hardware.showing_video:
            hardware.press_key("q")
        else:
            hardware.press_key("Escape")
    

def on_stick_connect():
    change_state("usb")


def on_stick_disconnect():
   if state == "usb":
       change_state("welcome")


# Main Loop
if len(hardware.list()) > 0:
    change_state("usb")
else:
    change_state("welcome")

running = True
draw()
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONUP:
        x, y = event.pos
        on_touch(x, y)
    elif event.type == hardware.USBCONNECT_EVENT:
        on_stick_connect()
    elif event.type == hardware.USBDISCONNECT_EVENT:
        on_stick_disconnect()
    
    if presentation_thread != None and not presentation_thread.is_alive():
        presentation_thread = None
        state = prior_state
    
    draw()

