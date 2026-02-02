## System Architecture

This diagram illustrates the high-level architecture of the Fantasy NFL platform,
including frontend clients, backend services, data persistence, data ingestion,
and scoring workflows.

```mermaid
graph TD

%% Clients
A["User<br/>React Web App"]
A2["User<br/>React Native Mobile App"]
ADMIN["Admin / Scheduler"]

%% Backend
B["FastAPI Backend<br/>(Async)"]

%% Data Layer
DB["PostgreSQL Database"]
JSON["JSON Data Snapshots<br/>(players_YYYY.json)"]

%% External Data
EXT["External NFL Data API<br/>(RapidAPI)"]

%% Infrastructure
subgraph Infrastructure
DOCKER["Docker"]
HOST["Fly.io / Render"]
end

%% CI/CD
CI["GitHub Actions<br/>CI/CD"]

%% Flows
A -->|HTTP Requests| B
A2 -->|HTTP Requests| B

ADMIN -->|Trigger Weekly Scoring| B

B -->|Read / Write| DB
B -->|Bootstrap / Load| JSON

EXT -->|Fetch Player & Team Data| B
B -->|Persist Snapshot| JSON

DOCKER --> B
HOST --> B
CI --> B
