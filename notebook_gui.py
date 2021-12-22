import tkinter
from tkinter import ttk

WIN_WIDTH = 1000
WIN_HEIGHT = 600

def read_files():
    ua = open('assets/week12_ua.txt', 'r').readlines()
    ip = open('assets/week12_ip.txt', 'r').readlines()
    summary = open('assets/week12_summary.txt', 'r').readlines()
    return ua, ip, summary



def config_scrollbar(frame, horizontal=False):
    if horizontal:
        scrollbar = tkinter.Scrollbar(frame, orient = tkinter.HORIZONTAL)
        scrollbar.pack(side = tkinter.BOTTOM, fill = tkinter.X)
    else:
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
    
    return scrollbar

def create_frame(notebook, title):
    frame = tkinter.Frame (notebook, width=WIN_WIDTH, height=WIN_HEIGHT)
    frame.pack(fill = 'both', expand = True)
    yscrollbar = config_scrollbar(frame)
    xscrollbar = config_scrollbar(frame, True)
    notebook.add(frame, text=title)
    return frame, yscrollbar, xscrollbar

def create_listbox_and_display_text (frame, yscrollbar, xscrollbar, lines):
    display = tkinter.Listbox(frame, yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set, width=WIN_WIDTH, height=WIN_HEIGHT, font='TkFixedFont')
    for line in lines:
        display.insert(tkinter.END, line)
        
    display.pack()
    return display

def main():
    # Reading the Data
    ua, ip, summary = read_files()
    
    # Constructing the Window 
    window = tkinter.Tk()
    window.title("Display Logs")
    window.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    
    # Configuring the TextBox Widget
    tabs = ttk.Notebook(window, width=WIN_WIDTH, height=WIN_HEIGHT)
    tabs.pack(fill = "both", expand = True)
   
    # Configuring its scroll bars -  Horizotal and vertical    
    frame_summary, yscrollbar_summary, xscrollbar_summary = create_frame(tabs, "Summary")
    frame_ua, yscrollbar_ua, xscrollbar_ua = create_frame(tabs, "User Agent Count")
    frame_ip, yscrollbar_ip, xscrollbar_ip = create_frame(tabs, "IP Address Count")

    # Displaying the Text Box 
    display_ua = create_listbox_and_display_text(frame_ua, yscrollbar_ua, xscrollbar_ua, ua)
    display_ip = create_listbox_and_display_text(frame_ip, yscrollbar_ip, xscrollbar_ip, ip)
    display_summary = create_listbox_and_display_text(frame_summary, yscrollbar_summary, xscrollbar_summary, summary)
    yscrollbar_ua.config(command = display_ua.yview); yscrollbar_ip.config (command = display_ip.yview); yscrollbar_summary.config(command = display_summary.yview)
    xscrollbar_ua.config(command = display_ua.xview), xscrollbar_ip.config (command = display_ip.xview); xscrollbar_summary.config(command = display_summary.xview)

    window.mainloop()

if __name__ == "__main__":
    main()


