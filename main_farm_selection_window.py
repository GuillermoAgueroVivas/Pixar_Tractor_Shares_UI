#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
This window is the Initial Window of the UI for Show Allocations.
Created using QtPy
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import sys
import json
import re
from collections import OrderedDict
from qtpy import QtWidgets, QtGui

# These are all the other windows being imported


class UiAllocationsMainWindow(QtWidgets.QMainWindow):
    """Main window class for the Farm UI for Show Allocations.

    This class creates the main window of the Farm UI application using QtPy.
    It handles the setup and display of UI components for farm selection and
    configuration.

     Methods:
        __init__(): Initializes the main window, loads configuration data, and
        sets up UI components.
        setup_ui(): Sets up the user interface components.
        generate_farm_sections(): Generates and sorts a list of farm sections.
        farm_selection_window_setup(): Sets up the main window for farm selection.
        groupbox_creation(): Creates a group box for farm selection.
        combo_box_creation(): Creates a combo box for farm selection.
        label_creation(): Creates a label for instructions.
        button_creation(): Creates a button for confirming farm selection.
        open_windows_farm_window(farm_name): Opens the Windows Farm window based on selection.
        open_linux_farm_window(farm_name, linux_farm_sections): Opens the Linux
        Farm window based on selection.
    """

    def __init__(self):
        """Initializes the main window for the Linux Farm application.

        This method sets up various configuration paths, initializes UI components,
        and loads the configuration data from a specified file.

        Attributes:
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder where temp files are created.
            backup_folder (str): Path to the backup folder where backup files are stored.

        UI Components:
            centralwidget (QWidget): Central widget of the main window.
            farm_select_groupbox (QGroupBox): Group box for farm selection.
            farm_select_push_button (QPushButton): Push button for confirming farm selection.
            farm_select_combo_box (QComboBox): Combo box for selecting a farm.

        Variables:
            farm_sections (list): List to hold the sections of the farm.

        Config Data:
            contents_dict (OrderedDict): Dictionary containing the configuration data
            loaded from the configuration file.

        Fonts:
            l_font (QFont): Large font for UI elements.
            s_font (QFont): Small font for UI elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # These are the location of both the main Config file and where the temp
        # file and backup files will be created

        self.config_file_path_name = "/sw/tractor/config/limits.config"
        self.temp_folder = "/sw/tractor/config/tmp/"
        self.backup_folder = "/sw/tractor/config/limits_backup/"

        # Sections of the window
        self.centralwidget = None
        self.farm_select_groupbox = None
        self.farm_select_push_button = None
        self.farm_select_combo_box = None

        # Variables
        self.farm_sections = []

        # Opening config file
        with open(self.config_file_path_name, "r") as i:
            self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # Windows

        # Fonts
        self.l_font = QtGui.QFont(
            "Cantarell", 14, QtGui.QFont.Bold, QtGui.QFont.StyleItalic
        )
        self.l_font.setUnderline(True)
        self.s_font = QtGui.QFont("Cantarell", 11)
        self.s_font.setWeight(QtGui.QFont.Thin)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components.

        This method calls various other methods to build and initialize all parts
        of the UI, including generating farm sections, setting up the main window,
        and creating various UI elements like group boxes, combo boxes, labels, and buttons.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Building all parts of the UI
        self.generate_farm_sections()
        self.farm_selection_window_setup()
        self.groupbox_creation()
        self.combo_box_creation()
        self.label_creation()
        self.button_creation()

    def generate_farm_sections(self):
        """Generates and sorts a list of farm sections.

        This method creates a list of all the farm sections from the configuration data,
        filters them based on specified criteria, and sorts them in natural order.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        # This generates a list of all farm sections
        include = ["linuxfarm", "_windowsfarm"]
        for farm_section in self.contents_dict["Limits"].keys():
            for word in include:
                if word in farm_section:
                    self.farm_sections.append(farm_section)  # IMPORTANT

        def check_if_digit(number):
            return int(number) if number.isdigit() else number

        def natural_keys(fs):  # Farm Sections
            return [check_if_digit(number) for number in re.split(r"(\d+)", fs)]

        # Using this to be able to properly sort the farm sections in the correct
        # order.
        self.farm_sections.sort(key=natural_keys)

    def farm_selection_window_setup(self):
        """This function sets up the farm selection window, including the size,
        style, and title of the window, as well as centering it on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Main Farm Selection Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # This function centers the Window in the screen according to what
        # monitor the mouse is hovering over
        def center_window(window):
            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """This method initializes and configures the combo box used for selecting
        a farm section, and populates it with farm sections.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        # Title of the Group Box
        self.farm_select_groupbox = QtWidgets.QGroupBox(
            "Farm Selection", self.centralwidget
        )
        self.farm_select_groupbox.setGeometry(10, 10, 441, 161)
        self.farm_select_groupbox.setFont(self.l_font)

    def combo_box_creation(self):
        """This method initializes and configures the combo box used for
        selecting a farm section, and populates it with farm sections.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        self.farm_select_combo_box = QtWidgets.QComboBox(self.farm_select_groupbox)
        self.farm_select_combo_box.setGeometry(10, 120, 201, 22)
        self.farm_select_combo_box.setFont(self.s_font)
        self.farm_select_combo_box.setStyleSheet("color : #A7F432")

        # Creating all the slots to be allocated in the Combo Box as well as
        # adding the titles
        index = 0
        for farm_section in self.farm_sections:
            if "linux" in farm_section:
                capital_name = farm_section.capitalize()
                self.farm_select_combo_box.addItem(capital_name)
                index += 1
            else:
                capital_name = farm_section.split("_")[1].capitalize()
                # capital_name = capital_name[1].capitalize()
                # self.farm_select_combo_box.setItemText(index, capital_name)
                self.farm_select_combo_box.addItem(capital_name)
                index += 1

    def label_creation(self):
        """Creates a label with specified properties and text.

        This method initializes and configures the label used to provide instructions
        to the user regarding farm selection.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Text inside the label can be changed here
        farm_select_label = QtWidgets.QLabel(
            "Utilizing the dropdown menu below, please select the "
            "portion of the Farm you would like to configure and then "
            "confirm your choice:",
            self.farm_select_groupbox,
        )
        farm_select_label.setGeometry(10, 40, 421, 61)
        farm_select_label.setFont(self.s_font)
        farm_select_label.setWordWrap(True)

    def button_creation(self):
        """Creates and set up the button for confirming the farm selection.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Text inside the button can be changed here
        self.farm_select_push_button = QtWidgets.QPushButton(
            "Confirm My Selection", self.farm_select_groupbox
        )
        self.farm_select_push_button.setGeometry(250, 120, 171, 22)
        self.farm_select_push_button.setFont(self.s_font)

        # IMPORTANT: This is what happens when the button is pressed to confirm selection
        # Opening the other windows according to the selection of the Combo Box
        def farm_select_button_clicked():  # Combo Box
            current = self.farm_select_combo_box.currentText()
            if "linux" in current.lower():

                linux_farm_sections = []

                for section in self.farm_sections:
                    # Doing only linux since we want the option to 'apply all the
                    # same values across the board' just for the Linux Farm.
                    if "windows" not in section:
                        linux_farm_sections.append(section)

                self.open_linux_farm_window(current.lower(), linux_farm_sections)

            elif "windows" in current.lower():
                self.open_windows_farm_window(f"_{current.lower()}")

        self.farm_select_push_button.clicked.connect(farm_select_button_clicked)
        self.farm_select_push_button.clicked.connect(self.close)

    def open_windows_farm_window(self, farm_name):
        """This function creates a new window for the Windows farm and sets up
        its UI.

        Parameters:
            self (object): The object instance.

        Returns:
            None (Creates a new window)
        """

        from windowsfarm_window import UiWindowsFarmMainWindow

        windows_farm = UiWindowsFarmMainWindow(
            farm_name,
            self.config_file_path_name,
            self.temp_folder,
            self.backup_folder,
            [self.l_font, self.s_font],
        )

        windows_farm.show()
        self.close()

    def open_linux_farm_window(
        self,
        farm_name,
        linux_farm_sections,
    ):
        """Creates and displays a new window for the Linux farm with the specified
        farm name and sections, and sets up its user interface.

        Parameters:
            self (object): The object instance.
            farm_name (str): Name of the Linux farm to be managed.
            linux_farm_sections (dict): Dictionary containing the sections
            of the Linux farm.

        Returns:
            None
        """
        from linuxfarm_window import UiLinuxFarmMainWindow

        linux_farm = UiLinuxFarmMainWindow(
            farm_name,
            linux_farm_sections,
            self.config_file_path_name,
            self.temp_folder,
            self.backup_folder,
            [self.l_font, self.s_font],
        )

        linux_farm.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    farm_selection_window = UiAllocationsMainWindow()
    farm_selection_window.show()
    sys.exit(app.exec_())
