# Fashion Studio ETL Pipeline

## 📌 Project Overview

This project implements a simple **ETL (Extract, Transform, Load) pipeline** to scrape competitor product data from: https://fashion-studio.dicoding.dev

The pipeline:

1. Extracts product data from 50 pages.
2. Transforms and cleans the dataset.
3. Loads the cleaned data into:
   - CSV (Flat File)
   - Google Sheets
   - PostgreSQL

## 🏗 ETL Architecture

            ┌────────────────────────────┐
            │ fashion-studio.dicoding.dev │
            └──────────────┬─────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │   Extract  │
                    │ (requests) │
                    └──────┬─────┘
                           │ Raw data (list[dict])
                           ▼
                    ┌────────────┐
                    │ Transform  │
                    │ (pandas)   │
                    └──────┬─────┘
                           │ Clean DataFrame
                           ▼
           ┌───────────────┼─────────────────┐
           ▼               ▼                 ▼
      ┌──────────┐    ┌───────────────┐   ┌─────────────┐
      │   CSV    │    │ Google Sheets │   │ PostgreSQL  │
      └──────────┘    └───────────────┘   └─────────────┘

## 🧩 Pipeline Flow

1. Extract all 50 pages
2. Clean & transform columns
3. Remove invalid, duplicate, and null data
4. Store cleaned dataset into three repositories

## ▶ Run Pipeline

```
python3 main.py
```

## 🗂 Project Structure

```
ElevateSubmission05/
├── utils/
│ ├── init.py
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── tests/
│ ├── test_extract.py
│ ├── test_transform.py
│ └── test_load.py
├── main.py
├── requirements.txt
├── submission.txt
└── README.md
```

---

## ⚙️ Features

### ✔ Extract

- Scrapes product data (Title, Price, Rating, Colors, Size, Gender)
- Extracts from all 50 pages
- Adds extraction timestamp
- Handles network and parsing errors

### ✔ Transform

- Converts price from USD to IDR (1 USD = Rp16.000)
- Cleans rating into float
- Extracts integer from colors
- Removes prefix from size & gender
- Removes:
  - Null values
  - Duplicates
  - "Unknown Product"
- Ensures correct data types

### ✔ Load

Stores cleaned data into:

- CSV file
- Google Sheets
- PostgreSQL database

Each load function includes error handling.

## 🚀 Installation

Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a .env file in the root directory:

```
DB_URI=postgresql+psycopg2://username:password@localhost:5432/<database_name>
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id
```

### 📄 google-sheets-api.json

You must generate a Google Service Account key:

1. Go to Google Cloud Console.
2. Enable Google Sheets API.
3. Create a Service Account.
4. Generate a JSON Key.
5. Save it as:

```
google-sheets-api.json
```

Place it in the project root directory.

### ▶️ Running the ETL Pipeline

```
python3 main.py
```

### 🧪 Running Unit Tests

```
python3 -m pytest tests
```

### 📊 Running Test Coverage

```
coverage run -m pytest tests
coverage report
```

Current coverage: ≥80%

## 📄 URL Google Sheets:

https://docs.google.com/spreadsheets/d/1tWZkZovHqIjOPCy7MkupIkFS7DC3f_IdBxCQ-QRHOWQ
