# Pixar_Tractor_Shares_UI
This complete UI has been created using PyQT and it serves as a way to manipulate a specific '.config' file which affects the allocations of specific Shows within a configuration file related to Tractor Engine. This UI automatically adjusts its size and the amount of optons displayed according to how many shows there is. 

- First window (**main_farm_selection_window.py**) allows for a selection of what section of the Farm you wish to modify. This list is auto-generated from the '.config' file in case any section is removed or added.
- Second window (depending on the selection, either **linuxfarm_window.py** or **windowsfarm_window.py** will run) displays a list of all available shows in the selected Farm section together with a slider and a combo box for each one showing the current percentage value individually. Here you can adjust the values and proceed to the next window or cancel and go back to selected another section of the Farm. There is also a check to make sure that the values do not go above 100%.
- The third window is a confirmation window (**changes_confirmation_window.py**) which displays all the changes made in the previous window versus the current values from the '.config' file.
- Last Window (**changes_applied_window.py**) will allow the user to stage and push the changes to the '.config' file, choose to go back to the first window and make more changes (this will create a temporary '.config' file) or simply exit and discard all changes.

After the changes have been submitted, the terminal running the script will display a multiple messages related to the success of the tool changing the '.config' file and reloading Tractor while comparing the values to the ones that are currently live. 

**Please note:**

- For this UI to work in a different environment, a '.config' file is necessary as well as changing the paths required in the first window
- The images have the name of Shows covered due to NDA agreements
