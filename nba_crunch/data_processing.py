import pandas as pd
import numpy as np

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