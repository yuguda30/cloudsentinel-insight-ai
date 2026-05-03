# CloudSentinel Insight AI

CloudSentinel Insight AI is an AI-powered business health analyzer for SMEs. It helps small business owners upload transaction records, analyze revenue and expenses, calculate a business health score, receive AI-based recommendations, and download professional business reports.

## Project Purpose

Many SMEs struggle with poor record keeping, weak financial visibility, and limited access to data-driven decision-making tools. This prototype helps business owners understand their numbers and identify risks early.

## Key Features

- User registration and login
- User-specific dashboard
- CSV and Excel transaction upload
- Revenue, expense, profit, and transaction analysis
- Business health score
- Risk level classification
- AI recommendations
- PDF business report generation
- Report history and download
- SQLite local database prototype

## Accepted Dataset Format

Recommended columns:

```csv
date,description,category,type,amount,currency,payment_method

Also supported:

Date
Product Category
Total Amount
TransactionAmount
Income/Expense
Mode
Vendor
TransactionDate

## Tech Stack

Python
Flask
SQLite
Pandas
Chart.js
HTML
CSS
JavaScript
ReportLab
Gunicorn

## Folder Structure

cloudsentinel-insight-ai/
├── app.py
├── config.py
├── requirements.txt
├── render.yaml
├── README.md
├── database/
│   ├── app.db
│   └── init_db.py
├── routes/
├── services/
├── templates/
├── static/
├── data/
│   └── uploads/
└── reports/
    └── generated/

## Local Setup

Clone the repository:

git clone https://github.com/yuguda30/cloudsentinel-insight-ai.git
cd cloudsentinel-insight-ai

Install dependencies:
pip install -r requirements.txt
Initialize database:
python database/init_db.py

Run the app:
python app.py
Open:
http://127.0.0.1:5000

## Demo Flow
1 Register a new account
2 Login
3 Upload CSV or Excel transaction data
4 View dashboard analysis
5 Check AI recommendations
6 Generate and download PDF report