# {{PROJECT_NAME}}
> Working title: City Climate Dashboard
> Final product name: TBD

City Climate Dashboard is a full-stack web application that gives a fast climate-risk briefing for any city. 

Users search a city and get a structured profile with mapped indicators, risk scores, and a plain-language summary.

## Features
1. User authentication
   - Email/password signup and login
   - OAuth login
   - JWT-based protected sessions
2. City search and geocoding
   - City lookup using Mapbox Geocoding API
   - Coordinates and location metadata returned for analysis
3. Risk profile generation
   - Backend fetches data from multiple sources asynchronously
   - Normalizes data into a shared 0-100 risk scoring model
   - Core indicators in MVP:
     - Heat risk
     - Flood risk
     - Air quality
     - Green cover
4. Map visualization
   - Mapbox map centered on selected city
   - City marker
   - Heat and flood overlays
5. Saved cities
   - Authenticated users can save and revisit city profiles
6. AI narrative
   - Claude API generates a concise city risk briefing based on computed indicators
7. Caching
   - Hybrid strategy: 12-hour cache TTL
   - Users can request a live refresh at any time

## Technologies
> Backend: FastAPI + Uvicorn
> Data: PostgreSQL, Pydantic, GeoJSON
> Frontend: React, JavaScript, Tailwind CSS, Mapbox GL JS
> Deployment: Render (backend), Vercel (frontend)
> Auth: JWT + OAuth

## Data Sources
> Mapbox Geocoding (city lookup)
> Open-Meteo (climate/heat)
> OpenAQ (air quality)
> others TBD


## Project Structure
City Climate Dashboard
  > backend
    > main.py
    > models/
    > routers/
    > schemas/
    > services/
    > core/
  > frontend
    > src/
      > components/
      > pages/
      > store/
      > services/
    > public/  
  > data/
    > README.md
    > requirements.txt
    > .gitignore

## Architecture Flow (MVP)
1. User submits city name
2. Backend geocodes city via Mapbox
3. Backend runs parallel data-source requests
4. Backend normalizes results into indicator scores
5. Cache check:
   - If cache age < 12 hours, return cached profile
   - If expired or refresh requested, fetch live and update cache
6. Frontend renders map, overlays, indicator cards, and AI narrative
7. User can save city profile if authenticated

## Local Setup
1. Create and activate virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate
2. Install backend dependencies:
   pip install -r requirements.txt
3. Run backend:
   uvicorn backend.main:app --reload
4. Run frontend (after React app scaffold is created):
   cd frontend
   npm install
   npm run dev

## Environment Variables
Required environment variables:

DATABASE_URL
JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY
MAPBOX_ACCESS_TOKEN
CLAUDE_API_KEY
OAUTH_CLIENT_ID
OAUTH_CLIENT_SECRET