# Fashion Studio ETL Pipeline

An end-to-end ETL pipeline built to collect competitor product data from Fashion Studio, clean and transform the dataset, and load it into multiple storage destinations including CSV, Google Sheets, and PostgreSQL.

This project simulates a real-world Data Engineering use case where a fashion retail company needs competitor product data to support downstream analytics and data science initiatives.

---

## Project Overview

The pipeline consists of three main stages:

### Extract

Scrapes product information from the Fashion Studio website across multiple pages.

Collected attributes include:

* Product Title
* Price
* Rating
* Available Colors
* Size
* Gender
* Extraction Timestamp

### Transform

Cleans and standardizes raw scraped data by:

* Removing null values
* Removing duplicate records
* Removing invalid products
* Converting prices from USD to IDR
* Converting ratings to numeric values
* Cleaning color, size, and gender fields
* Ensuring proper data types

### Load

Stores the transformed dataset into:

* CSV File
* Google Sheets
* PostgreSQL Database

---

## Architecture

```text
Fashion Studio Website
           │
           ▼
       Extract
           │
           ▼
      Transform
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
  CSV   Google   PostgreSQL
         Sheets
```

---

## Tech Stack

* Python
* Pandas
* Requests
* BeautifulSoup4
* Google Sheets API
* PostgreSQL
* SQLAlchemy
* Pytest
* Coverage
* python-dotenv

---

## Project Structure

```text
fashion-studio-etl/
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Features

* Modular ETL architecture
* Web scraping from competitor website
* Data cleaning and validation
* Multi-destination data loading
* Environment-based configuration
* Unit testing
* Test coverage support
* GitHub-safe credential management

---

## Environment Configuration

This project uses environment variables to securely manage credentials and configuration.

Create a `.env` file based on `.env.example`.

Example:

```env
LOAD_TO_GOOGLE_SHEETS=false
LOAD_TO_POSTGRESQL=false

GOOGLE_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_WORKSHEET_NAME=Sheet1
GOOGLE_APPLICATION_CREDENTIALS=google-sheets-api.json

POSTGRES_TABLE_NAME=products
POSTGRES_CONNECTION_STRING=postgresql+psycopg2://postgres:password@localhost:5432/fashion_studio
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fashion-studio-etl.git
cd fashion-studio-etl
```

### 2. Create a Virtual Environment

#### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Local Environment File

#### Windows

```powershell
copy .env.example .env
```

#### macOS / Linux

```bash
cp .env.example .env
```

Update the values according to your local setup.

---

## Running the Pipeline

### CSV Only

Configure:

```env
LOAD_TO_GOOGLE_SHEETS=false
LOAD_TO_POSTGRESQL=false
```

Run:

```bash
python main.py
```

Output:

```text
products.csv
```

---

## Loading Data into Google Sheets

### Step 1: Enable APIs

Enable the following APIs in Google Cloud Console:

* Google Sheets API
* Google Drive API

### Step 2: Create a Service Account

Create a Service Account and download its JSON credentials.

Place the file in the project root:

```text
google-sheets-api.json
```

### Step 3: Share the Spreadsheet

Share your Google Spreadsheet with the Service Account email and grant **Editor** permissions.

Example:

```text
etl-service-account@project-id.iam.gserviceaccount.com
```

### Step 4: Configure Environment Variables

```env
LOAD_TO_GOOGLE_SHEETS=true

GOOGLE_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_WORKSHEET_NAME=Sheet1
GOOGLE_APPLICATION_CREDENTIALS=google-sheets-api.json
```

### Step 5: Run

```bash
python main.py
```

Data will be loaded into both CSV and Google Sheets.

---

## Loading Data into PostgreSQL

### Step 1: Create Database

Connect to PostgreSQL:

```bash
psql -U postgres
```

Create database:

```sql
CREATE DATABASE fashion_studio;
```

Exit:

```sql
\q
```

### Step 2: Configure Environment Variables

```env
LOAD_TO_POSTGRESQL=true

POSTGRES_TABLE_NAME=products

POSTGRES_CONNECTION_STRING=postgresql+psycopg2://postgres:password@localhost:5432/fashion_studio
```

Adjust the username, password, host, port, and database name as needed.

### Step 3: Run

```bash
python main.py
```

### Step 4: Verify Data

```bash
psql -U postgres -d fashion_studio
```

```sql
SELECT COUNT(*) FROM products;
SELECT * FROM products LIMIT 5;
```

Exit:

```sql
\q
```

---

## Running the Full Pipeline

To load data into CSV, Google Sheets, and PostgreSQL simultaneously:

```env
LOAD_TO_GOOGLE_SHEETS=true
LOAD_TO_POSTGRESQL=true
```

Run:

```bash
python main.py
```

---

## Running Tests

Execute all unit tests:

```bash
python -m pytest tests
```

---

## Running Coverage

Generate coverage report:

```bash
coverage run -m pytest tests
coverage report -m
```

---

## Expected Dataset Schema

| Column    | Description                        |
| --------- | ---------------------------------- |
| Title     | Product name                       |
| Price     | Product price in Indonesian Rupiah |
| Rating    | Product rating as float            |
| Colors    | Number of available colors         |
| Size      | Product size                       |
| Gender    | Target gender                      |
| timestamp | Extraction timestamp               |

---

## Security

The following files should never be committed to GitHub:

```text
.env
google-sheets-api.json
products.csv
venv/
__pycache__/
```

Use `.env.example` as a public configuration template.

---

## Future Improvements

* Docker containerization
* Apache Airflow orchestration
* Incremental loading strategy
* Data quality monitoring
* CI/CD with GitHub Actions
* Cloud deployment (AWS, GCP, Azure)

---

## Author

Built as a Data Engineering portfolio project to demonstrate:

* Web Scraping
* ETL Development
* Data Cleaning
* Data Warehousing
* Automated Testing
* Configuration Management
* Data Pipeline Design
