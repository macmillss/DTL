# - Libraries
import datetime
import tkinter as tk
import dtl
from dtl import file_handler as fh
import customtkinter as ctk
import CTkMenuBar as ctkMenu
from PIL import Image

initialStationsList = ["Kilo","Lima","Mike","November"]
initialNetsList = ["CMD1","CMD2","CMD3"]
initialOperatorsList = ["LCpl Schmuckatelli","PFC Devil Dog", "SSgt Pena"]
initialLogsList = ["2025/Oct/21⟺00:19:56⟺SSgt Pena⟺CMD1⟺Operator⟺User⟺This is an example output for you."]

stationsList = fh.initializeFile(fh.stationsFile, initialStationsList)
fh.fileDictionary["stations"]["list"] = stationsList
netsList = fh.initializeFile(fh.netsFile, initialNetsList)
fh.fileDictionary["nets"]["list"] = netsList
operatorsList = fh.initializeFile(fh.operatorsFile, initialOperatorsList)
fh.fileDictionary["operators"]["list"] = operatorsList
logsList = fh.initializeFile(fh.logsFile, initialLogsList)

# - Main UI
UI = ctk.CTk()
UI.title("Digital Transmissions Log")
UI.iconbitmap(fh.resourcePath("dtl/appicon.ico"))
UI.geometry("800x600")
UI.minsize(800, 600)
UI.focus_force()
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")

# - Menu Bar -> Functions
def onMainClicked() -> None:
    if mainFrame.winfo_ismapped():
        pass
    else:
        settingsFrame.pack_forget()
        aboutFrame.pack_forget()
        mainFrame.pack(side="top", fill="both", expand=True)

def onSettingsClicked() -> None:
    if settingsFrame.winfo_ismapped():
        pass
    else:
        mainFrame.pack_forget()
        aboutFrame.pack_forget()
        settingsFrame.pack(side="top", fill="both", expand=True)

def onAboutClicked() -> None:
    if aboutFrame.winfo_ismapped():
        pass
    else:
        mainFrame.pack_forget()
        settingsFrame.pack_forget()
        aboutFrame.pack(side="top", fill="both", expand=True)

# - Menu Bar -> UI Elements
menuBar = ctkMenu.CTkMenuBar(UI, bg_color = "#1e1f22", height=30, padx=20)
menuBar.add_cascade(text="Transmissions Log", postcommand=onMainClicked)
menuBar.add_cascade(text="Settings", postcommand=onSettingsClicked)
menuBar.add_cascade(text="About", postcommand=onAboutClicked)

# - Main Frame
mainFrame = ctk.CTkFrame(UI)
mainFrame.pack(side="top", fill="both", expand=True)
mainFrame.rowconfigure(0, weight=3, uniform="rows") #Row for topFrame
mainFrame.rowconfigure(1, weight=4, uniform="rows") #Row for bottomFrame
mainFrame.columnconfigure(0, weight=1)

# - Top Frame
topFrame = ctk.CTkFrame(mainFrame, corner_radius=0)
topFrame.grid(row=0, column=0, sticky="nsew")
topFrame.grid_columnconfigure(0, weight=4)
topFrame.grid_columnconfigure(1, weight=6)
topFrame.grid_rowconfigure(0, weight=1)

# - Top Frame Left
topFrameLeft = ctk.CTkFrame(topFrame, corner_radius=0)
topFrameLeft.grid(row=0, column=0, sticky='nsew')
topFrameLeft.grid_columnconfigure(0, weight=0)
topFrameLeft.grid_columnconfigure(1, weight=1, uniform="fields")
topFrameLeft.grid_columnconfigure(2, weight=0)
topFrameLeft.grid_columnconfigure(3, weight=1, uniform="fields")

#  - From Label and Selection
ctk.CTkLabel(topFrameLeft, text="From -").grid(row=0, column=0, padx=6, pady=8, sticky="w")
fromSelection = ctk.CTkComboBox(topFrameLeft, values=stationsList, state="readonly")
fromSelection.set(stationsList[0])
fh.fileDictionary["stations"]["combobox"] = fromSelection
fromSelection.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

# - To Label and Selection
ctk.CTkLabel(topFrameLeft, text="To -").grid(row=0, column=2, padx=6, pady=8, sticky="w")
toSelection = ctk.CTkComboBox(topFrameLeft, values=stationsList, state="readonly")
toSelection.set(stationsList[0])
fh.fileDictionary["stations"]["combobox1"] = toSelection
toSelection.grid(row=0, column=3, padx=10, pady=8, sticky="ew")

# - Net Label and Selection
ctk.CTkLabel(topFrameLeft, text="Net -").grid(row=1, column=0, padx=6, pady=8, sticky="w")
netSelection = ctk.CTkComboBox(topFrameLeft, values=netsList, state="readonly")
fh.fileDictionary["nets"]["combobox"] = netSelection
netSelection.set(netsList[0])
netSelection.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

# - Operator Label and Selection
ctk.CTkLabel(topFrameLeft, text="Operator -").grid(row=1, column=2, padx=6, pady=8, sticky="w")
operatorSelection = ctk.CTkComboBox(topFrameLeft, values=operatorsList, state="readonly")
fh.fileDictionary["operators"]["combobox"] = operatorSelection
operatorSelection.set(operatorsList[0])
operatorSelection.grid(row=1, column=3, padx=10, pady=8, sticky="ew")

# - Top Frame Right
topFrameRight = ctk.CTkFrame(topFrame, corner_radius=0)
topFrameRight.grid(row=0, column=1, sticky='nsew')
topFrameRight.grid_columnconfigure(0, weight=1)
topFrameRight.grid_columnconfigure(1, weight=0)
topFrameRight.grid_columnconfigure(2, weight=0)
topFrameRight.grid_rowconfigure(0, weight=1)

# - Remarks Label and Input
ctk.CTkLabel(topFrameRight, text="Remarks -").grid(row=1, column=1, padx=6, pady=8, sticky="e")
placeholderText = "Type remarks here..."
remarkInput = ctk.CTkTextbox(topFrameRight, text_color="grey")
remarkInput.grid(row=0, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")
remarkInput.insert(ctk.INSERT, placeholderText)
remarkInput.bind("<FocusIn>", lambda event: dtl.onInputFocusIn(event, placeholderText))
remarkInput.bind("<FocusOut>", lambda event: dtl.onInputFocusOut(event, placeholderText))

# - Preset Selection
ctk.CTkLabel(topFrameLeft, text="Presets -").grid(row=2, column=0, columnspan=2, padx=6, pady=8, sticky="w")
def setPresetText(value, header_text):
    if not value == False:
        currentFrom = fromSelection.get()
        outputString = f"{currentFrom} {header_text}\n"
        for text in value:
            outputString += f"{text}\n"
            remarkInput.delete("1.0", "end")
            remarkInput.insert(ctk.INSERT, outputString)
            remarkInput.configure(text_color="white")
            remarkInput.focus_force()

def open9LineWindow():
    dlg = dtl.NineLineWindow(UI)
    value = dlg.show()  # blocks here until the dialog is closed
    setPresetText(value, "called the following 9-Line:")

def openZMISTWindow():
    dlg = dtl.ZMISTWindow(UI)
    value = dlg.show()  # blocks here until the dialog is closed
    setPresetText(value, "called the following Z-MIST:")

preset1Button = ctk.CTkButton(topFrameLeft, text="9-Line", command=open9LineWindow)
preset1Button.grid(row=3, column=0, columnspan=2, padx=6, pady=8, sticky="w")

preset2Button = ctk.CTkButton(topFrameLeft, text="Z-MIST", command=openZMISTWindow)
preset2Button.grid(row=4, column=0, columnspan=2, padx=6, pady=8, sticky="w")

# - Bottom Frame
bottomFrame = ctk.CTkFrame(mainFrame, corner_radius=0)
bottomFrame.grid(row=1, column=0, sticky="nsew")
bottomFrame.grid_columnconfigure(0, weight=1)
bottomFrame.grid_columnconfigure(1, weight=0, minsize=16)
bottomFrame.grid_rowconfigure(1, weight=1)

# - Bottom Frame Top
bottomFrameTop = ctk.CTkFrame(bottomFrame, corner_radius=0)
bottomFrameTop.grid(row=0, column=0, sticky="ew")

# - Bottom Frame Bottom
canvas = tk.Canvas(bottomFrame, highlightthickness=0, bg="#1e1f22")
scrollBar = ctk.CTkScrollbar(bottomFrame, command=canvas.yview, bg_color="#2b2b2b")
canvas.grid(row=0, column=1, sticky="nsew")
canvas.configure(yscrollcommand=scrollBar.set)
canvas.grid(row=1, column=0, sticky="nsew")
scrollBar.grid(row=0, column=1, rowspan=2, sticky="ns")

bottomFrameContent = ctk.CTkFrame(canvas, corner_radius=0)
window_id = canvas.create_window((0, 0), window=bottomFrameContent, anchor="nw")

COLUMN_TEXT = ["Date", "Time", "Operator", "Net", "From", "To", "Remark"]
COLUMN_WEIGHTS = [4, 3, 5, 4, 4, 4, 12]
COLUMN_FRACTION = tuple(w / sum(COLUMN_WEIGHTS) for w in COLUMN_WEIGHTS)

headerLabelOptions = dict(anchor="w", justify="left", bd=1, relief="solid", bg="#1e1f22", fg="white", font=("Roboto", 14))
for i in range(0,7):
    bottomFrameTop.grid_columnconfigure(i, weight=COLUMN_WEIGHTS[i], uniform="cols")
    bottomFrameContent.grid_columnconfigure(i, weight=COLUMN_WEIGHTS[i], uniform="cols")
    tk.Label(bottomFrameTop, text=COLUMN_TEXT[i], **headerLabelOptions).grid(row=0, column=i, sticky="nsew")

# - Canvas Mouse Logic
def onWheel(e): canvas.yview_scroll(-1 * int(e.delta / 120), "units")
def onWheelUp(_):   canvas.yview_scroll(-3, "units")
def onWheelDown(_):   canvas.yview_scroll(3, "units")
canvas.bind("<Enter>", lambda e: (
    canvas.bind_all("<MouseWheel>", onWheel),
    canvas.bind_all("<Button-4>", onWheelUp),
    canvas.bind_all("<Button-5>", onWheelDown)
))
canvas.bind("<Leave>", lambda e: (
    canvas.unbind_all("<MouseWheel>"),
    canvas.unbind_all("<Button-4>"),
    canvas.unbind_all("<Button-5>")
))

# - Logs Logic
cells = []

def updateWrap(total_width) -> None:
    pad = 12
    for label in cells:
        fraction = COLUMN_FRACTION[label.columnIndex]
        label.configure(wraplength=max(50, int(total_width * fraction) - pad))

def syncScrollRegion(_=None) -> None:
    bottomFrameContent.update_idletasks()
    content_h = bottomFrameContent.winfo_reqheight()
    content_w = bottomFrameContent.winfo_reqwidth()
    view_h    = canvas.winfo_height()
    canvas.itemconfigure(window_id, width=canvas.winfo_width())
    canvas.configure(scrollregion=(0, 0, content_w, max(content_h, view_h)))
    if content_h <= view_h:
        canvas.yview_moveto(0.0)
    updateWrap(canvas.winfo_width())
bottomFrameContent.bind("<Configure>", syncScrollRegion)
canvas.bind("<Configure>", lambda e: syncScrollRegion())

def clearContent():
    for child in bottomFrameContent.winfo_children():
        child.destroy()
    cells.clear()
    bottomFrameContent.update_idletasks()
    syncScrollRegion()

def copyToClipboard(text):
    UI.clipboard_clear()
    UI.clipboard_append(text)
    UI.update()

rightClickMenu = tk.Menu(UI, tearoff=False, font=("Roboto", 14), foreground="white", activebackground="#2fa572", background="#1e1f22")
rightClickMenu.add_command(label="Copy")

def rightClickLog(event,text):
    rightClickMenu.entryconfigure(0, command=lambda: copyToClipboard(text))
    try:
        rightClickMenu.tk_popup(event.x_root, event.y_root)
    finally:
        rightClickMenu.grab_release()

cellLabelOptions = dict(anchor="nw", justify="left", bd=1, relief="solid", fg="white", font=("Roboto", 14))
def getCurrentLog():
    clearContent()
    with (open(fh.logsFile, "r", encoding="utf-8") as file):
        lines = file.readlines()
        lines.reverse()
        for rowNumber, line in enumerate(lines):
            lineParts = [p.strip() for p in line.split(fh.COLUMN_SEPARATOR)]
            bgColor = "#3b3b3b" if rowNumber % 2 == 0 else "#2b2b2b"
            for columnNumber, part in enumerate(lineParts):
                if columnNumber == 6:
                    part = part.replace(fh.BODY_SEPARATOR, "\n")
                elif columnNumber == 7:
                    break
                label = tk.Label(bottomFrameContent, text=part, bg=bgColor, **cellLabelOptions)
                label.grid(row=rowNumber, column=columnNumber, sticky="nsew")
                label.columnIndex = columnNumber
                cells.append(label)
                if columnNumber == 6:
                    label.bind("<Button-3>",lambda event, current_text=part: rightClickLog(event, current_text))
    bottomFrameContent.update_idletasks()
    syncScrollRegion()
getCurrentLog()

def onSubmitClicked() -> None:
    currentText = remarkInput.get("1.0", "end").strip()
    currentText = currentText.replace("\n", fh.BODY_SEPARATOR)
    if currentText == "" or currentText == placeholderText:
        return
    else:
        currentDateTime = datetime.datetime.now()
        currentDate = currentDateTime.strftime("%Y/%b/%d")
        currentTime = currentDateTime.strftime("%H:%M:%S")
        currentOperator = operatorSelection.get()
        currentNet = netSelection.get()
        currentFrom = fromSelection.get()
        currentTo = toSelection.get()
        outputString = fh.COLUMN_SEPARATOR.join(
            [currentDate, currentTime, currentOperator, currentNet, currentFrom, currentTo, currentText]
        )
        with fh.logsFile.open("a", encoding="utf-8") as file:
            print(outputString, file=file)
        remarkInput.delete("1.0", "end")
        remarkInput.configure(text_color="grey")
        remarkInput.insert("1.0", placeholderText)
        mainFrame.focus_set()
        getCurrentLog()

submitButton = ctk.CTkButton(topFrameRight, text="Submit", command=onSubmitClicked)
submitButton.grid(row=1, column=2, padx=6, pady=8, sticky="e")

# - Settings Frame
settingsFrame = ctk.CTkFrame(master=UI)
settingsFrame.grid_columnconfigure(0, weight=1)
settingsFrame.grid_columnconfigure(1, weight=1)
settingsFrame.grid_columnconfigure(2, weight=1)
addIcon = ctk.CTkImage(dark_image=Image.open(fh.resourcePath("dtl/add.png")))
trashIcon = ctk.CTkImage(dark_image=Image.open(fh.resourcePath("dtl/trash.png")))

def addToList(section):
    dialog = ctk.CTkInputDialog(text=f"Enter your custom {section} entry:", title="Input Dialog")
    dialog.iconbitmap(fh.resourcePath("dtl/appicon.ico"))
    dialog.title(f"{section.title()} Entry")
    user_input = dialog.get_input()
    if user_input:
        user_input.strip()
        frameAdd(section, user_input)
        section_list = fh.fileDictionary[section]["list"]
        section_list.append(user_input)
        fh.fileDictionary[section]["combobox"].configure(values=section_list)
        if section == "stations":
            fh.fileDictionary[section]["combobox1"].configure(values=section_list)
        with fh.fileDictionary[section]["file"].open("a", encoding="utf-8") as file:
            print(user_input, file=file)

def removeFromList(section, frame, value):
    section_list = fh.fileDictionary[section]["list"]
    frame.destroy()
    section_list.remove(value)
    fh.fileDictionary[section]["combobox"].configure(values=section_list)
    if section == "stations":
        fh.fileDictionary[section]["combobox1"].configure(values=section_list)
    fh.removeValueFromFile(fh.fileDictionary[section]["file"], value)

def frameAdd(section, item):
    main_frame = fh.fileDictionary[section]["mainframe"]
    frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
    frame.pack(side="top", fill="x", padx=5, pady=1)
    frame.label = ctk.CTkLabel(frame, text=item, wraplength=160, anchor="w")
    frame.label.pack(side="left", fill="x", padx=5, pady=1)
    frame.removeButton = ctk.CTkButton(frame, command=lambda current_frame=frame, current_item=item: removeFromList(section, current_frame, current_item),text="", fg_color="transparent", image=trashIcon, width=25)
    frame.removeButton.pack(side="right")

def frameGenerate(section):
    section_list = fh.fileDictionary[section]["list"]
    for item in section_list:
        frameAdd(section, item)

stationsTopFrame = ctk.CTkFrame(master=settingsFrame, fg_color="transparent")
stationsTopFrame.grid(row=0, column=0, padx= 5, sticky="nsew")
ctk.CTkLabel(stationsTopFrame, text="Stations / Callsigns -", anchor="w").pack(side="left")
addStationButton = ctk.CTkButton(stationsTopFrame, command=lambda: addToList("stations"), text="", fg_color="transparent", image=addIcon, width=25)
addStationButton.pack(side="right")
stationsFrame = ctk.CTkScrollableFrame(master=settingsFrame)
fh.fileDictionary["stations"]["mainframe"] = stationsFrame
stationsFrame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
frameGenerate("stations")

netsTopFrame = ctk.CTkFrame(master=settingsFrame, fg_color="transparent")
netsTopFrame.grid(row=0, column=1, padx= 5, sticky="nsew")
ctk.CTkLabel(netsTopFrame, text="Nets / Transmission System -", anchor="w").pack(side="left")
addNetButton = ctk.CTkButton(netsTopFrame, command=lambda: addToList("nets"), text="", fg_color="transparent", image=addIcon, width=25)
addNetButton.pack(side="right")
netsFrame = ctk.CTkScrollableFrame(master=settingsFrame)
fh.fileDictionary["nets"]["mainframe"] = netsFrame
netsFrame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
frameGenerate("nets")

operatorsTopFrame = ctk.CTkFrame(master=settingsFrame, fg_color="transparent")
operatorsTopFrame.grid(row=0, column=2, padx= 5, sticky="nsew")
ctk.CTkLabel(operatorsTopFrame, text="Operators / Watchstander -", anchor="w").pack(side="left")
addOperatorButton = ctk.CTkButton(operatorsTopFrame, command=lambda: addToList("operators"), text="", fg_color="transparent", image=addIcon, width=25)
addOperatorButton.pack(side="right")
operatorsFrame = ctk.CTkScrollableFrame(master=settingsFrame)
fh.fileDictionary["operators"]["mainframe"] = operatorsFrame
operatorsFrame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
frameGenerate("operators")

# - About Frame
aboutFrame = ctk.CTkFrame(master=UI)
ctk.CTkLabel(aboutFrame, text="Digital Transmissions Log").pack(side="top", fill="x")
ctk.CTkLabel(aboutFrame, text="About This App").pack(side="top", fill="x", pady=(100,5))
ctk.CTkLabel(aboutFrame, wraplength=700, text="This application was developed by a SOCS-C who has spent countless watches managing stacks of logbooks or battling clunky Excel sheets during high-tempo operations. It was built from the hard-earned experience of trying to maintain accurate, standardized reports amid shifting taskings, heavy comms traffic, and relentless time pressure. The system cuts through that chaos by providing standardized reporting formats and drastically reducing the time spent on manual logging—allowing watchstanders to stay focused on the fight and the mission at hand.").pack(side="top", fill="x")
ctk.CTkLabel(aboutFrame, text="Version 2025.10.26").pack(side="bottom", fill="x")

UI.mainloop()