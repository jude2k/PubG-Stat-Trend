import sqlite3
import json

# Global variable to store the database connection
db_conn = None

def connect_to_database():
    global db_conn
    if db_conn is None:
        db_conn = sqlite3.connect('game_stats.db')
        print('Connected to database')
    return db_conn

def close_database_connection():
    global db_conn
    if db_conn is not None:
        db_conn.close()
        db_conn = None
        print('Closed database connection')


def create_or_add_entries_in_db(data, match_id, created_at):
    # Create/reuse a connection to the database
    conn = connect_to_database()

    # Create a cursor object
    c = conn.cursor()




    # Check if the table exists
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='player_stats'")
    if c.fetchone()[0] == 0:
        # Create the table if it does not exist
        c.execute('''CREATE TABLE player_stats
                     (id INTEGER PRIMARY KEY,
                      player_name TEXT,
                      kills INTEGER,
                      assists INTEGER,
                      dbnos INTEGER,
                      total_damage REAL,
                      match_id TEXT,
                      created_at TEXT)''')



    try:
        # Insert the stats into the database
        for player_name in data:
            c.execute("SELECT * FROM player_stats WHERE match_id = ? AND player_name = ?", (match_id, player_name))
            rows = c.fetchall()
            if len(rows) == 0:
                print(f'Adding {match_id}')
                c.execute("INSERT INTO player_stats (player_name, kills, assists, dbnos, total_damage, match_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (player_name, int(data[player_name]['Kills']), int(data[player_name]['Assists']), int(data[player_name]['Dbnos']), data[player_name]['Total Damage'], match_id, created_at))
            else:
                print(f'Skipping match id {match_id}, already exists in table for the player {player_name}')
    except Exception as e:
        print(str(e))
        return False

    # Commit the changes and close the connection
    conn.commit()
    return True

def group_by_name_and_date(names):
    conn = connect_to_database()
    cursor = conn.cursor()

    query_temp = "CREATE TEMPORARY TABLE player_names (name TEXT)"
    cursor.execute(query_temp)

    # Insert each name into the player_names table
    for name in names:
        cursor.execute('INSERT INTO player_names VALUES (?)', (name,))

    # Commit the changes
    conn.commit()

    # Define the SQL query
    query = "SELECT json_group_array(json_object('date', date, 'player_name', player_name, 'Average kills', kills, 'Average assists', assists, 'Average dbnos', dbnos, 'Average damage', average_damage)) AS data FROM (SELECT strftime('%Y-%m-%d', created_at) AS date, player_name, AVG(kills) AS kills, AVG(assists) AS assists, AVG(dbnos) AS dbnos, AVG(total_damage) AS average_damage FROM player_stats WHERE player_name IN (SELECT name FROM player_names) AND match_id IN (SELECT match_id FROM player_stats WHERE player_name IN (SELECT name FROM player_names) GROUP BY match_id HAVING COUNT(DISTINCT player_name) = (SELECT COUNT(*) FROM player_names)) GROUP BY date, player_name) t;"

    cursor.execute(query)

    row = cursor.fetchone()
    print(row)
    #data = {'date': entry[0], 'player_name': entry[1], 'kills': entry[2], 'assists': entry[3], 'dbnos': entry[4], 'total_damage': entry[5]}
    data = json.loads(row[0])
    cursor.close()

    return data

# # Register the function with SQLite
# conn = sqlite3.connect('your_database.db')
# conn.create_function("group_by_name_and_date", 0, group_by_name_and_date)
# conn.close()
#
# # Call the function
# conn = sqlite3.connect('your_database.db')
# cursor = conn.cursor()
# json_data = cursor.execute("SELECT group_by_name_and_date()").fetchone()[0]
# print(json_data)
# cursor.close()
# conn.close()