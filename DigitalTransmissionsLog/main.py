# - Libraries
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from customtkinter import *
from CTkMenuBar import *

# - Directory and File Management
homeDir = Path.home()
documentsDir = homeDir / "Documents"
programDir = documentsDir / "Digital Transmissions Log"
programDir.mkdir(parents=True, exist_ok=True)
stationsFile = programDir / "stations.txt"
netsFile = programDir / "nets.txt"
operatorsFile = programDir / "operators.txt"
logsFile = programDir / "logs.txt"

initialStationsList = ["Kilo","Lima","Mike","November"]
initialNetsList = ["CMD1","CMD2","CMD3"]
initialOperatorsList = ["LCpl Schmuckatelli","PFC Devil Dog", "SSgt Pena"]
initialLogsList = ["2025/Oct/21<|>00:19:56<|>SSgt Pena<|>CMD1<|>Operator<|>User<|>This is an example output for you."]

def appendList(path: Path) -> list[str]:
    return path.read_text().splitlines()

def writeInitialList(path: Path, initial_list: list) -> None:
    with path.open("x") as file:
        for value in initial_list:
            file.write(f"{value}\n")

def initializeFile(path: Path, initial_list: list) -> list[str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        writeInitialList(path, initial_list)
    except FileExistsError:
        if path.stat().st_size == 0:
            writeInitialList(path, initial_list)
    return appendList(path)

stationsList = initializeFile(stationsFile, initialStationsList)
netsList = initializeFile(netsFile, initialNetsList)
operatorsList = initializeFile(operatorsFile, initialOperatorsList)
logsList = initializeFile(logsFile, initialLogsList)

# - Main UI
UI = CTk()
UI.title("Digital Transmissions Log")
UI.geometry("800x600")
UI.minsize(800, 600)
UI.focus_force()
set_default_color_theme("green")
set_appearance_mode("dark")

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
menuBar = CTkMenuBar(UI, bg_color = "#1e1f22", height=30, padx=20)
menuBar.add_cascade(text="Transmissions Log", postcommand=onMainClicked)
menuBar.add_cascade(text="Settings", postcommand=onSettingsClicked)
menuBar.add_cascade(text="About", postcommand=onAboutClicked)

# - Main Frame
mainFrame = CTkFrame(UI)
mainFrame.pack(side="top", fill="both", expand=True)
mainFrame.rowconfigure(0, weight=3, uniform="rows") #Row for topFrame
mainFrame.rowconfigure(1, weight=4, uniform="rows") #Row for bottomFrame
mainFrame.columnconfigure(0, weight=1)

# - Top Frame
topFrame = CTkFrame(mainFrame, corner_radius=0)
topFrame.grid(row=0, column=0, sticky="nsew")
topFrame.grid_columnconfigure(0, weight=4)
topFrame.grid_columnconfigure(1, weight=6)
topFrame.grid_rowconfigure(0, weight=1)

# - Top Frame Left
topFrameLeft = CTkFrame(topFrame, corner_radius=0)
topFrameLeft.grid(row=0, column=0, sticky='nsew')
topFrameLeft.grid_columnconfigure(0, weight=0)
topFrameLeft.grid_columnconfigure(1, weight=1, uniform="fields")
topFrameLeft.grid_columnconfigure(2, weight=0)
topFrameLeft.grid_columnconfigure(3, weight=1, uniform="fields")

#  - From Label and Selection
CTkLabel(topFrameLeft, text="From -").grid(row=0, column=0, padx=6, pady=8, sticky="w")
fromSelection = CTkComboBox(topFrameLeft, values=stationsList, state="readonly")
fromSelection.set(stationsList[0])
fromSelection.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

# - To Label and Selection
CTkLabel(topFrameLeft, text="To -").grid(row=0, column=2, padx=6, pady=8, sticky="w")
toSelection = CTkComboBox(topFrameLeft, values=stationsList, state="readonly")
toSelection.set(stationsList[0])
toSelection.grid(row=0, column=3, padx=10, pady=8, sticky="ew")

# - Net Label and Selection
CTkLabel(topFrameLeft, text="Net -").grid(row=1, column=0, padx=6, pady=8, sticky="w")
netSelection = CTkComboBox(topFrameLeft, values=netsList, state="readonly")
netSelection.set(netsList[0])
netSelection.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

# - Operator Label and Selection
CTkLabel(topFrameLeft, text="Operator -").grid(row=1, column=2, padx=6, pady=8, sticky="w")
operatorSelection = CTkComboBox(topFrameLeft, values=operatorsList, state="readonly")
operatorSelection.set(operatorsList[0])
operatorSelection.grid(row=1, column=3, padx=10, pady=8, sticky="ew")

# - Top Frame Right
topFrameRight = CTkFrame(topFrame, corner_radius=0)
topFrameRight.grid(row=0, column=1, sticky='nsew')
topFrameRight.grid_columnconfigure(0, weight=1)
topFrameRight.grid_columnconfigure(1, weight=0)
topFrameRight.grid_columnconfigure(2, weight=0)
topFrameRight.grid_rowconfigure(0, weight=1)

# - Remarks Label and Input
CTkLabel(topFrameRight, text="Remarks -").grid(row=1, column=1, padx=6, pady=8, sticky="e")
placeholderText = "Type remarks here..."
remarkInput = CTkTextbox(topFrameRight, text_color="grey")
remarkInput.grid(row=0, column=0, columnspan=3, padx=6, pady=6, sticky="nsew")
remarkInput.insert(INSERT, placeholderText)

def onInputFocus(_) -> None:
    currentText = remarkInput.get("1.0", "end").strip()
    if currentText == placeholderText:
        remarkInput.delete("1.0", END)
        remarkInput.configure(text_color="white")
remarkInput.bind("<FocusIn>", onInputFocus)

# - Preset Selection
CTkLabel(topFrameLeft, text="Presets -").grid(row=2, column=0, columnspan=2, padx=6, pady=8, sticky="w")
preset1Button = CTkButton(topFrameLeft, text="9-Line", command=None)
preset1Button.grid(row=3, column=0, columnspan=2, padx=6, pady=8, sticky="w")
preset1Button = CTkButton(topFrameLeft, text="Submit", command=None)
preset1Button.grid(row=4, column=0, columnspan=2, padx=6, pady=8, sticky="w")

# - Bottom Frame
bottomFrame = CTkFrame(mainFrame, corner_radius=0)
bottomFrame.grid(row=1, column=0, sticky="nsew")
bottomFrame.grid_columnconfigure(0, weight=1)
bottomFrame.grid_columnconfigure(1, weight=0, minsize=16)
bottomFrame.grid_rowconfigure(1, weight=1)

# - Bottom Frame Top
bottomFrameTop = CTkFrame(bottomFrame, corner_radius=0)
bottomFrameTop.grid(row=0, column=0, sticky="ew")

# - Bottom Frame Bottom
style = ttk.Style()
style.theme_use("alt")
style.configure("TScrollbar", background="#1e1f22", troughcolor="#2b2b2b")
canvas = tk.Canvas(bottomFrame, highlightthickness=0, bg="#1e1f22")
scrollBar = ttk.Scrollbar(bottomFrame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollBar.set)
canvas.grid(row=1, column=0, sticky="nsew")
scrollBar.grid(row=0, column=1, rowspan=2, sticky="ns")
scrollBar.configure(style="TScrollbar")

bottomFrameContent = CTkFrame(canvas, corner_radius=0)
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

cellLabelOptions = dict(anchor="nw", justify="left", bd=1, relief="solid", fg="white", font=("Roboto", 14))
def getCurrentLog():
    clearContent()
    with (open(logsFile, "r", encoding="utf-8") as file):
        lines = file.readlines()
        lines.reverse()
        for rowNumber, line in enumerate(lines):
            lineParts = [p.strip() for p in line.split("<|>")]
            bgColor = "#3b3b3b" if rowNumber % 2 == 0 else "#2b2b2b"
            for columnNumber, part in enumerate(lineParts):
                if columnNumber == 6:
                    part = part.replace("<||>", "\n")
                label = tk.Label(bottomFrameContent, text=part, bg=bgColor, **cellLabelOptions)
                label.grid(row=rowNumber, column=columnNumber, sticky="nsew")
                label.columnIndex = columnNumber
                cells.append(label)
    bottomFrameContent.update_idletasks()
    syncScrollRegion()
getCurrentLog()

def onSubmitClicked() -> None:
    currentText = remarkInput.get("1.0", END).strip()
    currentText = currentText.replace("\n", "<||>")
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
        outputString = "<|>".join(
            [currentDate, currentTime, currentOperator, currentNet, currentFrom, currentTo, currentText]
        )
        with logsFile.open("a") as file:
            print(outputString, file=file)
        remarkInput.delete("1.0", END)
        remarkInput.configure(text_color="grey")
        remarkInput.insert(INSERT, placeholderText)
        mainFrame.focus_set()
        getCurrentLog()

submitButton = CTkButton(topFrameRight, text="Submit", command=onSubmitClicked)
submitButton.grid(row=1, column=2, padx=6, pady=8, sticky="e")

# - Settings Frame
settingsFrame = CTkFrame(master=UI)
# - About Frame
aboutFrame = CTkFrame(master=UI)

UI.mainloop()