#!/usr/bin/env python
# Name: Jochem van den Hoek
# Student number: 11066288
import pandas as pd
import matplotlib.pyplot as plt

# Parsing the data
df = pd.read_csv("input.csv", decimal=",", index_col='Country',
                 na_values="unknown", skipinitialspace=True)
df["Region"] = df["Region"].str.strip()

# Relevant columns
coltojson = ["Region", "Pop. Density (per sq. mi.)",
             "Infant mortality (per 1000 births)",
             "GDP ($ per capita) dollars"]

# Change notation of GDP to useable numbers for analyzing
GDP = "GDP ($ per capita) dollars"
df[GDP] = df[GDP].str.replace(" dollars", "")
df[GDP] = pd.to_numeric(df[GDP], downcast='float')

# Calculate interquantile range
q1 = df[GDP].quantile(0.25)
q3 = df[GDP].quantile(0.75)
iqr = q3 - q1

# Exclude extreme outliers
df = df[df[GDP] <= q3 + 3 * iqr]

# Look at median, mode, mean and stdev
print(df[GDP].mean())
print(df[GDP].median())
print(df[GDP].mode()[0])

# Plot a histogram
df[GDP].hist()
plt.show()

# Look at the five numbers (or use describe, just saying)
babies = "Infant mortality (per 1000 births)"
print(df[babies].median())
print(df[babies].quantile(0.25))
print(df[babies].quantile(0.75))
print(df[babies].min())
print(df[babies].max())

# Plot the death baby rate
df.boxplot(column="Infant mortality (per 1000 births)")
plt.show()

# Make into json file
df[coltojson].to_json("output.json", orient="index")
