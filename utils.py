import tkinter as tk
import datetime

def display_popup(entries_created):
    # create a popup window
    popup_window = tk.Tk()

    # set the title of the window
    popup_window.title("Popup Window")

    # set the size of the window
    popup_window.geometry("300x200")

    # add some text to the window
    if entries_created:
        popup_text = tk.Label(popup_window, text="Entries added to the db")
    else:
        popup_text = tk.Label(popup_window, text="Entries were not added to the db")
    popup_text.pack()

    # run the window
    popup_window.mainloop()


def convert_utc_to_cvt(utc_timestamp):
    from datetime import datetime, timedelta

    # Convert UTC timestamp to datetime object
    dt_utc = datetime.fromisoformat(utc_timestamp[:-1])

    # Calculate the time difference between CVT and UTC
    cvt_offset = timedelta(hours=-1)  # Standard Time

    # Convert UTC datetime object to CVT datetime object
    dt_cvt = dt_utc + cvt_offset

    # Format the CVT datetime object as a string
    cvt_timestamp = dt_cvt.isoformat() + 'Z'

    return cvt_timestamp




