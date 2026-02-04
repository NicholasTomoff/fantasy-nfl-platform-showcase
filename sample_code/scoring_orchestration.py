"""
Representative excerpt of weekly scoring orchestration.

This sample demonstrates the control flow and state transitions
of the weekly scoring engine without exposing the full production
implementation.

Focus areas:
- Carry-forward handling for users without picks
- Per-position streak evaluation
- Idempotent async writes

Business thresholds, logging, validation, and edge-case handling
are intentionally omitted for clarity.
"""
async def score_week_with_session(db: AsyncSession, week: int, season: int, league_id: int):
    """
    Orchestrates weekly fantasy scoring for a league.

    Coordinates carry-forward logic, streak evaluation,
    and weekly score persistence.
    """
    # --- Handle users without picks (carry-forward) ---
    picked_users = {p.user_email for p in picks}
    all_users = await get_league_users(db, league_id)

    for email in all_users - picked_users:
        prev = await get_previous_week_score(db, email, week, league_id)
        if not prev or await weekly_score_exists(db, email, week, league_id):
            continue

        db.add(
            WeeklyScore(
                user_email=email,
                week=week,
                season=season,
                league_id=league_id,
                total_points=prev.total_points,
            )
        )

    await db.commit()
    ...# --- Omitted
    # --- Load NFL games for this week
    ...# --- Omitted
    # --- Streak evaluations for league and users
    for pick in picks:
        prev = await get_previous_week_score(db, pick.user_email, week, league_id)
        total_points = prev.total_points if prev else 0
        all_hit = True

        for pos in ["qb", "rb", "wr"]:
            player_id = getattr(pick, pos)
            hit = await evaluate_pick_hit(db, player_id, pos, week, season)

            current_streak, pos_points = await update_position_streak(
                db,
                pick.user_email,
                pos,
                hit,
                week,
                league_id,
                initial_streak=get_previous_streak(prev, pos),
            )

            total_points += pos_points
            if pos_points == 0:
                all_hit = False

        _, all_bonus = await update_all_position_streak(
            db, pick.user_email, all_hit, week, league_id
        )
        total_points += all_bonus
        ...# --- Omitted
        # --- Save or update WeeklyScore
        existing = await get_weekly_score(db, pick.user_email, week, league_id)

        if existing:
            existing.total_points = total_points
        else:
            db.add(
                WeeklyScore(
                    user_email=pick.user_email,
                    week=week,
                    season=season,
                    league_id=league_id,
                    total_points=total_points,
                )
            )


