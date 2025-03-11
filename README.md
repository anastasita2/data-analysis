# VHI-Analysis
Project in learning purpose, data was collected, analyzed using different procedures

Overview

This project is designed to automate the process of downloading, processing, and analyzing Vegetation Health Index (VHI) data for administrative regions of Ukraine. The main objectives include data retrieval, preprocessing, transformation, and analysis for detecting extreme drought conditions.

Features
1. Downloading VHI Data

The script downloads VHI data for all administrative regions of Ukraine from NOAA.
Data is stored in structured CSV files with a timestamp to avoid overwriting.
Supports re-running the script to append new data without duplication.

2. Loading Data into DataFrame

Reads all downloaded CSV files and loads them into a Pandas DataFrame.
Cleans column names to ensure better readability and processing.
Handles missing values and removes unnecessary columns.

3. Region Index Mapping

Replaces numeric region indices from NOAA with their corresponding region names for better clarity.

4. VHI Analysis

  4.1 Retrieve VHI Series for a Specific Region and Year

  Filters the dataset to return the VHI values for a given region and year.

  4.2 Find Extremes (Min, Max), Mean, and Median for a Given Region and Year

  Calculates statistical values (min, max, mean, and median) for a given region and year.

  Displays the results in a well-formatted output.

  4.3 Retrieve VHI Data for a Given Range of Years and Regions

  Extracts and returns VHI data for a specified set of regions over a given time range.

  4.4 Detect Extreme Drought Events

  Identifies years where extreme drought (VHI < 15) affected more than 20% of administrative regions.

  Returns a list of affected years along with the impacted regions and their VHI values.


Installation & Setup

Prerequisites

Python 3.x

Required Libraries: pandas, numpy, os, shutil, datetime, urllib

Install missing dependencies using:

    pip install pandas numpy

Running the Project

Clone the repository:

    git clone https://github.com/VHI-Analysis
    
    cd VHI-Analysis

Run the data download script:

python script.py

Process and analyze the data using the provided functions.

Usage

Modify the function parameters to retrieve and analyze data for specific regions and years.
Example:

    wanted_reg = "Kyiv"
    
    wanted_year = "2020"
    
    vhi_series = get_vhi_series(df, wanted_reg, wanted_year)
    
    print(vhi_series)

Contribution

Feel free to fork and improve the code! If you find any issues, submit a pull request or open an issue in the repository.
