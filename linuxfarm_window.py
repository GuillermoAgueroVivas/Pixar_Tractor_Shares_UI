#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
- This window opens up when selected through the 'Farm_Selection_Window' of
the Atomic Farm UI.
Represents the Linux Farm section selected in the previous window.
- Created using QyPy.
- Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
import os
import re
from collections import OrderedDict
from functools import partial
from qtpy import QtWidgets, QtCore, QtGui
from changes_confirmation_window import UiConfirmFarmChangesMainWindow


class UiLinuxFarmMainWindow(QtWidgets.QMainWindow):
    """Main window class for the Linux Farm UI in the Atomic Farm application.

    This window is opened through the 'Farm_Selection_Window' of the Atomic Farm UI
    and represents the Linux Farm section selected in the previous window.
    It is created using QyPy and provides an interface to adjust the allocation
    percentages for different shows on the Linux Farm.

    Parameters:
        farm_name (str): The name of the farm section.
        linux_farm_sections (list): List of sections within the Linux farm.
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder for storing temp files.
        backup_folder (str): Path to the backup folder.
        fonts (list): List containing large and small QFont objects for UI elements.

    Methods:
        __init__(): Initializes the window, loads previus variables, and
        sets up UI components. Checks to see if there is temporary file to be used,
        otherwise the main configuration file is opened.
        setup_ui(): Sets up the user interface components.
        get_shows(): Generates a list of show names that the farm has access to.
        linux_farm_window_setup(): Sets up the main window properties.
        groupbox_creation(): Creates the main Group Box for the UI elements.
        groupbox_info_creation(): Creates and configures UI components within
        the Group Box.
        current_values_show(show, slider, spin_box, hardcap_spin_box): Updates
        current percentage values.
        info_label_creation(): Creates and sets text for various labels in the window.
        button_creation(): Creates and sets up the Submit and Cancel buttons.
        cancel_button_clicked(): Handles the Cancel button click event.
    """

    def __init__(
        self,
        farm_name,
        linux_farm_sections,
        config_file_path_name,
        temp_folder,
        backup_folder,
        fonts,
    ):
        """
        Initializes the UiLinuxFarmMainWindow instance.

        This constructor sets up the main window for the Linux Farm UI, initializing
        all necessary attributes and loading the configuration file. It prepares
        the UI elements and ensures that the window is ready to be displayed.

        Parameters:
            self (object): The object instance.
            farm_name (str): The name of the farm section.
            linux_farm_sections (list): List of sections within the Linux farm.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder for storing temp files.
            backup_folder (str): Path to the backup folder.
            fonts (list): List containing large and small QFont objects for UI elements.

        Attributes:
            shows (list): List of show names available on the farm.
            y_axis_window_size (int): Initial window height.
            cleaned_farm_name (str): Cleaned and formatted farm name for display.
            current_perc_list (list): List of current percentage values for shows.
            spinboxes_list (list): List of spin box widgets for nominal percentages.
            sliders_list (list): List of slider widgets for nominal percentages.
            spinboxes_hardcap_list (list): List of spin box widgets for hard cap
            percentages.
            current_values_full_dict (dict): Dictionary of current percentage
            values for shows.
            current_values_cap_full_dict (dict): Dictionary of current hard cap
            percentage values for shows.

        Config Data:
            contents_dict (dict): Dictionary containing the configuration file contents.

        UI Components:
            centralwidget (QWidget): Central widget for the main window.
            linux_farm_groupbox (QGroupBox): Group box containing UI elements.


        Fonts:
            s_font (QFont): Small font for UI elements.
            m_font (QFont): Medium font with underline for specific UI elements.
            l_font (QFont): Large font for UI elements.

        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Incoming Variables
        self.farm_name = farm_name
        self.linux_farm_sections = linux_farm_sections
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder
        self.l_font = fonts[0]
        self.s_font = fonts[1]
        self.fonts = fonts

        # Sections of the window
        self.centralwidget = ""
        self.shows = []
        self.y_axis_window_size = None
        self.cleaned_farm_name = None
        self.linux_farm_groupbox = None
        self.current_perc_list = []
        self.spinboxes_list = []
        self.sliders_list = []
        self.spinboxes_hardcap_list = []
        self.current_values_full_dict = dict()  # This is the value to use
        self.current_values_cap_full_dict = dict()

        # Opening config file
        if os.path.exists(self.temp_folder + "temp.config"):
            with open(self.temp_folder + "temp.config", "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file if temp file does not exist.
            with open(config_file_path_name, "r") as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        self.m_font = QtGui.QFont("Cantarell", 12, QtGui.QFont.Bold)
        self.m_font.setUnderline(True)

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components.

        This method calls various other methods to build and initialize all parts
        of the UI, including getting all shows, setting up the main window,
        and creating various UI elements like group boxes labels, and buttons.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        self.get_shows()
        self.linux_farm_window_setup()
        self.groupbox_creation()
        self.groupbox_info_creation()
        self.info_label_creation()
        self.button_creation()

    def get_shows(self):
        """Generates a list of show names that the farm has access to.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # This generates a list of all shows for this farm
        for key in self.contents_dict["Limits"][self.farm_name]["Shares"].keys():

            if len(key) == 3 and key != "RND":
                self.shows.append(key)

    def linux_farm_window_setup(self):
        """This function sets up the Linux Farm window, including the size,
        style, and title of the window, as well as centering it on the screen.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Linux Farm Window")
        self.y_axis_window_size = 390  # Initial window height 390
        # Window Size can be adjusted here
        self.setFixedSize(740, self.y_axis_window_size)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):
            """Centers the main window of the WindowsFarmUI_MainWindow object to
            the center of the screen.

            Parameters:
                WindowsFarmUI_MainWindow (object): The main window of the
                WindowsFarmUI.

            Returns:
                None.
            """

            frame = window.frameGeometry()
            screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())

            if screen is None:
                screen = QtGui.QGuiApplication.primaryScreen()

            frame.moveCenter(screen.geometry().center())
            window.move(frame.topLeft())

        center_window(self)

    def groupbox_creation(self):
        """Creates a Group Box widget within the main window to hold all the UI
        elements related to the Linux Farm.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        def cleaning_up_name(farm_name):
            """Static method that cleans up a farm name by capitalizing the
            first letter of each word and removing underscores, and adding a
            space between the word "farm" and any number that follows it.

            Parameters:
                farm_name (str): The name of the farm to be cleaned up.

            Returns:
                new_name (str): The cleaned up name of the farm.
            """

            new_name = re.split("(farm)", farm_name)
            if new_name[2]:
                number = new_name[2]
                number = number.replace("_", "")
                new_name = (
                    new_name[0].capitalize()
                    + " "
                    + new_name[1].capitalize()
                    + " "
                    + number
                )
            else:
                new_name = new_name[0].capitalize() + " " + new_name[1].capitalize()
            return new_name

        self.cleaned_farm_name = cleaning_up_name(self.farm_name)

        # Title of the Group Box
        self.linux_farm_groupbox = QtWidgets.QGroupBox(
            self.cleaned_farm_name, self.centralwidget
        )
        self.linux_farm_groupbox.setGeometry(10, 10, 721, 348)  # 348
        self.linux_farm_groupbox.setFont(self.l_font)

    def groupbox_info_creation(self):
        """Creates and configures UI components (labels, spin boxes, and sliders)
        within a group box for displaying and modifying show allocations.

        This function iterates through the list of shows and dynamically creates
        labels, spin boxes, and sliders for each show. It then connects the spin
        boxes and sliders to synchronize their values and calculates the total
        percentage of allocations. If the UI components exceed the initial window
        size, the window and group box sizes are adjusted accordingly.

        Parameters:
            self (object): instance of a class.

        Internal Functions:
            label_creation(show, y_axis_value): Creates a label for a show.
            spin_box_creation(y_axis_value): Creates spin boxes for show allocations
            and hard cap values.
            sliders_creation(y_axis_value): Creates a horizontal slider for a show.
            connect_parts(spin_box, slider): Connects a spin box and a slider to
            update each other's values.
            current_percent_spin_box_creation(): Creates a spin box to display the
            total current percentage of allocations.
        """

        y_axis_value = 70

        def label_creation(show, y_axis_value):
            """Creates a QLabel object with the provided show title and sets its
            properties.

            Parameters:
                show (str): The title of the show.
                y_axis_value (int): The y-axis value where the label will
                be created.

            Returns:
                None
            """

            # Tests

            label = QtWidgets.QLabel(show, self.linux_farm_groupbox)
            label.setGeometry(270, y_axis_value, 35, 20)
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)

        def spin_box_creation(y_axis_value):
            """Creates two QDoubleSpinBoxes for a show and its hard cap value

            Parameters:
                show (str): name of the show
                y_axis_value (int): y-axis value for positioning
                the spin boxes

            Returns:
                spin_box (QDoubleSpinBox): QDoubleSpinBox for the
                show
                hardCapSpinBox (QDoubleSpinBox): QDoubleSpinBox
                for the hard cap value of the show
            """
            minimum = 0
            maximum = 100

            spin_box = QtWidgets.QDoubleSpinBox(self.linux_farm_groupbox)
            spin_box.setGeometry(570, y_axis_value, 57, 22)
            spin_box.setFont(self.s_font)
            spin_box.setDecimals(1)
            spin_box.setMinimum(minimum)
            spin_box.setMaximum(maximum)

            hardcap_spin_box = QtWidgets.QDoubleSpinBox(self.linux_farm_groupbox)
            hardcap_spin_box.setGeometry(640, y_axis_value, 60, 22)
            hardcap_spin_box.setFont(self.s_font)
            hardcap_spin_box.setDecimals(1)
            hardcap_spin_box.setMinimum(minimum)
            hardcap_spin_box.setMaximum(maximum)

            return spin_box, hardcap_spin_box

        def sliders_creation(y_axis_value):
            """Creates a horizontal slider widget and sets its properties.

            Parameters:
                show (str): A string representing the name of the
                slider.
                y_axis_value (int): An integer representing the
                y-axis value of the slider.

            Returns:
                slider (QSlider): A horizontal slider widget with
                a specified range and name.
            """

            # Minimum and Maximum for all sliders
            minimum = 0
            maximum = 100
            # Setting up
            slider = QtWidgets.QSlider(self.linux_farm_groupbox)
            slider.setGeometry(310, y_axis_value, 251, 20)  # Location in window
            slider.setTracking(True)
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
            slider.setMinimum(minimum)
            slider.setMaximum(maximum)

            return slider

        def connect_parts(spin_box, slider):
            """Connects a Spin Box and Slider to update each other's values.

            Parameters:
                spin_box (QSpinBox): the spin box to be connected to the slider.
                slider (QSlider): the slider to be connected to the spin box.

            Returns:
                None
            """

            def _update_slider(slide, value):
                slide.setValue(value)

            def _update_box(box, value):
                box.setValue(value)

            spin_box.valueChanged.connect(partial(_update_slider, slider))
            slider.valueChanged.connect(partial(_update_box, spin_box))

        for show in self.shows:
            label_creation(show, y_axis_value)
            spin_box, hardcap_spin_box = spin_box_creation(y_axis_value)
            slider = sliders_creation(y_axis_value)
            # Connecting all sliders to their Spin Boxes and vice versa
            connect_parts(spin_box, slider)
            # Getting current Percentages per show to be able to pass it to the
            # Confirmation Window
            self.current_values_show(
                show,
                slider,
                spin_box,
                hardcap_spin_box,
            )

            self.sliders_list.append(slider)
            self.spinboxes_list.append(spin_box)
            self.spinboxes_hardcap_list.append(hardcap_spin_box)
            y_axis_value = y_axis_value + 40

        total_current_percent = sum(self.current_perc_list)

        def current_percent_spin_box_creation():
            """Creates a spinbox to be able to show the current total of all
            sliders/spin boxes added together

            Returns:
                None
            """
            total_spin_box = QtWidgets.QDoubleSpinBox(self.linux_farm_groupbox)
            total_spin_box.setGeometry(190, 250, 50, 22)
            total_spin_box.setFont(self.s_font)
            total_spin_box.setDecimals(0)
            total_spin_box.setValue(total_current_percent)
            total_spin_box.setDisabled(True)
            total_spin_box.setButtonSymbols(
                QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons
            )
            total_spin_box.setMaximum(2000)
            total_spin_box.setStyleSheet("color: green")

            def update_total():
                total_value = sum(box.value() for box in self.spinboxes_list)
                total_spin_box.setValue(total_value)

                if total_value > 100 or total_value < 100:
                    total_spin_box.setStyleSheet("color: red")
                else:
                    total_spin_box.setStyleSheet("color: green")

            for box, slide in zip(self.spinboxes_list, self.sliders_list):
                box.valueChanged.connect(update_total)
                slide.valueChanged.connect(update_total)

        current_percent_spin_box_creation()

        # If the size of the y-axis being used to create all the sliders,
        # labels and boxes is greater than the window size minus 50 then it
        # increases the size of both the Window and
        # the groupbox.

        if y_axis_value > (self.y_axis_window_size - 50):
            while y_axis_value > (self.y_axis_window_size - 50):
                self.y_axis_window_size = self.y_axis_window_size + 35  # 90
                self.setFixedSize(740, self.y_axis_window_size)

            self.y_axis_window_size = self.y_axis_window_size - 20
            self.linux_farm_groupbox.setGeometry(10, 10, 721, self.y_axis_window_size)

    def current_values_show(
        self,
        show,
        slider,
        spin_box,
        hardcap_spin_box,
    ):
        """Function to update the current percentage values for the nominal and
        hard cap for a given show.

        Parameters:
            self (object): instance of a class.
            show (str): The show name.
            slider (QSlider): The slider for the nominal percentage.
            spin_box (QSpinBox): The spin box for the nominal percentage.
            hardcap_spin_box (QSpinBox): The spin box for the hard cap
            percentage.

        Returns:
            None
        """

        # Nominal
        current_value = self.contents_dict["Limits"][self.farm_name]["Shares"][show][
            "nominal"
        ]
        current_perc = round(current_value * 100, 1)
        slider.setValue(current_perc)
        spin_box.setValue(current_perc)
        self.current_values_full_dict.update({show: current_perc})

        self.current_perc_list.append(current_perc)

        # Hard Cap
        current_cap_value = self.contents_dict["Limits"][self.farm_name]["Shares"][
            show
        ]["cap"]
        current_cap_perc = round(current_cap_value * 100, 1)
        hardcap_spin_box.setValue(current_cap_perc)
        self.current_values_cap_full_dict.update({show: current_cap_perc})

    def info_label_creation(self):
        """Creates and sets text for various labels in the window.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # Main Definition label
        if self.farm_name == "linuxfarm":
            linux_def_label = QtWidgets.QLabel(
                "To the right side you will see a list of all current "
                "working shows in the Linux Farm as a whole.",
                self.linux_farm_groupbox,
            )
        else:
            linux_def_label = QtWidgets.QLabel(
                f"To the right side you will see a list of all current "
                f"working shows in the {self.cleaned_farm_name} section.",
                self.linux_farm_groupbox,
            )

        linux_def_label.setGeometry(10, 50, 191, 71)
        linux_def_label.setFont(self.s_font)
        linux_def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        linux_def_label.setScaledContents(False)
        linux_def_label.setWordWrap(True)

        # Second Definition Label
        linux_def_sliders_label = QtWidgets.QLabel(
            "Utilizing the available sliders, please select "
            "how much allocation each show should be receiving: ",
            self.linux_farm_groupbox,
        )
        linux_def_sliders_label.setGeometry(10, 140, 201, 81)
        linux_def_sliders_label.setFont(self.s_font)
        linux_def_sliders_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        linux_def_sliders_label.setScaledContents(False)
        linux_def_sliders_label.setWordWrap(True)

        # Label for the Counter Updating with the boxes/sliders.
        counter_label = QtWidgets.QLabel(
            "Total Current Percentage: ",
            self.linux_farm_groupbox,
        )
        counter_label.setGeometry(
            10,
            250,
            175,
            20,
        )
        counter_label.setFont(self.s_font)
        counter_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        counter_label.setScaledContents(False)
        counter_label.setWordWrap(True)

        # Nominal and Hard Cap labels
        nominal_label = QtWidgets.QLabel("Nominal", self.linux_farm_groupbox)
        nominal_label.setGeometry(410, 40, 61, 20)
        nominal_label.setFont(self.m_font)
        nominal_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        nominal_label.setScaledContents(False)
        nominal_label.setWordWrap(True)
        nominal_label.setStyleSheet("color: yellow")

        cap_label = QtWidgets.QLabel("Hard Cap", self.linux_farm_groupbox)
        cap_label.setGeometry(636, 40, 71, 20)
        cap_label.setFont(self.m_font)
        cap_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        cap_label.setScaledContents(False)
        cap_label.setWordWrap(True)
        cap_label.setStyleSheet("color: yellow")

    def button_creation(self):
        """Creates and sets up the Submit and Cancel buttons. The Submit button
        does a check to see if the values add up to 100 and creates new
        dictionaries with the new values. The Cancel button returns the user
        to the previous window.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        # Name of the button can be changed here
        submit_button = QtWidgets.QPushButton("Submit", self.linux_farm_groupbox)
        # Takes in the y-axis created by the GroupBox Creation minus 30
        submit_button.setGeometry(
            510, (self.linux_farm_groupbox.frameGeometry().height() - 30), 91, 22
        )
        submit_button.setFont(self.s_font)

        # Runs when submit button is clicked
        def submit_button_clicked():
            """Handles the event when the submit button is clicked.

            Returns:
                None
            """

            new_values_list = []
            for box in self.spinboxes_list:
                new_value = box.value()
                new_values_list.append(new_value)

            new_hard_values_list = []
            for box in self.spinboxes_hardcap_list:
                new_hard_value = box.value()
                new_hard_values_list.append(new_hard_value)

            big_sum = round(sum(new_values_list), 1)

            if big_sum < 100.0 or big_sum > 100.0:
                error_label = QtWidgets.QLabel(
                    "The newly set values do not add up to 100! Try again.",
                    self.linux_farm_groupbox,
                )

                error_label.setGeometry(
                    10,
                    (self.linux_farm_groupbox.frameGeometry().height() - 30),
                    350,
                    20,
                )
                error_label.setFont(self.s_font)
                error_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
                error_label.setScaledContents(False)
                error_label.setWordWrap(True)
                error_label.setStyleSheet("color: red")
                error_label.show()

            else:
                new_values_dict = dict(zip(self.shows, new_values_list))
                new_hard_values_dict = dict(zip(self.shows, new_hard_values_list))
                # This check is needed for the following window to choose whether
                # to display the "Stage All" button or not
                linux_check = True

                changes_confirmation_window = UiConfirmFarmChangesMainWindow(
                    self.current_values_full_dict,
                    new_values_dict,
                    self.current_values_cap_full_dict,
                    new_hard_values_dict,
                    self.farm_name,
                    self.contents_dict,
                    self.config_file_path_name,
                    self.temp_folder,
                    self.backup_folder,
                    linux_check,
                    self.linux_farm_sections,
                    self.fonts,
                )

                changes_confirmation_window.show()
                self.close()

        submit_button.clicked.connect(submit_button_clicked)

        # Name can be changed here
        cancel_button = QtWidgets.QPushButton("Cancel", self.linux_farm_groupbox)
        cancel_button.setGeometry(
            620, (self.linux_farm_groupbox.frameGeometry().height() - 30), 91, 22
        )
        cancel_button.setFont(self.s_font)

        cancel_button.clicked.connect(self.cancel_button_clicked)
        cancel_button.clicked.connect(self.close)

    def cancel_button_clicked(self):
        """When the cancel button is clicked, it will open the first window of the UI
        and close this one.

        Parameters:
            self (object): instance of a class.

        Returns:
            None
        """

        from main_farm_selection_window import UiAtomicCartoonsAllocationsMainWindow

        farm_selection_windows = UiAtomicCartoonsAllocationsMainWindow()
        farm_selection_windows.show()
        self.close()
