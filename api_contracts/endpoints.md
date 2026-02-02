# API Endpoints

This document defines the core API endpoints exposed by the Fantasy NFL backend.

Endpoints are scoped by the minimum required context:

- User-scoped endpoints derive context from the authenticated user.
- League-scoped endpoints require a league_id path parameter.
- Season-scoped endpoints additionally require a season or season_year.

Authentication is required unless otherwise noted.

---

## Scoring Endpoints

### POST /score/week/{week}/league/{league_id}

Finalize scoring for a given league and week.

**Description**
Triggers the weekly scoring process, including streak evaluation, bonus calculation, and carry-forward handling.

**Path Parameters**
| Name       | Type | Description |
|-----------|------|-------------|
| week      | int  | NFL week number |
| league_id| int  | League identifier |

**Query Parameters**
| Name   | Type | Required | Description |
|--------|------|----------|-------------|
| season | int  | yes      | NFL season year |

**Returns**  
- `ScoreWeekResult` (see `schemas.md`)

**Notes**
- Idempotent
- Safe to re-run
- Writes `WeeklyScore` and streak tables

**Example Request**
```http
POST /score/week/7/league/42?season=2025
```

### GET /league/{league_id}/projected-max-points

Pulls maximum possible points for each user in a given league.

**Description**
Triggers the point calculation process assuming each remaining week in season achieves maxiumum ponts and bonus award.

**Path Parameters**
| Name       | Type | Description |
|-----------|------|-------------|
| league_id| int  | League identifier |

**Query Parameters**
| Name   | Type | Required | Description |
|--------|------|----------|-------------|
| season | int  | yes      | NFL season year |
| currentFinalizedWeek | int | yes | Most recent fully scored week |

**Returns**  
- `ProjectMaxPointsResponse` (see `schemas.md`)

**Example Request**
```http
GET /league/42/projected-max-points?season=2025&currentFinalizedWeek=13
```
---

## League Read Endpoints

### GET /api/leagues

Retrieve all leagues the currently authenticated user belongs to.

**Scope**
- User-scoped (derived from authentication context)

**Authentication**
- Required

**Description**

Returns a list of leagues where the logged-in user is a member.
Each item represents a League resource.

**Response**
- 200 OK: List of leagues
- 401 Unauthorized: User not authenticated

**Returns**
- `List[League]` (see `League` schema)

---

## Restricted Players (UX Control)

### GET /api/restricted_players/{user_email}

Retrieve players that the user is not allowed to select for the current week due to
streak continuation rules based on prior weeks’ picks and scoring results.

**Scope**

- User-scoped
- League-scoped
- Week-scoped
- Season-scoped

**Authentication**
- Required
- {user_email} is validated against the authenticated user context.

**Path Parameters**
| Name       | Type   | Description                            |
| ---------- | ------ | -------------------------------------- |
| user_email | string | User identifier for restriction lookup |

**Query Parameters**
| Name      | Type    | Required | Description     |
| --------- | ------- | -------- | --------------- |
| week      | integer | yes      | Target NFL week |
| league_id | integer | yes      | League context  |
| season    | integer | yes      | Season year     |

**Description**

This endpoint supports front-end pick flows by identifying players that are
restricted for selection due to:
- Active streak continuation rules
- Picks from prior weeks
- Scored outcomes from previous weeks

The endpoint does not return player metadata and is not intended for analytics or reporting.

**Response**
- 200 OK: Restricted players grouped by position
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User does not belong to the league
- 500 Internal Server Error: Unexpected scoring or data resolution error

**Returns**
-  `RestrictedPlayersResult` (see `schemas.md`)

**Usage Notes**
- Intended to be called when rendering or updating the weekly pick UI.
- Results should be cached client-side for the duration of the pick session.
- This endpoint enforces server-side business rules; the client must not attempt to infer restrictions independently.