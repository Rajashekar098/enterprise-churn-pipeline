# Enterprise Telecom Customer Churn & LTV Pipeline

## Project Overview
This project demonstrates an automated Extract, Transform, Load (ETL) pipeline designed to process large-scale customer data (100,000+ records). It highlights advanced data engineering techniques using Python to clean, scale, and aggregate telecom subscriber data, ultimately feeding a highly optimized executive dashboard for customer experience and retention strategy.

## Technology Stack
* **Data Engineering:** Python (`pandas`, `numpy`)
* **Development Environment:** Visual Studio Code with GitHub Copilot
* **Business Intelligence:** Tableau Public

## Pipeline Architecture & Feature Engineering
* **Data Scaling & Quality:** Ingested raw telecom data and synthetically scaled it to a 105,645-row enterprise volume, correcting data type anomalies in financial columns.
* **Vectorized Transformations:** Replaced inefficient loops with `pandas` vectorization and `numpy.where()` logic to engineer features in milliseconds.
* **Customer Lifetime Value (LTV):** Engineered an LTV proxy metric utilizing monthly spend and tenure.
* **Risk Scoring:** Developed a binary `High_Risk_Flag` isolating month-to-month contracts with elevated monthly charges.
* **Pre-Aggregation for BI:** Grouped the 100k+ records into a lightweight, 102-row summary matrix to ensure zero-latency loading in Tableau.

## Files in this Repository
* `pipeline.py`: The automated Python script handling ingestion, transformation, and aggregation.
* `Enterprise_Churn_100k.csv`: The processed 105,645-row dataset.
* `Tableau_Executive_Summary.csv`: The optimized grouping matrix used for visualization.

## Executive Retention Dashboard
[Click here to view the interactive Customer Churn Tableau Dashboard](https://public.tableau.com/app/profile/rajashekar.chinthala/viz/Enterprise-Churn-Dashboard/Sheet1)
