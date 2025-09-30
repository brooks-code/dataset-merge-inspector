# The Tome of missing values

## One dataset to rule them all

![Banner Image](/img/ErtaAle.gif "Magma animated gif.")

*It's data consolidation time (Erta Ale, Source R. Roscoe's [photovolcanica](http://www.photovolcanica.com/VolcanoInfo/Erta%20Ale/Erta%20Ale.html)).*

### Genesis

> This script is the offspring of an ongoing bigger project involving some scraping. And well, as many of you knows it already: scraping is *dirty*. In order to maximize the **performance** of the process, I gathered several variations of similar datasets with the aim to merge them into a most complete one. *This* missing values comparison tool is the visual companion that provides insights about it.

## Table of contents

<details>
<summary>Contents - click to expand</summary>

- [The Tome of missing values](#the-tome-of-missing-values)
  - [One dataset to rule them all](#one-dataset-to-rule-them-all)
    - [Genesis](#genesis)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Input CSV](#input-csv)
    - [Input Dataset Description](#input-dataset-description)
  - [Configuration Module](#configuration-module)
    - [Key attributes](#key-attributes)
    - [Configuration initialization](#configuration-initialization)
  - [Main functions overview](#main-functions-overview)
    - [process\_boolean\_columns function](#process_boolean_columns-function)
    - [generate\_color\_map function](#generate_color_map-function)
    - [plot\_heatmap function](#plot_heatmap-function)
  - [Limitations](#limitations)
  - [Troubleshooting](#troubleshooting)
  - [Deeper dive](#deeper-dive)
  - [License](#license)

</details>

## Overview

**Let the records be consolidated!**

This script reads a pandas DataFrame, where specific columns are boolean representations, and generates a visualization displaying the missing values in the datasets, allowing users to compare and analyze the data.

![Banner Image](/img/missing_values_dataviz.png "Matplotlib best practice missing values matrix.")
*This missing values chart allows a quick overview of several dataset versions.*

## Features

- **F.A.S.T:** Uses boolean representations.
- **Binary matrix visualization:** Displays **missing values** in the datasets.
- **Automatic color schemes:** a color map is automatically applied on a per dataset basis.
- **Confirmation footer:** Displays the website's status (link active) as a footer for better discriminative performance.
- **Customizable:** Finito Matplotlib's default quirks. Allows users to tune the colors and some other graphic perks.
- **Elegant design:** Careful chromatic choices. Aims to be easy on the eyes.

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)

## Installation

1. Ensure you have Python 3 installed.
2. Clone or download this repository.
3. From the script's directory, install the required dependencies using pip:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

Make sur you have a correctly formatted [input CSV](#input-dataset-description) in the right [directory](#configuration-module) and run the script.

  ```bash
  python missing_data_comparison.py
  ```

- The script will generate a visualization and display it.
- The visualization can be saved as a file using the `SAVE_PLOT_AS_FILE` parameter from the `params.py` file.

## Input CSV

This script **requires** a specific input file structure.
For reproductibility purposes, a *dummy dataset* is provided within this repository as well.

<details>
<summary>Contents - click to expand</summary>

*Example:*

  ```csv
  Link,Website_active,Title_fusioned.csv,Title_dataset1.csv,Title_dataset2.csv,Title_dataset.csv,Title_dataset3.csv,Title_dataset4.csv,Add Date_fusioned.csv,Add Date_dataset1.csv,Add Date_dataset2.csv,Add Date_dataset.csv,Add Date_dataset3.csv,Add Date_dataset4.csv,Last Modified_fusioned.csv,Last Modified_dataset1.csv,Last Modified_dataset2.csv,Last Modified_dataset.csv,Last Modified_dataset3.csv,Last Modified_dataset4.csv,last_checked_fusioned.csv,last_checked_dataset1.csv,last_checked_dataset2.csv,last_checked_dataset.csv,last_checked_dataset3.csv,last_checked_dataset4.csv,Active_fusioned.csv,Active_dataset1.csv,Active_dataset2.csv,Active_dataset.csv,Active_dataset3.csv,Active_dataset4.csv,h1_fusioned.csv,h1_dataset1.csv,h1_dataset2.csv,h1_dataset.csv,h1_dataset3.csv,h1_dataset4.csv,p_fusioned.csv,p_dataset1.csv,p_dataset2.csv,p_dataset.csv,p_dataset3.csv,p_dataset4.csv,meta_description_fusioned.csv,meta_description_dataset1.csv,meta_description_dataset2.csv,meta_description_dataset.csv,meta_description_dataset3.csv,meta_description_dataset4.csv
www.link1.com,yes,False,False,False,False,False,False,False,True,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,True,True,True,True,True
  ```

### Input Dataset Description

The input dataset is provided as a **comma-separated values (CSV)** file with a header row defining the structure of the data. In this particular use case,the overall layout consists of different categories of columns:

1. **Link and Activity Status:**
   - **Link:** The primary URL identifier for each record (string).
   - **Website_active:** A string ("yes"/"no") indicates whether the website associated with the link is active.

<ins>Boolean columns:</ins>
Indicates wether data is missing (True) or not (False).

   - Columns are prefixed with a column base name (e.g. "Title_") and suffixed with one of the individual dataset name or the fusioned version's one.

2. **Title columns**

3. **Add Date columns**

4. **Last Modified columns**

5. **Last Checked columns**

6. **Active columns**

7. **h1 columns**

8. **p columns**

9. **Meta Description columns**

</details>

## Configuration Module

A centralized approach simplifies development and maintenance, making it easier to manage the project's settings as it scales.

<details>
<summary>Contents - click to expand</summary>

The module, defined in `params.py`, serves as the backbone for the project's configuration settings is encapsulated within the `Config` class. It handles various parameters needed to control the behavior of the analysis and plotting routines.

### Key attributes

<ins>This script relevant ones only:</ins>

- **DISPLAY_PLOT (bool):**
  Determines whether the generated plot should be displayed to the user.

- **SAVE_PLOT_AS_FILE (bool):**
  Indicates if the plot should be saved as an image file.

- **SORT_DF (bool):**
  Specifies whether the missing flags data should be sorted by a designated column.

### Configuration initialization

When an instance of `Config` is created, it performs the following steps:

1. **Directory setup:**
   - Determines the base directory using the location of `params.py`.
   - Creates a `fusion_analysis` folder (if it doesn't already exist) where plot related files are located and written.

2. **Data and Results file configuration:**
   - `PLOT_FOLDER`: Directory (*default:* `fusion_analysis`) where the missing flags CSV  is located and where the plot is eventually saved .
   - `MISSING_FLAGS_FILENAME`: CSV file that holds missing flags information (*default:* `dummy_dataset.csv`).
   - `PLOT_FILENAME`: Path for saving the missing values comparison plot (*default:* `missing_values_comparison.png`).

3. **Sort configuration:**
   - `SORT_COLUMN`: The specific column name used for sorting the data (*default:* `Link`).

</details>

## Main functions overview

Some notable functions:

<details>
<summary>Contents - click to expand</summary>

### process_boolean_columns function

This function processes the boolean columns in the DataFrame, ensuring they are converted to boolean representations.

### generate_color_map function

This function generates a color map for the heatmap, assigning a color to each unique base-type of column names.

### plot_heatmap function

This function plots the final heatmap, combining the boolean image and website active image.
</details>

## Limitations

- The script assumes a specific structure for the input DataFrame; different or more complex datasets will require modifications.
- The visualization is limited to displaying missing values.

## Troubleshooting

- Check that the dependencies are correctly installed if you encounter import errors.
- Ensure that the input missing flags csv file contains the required *column structure* (dataset-suffixed column names and booleans as values).

## Deeper dive

This is only a small subset of bigger project involving scraping, datafusion, various machine learning algorithms and a bit of UX/UI ideas.

**Still very W.I.P.**

![Footer Image](/img/squid.gif "It's a colossal squid!")

**More will follow..**

## License

The source code is provided under a [Creative Commons CC0](https://creativecommons.org/public-domain/cc0/) license. See the [LICENSE](/LICENSE) file for details.
