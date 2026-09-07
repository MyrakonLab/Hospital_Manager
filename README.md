# Hospital Management System

A command-line hospital management system built in Python with MySQL, managing doctors, patients, medical tests, and billing.

## Overview

This project maintains records for doctors, patients, and medical tests, and generates an itemized bill combining doctor's fee, test charges, room charges (for admitted patients), and a 15% service charge. I reviewed and fixed the original code, verifying each bug empirically before correcting it.

## Features

- **Doctor Management** — add, update, delete, and display doctor records (ID, name, contact, specialization, fees, room number, date of birth)
- **Patient Management** — add, delete, and display patient records, including admission status (Admit / OPD) and assigned doctor
- **Medical Tests** — add tests, update charges, and view the full test list
- **Billing** — generate an itemized bill for a patient combining doctor's fee, selected test charge, room charges (if admitted, based on number of days), and a 15% service charge

## Tech Stack

- Python 3
- MySQL (via `mysql-connector`)

## How to Run

```bash
python3 hospital_management.py
```

Requires a MySQL server running locally with a `hospital` database containing the `doctor`, `patient`, and `medicaltest` tables (see the original project report for the exact table schema).

## Bugs Fixed From the Original

- **The doctor-deletion existence check was broken** — it was supposed to verify a given Doctor ID exists before deleting it, but the query was missing its `WHERE` clause entirely. I tested deleting an ID that was never in the table, and it reported "Deleted successfully" anyway. Fixed the query, and found and fixed the identical bug in patient deletion.
- **Billing crashed** if given a Patient ID, Doctor ID, or test name that doesn't exist in the database, instead of showing an error. Now handled gracefully.
- **Adding a patient crashed** if the admission status was typed as anything other than exactly `"admit"`, `"ADMIT"`, or `"OPD"` (e.g. lowercase `"opd"`) — the room number was never assigned in that case, causing an `UnboundLocalError`. Fixed with proper status handling and a clear error for invalid input.
- Replaced raw string-formatted SQL queries with parameterized queries throughout (the original was vulnerable to SQL injection and would break on any input containing a quote character), and wrapped doctor registration in error handling so a duplicate Doctor ID gives a clear message instead of crashing the whole program.
