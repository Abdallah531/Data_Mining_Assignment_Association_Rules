# Data_Mining_Assignment_Association_Rules



## Introduction

This tool implements association rule mining algorithms to analyze transaction data from a bakery dataset. The program allows users to discover frequent item sets and strong association rules based on their specified minimum support count and minimum confidence level.

## Problem Description

Consider the sets of transactions for a Bakery provided in the attached file "Bakery.csv". Each transaction represents a set of items defined with their names at a specific time. The task is to implement an association rule mining algorithm (such as Apriori, FP-Growth, or vertical data format) to find the association between items in the transactions. The program should allow users to input the minimum support count and minimum confidence (percentage value) during runtime. The final output should display the frequent item sets and association rules with their confidence.

## Features

- **User-Friendly Interface**: The program provides a graphical user interface (GUI) for easy interaction.
- **Variable Support and Confidence**: Users can input their desired minimum support count and minimum confidence level.
- **Percentage of Data Selection**: Users can specify the percentage of data from the input file to be analyzed.
- **Frequent Item Sets**: The program identifies frequent item sets based on the specified parameters.
- **Association Rules**: Strong association rules are generated and displayed along with their confidence levels.

## Screenshots

### Main GUI

![Main GUI](https://github.com/Abdallah531/Data_Mining_Assignment_Association_Rules/assets/117390537/00339b0f-fb06-4113-94a0-592367f88725)

### Analysis Results

![Analysis Results](https://github.com/Abdallah531/Data_Mining_Assignment_Association_Rules/assets/117390537/8b6d0038-d280-4809-9bbf-32162588b3a5)


## Requirements

- Python 3.x
- pandas
- tkinter (for GUI)
- collections
- itertools

## How to Use

1. **Input File**: Provide a CSV file containing transaction data.
2. **Percentage of Data**: Specify the percentage of data to be analyzed.
3. **Minimum Support Count**: Enter the minimum support count for frequent item sets.
4. **Minimum Confidence (%)**: Define the minimum confidence level for association rules.
5. Click the **Analyze** button to perform the analysis.
6. View the results in the text area below, which displays frequent item sets and association rules.


