import matplotlib.pyplot as plt
import pandas as pd

def generate_damage_trend(data):
    df = pd.DataFrame(data)

    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # group the data by player_name and date, and sum the total_damage
    grouped = df.groupby(['player_name', 'date'])['Average damage'].sum().reset_index()

    # pivot the data to have each player_name as a column
    pivoted = grouped.pivot(index='date', columns='player_name', values='Average damage')

    # plot the data
    pivoted.plot(figsize=(10, 6))
    plt.xlabel('Date')
    plt.ylabel('Average Damage')
    plt.title('Trend for Average Damage by Player Name')
    window = plt.gcf()
    return window

def generate_trend_for_kills_assists_dbnos(data):
    # read in the data
    df = pd.DataFrame(data)

    # create a list of unique player names
    players = df['player_name'].unique()

    # create subplots for each metric
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12))

    # set titles for each subplot
    axes[0].set_title('Average Kills')
    axes[1].set_title('Average Assists')
    axes[2].set_title('Average DBNOs')

    # iterate over the players and plot their data on the corresponding subplot
    for player in players:
        player_data = df[df['player_name'] == player]
        axes[0].plot(player_data['date'], player_data['Average kills'], label=player)
        axes[1].plot(player_data['date'], player_data['Average assists'], label=player)
        axes[2].plot(player_data['date'], player_data['Average dbnos'], label=player)

    # add legends to the subplots
    axes[0].legend()
    axes[1].legend()
    axes[2].legend()

    # set common x-axis label and tick parameters
    fig.text(0.5, 0.04, 'Date', ha='center')
    fig.subplots_adjust(hspace=0.3)
    plt.xticks(rotation=45)
    window = plt.gcf()
    # display the plot
    return window


def show_plot_windows(window1, window2):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.axis('off')
    ax2.axis('off')
    plt.close()
    plt.show()