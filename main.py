import datetime
import tkinter as tk
import sys
from chicken_dinner.pubgapi import PUBG
from graphs import generate_damage_trend, generate_trend_for_kills_assists_dbnos, show_plot_windows
from db import create_or_add_entries_in_db, close_database_connection, group_by_name_and_date
from utils import convert_utc_to_cvt

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNTNiNWI1MC03ZjA2LTAxM2ItNWIwYS00MzEzOWVkOWU4NmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjc0NjY5MTQ4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJvZ2RhbmFwcCJ9.saoty3AwtsqfJFVxvssaU1oUJS8jNLC22fCOf7exC5o"
pubg = PUBG(api_key=api_key, shard="steam")


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def on_close():
    root.destroy()
    print("Window closed")


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_close)
root.title("Pubg Trend Stats")

# Set window size
width = 400
height = 300

# Center window
center_window(root, width, height)

data = []
def get_data():
    global data
    data = [entry.get() for entry in [entry1, entry2, entry3, entry4] if entry.get()]
    root.quit()

# configure the rows and columns to expand or contract
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

label1 = tk.Label(root, text="Player 1 name:")
label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

label2 = tk.Label(root, text="Player 2 name:")
label2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

label3 = tk.Label(root, text="Player 3 name:")
label3.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

label4 = tk.Label(root, text="Player 4 name:")
label4.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
entry4 = tk.Entry(root)
entry4.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

def submit():
    data = get_data()
    root.destroy()

button = tk.Button(root, text="Submit", command=submit)
button.grid(row=4, column=0, columnspan=2)

root.deiconify()

root.wait_window(root)

if len(data) < 1:
    sys.exit(1)

# Creates a Players instance (iterable of Player instances)
players = pubg.players_from_names(data)

shared_matches = players.shared_matches()


# Get the current date and time in UTC
current_time = datetime.datetime.utcnow()

# Calculate the date and time 24 hours ago
delta = datetime.timedelta(hours=200)
start_time = current_time - delta

# Format the start and end times as ISO 8601 strings
start_time_str = start_time.isoformat() + "Z"
end_time_str = current_time.isoformat() + "Z"


for i, player in enumerate(players):
    globals()[f"player{i+1}"] = player

matches_count = 0

for match in shared_matches:

    stats = []

    current_match = pubg.match(match)
    if start_time_str <= current_match.created_at <= end_time_str:
        if current_match.game_mode == 'squad-fpp':
            rosters = current_match.rosters
            for roster in rosters:
                if player1.name in roster.player_names:
                    found_roster = roster
                    matches_count += 1
            # Participant from a roster
            roster_participants = found_roster.participants
            match_id = current_match.match_id
            created_at = current_match.created_at

            player_vars = {}
            for i, player in enumerate(players):
                player_vars[player.name] = f"player{i + 1}"

            stats = []
            player_stats = {}
            for participant in roster_participants:
                for player_name, player_var in player_vars.items():
                    if player_name in participant.name:
                        player_stats[player_name] = {
                            'Kills': participant.stats.get('kills'),
                            'Assists': participant.stats.get('assists'),
                            'Dbnos': participant.stats.get('dbnos'),
                            'Total Damage': participant.stats.get('damage_dealt')
                        }
            stats.append(player_stats)


            entries_created = create_or_add_entries_in_db(stats[0], match_id, convert_utc_to_cvt(created_at))

group = group_by_name_and_date(data)

close_database_connection()

show_plot_windows(generate_damage_trend(group), generate_trend_for_kills_assists_dbnos(group))