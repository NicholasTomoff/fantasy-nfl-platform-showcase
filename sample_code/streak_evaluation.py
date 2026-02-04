def evaluate_pick_hit(pos: str, stat, player_position: str = None) -> bool:
    """
    Evaluate whether a player meets positional performance thresholds.
    WR evaluation includes TE where applicable.
    """
    if pos == "qb":
        return stat.passing_yards >= threshold
    else:  # RB / WR
        return stat.yards >= threshold
