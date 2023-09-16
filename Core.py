"""
$ Developed by Shiven_Saini. 
Python libraries used  => 'Pytube', 'tkinter', 'tkinter.ttk', 'time', 'PIL'
Features of This Program :=>
1. Download youtube videos.
2. Download songs from YouTube
3. Download subtitles for youtube videos.
4. Download YouTube videos literally in every available Quality.
5. Show Details of YouTube videos.
6. Completely developed by Shiven Saini.
"""

# importing required modules.
import pyperclip
import requests
import shutil
import time
import ffmpeg
import os
import threading
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from PIL import ImageTk, Image

core_object = ''
pic_processed = ''
database_itags_mp4 = ['160', '133', '134', '135', '136', '137', '138', '264', '266']
video_title = ''
file_to_save = ''
mp3_savelocation = ''
format_id = ''
get_quality = ''
user_choice_audio = ''
thread_1 = ''
thread_2 = ''
thread_3 = ''

# Initializing booleans for correlations of functions.\
run_indeterminate = False


# Defining prerequisite Functions.
def thread_checker():
    thread_indeterminate = threading.Thread(target=indeterminate)
    thread_indeterminate.start()


# defining function to run progressbar in indeterminate mode.
def indeterminate():
    tasks_section_clr.pgbar.destroy()
    pgbar2 = ttk.Progressbar(root, mode='indeterminate', orient=HORIZONTAL, length=100)
    pgbar2.place(x=408, y=545)
    root.update_idletasks()
    while run_indeterminate:
        pgbar2['value'] = 0
        time.sleep(0.2)

        pgbar2['value'] = 20
        time.sleep(0.2)

        pgbar2['value'] = 40
        time.sleep(0.2)

        pgbar2['value'] = 60
        time.sleep(0.2)

        pgbar2['value'] = 80
        time.sleep(0.2)

        pgbar2['value'] = 100
        time.sleep(0.2)

        pgbar2['value'] = 80
        time.sleep(0.2)

        pgbar2['value'] = 60
        time.sleep(0.2)

        pgbar2['value'] = 40
        time.sleep(0.2)

        pgbar2['value'] = 20
        time.sleep(0.2)


    pgbar2.destroy()
    pgbar1 = ttk.Progressbar(root, length=200, mode='determinate', orient=HORIZONTAL)
    pgbar1.place(x=408, y=545)
    pgbar1['value'] = 100

    tasks_section_clr.lbl_statusshow.config(text='Current status :- Task completed.')
    tasks_section_clr.progress_percentage.config(text='Done!!!')


# defining function for showing progress bar.

def progress_status(stream, chunk, file_handle, remaining=None):
    file_size_bytes = stream.filesize
    file_size_mb = file_size_bytes / 1000000
    file_downloaded = (file_size_bytes - file_handle)
    per = (file_downloaded / file_size_bytes) * 100
    per_print = ("{:00.1f}".format(per))
    text_size = "File size :- {:00.2f} mb.".format(file_size_mb)
    lbl_strmsize = Label(root, text=text_size, font=('Segoe UI', 12))
    lbl_strmsize.place(x=290, y=440)
    tasks_section_clr.pgbar['value'] = per_print
    text_show = ('{} %'.format(per_print))
    tasks_section_clr.progress_percentage.config(text=text_show)


# Creating handler thread 1.
def thread_fetch():
    global thread_1
    thread_1 = threading.Thread(target=Core_engine, daemon=True)
    thread_1.start()


# Creating handler thread 2. downloading video files.
def thread_video_down():
    global thread_2
    thread_video_down.thread_2 = threading.Thread(target=down_vid, daemon=True)
    thread_video_down.thread_2.start()


# Creating handler thread 3. downloading audio files.
def thread_audio_down():
    global thread_3
    thread_audio_down.thread_3 = threading.Thread(target=down_audio, daemon=True)
    thread_audio_down.thread_3.start()


def popup_creator():
    messagebox.showinfo("About Developer", "Developed & maintained by Shiven Saini.")

def tasks_section_clr(location):
    tasks_section.lbl_response.config(text='Task - Section')
    tasks_section.lbl_response.place(x=460, y=300)

    # Removing all unwanted labels.
    tasks_section.lbl_tip1.config(text='')
    tasks_section.lbl_tip2.config(text='')
    tasks_section.lbl_tip3.config(text='')
    tasks_section.lbl_tip4.config(text='')
    tasks_section.lbl_tip5.config(text='')
    tasks_section.lbl_divider_tasks.config(text='')
    tasks_section.lbl_attention1.config(text='')
    tasks_section.lbl_attention2.config(text='')
    tasks_section.lbl_attention3.config(text='')

    # Applying status bar.
    lbl_status = Label(root, text='Download location :', font=('Segoe UI', 12))
    lbl_status.place(x=290, y=340)

    # applying download location.
    length_file_to_save = len(location)
    for i in range(0, length_file_to_save):
        if location[i] == '/':
            num_max = i
        else:
            pass

    show_location = location[:num_max]
    lbl_location = Label(root, text=show_location, font=('arial', 8), fg='white', bg='black')
    lbl_location.place(x=435, y=345)

    # applying file type.
    file_type = str("File type :- %s" % (format_id))
    lbl_filetype = Label(root, text=file_type, font=('Segoe UI', 12))
    lbl_filetype.place(x=290, y=390)
    if format_id == 'Audio only (mp3)':
        file_quality = str("| Quality :- %s" % (user_choice_audio))
    else:
        file_quality = str("| Resolution :- %s" % (get_quality))
    lbl_qualitytasks = Label(root, text=file_quality, font=('Segoe UI', 12))
    lbl_qualitytasks.place(x=510, y=390)

    # Applying progress bar in tkinter progress menu.

    tasks_section_clr.lbl_statusshow = Label(root, text='Current status :- Downloading', font=('Segoe UI', 12))
    tasks_section_clr.lbl_statusshow.place(x=290, y=490)
    lbl_progressbardenoter = Label(root, text='Task Progress : ', font=('Segoe UI', 12))
    lbl_progressbardenoter.place(x=290, y=540)

    tasks_section_clr.pgbar = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
    tasks_section_clr.pgbar.place(x=408, y=545)

    tasks_section_clr.progress_percentage = Label(root, text='', font=('Segoe UI', 12))
    tasks_section_clr.progress_percentage.place(x=620, y=542)


def tasks_section():
    # creating separate frame for tasks view section.
    tasks_section.lbl_tasks_bg = Label(root, image=background_png)
    tasks_section.lbl_tasks_bg.place(x=273, y=285)
    text_response = "Waiting for User's Response"
    tasks_section.lbl_response = Label(root, text=text_response, font=('Arial Rounded MT Bold', 14, 'underline'))
    tasks_section.lbl_response.place(x=405, y=300)

    tip1 = "1. Decide Format (Video/Audio) in which you want to download."
    tasks_section.lbl_tip1 = Label(root, text=tip1, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_tip1.place(x=310, y=340)

    tip2 = "2. Select available Resolution/Bitrate from dropdown menus."
    tasks_section.lbl_tip2 = Label(root, text=tip2, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_tip2.place(x=310, y=370)

    tip3 = "3. Start downloading by pressing download button."
    tasks_section.lbl_tip3 = Label(root, text=tip3, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_tip3.place(x=310, y=400)

    tip4 = "4. After that you will be directed to Choose your download location."
    tasks_section.lbl_tip4 = Label(root, text=tip4, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_tip4.place(x=310, y=430)

    tip5 = "5. If available, download subtitles by pressing 'Download-subtitle' Button."
    tasks_section.lbl_tip5 = Label(root, text=tip5, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_tip5.place(x=310, y=460)

    divider_tasks_text = "------------------------------------------------------ Attention ------------------------------------------------------"
    tasks_section.lbl_divider_tasks = Label(root, text=divider_tasks_text, font=('Arial Rounded MT Bold', 10), fg='Red')
    tasks_section.lbl_divider_tasks.place(x=280, y=485)

    attention_text = "Please Note that that this Software uses your System Resources for"
    attention_text2 = "transcoding of different formats so transcoding can take a bit of"
    attention_text3 = "time depending on your CPU Speed."

    tasks_section.lbl_attention1 = Label(root, text=attention_text, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_attention1.place(x=310, y=510)

    tasks_section.lbl_attention2 = Label(root, text=attention_text2, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_attention2.place(x=310, y=535)

    tasks_section.lbl_attention3 = Label(root, text=attention_text3, font=('Arial Rounded MT Bold', 10))
    tasks_section.lbl_attention3.place(x=310, y=560)

# defining function to download English subtitles.
def down_sub():
    save_location = filedialog.askdirectory(initialdir='/Downloads/', title='Choose your save location.')
    save_location = str(save_location + '/')
    sub_title = video_title + '.srt'
    fetch_sub.subtitles_unprocessed.download(output_path=save_location, title=sub_title)
    messagebox.showinfo("Task completed", "Subtitle file downloaded successfully.")

# Defining function to download Video file.
def down_vid():
    global file_to_save, format_id, get_quality, run_indeterminate

    get_quality = search_mp4.dropdown_quality.get()
    if get_quality == '144p':
        itag_value = '160'
    elif get_quality == '240p':
        itag_value = '133'
    elif get_quality == '360p':
        itag_value = '134'
    elif get_quality == '480p':
        itag_value = '135'
    elif get_quality == '720p':
        itag_value = '136'
    elif get_quality == '1080p60':
        itag_value = '137'
    elif get_quality == '4k':
        itag_value = '138'
    elif get_quality == '1440p60':
        itag_value = '264'
    elif get_quality == '2k':
        itag_value = '266'
    else:
        messagebox.showwarning("Parameters not specified",
                               "Kindly select a valid quality from dropdown box.\n(Under video section).")

    strm_download = core_object.streams.get_by_itag(itag_value)
    initial_savename = str('%s.mp4' % (video_title))
    file_to_save = filedialog.asksaveasfilename(title='Save your video', initialdir='/Downloads/',
                                                initialfile=initial_savename, filetypes=[('mp4 files', '*.mp4')])
    format_id = 'Video (mp4)'
    tasks_section_clr(file_to_save)

    tasks_section_clr.lbl_statusshow.config(text='Current status :- Downloading Video data', font=('Segoe UI', 12))
    strm_download.download(filename='raw_video.mp4', skip_existing=False)
    tasks_section_clr.lbl_statusshow.config(text='Current status :- Downloading Audio data', font=('Segoe UI', 12))

    strm_download = core_object.streams.get_by_itag('140')
    strm_download.download(filename='raw_audio.mp4', skip_existing=False)
    tasks_section_clr.lbl_statusshow.config(text='Current status :- Transcoding (Times depend on CPU power)', font=('Segoe UI', 12))
    tasks_section_clr.progress_percentage.config(text='')

    run_indeterminate = True
    thread_checker()

    # Applying transcoder 'muxing' to join video file and audio file.

    video_input = ffmpeg.input('raw_video.mp4')
    audio_input = ffmpeg.input('raw_audio.mp4')
    ffmpeg.concat(video_input, audio_input, v=1, a=1).output(file_to_save).run()
    os.remove('raw_audio.mp4')
    os.remove('raw_video.mp4')
    run_indeterminate = False
    messagebox.showinfo('Congratulations', 'Your video Downloaded successfully.')

# defining function to download available mp4 audio files.
def down_audio():
    global file_to_save, mp3_savelocation, format_id, user_choice_audio, run_indeterminate 

    user_choice_audio = str(check_audio.dropdown_audio.get())
    if user_choice_audio == '64 kbps (AAC)':
        itag_audio = '139'
    elif user_choice_audio == '128 kbps (AAC)':
        itag_audio = '140'
    elif user_choice_audio == '256 kbps (AAC)':
        itag_audio = '141'
    else:
        messagebox.showwarning("Parameters not specified",
                               "Kindly choose a valid option from the Dropdown menu\n(In Audio section).")

    audio_strm_download = core_object.streams.get_by_itag(itag_audio)
    mp3save_name = str('%s.mp3' % (video_title))
    mp3_savelocation = filedialog.asksaveasfilename(title='Choose your save location.', initialdir='/Downloads/',
                                                    initialfile=mp3save_name, filetypes=[('mp3 file', '*.mp3')])
    print(mp3_savelocation)
    format_id = 'Audio only (mp3)'
    tasks_section_clr(mp3_savelocation)
    audio_strm_download.download(filename='raw_audio.mp4', skip_existing=False)

    tasks_section_clr.lbl_statusshow.config(text='Current status :- Encoding', font=('Segoe UI', 12))
    tasks_section_clr.progress_percentage.config(text='')

    run_indeterminate = True
    thread_checker()

    # applying transcoder to encode mp4 file to mp3.
    # Will use ffmpeg open-source license project to decode.
    raw_audio_input = ffmpeg.input('raw_audio.mp4')
    processed_audio_output = ffmpeg.output(raw_audio_input, mp3_savelocation)
    ffmpeg.run(processed_audio_output)
    run_indeterminate = False
    os.remove('raw_audio.mp4')
    messagebox.showinfo('Congratulations', 'Your mp3 audio file downloaded successfully.')
    print(threading.activeCount(),"is running currently.(in download audio).")

# creating function to check existence of available mp4 video files.
def search_mp4():
    available_itags = []
    available_Qualities = []
    for i in database_itags_mp4:
        itag_testing = core_object.streams.get_by_itag(i)
        if itag_testing != None:
            available_itags.append(i)
        else:
            pass
    for j in available_itags:
        if j == '160':
            Resolution = '144p'
            available_Qualities.append(Resolution)
        elif j == '133':
            Resolution = '240p'
            available_Qualities.append(Resolution)
        elif j == '134':
            Resolution = '360p'
            available_Qualities.append(Resolution)
        elif j == '135':
            Resolution = '480p'
            available_Qualities.append(Resolution)
        elif j == '136':
            Resolution = '720p'
            available_Qualities.append(Resolution)
        elif j == '137':
            Resolution = '1080p60'
            available_Qualities.append(Resolution)
        elif j == '138':
            Resolution = '4k'
            available_Qualities.append(Resolution)
        elif j == '264':
            Resolution = '1440p60'
            available_Qualities.append(Resolution)
        elif j == '266':
            Resolution = '2k'
            available_Qualities.append(Resolution)
        else:
            pass
    download_btn_video = ttk.Button(root, image=download_png, command=thread_video_down)
    download_btn_video.place(x=7, y=370)
    if len(available_Qualities) > 0:
        search_mp4.dropdown_quality = ttk.Combobox(root, values=available_Qualities, width=15, state='readonly')
        search_mp4.dropdown_quality.current(0)
        search_mp4.dropdown_quality.bind("<<ComboboxSelected>>")
        search_mp4.dropdown_quality.place(x=88, y=335)
    else:
        lbl_null = Label(root, text=':( No supported mp4 file found for this video.', font=('Arial Rounded MT Bold', 8))
        lbl_null.place(x=80, y=335)
        download_btn_video['state'] = 'disabled'

# Defining function to check for available mpeg-4 audio files.
def check_audio():
    list_audioitags = ['139', '140', '141']
    available_bitrates = []
    values_drop = []
    for i in list_audioitags:
        if core_object.streams.get_by_itag(i) != None:
            available_bitrates.append(i)
        else:
            pass
    for j in available_bitrates:
        if j == '139':
            bitrate = '64 kbps (AAC)'
            values_drop.append(bitrate)
        elif j == '140':
            bitrate = '128 kbps (AAC)'
            values_drop.append(bitrate)
        elif j == '141':
            bitrate = '256 kbps (AAC)'
            values_drop.append(bitrate)
        else:
            pass

    # Creating divider for our audio section.
    lbl_divider_aud = Label(root, text='-------------------- Audio Section -------------------',
                            font=('Arial Rounded MT bold', 10)).place(x=15, y=460)
    lbl_quality = Label(root, text='Choose Quality', font=('Arial Rounded MT Bold', 10)).place(x=94, y=485)

    # applying audio pic for better UI
    pic_audio = Label(root, image=audio_png).place(x=5, y=480)
    # Creating download button for audio section.
    btn_mp3 = ttk.Button(root, image=download_png, command=thread_audio_down)
    btn_mp3.place(x=8, y=550)
    if len(available_bitrates) > 0:
        check_audio.dropdown_audio = ttk.Combobox(root, values=values_drop, width=15, state='readonly')
        check_audio.dropdown_audio.current(0)
        check_audio.dropdown_audio.place(x=90, y=510)
    else:
        lbl_null_audio = Label(root, text=':( Mp3 Audio file has not been found for your given link.',
                               font=('Arial Rounded MT Bold', 8))
        lbl_null_audio.place(x=82, y=510)
        btn_mp3['state'] = 'disabled'

    print(threading.activeCount(),"is running currently.(check audio).")
# Link checker valid or not.
def Check_validity():
    global core_object
    link = entry_link.get()
    try:
        core_object = YouTube(link, on_progress_callback=progress_status)
    except:
        messagebox.showerror("Error",
                             "Make sure you have :-\n1. Entered a Valid Youtube Link.\n2. You have an Active Internet-Connection.\n 4.It can be youtube side problem.")
    else:
        pass


# Defining Function for fetching and configuring title name.
def title_fetch():
    global video_title
    video_title = core_object.title
    # handling small errors.
    if video_title == 'YouTube':
        video_title = "Sorry, for inconvenience we are unable to fetch video title."
    
    # applying delimiter to length of youtube video title.
    total_length_title = len(video_title)
    if total_length_title >= 70:
        video_title = video_title[:65]
        video_title = (video_title + '...')
    else:
        pass
    # Configuring title unwanted parameters.
    list_dump = list(video_title)
    total_length_title = len(list_dump)
    for i in range(0, total_length_title):
        if list_dump[i] == ('<' or '>' or '|' or '?' or '*' or '/' or ':' or '"' or '\\'):
            list_dump[i] = '_'
        elif list_dump[i] == ('>'):
            list_dump[i] = '_'
        elif list_dump[i] == ('|'):
            list_dump[i] = '_'
        elif list_dump[i] == ('?'):
            list_dump[i] = '_'
        elif list_dump[i] == ('*'):
            list_dump[i] = '_'
        elif list_dump[i] == ('/'):
            list_dump[i] = '_'
        elif list_dump[i] == (':'):
            list_dump[i] = '_'
        elif list_dump[i] == ('"'):
            list_dump[i] = '_'
        elif list_dump[i] == ('\\'):
            list_dump[i] = '_'
        else:
            pass
    video_title = ''.join(list_dump)
    lbl_title = Label(root, text=video_title, font=('Consolas', 10, 'underline'))
    lbl_title.place(x=280, y=150)

# Defining Fetch core engine.
def fetch_view():
    # Fetching Views.
    try:
        total_views = int(core_object.views)
    except:
        lbl_views = Label(root, text='| Views = NA', font=('Consolas', 12))
        lbl_views.place(x=590, y=175)
    else:
        text_output = ('| Views = %d' % (total_views))
        lbl_views = Label(root, text=text_output, font=('Consolas', 12))
        lbl_views.place(x=590, y=175)
    finally:
        pass

# Defining functions for getting length of a video.
def fetch_length():
    length_sec = int(core_object.length)
    if length_sec < 60:
        total_length = ('Length = %d seconds' % (length_sec))
        lbl_length = Label(root, text=total_length, font=('Consolas', 12))
        lbl_length.place(x=280, y=175)
    elif (length_sec >= 60 and length_sec < 3600):
        length_min = length_sec // 60
        length_sec = length_sec % 60
        total_length = ('Length = %d min. %d sec.' % (length_min, length_sec))
        lbl_length = Label(root, text=total_length, font=('Consolas', 12))
        lbl_length.place(x=280, y=175)
    else:
        length_min = length_sec // 60
        length_sec_final = length_sec % 60
        length_hour = length_min // 60
        length_min = length_min % 60
        total_length = ('Length = %d hr. %d min. %d sec.' % (length_hour, length_min, length_sec_final))
        lbl_length = Label(root, text=total_length, font=('Consolas', 12))
        lbl_length.place(x=280, y=175)


# Defining function to fetch subtitles information.
def fetch_sub():
    # Adding Subtitles support only for english.
    fetch_sub.subtitles_unprocessed = core_object.captions.get_by_language_code('en')
    if fetch_sub.subtitles_unprocessed == None:
        lbl_sub = Label(root, text='Subtitles :- Not-Available', font=('Consolas', 12))
        lbl_sub.place(x=280, y=235)
    else:
        lbl_sub = Label(root, text='Subtitles :- Available', font=('Consolas', 12))
        lbl_sub.place(x=280, y=235)
        btn_sub = Button(root, text='Download Subs', font=('Comic sans MS', 8), relief=GROOVE, command=down_sub)
        btn_sub.place(x=600, y=235)

# defining function for downloading and processing thubmnail.
def fetch_thumbnail():
    global core_object, pic_processed

    image_url = core_object.thumbnail_url
    print(image_url)
    filename = 'thumbnail.png'

    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image Downloaded successfully.')

        # processing image
        img = Image.open('thumbnail.png')
        img = img.resize((250, 140), Image.ANTIALIAS)
        print('Resized successfully.')
        pic_processed = ImageTk.PhotoImage(img)
        thumbnail_lbl = Label(root, image=pic_processed)
        thumbnail_lbl.place(x=15, y=140)

    else:
        messagebox.showerror("Error!", "Unable to connect to our Server.\nKindly Check your Internet Connection.")
    os.remove('thumbnail.png')

# Principle Fetcher.
def fetch_information():
    global root
    global filename
    global core_object
    global pic_processed
    
    # Creating object
    link = entry_link.get()
    try:
        core_object = YouTube(link, on_progress_callback=progress_status)
    except:
        messagebox.showerror("Error",
                             "Make sure you have :-\n1. Entered a Valid Youtube Link.\n2. You have an Active Internet-Connection.\n 4.It can be youtube side problem.")
    else:
        pass

    # Fetching thumbnail information.
    fetch_thumbnail()

    # Fetching title information.
    title_fetch()

    # Fetching views of a youtube video.
    fetch_view()

    # Fetching length of a youtube video.
    fetch_length()

    # Fetching english subs.
    fetch_sub()

    # adding channel name.
    channel_name = core_object.author
    views_output = ('Uploaded By :- %s' % (channel_name))
    lbl_handle = Label(root, text=views_output, font=('Consolas', 12))
    lbl_handle.place(x=280, y=205)

    # Applying misc. information i.e. divider
    lbl_sectionv = Label(root, text='-------------------- Video Section -------------------',
                         font=('Arial Rounded MT bold', 10)).place(x=15, y=290)
    pic_video = Label(root, image=video_png).place(x=5, y=310)
    lbl_quality_choose = Label(root, text='Select Resolution', font=('Arial Rounded MT Bold', 10)).place(x=85, y=315)
    divider_text = ('-' * 130)
    lbl_divider = Label(root, text=divider_text, font=('Arial Rounded MT Bold', 10)).place(x=269, y=133)

    tasks_section()

def Core_engine():
    # fetching all types of video details.
    fetch_information()
    # Checking whether video file is available in specified in video link.
    search_mp4()
    # checking for available  audio files in mp3 formats.
    check_audio()

# Configuring root window.
root = Tk()
root.geometry('800x625+370+110')
root.resizable(0,0)
root.title('Youtube-Downloader')
#root.iconbitmap('icon.ico')

# Processing photos.
refresh_png = PhotoImage(file='Resources/refresh.png')
video_png = PhotoImage(file='Resources/video.png')
download_png = PhotoImage(file='Resources/download.png')
audio_png = PhotoImage(file='Resources/audio.png')
link_png = PhotoImage(file='Resources/link.png')
background_png = PhotoImage(file='Resources/background_task.png')

# Pre-Initialization
database_itags_mp4 = ['160', '133', '134', '135', '136', '137', '138', '264', '266']
available_itags = []
available_Qualities = []
core_object = ''
lbl_raw_load = Label(root, text='')
lbl_raw_load.place(x=500, y=300)

# Applying about us menu-bar.
menubar = Menu(root)
root.config(menu=menubar)

Submenu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label='About us', menu=Submenu1)
Submenu1.add_command(label='Developer', command=popup_creator)

# Main heading creator.
lbl_head = Label(root, text='Youtube - Video - Downloader', font=('BatmanForeverAlternate', 16, 'bold', 'underline'))
lbl_head.place(x=175, y=10)

# Creating entry denoter.
lbl_link = Label(root, text='Enter Link', font=('Lucida Sans', 12, 'underline'))
lbl_link.place(x=355, y=49)

# Creating pic along-side with entry_denoter.
pic_link = Label(root, image=link_png)
pic_link.place(x=438, y=52)

# Creating ttk widget Entry-bar.
entry_link = ttk.Entry(root, width=40, font=('Rockwell', 10))
entry_link.place(x=255, y=80)

# Creating refresh Button to refresh window.
refresh_it = ttk.Button(root, image=refresh_png, command=entry_link.delete(0, 'end'))
refresh_it.place(x=543, y=78)

# creating data-fetch button
fetch_btn = ttk.Button(root, text='Proceed', command=thread_fetch)
fetch_btn.place(x=357, y=110)

root.mainloop()
