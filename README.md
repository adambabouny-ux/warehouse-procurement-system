# Warehouse & Procurement Management System

A Python backend project I built to stop learning theory 
and start solving real problems.

## Why I Built This

I got tired of tutorials that teach you syntax but never 
show you how systems actually work in the real world.

So I picked a real problem — warehouse managers at 
industrial companies like OCP in Morocco are still tracking 
stock in Excel. No alerts. No automation. They find out 
something is missing when a machine stops working.

I built a system that fixes that.

## What It Does

The system monitors warehouse inventory automatically.
When a product drops below its minimum threshold, it fires 
an alert and creates a Purchase Order — without any human 
intervention. The PO goes through a real approval workflow 
(DRAFT → SUBMITTED → APPROVED → RECEIVED) and every morning 
it exports a clean Excel dashboard for the warehouse manager.

No more Excel files updated by hand. No more surprises.

## What I Actually Built

- Inventory tracking with full audit trail (every IN/OUT movement recorded)
- Automated low-stock alert engine
- Purchase Order system that checks for duplicates before creating new orders
- PO status workflow (like a mini SAP module)
- Daily Excel report with 3 sheets: Stock / Alerts / Purchase Orders
- Clean architecture: db / models / engine / reports — each module does one job

## Tech Stack

- Python 3.12
- SQLite (with foreign keys, constraints, UNIQUE validation)
- pandas + openpyxl for Excel reporting
- Git for version control (first time using it — learned it for this project)

## How To Run

```bash
# Clone the repo
git clone https://github.com/adambabouny-ux/warehouse-procurement-system.git
cd warehouse-procurement-system

# Install dependencies
pip install pandas openpyxl

# Initialize database (run once)
python seed.py

# Run the system
python main.py
```

## What I Learned

The hardest parts were not the code.

Getting Git to work on Windows with multiple Python 
installations fighting each other took longer than 
building the alert engine. I learned that real engineering 
is 30% writing code and 70% debugging things nobody 
warned you about.

I also learned that CSV files need consistent structure 
the hard way — after hitting a field mismatch error that 
took me an hour to understand.

But the most important thing I learned is that when you 
build something that solves a real problem, even a small 
one, the motivation to fix bugs is completely different 
from doing exercises.

## Context

This project is inspired by how companies like OCP Group 
and JESA manage industrial warehouses in Morocco. The 
problems are real. The automation gap is real.

I am a student building portfolio projects to get into 
supply chain and ERP systems. This is project one.

---
Built by Adam Babouny
