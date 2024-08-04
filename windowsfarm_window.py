#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
This window opens up when selected through the 'Farm_Selection_Window' of the
Atomic Farm UI.
Represents the Windows Farm as a whole.
Created using QtPy
Please only adjust values if totally sure of what you are doing!

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


class UiWindowsFarmMainWindow(QtWidgets.QMainWindow):
    """Main window class for the Windowa Farm UI in the Atomic Farm application.

    This window is opened through the 'Farm_Selection_Window' of the Atomic Farm UI
    and represents the Linux Farm section selected in the previous window.
    It is created using QyPy and provides an interface to adjust the allocation
    percentages for different shows on the Linux Farm.

    Attributes:
        farm_name (str): The name of the farm section.
        linux_farm_sections (list): List of sections within the Linux farm.
        config_file_path_name (str): Path to the main configuration file.
        temp_folder (str): Path to the temporary folder for storing temp files.
        backup_folder (str): Path to the backup folder.
        fonts (list): List containing large and small QFont objects for UI elements.


    """

    def __init__(
        self, farm_name, config_file_path_name, temp_folder, backup_folder, fonts
    ):
        """
        Initializes the UiWindowsFarmMainWindow instance.

        This constructor sets up the main window for the Windows Farm UI, initializing
        all necessary attributes and loading the configuration file. It prepares
        the UI elements and ensures that the window is ready to be displayed.

        Parameters:
            farm_name (str): The name of the farm section.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder for storing temp files.
            backup_folder (str): Path to the backup folder.
            fonts (list): List containing large and small QFont objects for UI elements.

        Attributes:
            shows (list): List of show names available on the farm.
            current_perc_list (list): List of current percentage values for shows.
            spinboxes_list (list): List of spin box widgets for nominal percentages.
            sliders_list (list): List of slider widgets for nominal percentages.
            spinboxes_hardcap_list (list): List of spin box widgets for hard cap
            percentages.
            current_values_full_dict (dict): Dictionary of current percentage
            values for shows.
            current_values_cap_full_dict (dict): Dictionary of current hard cap
            percentage values for shows.
            y_axis_window_size (int): Initial window height.

        Config Data:
            contents_dict (dict): Dictionary containing the configuration file contents.

        UI Components:
            centralwidget: The central widget of the main window.
            windows_farm_groupbox: Group box containing the UI elements.

        Fonts:
            l_font: Large font for UI elements.
            s_font: Small font for UI elements.
            m_font: Medium font with underline for specific UI elements.

        Calls:
            setup_ui(): Method to set up the user interface.
        """

        super().__init__()

        # Incoming Variables
        self.farm_name = farm_name
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder
        self.l_font = fonts[0]
        self.s_font = fonts[1]
        self.fonts = fonts

        # Sections of the window
        self.centralwidget = ""
        self.windows_farm_groupbox = None
        self.shows = []
        self.current_perc_list = []
        self.spinboxes_list = []
        self.sliders_list = []
        self.spinboxes_hardcap_list = []
        self.current_values_full_dict = dict()
        self.current_values_cap_full_dict = dict()
        self.y_axis_window_size = None

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
            self (object): The object instance.

        Returns:
            None
        """

        self.get_shows()
        self.windowsfarm_window_setup()
        self.groupbox_creation()
        self.groupbox_info_creation()
        self.info_label_creation()
        self.button_creation()

    def get_shows(self):
        """Generates a list of show names that the farm has access to.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # This generates a list of all shows for this farm
        avoid = ["default"]
        for key in self.contents_dict["Limits"][self.farm_name]["Shares"].keys():
            if all(word not in key for word in avoid):
                self.shows.append(key)

    def windowsfarm_window_setup(self):
        """This function sets up the farm selection window, including the size,
        style, and title of the window, as well as centering it on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Windows Farm Window")
        self.y_axis_window_size = 390
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
        elements related to the Windows Farm.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Group Box
        self.windows_farm_groupbox = QtWidgets.QGroupBox(
            "Windows Farm", self.centralwidget
        )
        self.windows_farm_groupbox.setGeometry(10, 10, 721, 490)  # 721 348
        self.windows_farm_groupbox.setFont(self.l_font)

    def groupbox_info_creation(self):
        """Creates and configures UI components (labels, spin boxes, and sliders)
        within a group box for displaying and modifying show allocations.

        This function iterates through the list of shows and dynamically creates
        labels, spin boxes, and sliders for each show. It then connects the spin
        boxes and sliders to synchronize their values and calculates the total
        percentage of allocations. If the UI components exceed the initial window
        size, the window and group box sizes are adjusted accordingly.

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

        labels_y_axis_value = 70
        slider_box_y_axis_value = 100

        def label_creation(show, labels_y_axis_value):
            """Creates a QLabel object with the provided show title and sets
            its properties.

            Parameters:
                show (str): The title of the show
                labels_y_axis_value (int): The y-axis value where the label
                will be created.

            Returns:
                None
            """

            spaced_out_label = re.sub(r"(\w)([A-Z])", r"\1 \2", show)
            label = QtWidgets.QLabel(spaced_out_label, self.windows_farm_groupbox)
            label.setGeometry(270, labels_y_axis_value, 180, 20)
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)

        def spin_box_creation(slider_box_y_axis_value):
            """Creates two QDoubleSpinBoxes for a show and its hard cap value

            Parameters:
                slider_box_y_axis_value (int): y-axis value for positioning
                the spin boxes.

            Returns:
                spin_box (QDoubleSpinBox): QDoubleSpinBox for the show
                hardcap_spin_box (QDoubleSpinBox): QDoubleSpinBox for the
                hard cap value of the show.
            """

            # Minimum and Maximum for all spin boxes
            minimum = 0
            maximum = 100

            spin_box = QtWidgets.QDoubleSpinBox(self.windows_farm_groupbox)
            spin_box.setGeometry(560, slider_box_y_axis_value, 57, 22)
            spin_box.setFont(self.s_font)
            spin_box.setDecimals(1)
            spin_box.setMinimum(minimum)
            spin_box.setMaximum(maximum)

            hardcap_spin_box = QtWidgets.QDoubleSpinBox(self.windows_farm_groupbox)
            hardcap_spin_box.setGeometry(640, slider_box_y_axis_value, 60, 22)
            hardcap_spin_box.setFont(self.s_font)
            hardcap_spin_box.setDecimals(1)
            hardcap_spin_box.setMinimum(minimum)
            hardcap_spin_box.setMaximum(maximum)

            return spin_box, hardcap_spin_box

        def sliders_creation(slider_box_y_axis_value):
            """Creates a horizontal slider widget and sets its properties.

            Parameters:
                show (str): A string representing the name of the slider.
                slider_box_y_axis_value (int): An integer representing the
                y-axis value of the slider.

            Returns:
                slider (QSlider): A horizontal slider widget with a specified
                range and name.
            """

            # Minimum and Maximum for all sliders
            minimum = 0
            maximum = 100
            # Setting up
            slider = QtWidgets.QSlider(self.windows_farm_groupbox)
            slider.setGeometry(270, slider_box_y_axis_value, 251, 20)
            slider.setTracking(True)
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
            slider.setMinimum(minimum)
            slider.setMaximum(maximum)

            return slider

        def connect_parts(spin_box, slider):
            """Connects a Spin Box and Slider to update each other's values.

            Parameters:
                spin_box (QSpinBox): the spin box to be connected to the
                slider.
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

        # This "for" loop individually sets-up every single show in the list of shows.
        for show in self.shows:
            label_creation(show, labels_y_axis_value)
            spin_box, hardcap_spin_box = spin_box_creation(slider_box_y_axis_value)
            slider = sliders_creation(slider_box_y_axis_value)
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
            labels_y_axis_value = labels_y_axis_value + 60
            slider_box_y_axis_value = slider_box_y_axis_value + 60

        total_current_percent = sum(self.current_perc_list)

        def current_percent_spin_box_creation():
            """Creates a spinbox to be able to show the current total of all
            sliders/spin boxes added together

            Returns:
                None
            """
            total_spin_box = QtWidgets.QDoubleSpinBox(self.windows_farm_groupbox)
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
        # increases the size of both the Window and the groupbox.

        if labels_y_axis_value > (self.y_axis_window_size - 50):
            self.y_axis_window_size = self.y_axis_window_size + 120
            self.setFixedSize(740, self.y_axis_window_size)
            self.y_axis_window_size = self.y_axis_window_size - 20  # 42
            self.windows_farm_groupbox.setGeometry(10, 10, 721, self.y_axis_window_size)

    def current_values_show(
        self,
        show,
        slider,
        spin_box,
        hardcap_spin_box,
    ):
        """Function to update the current percentage values for the nominal
        and hard cap for a given show.

        Parameters:
            self (object): The object instance.
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
            self (object): The object instance.

        Returns:
            None
        """

        # Main Definition label
        window_def_label = QtWidgets.QLabel(
            "To the right side you will see a list of all current "
            "working shows in the Windows Farm as a whole.",
            self.windows_farm_groupbox,
        )
        window_def_label.setGeometry(10, 50, 191, 71)
        window_def_label.setFont(self.s_font)
        window_def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        window_def_label.setScaledContents(False)
        window_def_label.setWordWrap(True)

        # Second Definition Label
        window_def_sliders_label = QtWidgets.QLabel(
            "Utilizing the available sliders, please select how much "
            "allocation each show should be receiving: ",
            self.windows_farm_groupbox,
        )
        window_def_sliders_label.setGeometry(10, 140, 201, 81)
        window_def_sliders_label.setFont(self.s_font)
        window_def_sliders_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        window_def_sliders_label.setScaledContents(False)
        window_def_sliders_label.setWordWrap(True)

        # Label for the Counter Updating with the boxes/sliders.
        counter_label = QtWidgets.QLabel(
            "Total Current Percentage: ",
            self.windows_farm_groupbox,
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
        nominal_label = QtWidgets.QLabel("Nominal", self.windows_farm_groupbox)
        nominal_label.setGeometry(560, 40, 61, 20)  # 565 10
        nominal_label.setFont(self.m_font)
        nominal_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        nominal_label.setScaledContents(False)
        nominal_label.setWordWrap(True)
        nominal_label.setStyleSheet("color: yellow")

        cap_label = QtWidgets.QLabel("Hard Cap", self.windows_farm_groupbox)
        cap_label.setGeometry(636, 40, 71, 20)
        cap_label.setFont(self.m_font)
        cap_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        cap_label.setScaledContents(False)
        cap_label.setWordWrap(True)
        cap_label.setStyleSheet("color: yellow")

    def button_creation(self):
        """Creates and sets up the Submit and Cancel buttons. The Submit button
        does a check to see if hte values add up to 100 and creates new
        dictionaries with the new values. The Cancel button returns the user
        to the previous window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Name can be changed here
        submit_push_button = QtWidgets.QPushButton("Submit", self.windows_farm_groupbox)
        # Takes in the y-axis created by the GroupBox Creation minus 30
        submit_push_button.setGeometry(
            510, (self.windows_farm_groupbox.frameGeometry().height() - 30), 91, 22
        )
        submit_push_button.setFont(self.s_font)
        submit_push_button.clicked.connect(self.submit_button_clicked)

        # Name can be changed here
        cancel_push_button = QtWidgets.QPushButton("Cancel", self.windows_farm_groupbox)
        cancel_push_button.setGeometry(
            620, (self.windows_farm_groupbox.frameGeometry().height() - 30), 91, 22
        )
        cancel_push_button.setFont(self.s_font)

        def cancel_button_clicked():
            """When the cancel button is clicked, it will open the first window of the UI
            and close this one.

            Returns:
                None
            """

            from main_farm_selection_window import UiAtomicCartoonsAllocationsMainWindow

            farm_selection_windows = UiAtomicCartoonsAllocationsMainWindow()
            farm_selection_windows.show()
            self.close()

        cancel_push_button.clicked.connect(cancel_button_clicked)
        cancel_push_button.clicked.connect(self.close)

    def submit_button_clicked(self):
        """Handles the event when the submit button is clicked.

        Parameters:
            self (object): The object instance.

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
                self.windows_farm_groupbox,
            )

            error_label.setGeometry(
                10,
                (self.windows_farm_groupbox.frameGeometry().height() - 30),
                375,
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
            linux_check: bool = False
            # This farm section variable comes in empty here because the Windows
            # Farm does not have the option to "Apply To all" like the Linux Farm does
            farm_sections: list = []

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
                farm_sections,
                self.fonts,
            )
            changes_confirmation_window.show()
            self.close()
