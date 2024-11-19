from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
from datetime import datetime, timedelta

players = players.get_active_players()
months_convert = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}
stats_weight = {
    "points": 1,
    "blocks": 4,
    "steals": 4,
    "assists": 2,
    "rebounds": 1,
    "turnovers": -2,
    "fgm": 2,
    "fga": -1,
    "ftm": 1,
    "fta": -1,
    "tpm": 1,
}
today = datetime.today()

spec_player = [player for player in players if player["full_name"] == "LeBron James"]
# [{'id': 1630170, 'full_name': 'Devin Vassell', 'first_name': 'Devin', 'last_name': 'Vassell', 'is_active': True}]
spec_player_id = spec_player[0]["id"]


def calculate_points(id, multiplier=0):
    games = get_games(id, 4)
    for week_games in games:
        week_points = (
            week_games["FGM"][:] * stats_weight["fgm"]
            + week_games["FGA"][:] * stats_weight["fga"]
            + week_games["FG3M"][:] * stats_weight["tpm"]
            + week_games["FTM"][:] * stats_weight["ftm"]
            + week_games["FTA"][:] * stats_weight["fta"]
            + week_games["REB"][:] * stats_weight["rebounds"]
            + week_games["AST"][:] * stats_weight["assists"]
            + week_games["STL"][:] * stats_weight["steals"]
            + week_games["BLK"][:] * stats_weight["blocks"]
            + week_games["TOV"][:] * stats_weight["turnovers"]
            + week_games["PTS"][:] * stats_weight["points"]
        )
        print(week_points)


def get_games(id, weeks=52):
    player_log = playergamelog.PlayerGameLog(player_id=id, season="2024")
    df_games = player_log.get_data_frames()[0]
    # ['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
    # 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
    # 'PLUS_MINUS', 'VIDEO_AVAILABLE']
    game_dates = df_games["GAME_DATE"][:]
    game_dates_converted = pd.Series(convert_date(i) for i in game_dates)
    df_games["GAME_DATE"] = game_dates_converted

    games = []
    max_date = today
    min_date = today - timedelta(weeks=1)
    while weeks > 0:
        games.append(
            df_games[
                (df_games["GAME_DATE"] <= max_date)
                & (df_games["GAME_DATE"] >= min_date)
            ]
        )
        max_date = min_date
        min_date = min_date - timedelta(weeks=1)
        weeks -= 1

    return games


# date = NOV 02, 2023
def convert_date(date):
    year = date[-5:]
    month = months_convert[date[:3]]
    day = date[4:6]
    converted_date = datetime(int(year), int(month), int(day))
    return converted_date


calculate_points(spec_player_id)
# print(convert_date("NOV 02, 2023"))
