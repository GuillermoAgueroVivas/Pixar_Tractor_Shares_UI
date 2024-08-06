#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
- This is the Changes Applied window of the Farm UI. Shows message saying
the changes made have been applied and asks if you would like to do more changes.
- Created using PyQt5
- Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
import os
import subprocess
from urllib.request import urlopen

# import urllib2
import sys

from collections import OrderedDict
from time import sleep
from datetime import datetime, date
from qtpy import QtWidgets, QtGui


class UiChangesAppliedMainWindow(QtWidgets.QMainWindow):
    """This class represents the main window for displaying changes applied to the Farm UI.

    It initializes the user interface components and sets up various sections of the
    window to show the details of the applied changes. The window allows users to
    write changes to the configuration file, make further changes, or exit the application.

    Methods:
        __init__(): Initializes the UiChangesAppliedWindow instance with the
        specified parameters.
        setup_ui(self): Sets up the user interface components by calling various
        helper methods.
        changes_applied_window_setup(self): Configures the properties of the
        changes applied window, such as size,style sheet, and title.
        groupbox_creation(self): Creates a group box widget to hold all the UI
        elements related to the changes applied window.
        label_creation(self): Creates a QLabel object inside the main group box
        to display the question prompt.
        button_creation(self): Creates and sets up the 'Write', 'More Changes',
        and 'Exit' buttons, with corresponding functionalities for each button.
        more_changes_button_clicked(self): Handles the click event of the 'More
        Changes' button and navigates back to the first window for making further
        changes to the current TMP file.
    """

    def __init__(
        self,
        config_file_path_name,
        contents_dict,
        tmp_file_name,
        backup_folder,
        new_values_dict,
        farm_name,
        fonts,
    ):
        """Initializes the UiChangesAppliedWindow instance.

        This constructor sets up the window for displaying changes applied to
        the Farm UI, initializing all necessary attributes to show the details
        of the applied changes. It prepares the UI elements and ensures the window
        is ready to be displayed.

        Parameters:
            config_file_path_name (str): Path to the main configuration file.
            contents_dict (dict): Dictionary containing the configuration file contents.
            tmp_file_name (str): Name of the temporary file used during the update process.
            backup_folder (str): Path to the backup folder.
            new_values_dict (dict): Dictionary of new values to be applied.
            farm_name (str): The name of the farm section.
            fonts (list): List containing large and small QFont objects for UI elements.

        Config Data:
            contents_dict (dict): Dictionary containing the configuration file contents.

        UI Components:
            centralwidget (QWidget): Central widget for the changes applied window.
            changes_applied_groupbox (QGroupBox): Group box containing UI elements
            showing applied changes.

        Fonts:
            l_font (QFont): Large font for UI elements.
            s_font (QFont): Small font for UI elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Incoming Variables
        self.config_file_path_name = config_file_path_name
        self.contents_dict = contents_dict
        self.tmp_file_name = tmp_file_name
        self.backup_folder = backup_folder
        self.new_values_dict = new_values_dict
        self.farm_name = farm_name
        self.l_font = fonts[0]
        self.s_font = fonts[1]

        # Sections of the window
        self.centralwidget = ""
        self.changes_applied_groupbox = None

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components.

        This method calls various other methods to build and initialize all parts
        of the UI, including getting all shows, setting up the main window,
        and creating various UI elements like group boxes labels, and buttons.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.changes_applied_window_setup()
        self.groupbox_creation()
        self.label_creation()
        self.button_creation()

    def changes_applied_window_setup(self):
        """Sets up the changes applied window with the specified properties.
         It sets the window size, style sheet, and window title.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Write File Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 161)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):

            # New method to replace the deprecated centering method

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates a Group Box widget within the main window to hold all the UI
        elements related to the Changes Applied Window.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # Title of the Group Box
        self.changes_applied_groupbox = QtWidgets.QGroupBox(
            "Write to File Or Make More Changes", self.centralwidget
        )
        self.changes_applied_groupbox.setGeometry(10, 10, 441, 141)
        self.changes_applied_groupbox.setFont(self.l_font)

    def label_creation(self):
        """Creates a QLabel object inside the main group box.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        question_label = QtWidgets.QLabel(
            "Would you like to write to Config File or make more changes?",
            self.changes_applied_groupbox,
        )
        question_label.setGeometry(10, 35, 271, 61)
        question_label.setFont(self.s_font)
        question_label.setWordWrap(True)

    def button_creation(self):
        """Creates and sets up the Write, More Changes and Exit buttons. Using the
        'Write' button will write the changes made to the main configuration being
        used by Tractor while creating a backup. The 'More Changes' button will
        allow the user to go back to the beginning whick will use a temporary config
        file to allow the user to adjust more values before writing. The 'exit'
        button will exit the application and delete the TMP file being used.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # Text can be changed here
        more_changes_button = QtWidgets.QPushButton(
            "More Changes", self.changes_applied_groupbox
        )
        more_changes_button.setGeometry(160, 110, 121, 22)
        more_changes_button.setFont(self.s_font)
        more_changes_button.setStyleSheet("color : yellow")
        more_changes_button.clicked.connect(self.more_changes_button_clicked)
        more_changes_button.clicked.connect(self.close)

        # Text can be changed here
        exit_button = QtWidgets.QPushButton(
            "Discard/Exit", self.changes_applied_groupbox
        )
        exit_button.setGeometry(310, 110, 121, 22)
        exit_button.setFont(self.s_font)
        exit_button.setStyleSheet("color : #D21404")

        def delete_tmp():
            os.remove(self.tmp_file_name)

        exit_button.clicked.connect(delete_tmp)
        exit_button.clicked.connect(self.close)

        # Text can be changed here
        write_button = QtWidgets.QPushButton("Write", self.changes_applied_groupbox)
        write_button.setGeometry(10, 110, 121, 22)
        write_button.setFont(self.s_font)
        write_button.setStyleSheet("color : #A7F432")

        # backup_folder, new_values_dict, farm_name, self.changes_applied_groupbox
        def write_to_config():
            """Writes contents to the config file and performs config file
            reload.

            Parameters:
                None

            Returns:
                None
            """

            print("The write_to_config() method has started")

            # Creates the Backup file for the config file and then deletes
            # the temporary one used while the tool is running
            if os.path.exists(self.config_file_path_name):
                backup_file_name = (
                    f"{self.backup_folder}D{date.today()}"
                    f"-T{datetime.now().strftime('%H:%M:%S')}.config"
                )

                final_backup_file = backup_file_name.replace(":", "")
                os.rename(self.config_file_path_name, final_backup_file)

            if os.path.exists(self.tmp_file_name):
                with open(self.tmp_file_name, mode="r") as tmp_file:
                    tmp_data = json.load(tmp_file, object_pairs_hook=OrderedDict)
                json.dump(
                    tmp_data, open(self.config_file_path_name, mode="w"), indent=4
                )
                sleep(5)
                os.remove(self.tmp_file_name)
            else:
                json.dump(
                    self.contents_dict,
                    open(self.config_file_path_name, mode="w"),
                    indent=4,
                )
                sleep(5)

            return_code = subprocess.call(["tq", "reloadconfig", "--limits"])
            if return_code != 0:
                print("Command failed with error code: ", return_code)
                print("Tryin again with os.system()")
                os.system("tq reloadconfig --limits")  # , shell=True
                sleep(10)
            else:
                print("Command executed successfully")

            # Loading website containing the updated '.config' file info
            web_info = urlopen("http://tractor-engine/Tractor/queue?q=limits")
            sleep(5)
            web_info_dict = json.load(web_info)
            print("Config-file website has just been fully loaded!")

            # Iterates through the 'New Values Directory' sent from the
            # previous window and compares every value to those in the
            # 'Tractor Limits' website.
            index = 1
            for show, percentage in self.new_values_dict.items():

                full_number = float(percentage)
                web_value = (
                    float(
                        web_info_dict["Limits"][self.farm_name]["Shares"][show][
                            "nominal"
                        ]
                    )
                    * 100
                )

                web_value = round(web_value, 1)
                print(f"Show: {show}")
                print("Full Number | Web Value")
                print(full_number, web_value)

                while web_value != full_number:

                    web_info = urlopen("http://tractor-engine/Tractor/queue?q=limits")

                    web_info_dict = json.load(web_info)
                    web_value = (
                        float(
                            web_info_dict["Limits"][self.farm_name]["Shares"][show][
                                "nominal"
                            ]
                        )
                        * 100
                    )

                    web_value = round(web_value, 1)
                    print(f"Show: {show}")
                    print("Full Number | Web Value")
                    print(full_number, web_value)

                    index += 1

                    if 1 < index <= 7:

                        return_code = subprocess.call(
                            ["tq", "reloadconfig", "--limits"]
                        )

                        print(f"Amount of config-reloads: {index}")

                        sleep(10)
                        if return_code != 0:
                            print("Command failed with error code: ", return_code)
                            print("Trying again with os.system()")
                            os.system("tq reloadconfig --limits")  # , shell=True
                            sleep(10)
                        else:
                            print("Command executed successfully")

                    elif index == 8:
                        print(
                            "The Config was reloaded too many times before "
                            "this change could be properly applied. "
                            "Attempt to reload manually."
                        )
                        sys.exit()

        write_button.clicked.connect(write_to_config)
        write_button.clicked.connect(self.close)

    def more_changes_button_clicked(self):
        """Handles the click event of the 'More Changes' button and goes back
        to the first window so the user can make more changes to the current
        TMP file.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        from main_farm_selection_window import UiAllocationsMainWindow

        farm_selection_window = UiAllocationsMainWindow()
        farm_selection_window.show()
