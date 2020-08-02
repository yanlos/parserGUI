Telemetry Parsing and Pulling GUI:

This GUI was built using Python and it's built in GUI framework, Tkinter.

In order to use the GUI a user would launch it from an IDE using the "run" button or by calling upon the script from their terminal using the CLI command "py" and their directory, for example: 
"py C:/Users/Yan_los/Desktop/telelog_toolkit/gui.py"


The first thing to set up would be the directory by clicking the "Configurations" button where the user can enter in which directory they want the output files to be saved ,otherwise they are going to be created inside of the default directory where the gui.py file is located.

In order to use the GUI to parse files they would select one of the several buttons of the left of the interface labeled "Parse Telemetry File", "Parse Smart Log", etc.. These correspond to the files such as the telemetry.bin file inside the telemetryLog folder, you need to click the "Parse Telemetry File" and select the telemetry.bin file to parse it.

As of now the Parse Telemetry File function has been implemented, specifically the "Parse Log" function. In order to do that you would click the "Parse Telemetry File" which opens up the system's browse feature where you can select the file you want to open. In order to do that we select the "telemetry" bin file we want to parse and open it up. It will then parse the file and bring up more options such as "Parse Event Log", "Parse Debug Data", and "Parse Crash Dump" which correspond to the different data areas within the telemetry file.
 
To further parse the event log press the "Parse Event Log" button and it will bring up the parsed file with some more options to filter them by error code and also reverse the time. The user can scroll down the text window to see the whole file. 

After parsing each file, they are saved into the user's chosen directory or default directory.
For example after parsing the telemetry file it creates a folder called "logsNotParsed" with an unparsed event log inside of it (or any other data provided by that file).
Parsing further how we did using the "Parse Event Log" button puts 2 time stamped files inside the ParsedFiles folder, one as a text .log file and the other as a .csv file.

The pulling from the NVME CLI feature and other "Parse" functions have not been built in yet but can be easily added into the methods of the GUI by attaching them to buttons.

The user can also "Save File As" which will save the information displayed inside of the GUI's text editor as is into any file they want or reopen a file using the "Open" function


Using Tkinter:

At the bottom of the gui.py file you will see something like:
btn_parse_telemetry = tk.Button(fr_buttons, text="Parse Telemetry File", command=telem_parser)

This corresponds to the buttons on the left and are contained by a frame created using Tkinter.
In order to attach a method to the buttons you have to using the "command=" parameter and then the method it corresponds to.

In order to place information into the text editor the user has to take an input file and then just insert it into the text window created below by "txt_edit = tk.Text(window)" and then insert it into it by writing "txt_edit.insert(tk.END, text)" with 'text' being the information they want to output.



For more information if needed please email me, Yan Los, at yanlos@yahoo.com


The files that are in this folder:
telemetryLog folder - holds a sample telemetry.bin file used for parsing (and an event log which is created by it which you don't need to parse)
getTelemetryLog.py - pulls a telemetry log from a drive
eventLogParser.py - used to parse the event log which is a data area of the telemetry blob (uses the stringFile JSON file)
telemetryParser.py - parses the table of contents information from the telemetry blob 

GUI.py - puts all of these files together into a graphical user interface for the user to further manipulate the files 
