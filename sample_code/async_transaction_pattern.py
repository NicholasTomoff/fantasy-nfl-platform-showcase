"""
Representative async transaction pattern used for idempotent scoring operations.

Ensures partial writes are rolled back on failure and preserves database consistency.
"""
async with async_session() as db:
    try:
        await perform_scoring(db)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
