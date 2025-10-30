import customtkinter as ctk
from . import ui_functions as uifunc, file_handler as fh

class ZMISTWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.title("Z-MIST Template")
        self.iconbitmap(fh.resourcePath("dtl/appicon.ico"))
        self.resizable(False, False)
        self.initialLines = ["  #:", "  Z:","  M:","  I:","  S:","  T:"]
        self.results = ""
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        # --- UI ---
        self.uis = {"labels":{},"entries":{}}
        self.text = ["Z-MIST Number...", "Personal identifier...", "Mechanism of injury...",
                "Injury sustained...", "Signs and symptons...", "Treatment given..."]
        pad = {"padx": 5, "pady": 5}

        topLabel = ctk.CTkLabel(self, text="Enter Z-MIST Information", anchor="center")
        topLabel.grid(row=0, column=0, columnspan=2, sticky="ew")

        frame = ctk.CTkFrame(self, corner_radius=0)
        frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=3)

        for i in range(1,7):
            frame.grid_rowconfigure(i, weight=1)
            self.uis["labels"][f"label{i}"] = ctk.CTkLabel(frame, text=f"{self.initialLines[i-1].strip()}")
            self.uis["labels"][f"label{i}"].grid(row=i, column=0, padx=(5,0), sticky="ew")
            self.uis["entries"][f"entry{i}"] = ctk.CTkEntry(frame, text_color="grey", border_width=0)
            self.uis["entries"][f"entry{i}"].grid(row=i, column=1, **pad, sticky="ew")
            self.uis["entries"][f"entry{i}"].insert(ctk.INSERT, self.text[i-1])
            self.uis["entries"][f"entry{i}"].bind("<FocusIn>", lambda event, current_text=self.text[i-1]: uifunc.onInputFocusIn(event, current_text))
            self.uis["entries"][f"entry{i}"].bind("<FocusOut>", lambda event, current_text=self.text[i-1]: uifunc.onInputFocusOut(event, current_text))

        self.btn_cancel = ctk.CTkButton(self, text="Cancel", command=self.on_cancel)
        self.btn_cancel.grid(row=10, column=0, **pad, sticky="e")

        self.btn_ok = ctk.CTkButton(self, text="OK", command=self.on_ok)
        self.btn_ok.grid(row=10, column=1, **pad, sticky="w")

        self.bind("<Escape>", lambda _e: self.on_cancel())
        #self.bind("<Return>", lambda _e: self.on_ok())

        uifunc.centerOnMaster(self)
        self.grab_set()

    def on_ok(self):
        returnList = []
        for i,ui in enumerate(self.uis["entries"].values()):
            currentText = ui.get().strip()
            if currentText == "" or currentText == self.text[i]:
                returnList.append(f"{self.initialLines[i]} N/A")
            else:
                returnList.append(f"{self.initialLines[i]} {currentText}")
        self.results = returnList
        self.destroy()

    def on_cancel(self):
        self.destroy()
        return False

    def show(self):
        self.master.wait_window(self)
        return self.results