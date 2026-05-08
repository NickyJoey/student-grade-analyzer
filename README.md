# Class Percentile & Letter-Grade Estimator

A Python-based command-line tool that estimates a student's percentile rank and expected letter grade using customizable class grade distributions.

This project allows users to define grade tiers, score ranges, and student counts for each tier in order to estimate:

- Expected letter grade
- Approximate class rank
- Top percentage placement
- Percentile standing

---

## Features

- Customizable grade tiers (A+, A, A-, B+, etc.)
- Editable score ranges for each grade tier
- Input validation for score ranges and class counts
- Percentile and rank estimation
- JSON output support
- Organized modular code structure
- Simple command-line interface

---

## How It Works

The estimator calculates:

1. The number of students in higher grade tiers
2. Your estimated position within your current grade tier
3. An approximate class rank based on score distribution
4. Your percentile placement within the class

The estimation is based on user-provided class distribution data and score ranges.

---

## Project Structure

```text
student-grade-analyzer/
│
├── main.py              # Main CLI application flow
├── utils.py             # Validation and estimation logic
├── README.md
├── requirements.txt
└── example_run.txt
Installation

Clone the repository:

git clone https://github.com/NickyJoey/student-grade-analyzer.git
cd student-grade-analyzer

Run the program:

python main.py
Example Usage
Default grade tiers (from highest to lowest):
A+, A, A-, B+, B, B-, C+, C, C-, D, F

Class size (N): 85

Count in A+: 4
Count in A: 7
Count in A-: 10
Count in B+: 14
Count in B: 20
Count in B-: 12
Count in C+: 8
Count in C: 6
Count in C-: 2
Count in D: 1
Count in F: 1

Your estimated score (0-100): 86

Output:

===== ESTIMATE =====
Estimated tier: A-
Estimated rank: ~12 / 85
Approximate percentile: 85.9th
Estimated position: Top 14.1%
====================
Technologies Used
Python 3
Standard Python libraries
Command-line interface (CLI)
Future Improvements

Planned features for future versions include:

CSV file import support
GPA calculation support
Data visualization and graphs
GUI or web-based interface
Enhanced statistical analysis
Exporting results to JSON or CSV
Author

Yucheng Qiao
University of Alberta — Computer Science Student

GitHub: https://github.com/NickyJoey
