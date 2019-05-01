#!/usr/bin/env python
# Name: Jochem van den Hoek
# Student number: 11066288
# Takes a csv file and converts it to json
from sys import argv
import pandas as pd


def csvtojson(input):
    """
    Make a dataframe and convert to json
    Assumes headers as first row, dots as delimiters and
    no unknown values not default to pandas
    """
    df = pd.read_csv(f"{input}", index_col=0)
    df.to_json("output.json", orient="index")


if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1].endswith('.csv'):
            input = argv[1]
            csvtojson(input)
        else:
            print("Give csv file")
    else:
        print("Usage: python converCSV2JSON <inputfile.csv>")
