import pandas as pd
import numpy as np
from nba_api.stats.endpoints import playbyplayv3, leaguegamefinder
from pathlib import Path
import time
from tqdm import tqdm

def parse_clock(clock_str):
    """
    Parse ISO 8601 duration string like 'PT08M11.00S' to total seconds remaining.
    
    Examples:
        parse_clock('PT08M11.00S') -> 491.0
        parse_clock('PT00M30.00S') -> 30.0
        parse_clock('PT12M00.00S') -> 720.0
    """
    # Strip the 'PT' prefix and split on M
    parts = clock_str.replace('PT', '').split('M')

    # Parse mins and secs and convert to float
    mins = float(parts[0])
    secs = float(parts[1].replace('S', ''))

    # Return total seconds (minutes * 60 + seconds)
    seconds = (mins * 60) + secs
    return seconds

def enrich_free_throws(pbp):
    """
    Take a raw play-by-play dataframe (one game) and return a dataframe of
    free throws enriched with crunch-time flags and other useful columns.
    
    Parameters
    ----------
    pbp : pd.DataFrame
        Raw play-by-play from playbyplayv3, must include columns:
        'actionType', 'description', 'clock', 'period', 'scoreHome', 
        'scoreAway', 'location', 'personId', 'playerName'.
    
    Returns
    -------
    pd.DataFrame
        Free throw rows with added columns:
        - clock_seconds: seconds remaining in period (float)
        - made: True if FT was made, False if missed (bool)
        - margin: absolute score margin at time of FT (int)
        - is_crunch: True if FT meets crunch-time criteria (bool)
    """
    # forward fill scores
    pbp['scoreHome'] = pbp['scoreHome'].replace('', np.nan).ffill().fillna(0).astype(int)
    pbp['scoreAway'] = pbp['scoreAway'].replace('', np.nan).ffill().fillna(0).astype(int)

    # filter free throws
    fts = pbp[pbp['actionType'] == 'Free Throw'].copy()

    # convert time remaining to seconds
    fts['clock_seconds'] = fts['clock'].apply(parse_clock)

    # identify made free throws
    fts['made'] = ~fts['description'].str.startswith('MISS')

    # calculate margin
    fts['margin'] = (fts['scoreHome'] - fts['scoreAway']).abs()

    # define crunch time
    fts['is_crunch'] = (
    (fts['period'] >= 4) &
    (fts['clock_seconds'] <= 300) &
    (fts['margin'] <= 5)
    )
    return fts

def get_season_game_ids(season):
    """
    Takes a season id and lists all game ids for the season
    
    Parameters
    ----------
    season : str
        ex: '2025-26'
    
    Returns
    -------
    list
        List of game ids
    """
    gamefinder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable='Regular Season',
        league_id_nullable='00'
    )

    games = gamefinder.get_data_frames()[0]
    game_ids = games['GAME_ID'].unique().tolist()
    return game_ids

def pull_and_save_pbp(game_id, output_dir, sleep_seconds=0.6):
    """
    Pull play-by-play for one game and save to disk. 
    Skips if the file already exists.
    
    Parameters
    ----------
    game_id : str
    output_dir : Path
        Directory to save the file in. Filename will be {game_id}.csv.
    sleep_seconds : float
        Seconds to sleep AFTER the API call (rate limiting). 
        Only applies if we actually called the API.
    
    Returns
    -------
    str
        One of: 'pulled', 'skipped', 'failed'
    """
    output_dir = Path(output_dir)
    filepath = output_dir / f"{game_id}.csv"

    if filepath.exists():
        return 'skipped'
 
    try:
        pbp = playbyplayv3.PlayByPlayV3(game_id=game_id).get_data_frames()[0]
        pbp.to_csv(filepath, index=False)
        time.sleep(sleep_seconds)
        return 'pulled'
    except Exception as e:
        print(f"Failed to pull {game_id}: {e}")
        return 'failed'
    
def season_from_game_id(game_id):
    """Extract season string like '2023-24' from a regular-season game ID."""
    yy = game_id[3:5]
    next_yy = str((int(yy) + 1) % 100).zfill(2)
    return f"20{yy}-{next_yy}"