#!/sw/pipeline/rendering/python3/venv/bin/python

""" 
This is the Changes Confirmation window of the Atomic Farm UI. Helps the user
see the changes to be made before they are applied.

Created using PyQt5
Please only adjust values if totally sure of what you are doing!

Created by Guillermo Aguero - Render TD

Written in Python3.
"""

import json
from qtpy import QtGui, QtWidgets

from changes_applied_window import UiChangesAppliedMainWindow


class UiConfirmFarmChangesMainWindow(QtWidgets.QMainWindow):
    """The Confirmation Window class to create and manage the UI for confirming
    changes in farm settings.

    This class provides methods to initialize the main window, set up the user interface,
    and handle user interactions for confirming changes in the farm settings.

    Parameters:
        current_values_dict (dict): The current values for the farm's settings.
        new_values_dict (dict): The new values to be applied to the farm's settings.
        current_values_cap_dict (dict): The current cap values for the farm's settings.
        new_hard_values_dict (dict): The new hard cap values to be applied to the farm's settings.
        farm_name (str): The name of the farm.
        contents_dict (dict): The configuration content for the farm.
        config_file_path_name (str): Path to the configuration file.
        temp_folder (str): Path to the temporary folder for storing temp files.
        backup_folder (str): Path to the backup folder.
        linux_check (bool): Flag to check if Linux is being used.
        farm_sections (list): List of sections within the farm.
        fonts (list): List containing large and small QFont objects for UI elements.

    Methods:
        setup_ui(): Sets up the user interface components.
        changes_confirmation_window_setup(): Sets up the changes confirmation window.
        groupbox_creation(): Creates a group box for UI elements.
        label_creation(): Creates labels for the UI.
        text_browser_creation(): Creates text browsers to display values before and after changes.
        button_creation(): Creates and sets up buttons for the changes confirmation group box.
        cancel_button_clicked(): Handles the click event for the cancel button.
    """

    def __init__(
        self,
        current_values_dict,
        new_values_dict,
        current_values_cap_dict,
        new_hard_values_dict,
        farm_name,
        contents_dict,
        config_file_path_name,
        temp_folder,
        backup_folder,
        linux_check: bool,
        farm_sections: list,
        fonts,
    ):
        """Initializes the UiConfirmFarmChangesMainWindow instance.

        This constructor sets up the confirmation window for the UI, initializing
        all necessary attributes to display the current and new values for verification
        before making changes permanent. It prepares the UI elements and ensures the window
        is ready to be displayed.

        Parameters:
            current_values_dict (dict): Dictionary of current nominal percentage values for shows.
            new_values_dict (dict): Dictionary of new nominal percentage values for shows.
            current_values_cap_dict (dict): Dictionary of current hard cap
            percentage values for shows.
            new_hard_values_dict (dict): Dictionary of new hard cap percentage values for shows.
            farm_name (str): The name of the farm section.
            config_file_path_name (str): Path to the main configuration file.
            temp_folder (str): Path to the temporary folder for storing temp files.
            backup_folder (str): Path to the backup folder.
            linux_check (bool): Boolean indicating if the farm is a Linux farm.
            farm_sections (list): List of sections within the Linux farm.
            fonts (list): List containing large and small QFont objects for UI elements.

        Attributes:
            sorted_current_values_dict (dict): Sorted dictionary of current nominal
            percentage values.
            sorted_current_values_cap_dict (dict): Sorted dictionary of current
            hard cap percentage values.
            l_font (QFont): Large font for UI elements.
            s_font (QFont): Small font for UI elements.

        Config Data:
            contents_dict (dict): Dictionary containing the configuration file contents.

        UI Components:
            centralwidget (QWidget): Central widget for the confirmation window.
            changes_confirmation_groupbox (QGroupBox): Group box containing UI
            elements for confirmation.

        Fonst:
            l_font (QFont): Large font for UI elements.
            s_font (QFont): Small font for UI elements.


        Calls:
            setup_ui(): Sets up the user interface components.
        """

        super().__init__()

        # Incoming Variables
        self.sorted_current_values_dict = dict(sorted(current_values_dict.items()))
        self.sorted_current_values_cap_dict = dict(
            sorted(current_values_cap_dict.items())
        )
        self.new_values_dict = new_values_dict
        self.new_hard_values_dict = new_hard_values_dict
        self.farm_name = farm_name
        self.contents_dict = contents_dict
        self.config_file_path_name = config_file_path_name
        self.temp_folder = temp_folder
        self.backup_folder = backup_folder
        self.linux_check = linux_check
        self.farm_sections = farm_sections
        self.l_font = fonts[0]
        self.s_font = fonts[1]
        self.fonts = fonts

        # Sections of the Window
        self.centralwidget = ""
        self.changes_confirmation_groupbox = None

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components.

        This method calls various other methods to build and initialize all parts
        of the UI, including getting all shows, setting up the main window,
        and creating various UI elements like group boxes labels, and buttons.

        Returns:
            None
        """

        self.changes_confirmation_window_setup()
        self.groupbox_creation()
        self.label_creation()
        self.text_browser_creation()
        self.button_creation()

    def changes_confirmation_window_setup(self):
        """This function sets up the farm selection window, including the size,
        style, and title of the window, as well as centering it on the screen.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Main Window can be changed here.
        self.setWindowTitle("Changes Confirmation Window")
        # Window Size can be adjusted here
        self.setFixedSize(463, 349)
        # Using this style sheet the theme can be changed
        self.setStyleSheet(
            """background-color: rgb(46, 52, 54);color: rgb(238, 238, 236);"""
        )
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        def center_window(window):

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
            self (object): The object instance.

        Returns:
            None
        """

        # Title of the Group Box
        self.changes_confirmation_groupbox = QtWidgets.QGroupBox(
            "Review Your Changes", self.centralwidget
        )
        self.changes_confirmation_groupbox.setGeometry(10, 10, 441, 331)
        self.changes_confirmation_groupbox.setFont(self.l_font)

    def label_creation(self):
        """Creates and sets text for various labels in the window.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        # Text inside the label can be changed here
        review_changes_label = QtWidgets.QLabel(
            "Please take a close look below to compare the changes you "
            "have made against the previous settings before you "
            "fully apply them:",
            self.changes_confirmation_groupbox,
        )
        review_changes_label.setGeometry(10, 40, 421, 61)
        review_changes_label.setFont(self.s_font)
        review_changes_label.setWordWrap(True)

        before_label = QtWidgets.QLabel("Before:", self.changes_confirmation_groupbox)
        before_label.setGeometry(10, 110, 61, 20)
        before_label.setFont(self.l_font)
        before_label.setWordWrap(True)
        before_label.setStyleSheet("color : #D21404")

        after_label = QtWidgets.QLabel("After:", self.changes_confirmation_groupbox)
        after_label.setGeometry(230, 110, 51, 20)
        after_label.setFont(self.l_font)
        after_label.setWordWrap(True)
        after_label.setStyleSheet("color : #A7F432")

    def text_browser_creation(self):
        """Creates text browsers to display values before and after changes.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        before_text_browser = QtWidgets.QTextBrowser(self.changes_confirmation_groupbox)
        before_text_browser.setGeometry(10, 140, 141, 131)
        before_text_browser.setFont(self.s_font)
        before_text_browser.setReadOnly(True)

        # This is how the shows are displayed in the Text Browser
        before_text_browser.append("Nominal:\n")
        for show, percentage in self.sorted_current_values_dict.items():
            before_text_browser.append(f"{show}: {percentage}%")
        before_text_browser.append("\nHard Cap:\n")
        for show, percentage in self.sorted_current_values_cap_dict.items():
            before_text_browser.append(f"{show}: {percentage}%")

        before_text_browser.horizontalScrollBar().setValue(0)

        # Sorted dictionaries
        sorted_new_values_dict = dict(sorted(self.new_values_dict.items()))
        sorted_new_hard_values_dict = dict(sorted(self.new_hard_values_dict.items()))

        after_text_browser = QtWidgets.QTextBrowser(self.changes_confirmation_groupbox)
        after_text_browser.setGeometry(230, 140, 141, 131)
        after_text_browser.setFont(self.s_font)
        after_text_browser.setReadOnly(True)
        after_text_browser.setObjectName("after_text_browser")

        # This is how the shows are displayed in the Text Browser
        after_text_browser.append("Nominal:\n")
        for show, percentage in sorted_new_values_dict.items():
            after_text_browser.append(f"{show}: {percentage}%")
        after_text_browser.append("\nHard Cap:\n")
        for show, percentage in sorted_new_hard_values_dict.items():
            after_text_browser.append(f"{show}: {percentage}%")

    def button_creation(self):
        """Creates and sets up the buttons for the changes confirmation groupbox.

        This method creates and configures the "Stage", "Stage All" (if applicable),
        and "Cancel" buttons, setting their geometry, font, and click event handlers.

        Internal Functions:
            stage_button_clicked: Handles the click event for the "Stage" button.
            apply_to_all_button_clicked: Handles the click event for the
            "Stage All" button.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """

        stage_button = QtWidgets.QPushButton(
            "Stage", self.changes_confirmation_groupbox
        )
        stage_button.setGeometry(160, 300, 121, 22)
        stage_button.setFont(self.s_font)

        def stage_button_clicked():
            """Handles the click event for the "Stage" button.

            This function updates the configuration with the new nominal and cap
            values, saves the updated configuration to a temporary file, and
            shows the changes applied window.

            Returns:
                None
            """

            tmp_file_name = f"{self.temp_folder}temp.config"

            for show, percentage in self.new_values_dict.items():
                self.contents_dict["Limits"][self.farm_name]["Shares"][show][
                    "nominal"
                ] = round(percentage / 100, 3)

            for show, percentage in self.new_hard_values_dict.items():
                self.contents_dict["Limits"][self.farm_name]["Shares"][show]["cap"] = (
                    round(percentage / 100, 3)
                )

            json.dump(self.contents_dict, open(tmp_file_name, mode="w"), indent=4)

            changes_applied_window = UiChangesAppliedMainWindow(
                self.config_file_path_name,
                self.contents_dict,
                tmp_file_name,
                self.backup_folder,
                self.new_values_dict,
                self.farm_name,
                self.fonts,
            )
            changes_applied_window.show()

        stage_button.setStyleSheet("color: yellow")

        stage_button.clicked.connect(stage_button_clicked)
        stage_button.clicked.connect(self.close)

        if self.linux_check:

            # Name can be changed here
            stage_all_button = QtWidgets.QPushButton(
                "Stage All", self.changes_confirmation_groupbox
            )
            # Takes in the y-axis created by the GroupBox Creation minus 30
            stage_all_button.setGeometry(
                10,
                300,
                121,
                22,
            )
            stage_all_button.setFont(self.s_font)

            def apply_to_all_button_clicked():
                """Handles the click event for the "Stage All" button.

                This function updates the configuration for all farm sections
                with the new nominal and cap values, saves the updated
                configuration to a temporary file, and shows the changes applied
                window.

                Return:
                    None
                """

                tmp_file_name = f"{self.temp_folder}temp.config"

                for section in self.farm_sections:
                    if section != "linuxfarm_Denoise":
                        for show, percentage in self.new_values_dict.items():
                            self.contents_dict["Limits"][section]["Shares"][show][
                                "nominal"
                            ] = round(percentage / 100, 3)

                        for show, percentage in self.new_hard_values_dict.items():
                            self.contents_dict["Limits"][section]["Shares"][show][
                                "cap"
                            ] = round(percentage / 100, 3)

                json.dump(self.contents_dict, open(tmp_file_name, mode="w"), indent=4)

                changes_applied_window = UiChangesAppliedMainWindow(
                    self.config_file_path_name,
                    self.contents_dict,
                    tmp_file_name,
                    self.backup_folder,
                    self.new_values_dict,
                    self.farm_name,
                    self.fonts,
                )
                changes_applied_window.show()

            stage_all_button.setStyleSheet("color: orange")
            stage_all_button.clicked.connect(apply_to_all_button_clicked)
            stage_all_button.clicked.connect(self.close)

        cancel_button = QtWidgets.QPushButton(
            "Cancel", self.changes_confirmation_groupbox
        )
        cancel_button.setGeometry(310, 300, 121, 22)
        cancel_button.setFont(self.s_font)
        cancel_button.clicked.connect(self.cancel_button_clicked)
        cancel_button.clicked.connect(self.close)

    def cancel_button_clicked(self):
        """When the cancel button is clicked, it will open the first window of the UI
        and close this one.

        Parameters:
            self (object): The object instance.

        Returns:
            None
        """
        from main_farm_selection_window import UiAtomicCartoonsAllocationsMainWindow

        farm_selection_window = UiAtomicCartoonsAllocationsMainWindow()
        farm_selection_window.show()
        self.close()
