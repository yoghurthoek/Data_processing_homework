#!/usr/bin/env python
# Name: Jochem van den Hoek
# Student number: 11066288
"""
This script visualizes data obtained from a .csv file
"""
from statistics import mean
import csv
import matplotlib.pyplot as plt

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}


# Read csv file
with open(INPUT_CSV, 'r', encoding = "utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data_dict[row['Year']].append(float(row['Rating']))

# Plot your findings
plt.plot([year for year in range(START_YEAR, END_YEAR)],
         [mean(data_dict[key]) for key in data_dict])
plt.ylabel("Average Rating")
plt.xlabel("Year of Release")
plt.ylim(8,9)
plt.show()

if __name__ == "__main__":
    print(data_dict)
