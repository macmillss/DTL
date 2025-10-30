import customtkinter as ctk

def onInputFocusIn(event,placeholder_text) -> None:
    widget = event.widget.master
    if isinstance(widget, ctk.CTkTextbox):
        currentText = widget.get("1.0", "end").strip()
        if currentText == placeholder_text:
            widget.delete("1.0", "end")
            widget.configure(text_color="white")
    elif isinstance(widget, ctk.CTkEntry):
        currentText = widget.get().strip()
        if currentText == placeholder_text:
            widget.delete(0, "end")
            widget.configure(text_color="white")

def onInputFocusOut(event,placeholder_text) -> None:
    widget = event.widget.master
    if isinstance(widget, ctk.CTkTextbox):
        currentText = widget.get("1.0", "end").strip()
        if currentText == "":
            widget.delete("1.0", "end")
            widget.insert(ctk.INSERT, placeholder_text)
            widget.configure(text_color="grey")
    elif isinstance(widget, ctk.CTkEntry):
        currentText = widget.get().strip()
        if currentText == "":
            widget.delete(0, "end")
            widget.insert(ctk.INSERT, placeholder_text)
            widget.configure(text_color="grey")

def centerOnMaster(ui):
    ui.update_idletasks()
    mx = ui.master.winfo_rootx()
    my = ui.master.winfo_rooty()
    mw = ui.master.winfo_width()
    mh = ui.master.winfo_height()
    w = ui.winfo_reqwidth()
    h = ui.winfo_reqheight()
    if mw <= 1 and mh <= 1:
        ui.geometry("+%d+%d" % (mx + 80, my + 80))
    else:
        x = mx + (mw - w) // 2
        y = my + (mh - h) // 2
        ui.geometry(f"+{x}+{y}")