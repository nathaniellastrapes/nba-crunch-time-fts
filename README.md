# NBA Crunch-Time Free Throw Analysis

A descriptive analysis of NBA free throw shooting in high-pressure end-of-game situations across the 2023-24, 2024-25, and 2025-26 seasons (n = 164,510 free throws across 3,690 regular season games).

## The question

While watching a tight playoff game, I wondered whether the pressure of late-game situations meaningfully affects free throw shooting. The two questions I set out to answer:
1. Across the league, do players shoot free throws at a different rate in crunch time than in non-crunch time?
2. Among individual high-volume crunch-time shooters, are there players whose performance reliably differs from their baseline?

## Approach

- Data: NBA play-by-play via `nba_api`, 3 regular seasons
- Crunch time defined as: NBA official definition (last 5 minutes, margin within 5)
- Pooled analysis: two-proportion z-test for league-wide effect
- Player-level analysis: per-player z-tests for the 55 players with ≥50 crunch FTs, with Benjamini-Hochberg correction for multiple comparisons

## Findings

**Pooled effect:** Pooled across 164,510 free throws over three seasons, crunch-time FT% (77.46%, n=9,402) was 0.82 percentage points lower than non-crunch FT% (78.28%, n=155,108). A two-proportion z-test yielded p = 0.062, providing weak-to-moderate evidence against the null hypothesis of no difference. The magnitude is small enough that it would be unlikely to inform coaching decisions, even if real.

**Player-level effects:** Across the 55 players who have shot 50 or more free throws in crunch time, the baseline gap ranges from roughly -13pp (Tatum) to +9pp (Bridges). The largest negatives were Jayson Tatum, Victor Wembanyama, Jaylen Brown,  Pascal Siakam, and Jamal Murray. The largest positives were Mikal Bridges, Wendell Carter, Norman Powell, and Giannis Antetokounmpo. The table is informative as a descriptive ranking, but individual player claims should be treated as suggestive rather than confirmed.

Notably, the players with the largest negative gaps tend to be high-usage offensive creators (Tatum, Wemby, Brunson, Siakam), suggesting fatigue or game-flow factors may matter more than 'clutch psychology' alone.

Individual player tests were corrected using the Benjamini-Hochberg procedure to account for testing 55 players simultaneously. Without correction, a few player-level results appear "significant" (p < 0.05), but this is consistent with what would be expected from chance alone given the number of tests. After correction, no individual player's effect remains statistically significant — the data does not support strong claims about which specific players genuinely shoot differently in crunch time.

## Limitations and future work

- Per-player sample sizes (50-160 crunch FTs over three seasons) limit the statistical power to detect individual effects after correcting for testing 55 players simultaneously.
- Home/road interaction was scoped but not analyzed.

## Repository structure 
```
nba-crunch-time-fts/
├── nba_crunch/              # Reusable functions (data pulling, enrichment, parsing)
├── notebooks/
│   ├── 01_data_exploration.ipynb    # API schema and one-game logic
│   ├── 02_data_collection.ipynb     # Bulk pull of 3,690 games
│   ├── 03_pooled_analysis.ipynb     # League-wide test
│   └── 04_player_level_analysis.ipynb  # Per-player tests with FDR correction
├── docs/
│   ├── decisions.md         # Design decisions and tradeoffs
│   ├── concepts.md          # Statistical concepts learned during the project
│   └── prior.md             # Predictions written before analysis
├── data/                    # Raw and processed (gitignored)
└── pyproject.toml           # Installable package config
```