# API Schemas

This document defines canonical response objects returned by the Fantasy NFL API.

Schemas are ordered by primary domain relevance:
1. Scoring & projections
2. League metadata
<br>(Future domains such as finance and payments are intentionally excluded from this document.)

---

## ScoreWeekResult

Returned by:
- `POST /api/score/week/{week}/league/{league_id}`

```json
{
  "status": "success",
  "message": "string"
}
```

| Field    | Type   | Meaning |
|---------|--------|--------|
status | string | Outcome of scoring operation. One of: `success`, `error`
| message | string | Human-readable confirmation including league, season, and week. Content is informational and must not be parsed programmatically. |

## ProjectMaxPointsResponse

Returned by:
- `GET /api/league/{league_id}/projected-max-points`

```json
{
  "league_id": 123,
  "season": 2025,
  "currentFinalizedWeek": 6,
  "projected_to_week": 18,
  "members": [
    {
      "user_email": "user@example.com",
      "current_total_points": 87,
      "projected_additional_points": 214,
      "projected_final_total": 301,
      "projected_positions_total": {
        "qb": 72,
        "rb": 71,
        "wr": 71
      },
      "final_projected_streaks": {
        "qb_streak": 9,
        "rb_streak": 8,
        "wr_streak": 10,
        "all_positions_streak": 7
      },
      "weeks_projected": 12
    }
  ]
}
```

| Field                  | Meaning                                        |
| ---------------------- | ---------------------------------------------- |
| `league_id`            | League identifier                              |
| `season`               | Season year                                    |
| `currentFinalizedWeek` | Most recent fully scored week used as baseline |
| `projected_to_week`    | Final week included in projections (typically 18) |
| `members`              | Projection results per league member           |

### ProjectMaxPointsResponse.members[]

user_email is used as a stable human-readable identifier for projections and may differ from internal user IDs.

Each entry represents one user’s maximum possible outcome assuming perfect future weeks.
| Field                         | Meaning                                              |
| ----------------------------- | ---------------------------------------------------- |
| `user_email`                  | League member identifier                             |
| `current_total_points`        | Points earned through `currentFinalizedWeek`         |
| `projected_additional_points` | Points added from projected future weeks             |
| `projected_final_total`       | `current_total_points + projected_additional_points` |
| `weeks_projected`             | Number of future weeks simulated                     |


### projected_positions_total
```json
{
  "qb": number,
  "rb": number,
  "wr": number
}
```

| Field | Type | Meaning |
|-----|----|--------|
| qb | number | Projected QB points |
| rb | number | Projected RB points |
| wr | number | Projected WR points |

### final_projected_streaks
```json
{
  "qb_streak": number,
  "rb_streak": number,
  "wr_streak": number,
  "all_positions_streak": number
}
```

| Field | Type | Meaning |
|-----|----|--------|
| qb_streak | number | Projected QB streak count |
| rb_streak | number | Projected RB  streak count |
| wr_streak | number | Projected WR  streak count |
| all_positions_streak | number | Projected triple streak count |

## League

Represents a fantasy league.

All fields are non-nullable unless otherwise specified.
Arrays may be empty.

Returned by:
- `GET /api/leagues` 
returns only leagues the authenticated user is a member of.
- `GET /api/leagues/{league_id}`

```json
{
  "id": 12,
  "name": "Sunday Crushers",
  "season_year": 2025,
  "min_players": 4,
  "created_by_user_id": 7,
  "created_at": "2025-08-01T14:22:11",
  "banner": "https://images.pexels.com/photos/7005488/pexels-photo-7005488.jpeg",
  "members": [
    {
      "user_id": 7,
      "user_name": "Nick"
    }
  ]
}
```

| Field                | Type           | Meaning                       |
| -------------------- | -------------- | ----------------------------- |
| `id`                 | integer        | Unique league identifier      |
| `name`               | string         | League name (globally unique) |
| `season_year`        | integer        | Primary season for the league |
| `min_players`        | integer        | Minimum required members      |
| `created_by_user_id` | integer        | User who created the league   |
| `created_at`         | datetime (UTC) | League creation timestamp     |
| `banner`             | string (URL)   | Display image for the league  |
| `members`            | array          | League membership summary     |

members[]

Each entry represents a league member.
```json
{
  "user_id": 7,
  "user_name": "Nick"
}
```

| Field | Type | Meaning |
|----|----|--------|
| user_id | integer | League member identifier |
| user_name | string | Display name |

**Notes**
- Membership is derived from the authenticated user context.
- Not all endpoints return full member or host details.
- Host user details are not embedded in the League object unless explicitly documented by the endpoint.
- Finance, scoring, and seasonal data are exposed via separate endpoints.


## RestrictedPlayersResult

Represents players the user is not allowed to select for the current week due to
streak continuation or game lock rules.

Returned by:
`GET /api/restricted_players/{user_email}`

| Name      | Type    | Required | Meaning         |
| --------- | ------- | -------- | --------------- |
| week      | integer | yes      | Target NFL week |
| league_id | integer | yes      | League context  |
| season    | integer | yes      | Season year     |

```json
{
  "qb": [123, 456],
  "rb": [789],
  "wr": []
}
```

**Semantics**
- Keys are lowercase position identifiers.
- Values are lists of player_id values that are restricted for that position.
- An empty array means no restrictions for that position.
- Positions with no applicable restrictions may be omitted from the response.

**Rules**
- Restrictions are derived from prior weeks’ picks and scoring results.
- Once a streak is broken or missing data is encountered, restrictions stop propagating backward.
- This endpoint is read-only and intended solely for client-side pick validation and UX control.

| Field | Type       | Meaning                       |
| ----- | ---------- | ----------------------------- |
| qb    | array[int] | Restricted QB player IDs      |
| rb    | array[int] | Restricted RB player IDs      |
| wr    | array[int] | Restricted WR / TE player IDs |

**Notes**
- This endpoint is UX-driven and should be called when rendering the weekly pick interface.
- It does not return player metadata; clients should resolve IDs using cached player data.
- Authorization is assumed via authenticated session; user_email is scoped and validated server-side.