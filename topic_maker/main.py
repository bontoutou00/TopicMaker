"""Topic Maker"""
import base64
import os
import subprocess
import re
import sys
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import yaml
import PyMDL
from pymediainfo import MediaInfo
import pyperclip
import sv_ttk
import imgbbpy
from template import Templates
from omdb_api_fetcher import Client
from pyperclip import copy
from exceptions import InvalidApiKey, NoApiKeyProvided, TooManyResults, IncorrectImdbId, MovieNotFound, ErrorGettingData, SomethingWentWrong
from config import logger, Config
from constants import DATA_PATH, VERSION, DEFAULT_TEMPLATE, VALUES_TEMPLATE, Path

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.print_topic_name = tk.StringVar()
        self.print_topic = tk.StringVar()
        self.mdl_var = tk.BooleanVar()
        self.screenshoots_var = tk.BooleanVar()
        self.base64_var = tk.BooleanVar()
        self.bottom_var = tk.BooleanVar()
        self.button_choose_file = ttk.Button(command=lambda: threading.Thread(target=Functions().main).start(),
                                             text="Start", state=tk.DISABLED)
        self.button_about = ttk.Button(parent, text = "About", command = self.about)
        self.button_modify_template = ttk.Button(parent, text = "Modify Template", command = self.template_editor)
        self.source_var = tk.StringVar()
        self.entry_name= ttk.Entry()
        self.entry_year= ttk.Entry()
        self.combo_source= ttk.Combobox(values = self.yaml_source(), textvariable=self.source_var)
        self.button_save_source= ttk.Button(text = "Save", command=self.yaml_write)
        self.entry_download_link = ttk.Entry()
        self.checkbutton_mdl = ttk.Checkbutton(text = "MyDramaList",
                                               variable = self.mdl_var,
                                               onvalue = 1, offvalue = 0)
        self.checkbutton_screenshots = ttk.Checkbutton(text = "Screenshots",
                                                       variable = self.screenshoots_var,
                                                       onvalue = 1, offvalue = 0,
                                                       command=self.screenshots_number)
        self.checkbutton_base64 = ttk.Checkbutton(text = "Base64",
                                                  variable = self.base64_var,
                                                  onvalue = 1, offvalue = 0,
                                                  command=self.base64_number)
        self.label_topic_name = ttk.Label(textvariable=self.print_topic_name)
        self.label_topic = ttk.Label(textvariable=self.print_topic)
        self.button_choose_file.place(x=570.0, y=35.0, width=120.0, height=50.0)
        self.button_about.place(x=610.0, y=110.0, width=80.0, height=35.0)
        self.button_modify_template.place(x=460.0, y=110.0, width=140.0, height=35.0)
        self.entry_name.pack()
        self.entry_name.place(x=10.0, y=10.0, width=270.0, height=35.0)
        self.entry_year.pack()
        self.entry_year.place(x=290.0, y=10.0, width=80.0, height=35.0)
        self.combo_source.pack()
        self.combo_source.place(x=10.0, y=60.0, width=270.0, height=35.0)
        self.button_save_source.pack()
        self.button_save_source.place(x=290.0, y=60.0, width=80.0, height=35.0)
        self.entry_download_link.pack()
        self.entry_download_link.place(x=10.0, y=110.0, width=400.0, height=35.0)
        self.checkbutton_mdl.pack()
        self.checkbutton_mdl.place(x=425.0, y=10.0, width=120.0, height=30.0)
        self.checkbutton_screenshots.pack()
        self.checkbutton_screenshots.place(x=425.0, y=40.0, width=120.0, height=30.0)
        self.checkbutton_base64.pack()
        self.checkbutton_base64.place(x=425.0, y=70.0, width=90.0, height=30.0)
        self.label_topic_name.pack()
        self.label_topic_name.place(x=10.0, y=165.0, width=595.0, height=35.0)
        self.label_topic_name.configure(anchor="center")
        self.label_topic.pack()
        self.label_topic.place(x=10.0, y=210.0, width=595.0, height=35.0)
        self.label_topic.configure(anchor="center")
        self.init_placeholder(self.entry_name, "Movie or TV Name")
        self.init_placeholder(self.entry_year, "Year")
        self.init_placeholder(self.combo_source, "Source")
        self.init_placeholder(self.entry_download_link, "Download Link")

    def template_editor(self):
        """
        The template_edit function is used to edit the template file.\n
        It creates a new window with a text editor and some buttons.\n
        The user can save his changes and restore the default template
        """
        template_edit_ = tk.Toplevel(self)
        template_edit_.title("Template Editor")
        template_edit_.geometry("1100x600")
        self.var_info = tk.StringVar()
        button_save = ttk.Button(template_edit_, text = "Save", command = self.save_file)
        button_save.place(x=840.0, y=555.0, width=80.0, height=35.0)
        button_restore = ttk.Button(template_edit_, text = "Restore Default", command = self.restore_default_file)
        button_restore.place(x=930.0, y=555.0, width=160.0, height=35.0)
        self.combo_values = ttk.Combobox(template_edit_, values = list(VALUES_TEMPLATE.values()))
        self.combo_values.pack()
        self.combo_values.place(x=10.0, y=555.0, width=150.0, height=35.0)
        self.combo_values.bind('<<ComboboxSelected>>', lambda e: self.var_info.set(list(VALUES_TEMPLATE.keys())[self.combo_values.current()]))
        self.init_placeholder(self.combo_values, "Available Values")
        label_info = ttk.Label(template_edit_, textvariable=self.var_info)
        label_info.pack()
        label_info.place(x=170.0, y=555.0, width=650.0, height=35.0)
        self.text_edit = tk.Text(template_edit_, undo=True)
        self.text_edit.pack()
        self.text_edit.configure(font=("TkDefaultFont", 11))
        self.text_edit.place(x=10.0, y=10.0, width=1080.0, height=535.0)
        self.read_file()
        self.text_edit.bind('<Control-s>', lambda e: self.save_file())
        template_edit_.resizable(False, False)

    def save_file(self):
        """
        The save_file function saves the contents of the text_edit widget to a file.
        """
        content = self.text_edit.get(1.0, "end-1c")
        with open(DATA_PATH/'template.txt', 'w', encoding='utf8') as file:
            file.write(content)

    def read_file(self):
        """
        The read_file function reads the template.txt file and inserts it into the text_edit widget.
        """
        self.text_edit.delete('1.0', tk.END)
        with open(DATA_PATH/'template.txt', 'r', encoding='utf8') as file:
            self.text_edit.insert(tk.END, file.read())

    def restore_default_file(self):
        """
        The restore_default_file function restores the template.txt file to its default state.
        """
        res = messagebox.askquestion('Restore Template.txt', 'Do you really want to restore to default?')
        if res == 'yes' :
            with open(DATA_PATH/'template.txt', 'w', encoding='utf8') as file:
                file.write(DEFAULT_TEMPLATE)
            self.read_file()
        else:
            pass

    def about(self):
        """
        The about function creates a new window that show all the modules used.

        """
        about_ = tk.Toplevel(self)
        about_.title("About")
        about_.geometry("340x175")
        label_name_version = ttk.Label(about_,
                                       text=f'Topic Maker {VERSION}',
                                       font=("Inter", 18 * -1))
        label_name_version.pack()
        label_name_version.place(x=20.0, y=20.0, width=300.0, height=20.0)
        label_name_version.configure(anchor="center")
        button_open_python_website = ttk.Button(about_, text = "Python",
                                                command = lambda: webbrowser.open_new_tab('https://www.python.org/'))
        button_open_python_website.place(x=20.0, y=50.0, width=70.0, height=35.0)
        button_open_pymdl_website = ttk.Button(about_, text = "PyMDL",
                                               command = lambda: webbrowser.open_new_tab('https://pypi.org/project/PyMDL/'))
        button_open_pymdl_website.place(x=100.0, y=50.0, width=95.0, height=35.0)
        button_open_pymi = ttk.Button(about_, text = "pymediainfo",
                                      command = lambda: webbrowser.open_new_tab('https://pypi.org/project/pymediainfo/'))
        button_open_pymi.place(x=205.0, y=50.0, width=120.0, height=35.0)
        button_open_omdb_website = ttk.Button(about_, text = "OMDB",
                                              command = lambda: webbrowser.open_new_tab('https://omdbapi.com/'))
        button_open_omdb_website.place(x=20.0, y=95.0, width=70.0, height=35.0)
        button_open_imgbbpy_website = ttk.Button(about_, text = "imgbbpy",
                                                 command = lambda:webbrowser.open_new_tab('https://pypi.org/project/imgbbpy/'))
        button_open_imgbbpy_website.place(x=100.0, y=95.0, width=95.0, height=35.0)
        button_open_imgbbpy_website = ttk.Button(about_, text = "GitHub Repo",
                                                 command = lambda: webbrowser.open_new_tab('https://github.com/bontoutou00/topic_maker'))
        button_open_imgbbpy_website.place(x=205.0, y=95.0, width=120.0, height=35.0)
        label_name = ttk.Label(about_, text="@bontoutou", font=("Inter", 16 * -1))
        label_name.pack()
        label_name.place(x=20.0, y=140.0, width=300.0, height=20.0)
        label_name.configure(anchor="center")
        about_.resizable(False, False)

    def omdb(self):
        """
        The omdb function creates a new window that allows the user to enter their OMDB API key.
        """
        self.omdb_ = tk.Toplevel(self)
        self.omdb_.title("Add your OMDB API Key")
        self.omdb_.geometry("330x110")
        self.omdb_api_key_var = tk.StringVar()
        self.waiting_var = tk.IntVar()
        omdb_api_key_label = ttk.Label(self.omdb_, text="OMDB API key")
        omdb_api_key_entry = ttk.Entry(self.omdb_, textvariable=self.omdb_api_key_var)
        omdb_api_key_label.pack()
        omdb_api_key_label.place(x=10.0, y=10.0, width=100.0, height=35.0)
        omdb_api_key_entry.pack()
        omdb_api_key_entry.place(x=120.0, y=10.0, width=200.0, height=35.0)
        button_help = ttk.Button(self.omdb_, text = "Register OMDB API Key",
                                 command=lambda: webbrowser.open_new_tab('https://www.omdbapi.com/apikey.aspx'))
        button_help.place(x=10.0, y=65.0, width=170.0, height=35.0)
        button_save = ttk.Button(self.omdb_, text = "Save", command = lambda: self.destroy_window(self.omdb_))
        button_save.place(x=230.0, y=65.0, width=90.0, height=35.0)
        self.omdb_.resizable(False, False)

    def imgbb(self):
        """
        The imgbb function creates a new window that allows the user to enter their ImgBB API key.
        """
        self.imgbb_ = tk.Toplevel(self)
        self.imgbb_.title("Add your ImgBB API Key")
        self.imgbb_.geometry("330x110")
        self.imgbb_api_key_var = tk.StringVar()
        self.waiting_var = tk.IntVar()
        imgbb_api_key_label = ttk.Label(self.imgbb_, text="ImgBB API key")
        imgbb_api_key_entry = ttk.Entry(self.imgbb_, textvariable=self.imgbb_api_key_var)
        imgbb_api_key_label.pack()
        imgbb_api_key_label.place(x=10.0, y=10.0, width=100.0, height=35.0)
        imgbb_api_key_entry.pack()
        imgbb_api_key_entry.place(x=120.0, y=10.0, width=200.0, height=35.0)
        button_help = ttk.Button(self.imgbb_, text = "Register ImgbBB API Key",
                                 command=lambda: webbrowser.open_new_tab('https://api.imgbb.com/'))
        button_help.place(x=10.0, y=65.0, width=180.0, height=35.0)
        button_save = ttk.Button(self.imgbb_, text = "Save", command = lambda: self.destroy_window(self.imgbb_))
        button_save.place(x=230.0, y=65.0, width=90.0, height=35.0)
        self.imgbb_.resizable(False, False)

    def omdb_results(self):
        """
        The omdb_results function creates a new window that displays the results of an OMDB search.\n
        The user can select one of the results and double-click on it to choose it.
        """
        self.omdb_results_ = tk.Toplevel(self)
        self.omdb_results_.title("OMDB Search Results")
        self.omdb_results_.geometry("650x290")
        self.waiting_var = tk.IntVar()
        self.imdb_id_search = tk.StringVar()
        columns = ('title', 'year', 'mediatype')
        self.tree_omdb = ttk.Treeview(self.omdb_results_, columns=columns, show='headings')
        self.tree_omdb.heading('title', text='Title')
        self.tree_omdb.column('title', width=300, anchor=tk.W)
        self.tree_omdb.heading('year', text='Year')
        self.tree_omdb.column('year', width=50, anchor=tk.W)
        self.tree_omdb.heading('mediatype', text='Mediatype')
        self.tree_omdb.column('mediatype', width=50, anchor=tk.W)
        self.tree_omdb.bind('<<TreeviewSelect>>',
                            lambda event: self.result_selected(search='omdb', tree=self.tree_omdb, event=event))
        self.tree_omdb.bind('<Double-Button>',
                            lambda event: self.choice_result(search='omdb', tree=self.tree_omdb, event=event))
        self.tree_omdb.place(x=10.0, y=10.0, width=630, height=270)
        self.omdb_results_.resizable(False, False)

    def mdl_results(self):
        """
        The omdb_results function creates a new window that displays the results of an OMDB search.\n
        The user can select one of the results and double-click on it to choose it.
        """
        self.mdl_results_ = tk.Toplevel(self)
        self.mdl_results_.title("MyDramaList Search Results")
        self.mdl_results_.geometry("650x290")
        self.waiting_var = tk.IntVar()
        self.mdl_search = tk.StringVar()
        columns = ('title', 'mediatype')
        self.tree_mdl = ttk.Treeview(self.mdl_results_, columns=columns, show='headings')
        self.tree_mdl.heading('title', text='Title')
        self.tree_mdl.column('title', width=300, anchor=tk.W)
        self.tree_mdl.heading('mediatype', text='Mediatype')
        self.tree_mdl.column('mediatype', width=50, anchor=tk.W)
        self.tree_mdl.bind('<<TreeviewSelect>>',
                           lambda event: self.result_selected(search='mdl', tree=self.tree_mdl, event=event))
        self.tree_mdl.bind('<Double-Button>',
                           lambda event: self.choice_result(search='mdl', tree=self.tree_mdl, event=event))
        self.tree_mdl.place(x=10.0, y=10.0, width=630, height=270)
        self.mdl_results_.resizable(False, False)

    def choice_result(self, search, tree, event):
        """
        The choice_result function is called when the user clicks on a row in the omdb_results window.\n
        It takes the imdbID of that movie and puts it into self.imdb_id_search,\n
        which is then used to search for the movie in question.
        """
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            if search == 'omdb':
                self.imdb_id_search.set(record[3])
                self.destroy_window(self.omdb_results_)
            else:
                self.mdl_search.set(record[0])
                self.destroy_window(self.mdl_results_)

    def result_selected(self, search, tree, event):
        """
        The result_selected function is called when the user right-clicks on a row in the treeview.\n
        It creates a context menu with two options: Copy Link and Open iMDB link. The first option copies\n
        the IMDb URL of the selected movie to clipboard, while the second opens it in your default browser.
        """
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            if record:
                if search == 'omdb':
                    context_menu = tk.Menu(gui.omdb_results_, tearoff=0)
                    context_menu.add_command(label="Copy Link", command=lambda: copy(f'https://www.imdb.com/title/{record[3]}'))
                    context_menu.add_command(label="Open iMDB Link", command = lambda: webbrowser.open_new_tab(f'https://www.imdb.com/title/{record[3]}'))
                    tree.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))
                else:
                    context_menu = tk.Menu(gui.mdl_results_, tearoff=0)
                    context_menu.add_command(label="Copy Link", command=lambda: copy(record[2]))
                    context_menu.add_command(label="Open MyDramaList Link", command = lambda: webbrowser.open_new_tab(record[2]))
                    tree.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))

    def destroy_window(self, window):
        """
        The destroy_window function is used to destroy a window.\n
        It takes one argument, the window that you want to destroy.\n 
        Args:
            window: Destroy the window
        """
        gui.waiting_var.set(1)
        window.destroy()

    def remove_placeholder(self, event): ## https://stackoverflow.com/a/63652882
        """Remove placeholder text, if present"""
        placeholder_text = getattr(event.widget, "placeholder", "")
        if placeholder_text and event.widget.get() == placeholder_text:
            event.widget.delete(0, "end")
            gui.button_choose_file['state'] = tk.NORMAL

    def add_placeholder(self, event): ## https://stackoverflow.com/a/63652882
        """Add placeholder text if the widget is empty"""
        placeholder_text = getattr(event.widget, "placeholder", "")
        if placeholder_text and event.widget.get() == "":
            event.widget.insert(0, placeholder_text)

    def init_placeholder(self, widget, placeholder_text): ## https://stackoverflow.com/a/63652882
        widget.placeholder = placeholder_text
        if widget.get() == "":
            widget.insert("end", placeholder_text)
        widget.bind("<FocusIn>", self.remove_placeholder)
        widget.bind("<FocusOut>", self.add_placeholder)

    def save_config_settings(self, type_var):
        """
        The save_config_settings function saves the user's input to the config file.\n
        """
        if type_var == 'omdb':
            omdb_api_key = self.omdb_api_key_var.get()
            Config().config.set("SETTINGS", "omdb_api", str(omdb_api_key))
            logger.info(f'omdb_api: {omdb_api_key}')
        elif type_var == 'imgbb':
            imgbb_api_key = self.imgbb_api_key_var.get()
            Config().config.set("SETTINGS", "imgbb_api", str(imgbb_api_key))
            logger.info(f'imgbb_api: {imgbb_api_key}')
        Config().write_config_file()

    def yaml_source(self):
        with open(DATA_PATH/'list_sources.yaml', 'r', encoding="utf8") as file:
            sources = yaml.safe_load(file)
            return sources

    def yaml_write(self):
        sources = self.yaml_source()
        add_source =  [gui.combo_source.get()]
        if add_source == 'Source':
            pass
        elif "".join(add_source) in sources:
            Functions().alert('', f'{"".join(add_source)} is already in list_sources.yaml',
                              kind='warning')
        else:
            with open(DATA_PATH/'list_sources.yaml', 'a+', encoding='utf8') as file:
                yaml.safe_dump(add_source, file, sort_keys=False)
                Functions().alert('', f'{"".join(add_source)} was added to list_sources.yaml', kind='info')

    def base64_number(self):
        if gui.base64_var.get() is True:
            self.var_number_base64 = tk.StringVar()
            self.entry_number_base64 = ttk.Entry(textvariable=self.var_number_base64)
            self.entry_number_base64.pack()
            self.entry_number_base64.place(x=390.0, y=70.0, width=25.0, height=30.0)
            self.entry_number_base64.insert(0, 1)
            self.var_number_base64.trace("w",
                                         lambda *args: self.character_limit(self.var_number_base64))
        elif gui.base64_var.get() is False:
            self.entry_number_base64.destroy()

    def screenshots_number(self):
        if gui.screenshoots_var.get() is True:
            self.var_number_screenshots = tk.StringVar()
            self.entry_number_screenshots = ttk.Entry(textvariable=self.var_number_screenshots)
            self.entry_number_screenshots.pack()
            self.entry_number_screenshots.place(x=390.0, y=40.0, width=25.0, height=30.0)
            self.entry_number_screenshots.insert(0, 1)
            self.var_number_screenshots.trace("w",
                                              lambda *args: self.character_limit(self.var_number_screenshots))
        elif gui.screenshoots_var.get() is False:
            self.entry_number_screenshots.destroy()

    def character_limit(self, entry):
        """
        The character_limit function is used to limit the number of characters that can be entered into an Entry widget.\n
        Args:
            entry: Get the value of the entry widget
        """
        if len(entry.get()) > 0:
            entry.set(entry.get()[-1])
        elif len(entry.get()):
            entry.set(entry.get()[-1])

class Functions:
    def __init__(self) -> None:
        self.search_results = []
        self.imdb_results = []

    def omdb_handling(self):
        """
        The omdb_handling function is the main function that handles all of the omdb API calls.\n
        It first checks to see if an api key has been entered in the config file, and if not it will prompt for one.\n
        Then it takes in a name and year from user input, or an imdb id from user input (if they have one).\n
        It then uses this information to make a call to omdb's mediatype_search function\n
        which returns either a movie or tv show object depending on what was searched for.
        """
        if Config().config.get("SETTINGS", "omdb_api"):
            omdb_api = Config().config.get("SETTINGS", "omdb_api")
        else:
            gui.omdb()
            gui.wait_variable(gui.waiting_var)
            gui.save_config_settings('omdb')
            omdb_api = Config().config.get("SETTINGS", "omdb_api")
        self.omdb_client = Client(omdb_api)
        self.name = gui.entry_name.get().strip()
        imdb_entry = re.search(r'(tt\d{1,})', self.name)
        if self.name == 'Movie or TV Name':
            sys.exit()
        else:
            self.year = gui.entry_year.get()
            if imdb_entry:
                imdbid = imdb_entry.group()
                logger.info(imdbid)
                self.omdb_mediatype(imdbid)
            elif self.year != 'Year':
                logger.info(self.name)
                logger.info(self.year)
                try:
                    imdbid = self.omdb_client.mediatype_search({'t': self.name, 'y': self.year})
                except (InvalidApiKey, NoApiKeyProvided, TooManyResults, MovieNotFound, ErrorGettingData, SomethingWentWrong) as error:
                    logger.warning(error)
                    self.alert('Error', error, kind='error')
                    sys.exit()
                else:
                    self.omdb_mediatype(imdbid)
            else:
                self.imdb_search_list()

    def omdb_mediatype(self, imdbid: str):
        """
        The omdb_mediatype function takes an IMDb ID as a string and uses the omdb_client to determine if it is a movie or series.\n
        If it is a movie, then the function calls the movie_omdb function with that IMDb ID.\n
        If it is not, then the function calls the series_omdb function with that IMDb ID.\n
        Args:
            imdbid: str: Pass the imdbid to the function
        """
        try:
            mediatype = self.omdb_client.mediatype_imdb(imdbid)
        except (InvalidApiKey, NoApiKeyProvided, TooManyResults, IncorrectImdbId, ErrorGettingData, SomethingWentWrong) as error:
            logger.warning(error)
            self.alert('Error', error, kind='error')
            sys.exit()
        else:
            if mediatype == 'movie':
                self.movie_omdb(imdbid)
            elif mediatype == 'series' or mediatype == 'episode':
                self.series_omdb(imdbid)
            else:
                logger.info('Unexpected media type')
                self.alert('Error', 'Unexpected media type', kind='error')
                sys.exit()

    def imdb_search_list(self):
        """
        The imdb_search_list function is used to search for a movie or TV show on IMDb.\n
        It takes the user's input and searches for it using the omdb_request function from the OMDb API client.\n
        It then displays all of the results in a listbox, allowing the user to select which one they want.
        """
        try:
            self.search_results.clear()
            resp = self.omdb_client.omdb_request({'s': self.name})
        except (InvalidApiKey, NoApiKeyProvided, TooManyResults, MovieNotFound, ErrorGettingData, SomethingWentWrong) as error:
            logger.warning(error)
            self.alert('Error', error, kind='error')
            sys.exit()
        else:
            for value in resp['Search']:
                self.search_results.append({'title': value['Title'], 'year': value['Year'], 'mediatype': value['Type'], 'imdb_id': value['imdbID']})
            gui.omdb_results()
            for result in self.search_results:
                gui.tree_omdb.insert('', tk.END, values=list(result.values()))
            gui.wait_variable(gui.waiting_var)
            gui.entry_name.delete(0, tk.END)
            gui.entry_name.insert(tk.END, gui.imdb_id_search.get())
            self.omdb_handling()

    def movie_omdb(self, imdbid: str):
        """
        The movie_omdb function takes an IMDB ID and uses the omdbapi.com API to retrieve information about that movie.
        The function then sets the entries for this object using set_entries()\n
        Args:
            imdbid: str: Pass the imdbid of a movie to the omdb api
        """
        self.data =  self.omdb_client.movie(imdbid)
        self.set_entries()

    def series_omdb(self, imdbid: str):
        """
        The series_omdb function takes an IMDB ID and uses the omdbapi.com API to retrieve information about that series.
        The function then sets the entries for this object using set_entries()\n
        Args:
            imdbid: str: Pass the imdbid of a series to the omdb api
        """
        self.data = self.omdb_client.series(imdbid)
        self.set_entries()

    def set_entries(self):
        self.name = self.data['title']
        self.year = self.data['year']
        gui.entry_name.delete(0, tk.END)
        gui.entry_year.delete(0, tk.END)
        gui.entry_name.insert(tk.END, self.name)
        gui.entry_year.insert(tk.END, self.year)
        self.mdl()

    def mdl(self):
        """
        The mdl function searches MyDramaList for the title and year of the movie / drama.
        """
        if gui.mdl_var.get() is True:
            try:
                mdl_year = re.search(r'(\d{4})', self.year).group(1)
                self.search_results.clear()
                resp = PyMDL.search(name=self.name, year=mdl_year, max_results=5)
                logger.info(f'MyDramaList results: {resp}')
            except AttributeError:
                return False
            else:
                if resp is not None:
                    for value in resp.get_all():
                        self.search_results.append({'title': value.title, 'mediatype': value.type, 'link': value.url})
                    gui.mdl_results()
                    for result in self.search_results:
                        gui.tree_mdl.insert('', tk.END, values=list(result.values()))
                    gui.wait_variable(gui.waiting_var)
                    try:
                        resp = PyMDL.search(name=gui.mdl_search.get())
                        mdl_dic = resp.get(0)
                    except AttributeError:
                        return False
                    else:
                        data_mdl = {
                        'title_mdl' : mdl_dic.title,
                        'thumbnail_mdl' :  mdl_dic.thumbnail,
                        'media_type_mdl' :  mdl_dic.type,
                        'url_mdl' :  mdl_dic.url,
                        'ratings_mdl' :  mdl_dic.ratings,
                        'plot_mdl' :  mdl_dic.synopsis,
                        'actors_mdl' : ",".join(mdl_dic.casts),
                        'native_title_mdl' :  mdl_dic.native,
                        'genre_mdl' :  mdl_dic.genre,
                        'runtime_mdl' :  mdl_dic.duration,
                        'country_mdl' :  mdl_dic.country,
                        'aka_mdl' : ",".join(mdl_dic.aka),
                        'director_mdl' :  mdl_dic.director,
                        'writer_mdl' :  mdl_dic.screenwriter,
                        'release_date_mdl' :  mdl_dic.date,
                        }
                        logger.info(data_mdl)
                        self.data.update(data_mdl)
                else:
                    self.alert('Error', f'No results for {self.name} ({mdl_year})', 'error')

    def media_info(self):
        """
        The media_info function is used to get the metadata of a video file.
        """
        self.file_path = filedialog.askopenfilename(title="Select a file")
        logger.info(f'Filepath: {self.file_path}')
        if self.file_path:
            self.filename_no_extension = Path(self.file_path).stem
            self.mediainfo = MediaInfo.parse(self.file_path,
                                             full=False,
                                             output="txt").replace('\n','')
            self.size = self.convert_bytes(os.stat(self.file_path).st_size)
            logger.info(f'Size of file: {self.size}')
            return True
        else:
            return False

    def convert_bytes(self, size):
        """ Convert bytes to KB, or MB or GB"""
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f'{size:3.2f} {x:s}'
            size /= 1024.0
        return size

    def imgbb(self):
        """
        The imgbb function is used to set the imgbb_api variable.\n
        If the user has already entered their API key in the settings, it will be retrieved from there.\n
        Otherwise, a popup window will appear asking for an API key and then save it to settings.

        """
        if Config().config.get("SETTINGS", "imgbb_api"):
            self.imgbb_api = Config().config.get("SETTINGS", "imgbb_api")
        else:
            gui.imgbb()
            gui.wait_variable(gui.waiting_var)
            gui.save_config_settings('imgbb')
            self.imgbb_api = Config().config.get("SETTINGS", "imgbb_api")
        logger.info(f'ImgBB API Key: {self.imgbb_api}')

    def imgbb_screenshot(self):
        """
        The imgbb_screenshot function takes a screenshot of the video file and uploads it to ImgBB.\n
        It returns a list of links to the uploaded screenshots.\n
        Returns:
            A list of links, so you can use it like this:
        """
        self.imgbb()
        try:
            client = imgbbpy.SyncClient(self.imgbb_api)
        except ValueError:
            logger.info(f'Wrong ImgBB API Key: {self.imgbb_api}')
            self.alert('Error', 'Wrong ImgBB API Key.', kind='error')
            return
        else:
            screenshots_links = []
            path = os.path.dirname(self.file_path)
            root.geometry("700x210")
            file_list = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))
                         and f.endswith('.png')]
            logger.info(file_list)
            if not file_list:
                if gui.screenshoots_var.get() is True:
                    logger.info('Creating new screenshots')
                    number = gui.entry_number_screenshots.get()
                    if number:
                        if number.isdigit():
                            number = number
                        else:
                            number = str(1)
                            gui.entry_number_screenshots.delete(0, tk.END)
                            gui.entry_number_screenshots.insert(0, number)
                    else:
                        number = str(1)
                        gui.entry_number_screenshots.delete(0, tk.END)
                        gui.entry_number_screenshots.insert(0, number)
                    logger.info(f'Number of screenshots to make: {number}')
                path_without_extension = ".".join(self.file_path.split(".")[:-1])
                output_join = f'{path_without_extension}-%03d.png'
                try:
                    output = subprocess.Popen(f'ffmpeg -ss 00:02:00 -i "{str(self.file_path)}" -vf fps=1/60 -frames:v {number} -f image2 "{output_join}"',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=1)
                    for line in output.stdout:
                        logger.info(line)
                        gui.print_topic_name.set(line)
                except subprocess.CalledProcessError as error:
                    logger.info(error)
                    gui.print_topic_name.set(error)
                else:
                    file_list = [f for f in os.listdir(path)
                                 if os.path.isfile(os.path.join(path, f))
                                 and f.endswith('.png')]
            i = 0
            total = len(file_list)
            logger.info(file_list)
            for file in file_list:
                i += 1
                file_name = ".".join(file.split(".")[:-1])
                img_path = os.path.join(path, file)
                logger.info(f"Uploading screenshots ({i}/{total})")
                gui.print_topic_name.set(f"Uploading screenshots ({i}/{total})")
                try:
                    image = client.upload(file=str(img_path), name=str(file_name))
                except (imgbbpy.imgerrors.ImgbbError) as error:
                    gui.print_topic_name.set(error)
                    self.alert('Error', error, kind='error')
                    sys.exit()
                except requests.exceptions.TooManyRedirects:
                    logger.error('Error: Exceeded 30 redirects.')
                    gui.print_topic_name.set('Error: Exceeded 30 redirects.')
                    self.alert('Error', 'Error: Exceeded 30 redirects.', kind='error')
                    sys.exit()
                else:
                    logger.success(f"Uploaded {total} screenshots")
                    screenshots_links.append('[img]' + image.url + '[/img]')
            logger.info(screenshots_links)
            return screenshots_links

    def alert(self, title, message, kind='info', hidemain=True):
        if kind not in ('error', 'warning', 'info'):
            raise ValueError('Unsupported alert kind.')
        show_method = getattr(messagebox, f'show{kind}')
        show_method(title, message)

    def link_handling(self):
        """
        The link_handling function is responsible for handling the link that was entered by the user.
        """
        self.link = gui.entry_download_link.get()
        link_not_base64 = self.link
        logger.info(self.link)
        if gui.base64_var.get() is True:
            number = gui.entry_number_base64.get()
            if number:
                if number.isdigit():
                    number = int(number)
                else:
                    number = 1
                    gui.entry_number_base64.delete(0, tk.END)
                    gui.entry_number_base64.insert(0, number)
            else:
                number = 1
                gui.entry_number_base64.delete(0, tk.END)
                gui.entry_number_base64.insert(0, number)
            for i in range(number):
                self.link = self.base64_link(self.link)
            logger.info(f'Link was encoded {number} time(s) in base64: {self.link}')
        if re.match(r'https://mega.nz/', link_not_base64):
            self.link_provider = "MEGA"
        elif re.match(r'http.*zippyshare.*\.html', link_not_base64):
            self.link_provider = "Zippy"
        elif re.match(r'https://drive.google.com/', link_not_base64):
            self.link_provider = "GDRIVE"
        elif re.match(r'https://www.mediafire.com/', link_not_base64):
            self.link_provider = "MFIRE"
        else:
            self.link_provider = "LINK"
        logger.info(f'Link provider: {self.link_provider}')

    def base64_link(self, link: str):
        """
        The base64_link function takes a link as an argument and returns the base64 encoded version of that link.\n
        Args:
            link: str: Pass the link to be encoded\n
        Returns:
            A base64 encoded string
        """
        link_encoded = base64.b64encode(bytes(link, 'utf8'))
        link_encoded = link_encoded.decode('utf8')
        return link_encoded

    def template_maker(self):
        """
        The template_maker function is the main function of this class.
        It handles all the other functions and variables to create a template based on the template.txt file.
        """
        self.link_handling()
        source = gui.combo_source.get()
        name = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", self.name)
        self.data.update({
            'link': self.link,
            'link_provider': self.link_provider,
            'source': source,
            'mediainfo': self.mediainfo
            })
        if gui.screenshoots_var.get() is True:
            screenshots_links = self.imgbb_screenshot()
            self.data.update({'screenshots': ("".join(screenshots_links) +'\n')})
        imdb_template_res = Templates().complete_template(self.data)
        with open(f"{name}.txt", 'w', encoding="utf8") as file:
            file.write(imdb_template_res)
        try:
            root.geometry("700x260")
            topic_name = f"[{self.link_provider}] {self.filename_no_extension} [{self.size}]"
            gui.print_topic_name.set(topic_name)
            gui.print_topic.set(f'{name}.txt')
            button_clipboard = ttk.Button(root, text='Copy',
                                          command=lambda: pyperclip.copy(topic_name))
            button_clipboard.place(x=615.0, y=165.0, width=65.0, height=35.0)
            button_clipboard = ttk.Button(root, text='Copy',
                                          command=lambda: pyperclip.copy(open(f'{name}.txt',
                                          encoding='utf8').read()))
            button_clipboard.place(x=615.0, y=210.0, width=65.0, height=35.0)
            gui.update()
        except ValueError:
            logger.exception('An error occured.')
            self.alert('Error', 'An error occured.', kind='error')

    def on_closing(self):
        logger.info('Closing TopicMaker...')
        root.destroy()
        sys.exit()

    def main(self):
        self.omdb_handling()
        if self.media_info():
            self.template_maker()

if __name__ == '__main__':
    config = Config()
    config.read_config_file()
    root = tk.Tk()
    root.title(f'Topic Maker {VERSION}')
    root.geometry("700x155")
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
    root.iconbitmap(default=os.path.join(application_path, 'favicon.ico'))
    Application(root).pack()
    gui = Application(root)
    root.protocol("WM_DELETE_WINDOW", Functions().on_closing)
    sv_ttk.set_theme("dark")
    root.resizable(False, False)
    root.mainloop()
