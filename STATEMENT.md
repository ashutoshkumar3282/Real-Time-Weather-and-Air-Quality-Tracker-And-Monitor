# Project Statement: Real-Time Weather and AQI Tracker

## I. Objective

The objective is the construction of a stable, aggregated data reporting tool. This tool must process user text input (city name) and return consolidated environmental data (weather and air quality) from third-party APIs via a command-line interface.

## II. Technology Stack

* **Language:** Python 3
* **Libraries:** `requests`
* **APIs:** Open-Meteo (Geocoding, Weather, Air Quality)

## III. Functional Requirements (FRs)

These define the required outputs of the system:

1.  **FR-Coordinate:** Resolve city name to unique latitude and longitude coordinates.
2.  **FR-Fetch:** Successfully retrieve current data from both the weather and air quality API endpoints.
3.  **FR-Merge:** Combine all fetched data streams into a unified data structure.
4.  **FR-Translate:** Convert all raw API codes (e.g., WMO codes) into descriptive strings for the user.
5.  **FR-Display:** Output the final, structured report to standard output (console).

## IV. Non-Functional Requirements (NFRs)

These requirements govern the quality and operational resilience of the system:

1.  **NFR-Stability:** All external service calls must implement an automated retry mechanism with exponential backoff for fault tolerance.
2.  **NFR-Modularity:** Data fetching logic and data presentation logic must be strictly separated into distinct functions.
3.  **NFR-Clarity:** Output structure must be unambiguous and clearly categorized for quick data assimilation.
