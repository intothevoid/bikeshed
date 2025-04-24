# Responsive Mobile Dashboard App

## 1. Product Requirements Document (PRD)

### 1.1 Overview
A lightweight, responsive dashboard application optimized for small screens (7" tablets and smartphones). Aggregates and displays timely, glanceable widgets including News (with summarization & podcast), Weather, MotoGP & Formula 1 races, Stock & Crypto tickers, Google Calendar events, Quote of the Day, and Photo of the Day in a modern, eye‑pleasing interface.

### 1.2 Objectives & Success Metrics
- **Engagement**: Daily active users ≥ 5,000 within 3 months; average session ≥ 2 minutes.
- **Performance**: First contentful paint < 1 s on mid-range devices; widget refresh < 5 s.
- **Usability**: 90th percentile task completion < 10 s for checking any widget.
- **Reliability**: 99.9% uptime; offline fallback for last‑cached data.

### 1.3 Target Users & Personas
| Persona         | Description                                   | Needs                                                      |
| --------------- | --------------------------------------------- | ---------------------------------------------------------- |
| Commuter Carla  | Uses 7" tablet on train for quick updates.    | Glanceable headlines, race times, weather; offline cache. |
| On‑the‑go Omar  | Mobile phone user juggling meetings, news.    | Calendar alerts, top‑story summaries, market tickers.     |
| Racing Fan Raj  | Follows MotoGP & F1 globally.                | Localized event schedules, session start alerts.          |
| Investor Isla   | Monitors US/Australian stocks & crypto.       | Real‑time quotes, daily summaries, price alerts.          |
| Inspiration Ivy | Seeks daily motivation and visuals.           | Quote of the Day, Photo of the Day widget.                |

### 1.4 Key Features
1. **News Feed**: Top headlines with images; one‑tap summary of all top stories; generate AI‑narrated news podcast.
2. **Weather Widget**: Current conditions, hourly & 7‑day forecast, severe weather alerts.
3. **Racing Schedule**: MotoGP & Formula 1 upcoming events with local date/time for practice, qualifying, sprint, race.
4. **Market Tickers**: Real‑time US & Australian stock indices and individual symbols; change %, sparkline.
5. **Crypto Prices**: Live prices for selected cryptocurrencies; 24 h change and market cap.
6. **Calendar**: Google Calendar day/week view; event reminders; add/edit events.
7. **Quote of the Day**: Daily inspirational quote with author.
8. **Photo of the Day**: High‑quality daily image from a curated API.
9. **Custom Layouts**: Drag‑and‑drop widget arrangement; light/dark themes; font-size adjustment.

### 1.5 Functional Requirements
- FR1: Fetch and display news articles with images, summaries, and podcast generation option.
- FR2: Retrieve weather via public API (e.g., OpenWeatherMap) including alerts.
- FR3: Pull MotoGP & F1 schedules from sports API; convert to user’s local timezone.
- FR4: Stream US/AU stock quotes and crypto prices with real‑time updates.
- FR5: Sync and manage Google Calendar events via OAuth2.
- FR6: Fetch daily quote and photo from external APIs.
- FR7: Support drag‑and‑drop widget arrangement; persist layout per user.
- FR8: Offline caching of all widget data with time‑to‑live policies.

### 1.6 Non‑Functional Requirements
- NFR1: Responsive layout down to 320×480 px; grid adapts 1–3 columns.
- NFR2: Accessibility: WCAG AA compliance; screen‑reader labels on widgets.
- NFR3: Secure local storage: encrypt OAuth tokens and user preferences.
- NFR4: Internationalization: support English, Spanish, Mandarin; localized date/time.
- NFR5: Error logging and monitoring (Sentry); retry policies for failed API calls.

### 1.7 Technology Stack
- **Frontend**: React Native + Tailwind CSS
- **State**: Redux Toolkit, React Query, AsyncStorage
- **Backend**: Node.js + Express, GraphQL API
- **DB**: PostgreSQL (user data, settings), Redis (cache)
- **Auth**: OAuth2 (Google Calendar)
- **CI/CD**: GitHub Actions, Fastlane
- **Hosting**: AWS ECS Fargate, RDS, S3
- **External APIs**: News API, OpenWeatherMap, Ergast/F1/MotoGP API, Alpha Vantage/IEOD, CoinGecko, Unsplash, Quotes REST API

## 2. Cursor Smart‑Prompting & Modes

### 2.1 System Design Planner
```text
[System Design Planner]
– List subsystems: Mobile UI, Widget Engine, API Gateway, Auth Service, Data Aggregators.
– Responsibilities, scaling, tech options for each.
– Comm patterns: GraphQL for dashboard queries, WebSocket for live updates.
```

### 2.2 Architect Mode
```text
[Architect Mode]
Subsystem: "Widget Engine"
1. Microservices: news-fetcher, weather-fetcher, racing-scheduler, market-ticker, crypto-ticker, calendar-sync, quote-fetcher, photo-fetcher, widget-orchestrator.
2. Data contracts: GraphQL types and subscriptions.
3. Resilience: caching, circuit breakers, retries.
```

### 2.3 Database Design Mode
```text
[Database Design Mode]
"Widget State"
– Schema: widget(id, user_id, type, position, config JSON, last_updated).
– Indexes: user_id, type.
– Partition by user_id for scale.
```

### 2.4 API Design Mode
```text
[API Design Mode]
"Dashboard API"
- Query: getDashboard(userId) returns widget list and data references.
- Subscriptions: onWidgetDataUpdate(userId).
- Mutations: addWidget, removeWidget, updateWidgetConfig, reorderWidgets.
- Auth: JWT via OAuth2.
```

### 2.5 UI & Frontend Mode
```text
[UI and Frontend Mode]
"Dashboard Screen"
- React Native components: Header, WidgetGrid, WidgetCard, PodcastPlayer.
- Grid: 1 col on phones, 2 cols portrait, 3 cols landscape/tablet.
- WidgetCard variations for each type with iconography, concise typography.
```

### 2.6 Review Mode
```text
[Review]
– Edge cases: daylight‑savings in race times, API rate limits, offline re‑sync.
– Performance: initial load with 8 widgets, virtualization.
```

## 3. .cursorrules for Team Conventions
```json
{
  "rules": [
    { "mode": "Architect Mode", "require": ["component diagram","data contracts"] },
    { "mode": "API Design Mode", "require": ["openapi.yaml","error codes"] },
    { "mode": "UI and Frontend Mode", "require": ["accessibility labels","responsive breakpoints"] },
    { "mode": "System Design Planner", "require": ["subsystem list","communication patterns"] }
  ],
  "styles": {
    "indent": 2,
    "semi": true,
    "quotes": "double"
  }
}
```

## 4. Additional Artifacts
- **ADRs**: Tech choices for real‑time data (WebSocket vs polling), caching strategy.
- **CI/CD**: YAML templates for automated test, build, deploy.
- **Design Tokens**: Color palette, typographic scale, spacing units.
- **Prompt Library**: Stored smart prompts for each Cursor mode.

---

This updated plan incorporates all requested widgets—news with podcast, weather, racing schedules, markets, crypto, calendar, quote, and photo—ensuring an end‑to‑end blueprint for your responsive mobile dashboard app.


