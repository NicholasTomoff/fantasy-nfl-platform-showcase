# API Contracts

This directory documents the **public-facing API contracts** for the Fantasy NFL platform.

The production FastAPI implementation is private; these documents serve as a **contract-first reference** describing request/response shapes, endpoint responsibilities, and behavioral guarantees without exposing proprietary logic.

## Purpose

- Define stable request/response contracts between frontend and backend
- Demonstrate backend API design, consistency, and scalability
- Enable frontend or client development without backend source access

## Scope

Included:
- Endpoint definitions and HTTP semantics
- Required and optional parameters
- Response payload shapes
- Error conditions and idempotency notes

Excluded:
- Internal scoring algorithms
- Database schemas and queries
- Authentication implementation details
- Infrastructure secrets or environment configuration
- Admin and internal tooling routes
- Full CRUD coverage for all domain entities

## Design Principles

- RESTful, resource-oriented endpoints
- Idempotent scoring and projection operations
- Async-first backend execution
- Explicit league, season, and week scoping
- Deterministic responses for replayability and testing

## Documentation Structure

- `endpoints.md`  
  High-level definitions of selected API endpoints, grouped by category
  (scoring, league data, projections).

- `schemas.md`  
  Canonical response object definitions used across endpoints.
  This avoids repeating large JSON payloads in multiple places.

- `flows/`  
  Narrative descriptions of how complex backend processes execute
  (e.g., weekly scoring).

## How to Read These Docs

1. Start with `endpoints.md` to understand available operations.
2. Refer to `schemas.md` for full response shapes.
3. Use the flow documents to understand system behavior over time.

These documents are intended to be **accurate but non-exhaustive**.
