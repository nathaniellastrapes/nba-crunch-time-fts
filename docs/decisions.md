# Decisions

## Decision 1: Crunch Time Definition
I will be using the NBA's official crunch time definition for the initial analysis. The NBA's definition of crunch time is "A game within 5 points with less than 5 minutes remaining." I chose this definition because it is an official NBA metric and is the league standard. It will be comparable to existing analyses. I considered altering crunch time to be a game within 3 points with less than 3 minutes, but opted against that for now in favor of the NBA's definition. I may revisit the altered definition. Another option is win-probability based, but that metric is not as interpretable as the official NBA definition of crunch time. The official definition may contain some situations where there aren't true high-pressure moments, but I will accept that risk in the initial analysis in exchange for sample size and comparability.

## Decision 2: Pooled vs. player-level analysis
I'll analyze pooled analysis first to see if there is any statistically significance in free throw percentage overall. But primarily, I will be looking at individual percentages to analyze which players have a statistically significant different free throw percentage in common time versus crunch time. This analysis could inform coaching decisions about intentional fouling, with appropriate caveats about causality

## Decision 3: How many seasons of data
Three regular seasons of data: 
- 2023-24
- 2024-25
- 2025-26

A lot of players will have a small sample size, and three seasons is enough to capture enough data while retaining relevancy for recent seasons.

## Decision 4: Your written prior
# Overall pooled effect
I expect a slight uptick in pooled effect during crunch time. The reason is because the best and highest percentage free throw shooters will have the ball in their hands during crunch time.

# Player-level heterogeneity
I predict that low percentage free throw shooters will have a slightly lower percentage in free throw percentage in crunch time because of a lack of confidence and high pressure.

# Home vs. road interaction
I expect there to be a slight decline in percentage for players on the road in crunch time.

# Confidence
Overall pooled effect - Medium
Player-level heterogeneity - High
Home vs. road interaction - Medium

# What would surpise me?
I would be genuinely suprised if poor free throw shooters have a better free throw percentage in crunch time versus regular time. Shaq is famous for saying he makes his free throws "when they count." 

## Decision 5: Data source
NBA_API