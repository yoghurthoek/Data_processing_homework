#!/usr/bin/env python
# Name: Jochem van den Hoek
# Student number: 11066288
import pandas as pd
import matplotlib.pyplot as plt

# Parsing the data
# (Make sure unknown get recognized as missing data and comma as decimal sep)
df = pd.read_csv("input.csv", decimal=",", index_col='Country',
                 na_values="unknown", skipinitialspace=True)

# Clean Whitespaces around regions
df["Region"] = df["Region"].str.strip()

# Relevant columns for the json file
coltojson = ["Region", "Pop. Density (per sq. mi.)",
             "Infant mortality (per 1000 births)",
             "GDP ($ per capita) dollars"]

# Change notation of GDP to useable numbers for analyzing
GDP = "GDP ($ per capita) dollars"
df[GDP] = df[GDP].str.replace(" dollars", "")
df[GDP] = pd.to_numeric(df[GDP], downcast='float')


def xexoutlier(dafr, column):
    """
    Excludes extreme outliers based on IQR range
    """
    # Calculate interquantile range
    q1 = dafr[column].quantile(0.25)
    q3 = dafr[column].quantile(0.75)
    iqr = q3 - q1
    # Exclude extreme outliers in GDP
    dafr = dafr[dafr[column] <= q3 + 3 * iqr]
    return dafr


# exclude outliers GDP
df = xexoutlier(df, GDP)

# Look at median, mode, mean and stdev
print(f"Mean GDP : {df[GDP].mean()}\n"
      + f"Median GDP : {df[GDP].median()}\n"
      + f"Mode GDP : {df[GDP].mode()[0]}")

# Plot a histogram
df.hist(column="GDP ($ per capita) dollars", bins=20, grid=False,
        color='hotpink', rwidth=0.9)
plt.title("Oneerlijkheid op de wereld")
plt.xlabel("GDP ($ per capita) dollars")
plt.ylabel("Frequency")
plt.show()


# Exclude extreme outliers of infant mort
babies = "Infant mortality (per 1000 births)"
df = xexoutlier(df, babies)
# Look at the five numbers (or use describe, just saying)
print(f"Median infant mortality : {df[babies].median()}\n"
      + f"Q1 infant mortality : {df[babies].quantile(0.25)}\n"
      + f"Q3 infant mortality : {df[babies].quantile(0.75)}\n"
      + f"Minimum infant mortality : {df[babies].min()}\n"
      + f"Maximum infant mortality : {df[babies].max()}")

# Make the boxplot of infant mortality
df.boxplot(column="Infant mortality (per 1000 births)", grid=False)
plt.title("Kindersterfte")
plt.show()

# Make into jason file
df[coltojson].to_json("output.json", orient="index")
