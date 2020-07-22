import ctypes
import tkinter as tk
from time import strftime
from tkinter import ttk
import tkinter.messagebox as tkError
from tkinter.filedialog import *
import os.path

import os
import subprocess

import telemetryParser as telPar
import eventLogParser as logPar


def openNotebook1():
    print("pressed")
    tab_parent = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="TOC1")


def smartlog_parse():
    print("works")
    # subprocess.Popen()

def telem_parser():
    filepath = askopenfilename(
        filetypes=[("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)

    print(filepath)

    global personalDirectoryPath
    print(personalDirectoryPath)
    outputDir = personalDirectoryPath + "\logsNotParsed"
    # outputDir = personalRootDir + "telelog_toolkit/logsNotParsed"
    # telemDir = "C:/Users/Yan_los/Desktop/telemetry/telemetryLog/telemetry.bin "
    telemDir = filepath

    if not os.path.exists(telemDir):
        raise ValueError("telemetry binary path %s is invalid." % telemDir)
    if outputDir and not os.path.exists(outputDir):
        os.mkdir(outputDir)
    telemetryParser = telPar.TelemetryParser(telemetryBinPath=telemDir)

    checkType = os.path.splitext(filepath)[1]
    if checkType == ".bin":

        window.title(f"Telemetry Parser Information For - {telemDir}")
        txt_edit.insert(tk.END, ">>===========Host Header===============<<" + '\n')
        telemetryTypeStr = {7: "Host telemetry", 8: "Controller telemetry"}[telemetryParser.telemetryHeader.log_id]
        txt_edit.insert(tk.END, "%s log ID: %d" % (telemetryTypeStr, telemetryParser.telemetryHeader.log_id) + '\n')
        txt_edit.insert(tk.END, "%s area1 LBLK: %d" % (telemetryTypeStr, telemetryParser.telemetryHeader.data_area1_lblk)+ '\n')
        txt_edit.insert(tk.END, "%s area2 LBLK: %d" % (telemetryTypeStr, telemetryParser.telemetryHeader.data_area2_lblk)+ '\n')
        txt_edit.insert(tk.END, "%s area3 LBLK: %d" % (telemetryTypeStr, telemetryParser.telemetryHeader.data_area3_lblk)+ '\n')
        txt_edit.insert(tk.END, ">>===========File Header===============<<"+ '\n')
        txt_edit.insert(tk.END, "File header magic_word: %s" % ctypes.string_at(ctypes.addressof(telemetryParser.fileHeader.magic_word), 8)+ '\n')
        txt_edit.insert(tk.END, "File header max_size: %d" % telemetryParser.fileHeader.max_size + '\n')
        txt_edit.insert(tk.END, "File header file_size: %d" % telemetryParser.fileHeader.file_size + '\n')
        txt_edit.insert(tk.END, "File header section_num: %d" % telemetryParser.fileHeader.section_num + '\n')
        txt_edit.insert(tk.END, "File header section_descr_length: %d" % telemetryParser.fileHeader.section_descr_length + '\n')
        txt_edit.insert(tk.END, "File header section_descr_offset: %d" % telemetryParser.fileHeader.section_descr_offset + '\n')
        txt_edit.insert(tk.END, ">>===========Sections===============<<" + '\n')
        for section in telemetryParser.sectionList:
            #TODO put so it makes dynamic buttons in here
            sectionName = section.header.name.strip().decode("ascii")
            sectionPath = os.path.join(outputDir, sectionName + ".bin")
            txt_edit.insert(tk.END, "Section name: %s" % sectionName + '\n')
            txt_edit.insert(tk.END, "Section bin path: %s" % sectionPath + '\n')
            txt_edit.insert(tk.END, "Section data_offset: %d" % section.header.data_offset + '\n')
            txt_edit.insert(tk.END, "Section data_len: %d" % section.header.data_len + '\n')
            txt_edit.insert(tk.END, "Section module: %d" % section.header.module + '\n')
            section.dumpToFile(sectionPath)
            txt_edit.insert(tk.END, ">>----------------------------------<<" + '\n')


        telem_parser_options = tk.Frame(window, relief=tk.RAISED, bd=2)

        btn_parse_log = tk.Button(telem_parser_options, text="Parse Event Log", command = parse_log)
        btn_parse_debug = tk.Button(telem_parser_options, text="Parse Debug Data")
        btn_parse_crashdump = tk.Button(telem_parser_options, text="Parse Crash Dump")
        btn_parse_all = tk.Button(telem_parser_options, text="Parse Whole File")

        btn_parse_log.grid(column=0, sticky="swe", pady=5)
        btn_parse_debug.grid(column=0, sticky="swe", pady=5)
        btn_parse_crashdump.grid(column=0, sticky="swe", pady=5)
        btn_parse_all.grid(column=0, sticky="swe", pady=5)

        telem_parser_options.grid(row=0, column=1, sticky="nsew")


    else:
        tkError.showerror(title = "Parse Error", message= "Can only parse .bin telemetry files")
        raise ValueError("Can only parse .bin telemetry files")


def parse_log():

    # You can't use ":" so I used dashes
    logTimestamp = "/"+ strftime("%m-%d-%Y_%H-%M-%S") + "event.log"

    parsedFiles = personalDirectoryPath + "/ParsedFiles"
    if os.path.exists(parsedFiles):
        print("here is" + parsedFiles + logTimestamp)
        os.system("py .\eventLogParser.py -eb " + personalDirectoryPath + "/logsNotParsed/event_log.bin -s .\stringFile.json -on " + parsedFiles + logTimestamp)
    else:
        tk.messagebox.showinfo(title="Created New Folder", message="Created folder to store parsed files! Under: " + parsedFiles)
        os.mkdir(parsedFiles)
        os.system("py .\eventLogParser.py -eb " + personalDirectoryPath + "/logsNotParsed/event_log.bin -s .\stringFile.json -on " + parsedFiles + logTimestamp)

    with open(parsedFiles + logTimestamp, "r") as input_file:
        txt_edit.delete(1.0, tk.END)
        text = input_file.read()
        txt_edit.insert(tk.END, text)
        window.title(f"File Open: - {input_file}")

    # print(personalRootDir)

    # Get the status of the checkboxes, prints 1 if checked, 0 if not checked
    # Then it puts all the error codes in a list and removes the ones that are unchecked
    def var_states():
        logs = ["DBG", "INF", "WRN", "ERR"]
        print(DBGshow.get())
        if DBGshow.get() == 0:
            logs.remove("DBG")

        print(INFshow.get())
        if INFshow.get() == 0:
            logs.remove("INF")

        print(WRNshow.get())
        if WRNshow.get() == 0:
            logs.remove("WRN")

        print(ERRshow.get())
        if ERRshow.get() == 0:
            logs.remove("ERR")

        # print the selected checkboxes as a reference
        print(logs)


        # open our file, reset the texteditor, and write it line by line depending on the checkboxes
        with open(parsedFiles+logTimestamp, "r") as input_file:
            txt_edit.delete(1.0, tk.END)

            #If the reversed box is checked it will read from the file in reverse order
            if reverseOption.get() == 0:
                for line in input_file:
                # check if a line has one of the strings in our logs list
                    if any(s in line for s in logs):
                        txt_edit.insert(tk.END, line)
            else:
                lines = input_file.readlines()
                for line in reversed(lines):
                    if any(s in line for s in logs):
                        txt_edit.insert(tk.END, line)

            window.title(f"File Filtering: - {input_file}")


    # This creates the check boxes and the filter button, the filter button then calls the var_states() function
    DBGshow = IntVar()
    INFshow = IntVar()
    WRNshow = IntVar()
    ERRshow = IntVar()
    reverseOption = IntVar()

    boxes = tk.Frame(window, relief=tk.RAISED, bd=2)
    c1 = tk.Checkbutton(boxes, text='DBG', variable=DBGshow, onvalue=1, offvalue=0)
    c2 = tk.Checkbutton(boxes, text='INF', variable=INFshow, onvalue=1, offvalue=0)
    c3 = tk.Checkbutton(boxes, text='WRN', variable=WRNshow, onvalue=1, offvalue=0)
    c4 = tk.Checkbutton(boxes, text='ERR', variable=ERRshow, onvalue=1, offvalue=0)
    butt = Button(boxes, text='Filter', command=var_states)
    reverse_checkbox = tk.Checkbutton(boxes, text='Sort Reverse', variable=reverseOption, onvalue=1, offvalue=0)

    c1.grid(column=0, sticky='new', pady=5, padx=5)
    c2.grid(column=0, sticky='new', pady=5, padx=5)
    c3.grid(column=0, sticky='new', pady=5, padx=5)
    c4.grid(column=0, sticky='new', pady=5, padx=5)
    butt.grid(column = 0, sticky='new', pady=10)
    reverse_checkbox.grid(column=0, sticky='new', pady=5, padx=5)

    boxes.grid(row=0, column=2, sticky="nsew")
    txt_edit.grid(row=0, column=3, sticky="nsew")

#why not what

def open_file():
    filepath = askopenfilename(
        filetypes=[("All Files", "*.*")]
    )

    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)

    checkType = os.path.splitext(filepath)[1]
    if checkType == ".bin":
        with open(filepath, "rb") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
            window.title(f"File Open: - {filepath}")
    else:
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
            window.title(f"File Open: - {filepath}")



def save_file():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Saved File To - {filepath}")


def writeConfig():
    global dirPath
    print(dirPath.get())
    print(os.getcwd())
    f = open(os.getcwd() + "\configurations.txt", "w")
    f.write(dirPath.get())
    f.close()

    if dirPath.get() is not "":
        currentDirectoryLabel = tk.Label(text="Your current directory is: " + dirPath.get())
        # print(dirPath.get())
        # currentDirectoryLabel = tk.Label(text="Your current directory is set")
        currentDirectoryLabel.grid(row = 3, column = 0)



if not (os.path.exists("./configurations.txt")):
    configs = tk.Tk()

    dirPath = StringVar()
    configs.geometry("450x200")
    configs.title("Configurations")
    # Label is the text, entry is the empty box, button is the submit button
    directoryLabel = tk.Label(text="Directory")
    directoryLabel.grid(row=1, column=0)

    directoryEntry = tk.Entry(textvariable=dirPath)
    directoryEntry.grid(row=1, column=1)

    submitButton = tk.Button(text="Submit", command=writeConfig)
    submitButton.grid(row=2, column=0)

    configs.mainloop()

else:
    window = tk.Tk()
    window.title("Telemetry GUI")

    f = open(os.getcwd() + "\configurations.txt", "r")
    personalDirectoryPath = f.readline()
    print(personalDirectoryPath)

    fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

    btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
    btn_save = tk.Button(fr_buttons, text="Save File As", command=save_file)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)

    btn_parse_telemetry = tk.Button(fr_buttons, text="Parse Telemetry File", command=telem_parser)
    btn_parse_telemetry.grid(row=5, column=0, sticky="nwe", pady=50)
    btn_parse_smartlog = tk.Button(fr_buttons, text="Parse Smart Log", command = smartlog_parse)
    btn_parse_smartlog.grid(row=6, column=0, sticky="swe", pady=5)
    btn_parse_delllog = tk.Button(fr_buttons, text="Parse Dell Log")
    btn_parse_delllog.grid(row=7, column=0, sticky="swe", pady=5)
    btn_parse_errorlog = tk.Button(fr_buttons, text="Parse Error Log")
    btn_parse_errorlog.grid(row=8, column=0, sticky="swe", pady=5)
    btn_parse_persistentlog = tk.Button(fr_buttons, text="Parse Persistent Log")
    btn_parse_persistentlog.grid(row=9, column=0, sticky="swe", pady=5)
    btn_parse_asynceventsupport = tk.Button(fr_buttons, text="Asynchronous Event")
    btn_parse_asynceventsupport.grid(row=10, column=0, sticky="swe", pady=5)
    btn_parse_deviceselftest = tk.Button(fr_buttons, text="Run Device Self-Test")
    btn_parse_deviceselftest.grid(row=11, column=0, sticky="swe", pady=5)


    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit = tk.Text(window)
    txt_edit.grid(row=0, column=2, sticky="nsew")

    window.mainloop()


