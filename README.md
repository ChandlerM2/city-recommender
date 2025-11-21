# City Recommender Pipeline

## Purpose
An interactive city recommendation system that analyzes US cities (100K+ population) across multiple factors (affordability, safety, income, quality of life) and recommends the best matches based on user-weighted preferences.

## Architecture
APIs → BigQuery → dbt → Looker Studio Dashboard

## Setup Instructions

1. Clone repo
2. Create venv
3. Install dependencies through .txt
    - `pip install -r requirements.txt`
4. Configure .env
    - **CENSUS_API_KEY** = ""
5. Run extraction

## Usage

Not set up quite yet

## Data Sources

- Census ACS1 2024
- BLS Public API
- FBI Crime Data
- FCC Broadband
- reddit forum

## Output

Produces a dashboard in Looker Studio that allows users to dynamically navigate through different cities depending on preference.
