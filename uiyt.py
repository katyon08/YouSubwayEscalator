import os
import threading
from tkinter import Frame, IntVar, BooleanVar, Text, StringVar, RAISED, BOTH, messagebox

from tkinter import *
from tkinter.scrolledtext import ScrolledText

import pytube
import datetime
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError


class App(Frame):
    lock = False

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self. grid()
        self.pack()
        self.master = master
        self.download_type = IntVar()
        self.audio_only = BooleanVar()
        self.from_url = StringVar()
        self.to_url = StringVar()

        self.radois = Frame(self, relief=RAISED, borderwidth=1)
        self.radois.pack(fill=BOTH, expand=True)

        self.download_playlist = Radiobutton(
            self.radois,
            text='Плейлист целиком',
            variable=self.download_type,
            value=0)
        self.download_playlist.pack(ipadx=10, ipady=10, side=LEFT)

        self.download_file_only = Radiobutton(
            self.radois,
            text='Только файл',
            variable=self.download_type,
            value=1
        )
        self.download_file_only.pack(ipadx=10, ipady=10, side=LEFT)

        self.download_url_label = Label(text="Откуда качать")
        self.download_url_label.pack(ipadx=10, ipady=10)

        self.download_url = Entry(self.master, textvariable=self.from_url)
        self.download_url.pack(ipadx=10, ipady=3, expand=True, fill=BOTH)

        self.download_url_label = Label(text="Куда качать")
        self.download_url_label.pack(ipadx=10, ipady=10)

        self.save_url = Entry(self.master, textvariable=self.to_url)
        self.save_url.pack(ipadx=10, ipady=3, expand=True, fill=BOTH)

        self.audio_checkbox = Checkbutton(
            self.master,
            text='Только аудио',
            variable=self.audio_only,
            onvalue=True,
            offvalue=False)
        self.audio_checkbox.pack(ipadx=10, ipady=10)

        self.message_button = Button(text="Скачать", command=self.run_program)
        self.message_button.pack(ipadx=10, ipady=10)

        self.editArea = ScrolledText(
            master=self.master,
            wrap=WORD,
            width=20,
            height=10)
        self.editArea.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def run_program(self):

        if not self.lock:
            self.lock = True
            thread = threading.Thread(target=self.run, args=(), )
            thread.daemon = True
            thread.start()
        else:
            messagebox.showerror("Error", "В данный момент уже идет загрузка, подождите окончания предыдущей и попробуйте снова!")

    def run(self):
        if self.download_type.get() == 0:
            self.edit_print("Качаем весь плейлист")
            download_playlist(self.from_url.get(), self.to_url.get(), self.audio_only.get())
        elif self.download_type == 1:
            self.edit_print("Качаем один файл")
            download_song(self.from_url.get(), self.to_url.get(), self.audio_only.get())
        self.lock = False

    def edit_print(self, text):
        self.editArea.insert(END, text + "\n")
        self.editArea.yview(END)


global app


def download_playlist(playlist_path, out_path, audio):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    app.edit_print("Скачиваю плейлист:\n\t" + playlist_path)
    i = 1
    dplaylist = Playlist(playlist_path).parse_links()
    for item in dplaylist:
        app.edit_print("{}/{}".format(i, dplaylist.__len__()))
        i += 1
        download_song(item, out_path, audio)


def exist(in_path, in_file):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if in_file in file:
                return True
    return False


def download_song(song_path, pl_path, audio, with_size=True):
    try:
        app.edit_print("Парсим: " + song_path)
        yt = YouTube(song_path)

        if exist(pl_path, yt.title):
            app.edit_print("\t\tУже скачано: " + os.path.join(pl_path, yt.title))
            return

        if audio:
            app.edit_print("\tКачаю только аудио: " + yt.title)
            stream = yt.streams.filter(only_audio=True, subtype='mp4').order_by('resolution').first()
        else:
            app.edit_print("\tКачаю: " + yt.title)
            stream = yt.streams.first()
        if True and stream.filesize > 1024 * 1024:
            if stream.filesize > 1024 * 1024 * 1024:
                app.edit_print(
                    "Ничего себе, а файл-то не маленький, целых {} ГигоБайт, Мне понадобится какое-то время для этого!"
                    .format(str(stream.filesize // (1024 * 1024 * 1024))))
            else:
                app.edit_print(
                    "Ничего себе, а файл-то не маленький, целых {} МегаБайт, Мне понадобится какое-то время для этого!"
                    .format(str(stream.filesize // (1024 * 1024))))
        # print("Info: \n" +
        #       "\tsize = {}\n".format(stream.filesize) +
        #       "\tdefault_filename = {}\n".format(stream.default_filename) +
        #       "\taudio_codec = {}\n".format(stream.audio_codec) +
        #       "\tvideo_codec = {}\n".format(stream.video_codec) +
        #       "\tfps = {}\n".format(stream.fps) +
        #       "\tincludes_audio_track = {}\n".format(stream.includes_audio_track) +
        #       "\tincludes_video_track = {}\n".format(stream.includes_video_track) +
        #       "\tis_adaptive = {}\n".format(stream.is_adaptive) +
        #       "\tis_progressive = {}\n".format(stream.is_progressive) +
        #       "\tcodecs = {}\n".format(stream.codecs) +
        #       "\tsubtype = {}\n".format(stream.subtype) +
        #       "\ttype = {}\n".format(stream.type) +
        #       "\titag = {}\n".format(stream.itag) +
        #       "\tfmt_profile = {}\n".format(stream.fmt_profile) +
        #       "\tmime_type = {}\n".format(stream.mime_type) +
        #       "\turl = {}\n".format(stream.url) +
        #       "\tabr = {}\n".format(stream.abr) +
        #       "\tres = {}\n".format(stream.res)
        #       )
        global prev
        global timestart
        prev = 0
        timestart = datetime.datetime.now()
        yt.register_on_progress_callback(show_progress)

        stream.download(pl_path)

        app.edit_print("\t\tЗагруженно: " + os.path.join(pl_path, yt.title))
    except KeyError as e:
        app.edit_print(
            u"OOPS! С этим видео что-то не так (KeyError)! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

    # except AttributeError as e:
    #     app.edit_print(u"OOPS! С этим видео что-то не так (AttributeError)! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

    except UnicodeDecodeError as e:
        app.edit_print(
            u"OOPS! С этим видео что-то не так (UnicodeDecodeError)! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

    # except TypeError as e:
    #     app.edit_print(u"OOPS! С этим видео что-то не так (TypeError)! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

    except pytube.exceptions.RegexMatchError:
        app.edit_print(u"Я не вижу тут видео")
    except AttributeError:
        if with_size:
            download_song(song_path, pl_path, audio, with_size=False)
        else:
            app.edit_print(
                u"OOPS! С этим видео что-то не так (AttributeError)! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")


def show_progress(stream, chunk, file_handle, bytes_remaining):
    global prev
    global timestart
    now = datetime.datetime.now()

    # (file_handle.tell() * 100) // (bytes_remaining + file_handle.tell())) % 5 == 0
    #                                                                         and prev is not (
    # (file_handle.tell() * 100) // (bytes_remaining + file_handle.tell()))

    if (now - timestart).seconds > 10:
        timestart = now
        prev = ((file_handle.tell() * 100) // (bytes_remaining + file_handle.tell()))
        app.edit_print("Уже " + str((file_handle.tell() * 100) // (bytes_remaining + file_handle.tell())) + '%')


if __name__ == '__main__':
    root = Tk()
    root.title('YT Downloader')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = App(root)
    app.mainloop()
