````markdown
# 🌍 Country Currency & Exchange API

A FastAPI backend that fetches country data and exchange rates from public APIs, computes an **estimated GDP**, caches everything in MySQL, and exposes clean RESTful endpoints — including a generated summary image.

---

## 🚀 Features

- **POST /countries/refresh** → Fetch all countries + exchange rates, cache them in DB.
- **GET /countries** → List cached countries (supports filters + sorting).
- **GET /countries/{name}** → Get details of one country.
- **DELETE /countries/{name}** → Delete a country from DB.
- **GET /status** → Shows total cached countries + last refresh timestamp.
- **GET /countries/image** → Serves generated summary image (top 5 by GDP).

---

## 🧩 Stack

| Component | Tech |
|------------|------|
| Language | Python 3.11 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | MySQL |
| HTTP Client | httpx |
| Image Generation | Pillow |
| Config | pydantic-settings (.env) |
| Deployment | Railway / EC2 / Docker |

---

## ⚙️ Setup (Local)

### 1️⃣ Clone + enter project
```bash
git clone https://github.com/<yourname>/country-currency-api.git
cd country-currency-api
````

### 2️⃣ Create `.env`

```bash
cp .env.example .env
```

Then edit values if needed:

```
APP_PORT=8000
DB_DIALECT=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASS=pass
DB_NAME=country_cache
LOG_LEVEL=info
```

### 3️⃣ Start MySQL (via Docker)

```bash
docker compose up -d db
```

### 4️⃣ Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Run FastAPI

```bash
python -m uvicorn src.app:app --reload
```

Visit:
➡️ [http://localhost:8000/health](http://localhost:8000/health) → should return `{ "ok": true }`

---

## 💾 Refresh and Cache Data

```bash
curl -X POST http://localhost:8000/countries/refresh
```

This will:

* Fetch data from `restcountries.com` + `open.er-api.com`
* Calculate `estimated_gdp = population × random(1000–2000) ÷ exchange_rate`
* Insert/update DB
* Generate `cache/summary.png`

---

## 🔍 Example Endpoints

### Get all countries

```bash
GET /countries
```

### Filter by region

```bash
GET /countries?region=Africa
```

### Sort by GDP (descending)

```bash
GET /countries?sort=gdp_desc
```

### Get by name

```bash
GET /countries/Nigeria
```

### Delete by name

```bash
DELETE /countries/Nigeria
```

### Status

```bash
GET /status
```

Response:

```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-27T12:00:00Z"
}
```

### Summary image

```bash
GET /countries/image
```

Returns PNG file like:

* Total number of countries
* Top 5 by GDP
* Last refresh time

---

## 🧮 Database Schema

**countries**

| Column            | Type     | Description                                  |
| ----------------- | -------- | -------------------------------------------- |
| id                | int (PK) | Auto ID                                      |
| name              | varchar  | Country name                                 |
| capital           | varchar  | Capital city                                 |
| region            | varchar  | Continent/region                             |
| population        | bigint   | Population                                   |
| currency_code     | varchar  | Currency ISO code                            |
| exchange_rate     | decimal  | Rate vs USD                                  |
| estimated_gdp     | decimal  | population × random(1000–2000)/exchange_rate |
| flag_url          | text     | Flag image                                   |
| last_refreshed_at | datetime | Auto-updated timestamp                       |

**meta**

| key             | value                         |
| --------------- | ----------------------------- |
| last_refresh_ts | ISO timestamp of last refresh |

---

## ⚡ Error Responses

| Code | Response                                                                                                               |
| ---- | ---------------------------------------------------------------------------------------------------------------------- |
| 400  | `{ "error": "Validation failed" }`                                                                                     |
| 404  | `{ "error": "Country not found" }`                                                                                     |
| 503  | `{ "error": "External data source unavailable", "details": "Could not fetch data from restcountries or open-er-api" }` |
| 500  | `{ "error": "Internal server error" }`                                                                                 |

---

## 🧠 Design Notes

* Refresh logic merges by **country name** (case-insensitive).
* Random multiplier regenerated on every `/refresh`.
* Countries with missing currencies are still cached with GDP = 0.
* Only first currency code per country is used.
* Summary image automatically updated after refresh.

---

## 🖼️ Summary Image Example

`cache/summary.png` shows:

* Total cached countries
* Top 5 by estimated GDP
* Timestamp of last refresh

Example (after refresh):

```
Country Cache Summary
Total countries: 250
Top 5 by estimated GDP:
1. United States — 123,456,789,012.45
2. China — 113,222,345,678.90
...
Last refresh: 2025-10-27T12:00:00Z
```

---

## 🧰 Commands (Quick Reference)

```bash
# Start DB
docker compose up -d db

# Run API
uvicorn src.app:app --reload

# Refresh cache
curl -X POST http://localhost:8000/countries/refresh

# List countries
curl http://localhost:8000/countries
```

---

## ☁️ Deployment (Railway / EC2)

### Railway

1. Create a new **MySQL** plugin
2. Create a **Python** service and link this repo
3. Add env vars from `.env`
4. Start command:

   ```
   uvicorn src.app:app --host 0.0.0.0 --port ${APP_PORT}
   ```
5. Test `/health` and `/status` once deployed

### EC2

```bash
sudo apt update
sudo apt install docker docker-compose -y
git clone https://github.com/<yourname>/country-currency-api.git
cd country-currency-api
docker compose up -d
```

---

## 🧾 Submission Details

After verifying your live API works:

1. Go to Slack channel **#stage-2-backend**
2. Run `/stage-two-backend`
3. Submit:

   * ✅ API base URL (e.g., `https://countryapi-production.up.railway.app`)
   * ✅ GitHub repo link
   * ✅ Full name
   * ✅ Email

---

## 👨‍💻 Author

**Segun Oladimeji**
Berlin, Germany
GitHub: [TheGreatWizard16](https://github.com/TheGreatWizard16)
Slack: `@SegunO` – HNG13 Backend Wizards



# country-currency-api
