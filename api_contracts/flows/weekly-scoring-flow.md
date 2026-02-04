# Weekly Scoring Flow

This document describes how weekly fantasy scoring is finalized for a league.

## Trigger

- Manual API call to:
  `POST /api/score/week/{week}/league/{league_id}`

## Step-by-Step Flow

1. Load all `WeeklyPick` records for the given league and week.
2. Identify league members without submitted picks.
3. For users without picks:
   - Load previous week’s `WeeklyScore`
   - Create a carry-forward score entry if none exists.
4. Load NFL games for the specified week and season.
5. For each user with picks:
   - Evaluate positional performance against thresholds
   - Update position streaks (QB, RB, WR)
   - Accumulate streak-based points
6. If all positions hit:
   - Increment all-position streak
   - Apply cross-position bonus
7. Insert or update `WeeklyScore`.
8. Commit transaction.

## Guarantees

- Scoring is idempotent
- Streaks update only once per week
- Partial failures rollback safely

## Non-Goals

- Real-time scoring
- Play-by-play updates