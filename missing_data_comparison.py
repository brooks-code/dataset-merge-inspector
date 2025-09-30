#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File name: missing_data_comparison.py
# Author: B1977.14.11944
# Date created: 2025-04-30
# Version = "1.0"
# License =  "CC0 1.0"
# =============================================================================
""" A simple and yet innovative approach to visualize missing values from 
similar datasets."""
# =============================================================================

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgba
from typing import List, Tuple, Dict, Optional
from params import Config


# Parameters
params: Config = Config()

PRIMARY_DARK_COLOR = 'dimgrey'
SECONDARY_DARK_COLOR = 'darkslategrey'
BACKGROUND_COLOR = 'aliceblue'


# Global matplotlib style configuration
plt.rcParams['axes.facecolor'] = BACKGROUND_COLOR
plt.rcParams['figure.facecolor'] = BACKGROUND_COLOR
plt.rcParams['axes.edgecolor'] = 'none'
plt.rcParams['axes.grid'] = False

plt.rcParams['ytick.left'] = False
plt.rcParams['xtick.bottom'] = False

plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['axes.labelcolor'] = PRIMARY_DARK_COLOR
plt.rcParams['xtick.color'] = PRIMARY_DARK_COLOR
plt.rcParams['text.color'] = PRIMARY_DARK_COLOR
plt.rcParams["font.family"] = "sans-serif"



# ---------------------------------------------------------------------------
# Functions
def extract_base_suffix(col: str) -> Tuple[str, str]:
    """
    Extracts the base name and suffix from a column name.

    For a column name that contains an underscore, returns a tuple
    (base, suffix) where 'base' is the part before the last underscore and
    'suffix' is the part after that underscore. If no underscore is present,
    the entire column name is returned as base with an empty suffix.

    Parameters:
    - col: The column name as a string.

    Returns:
    - A tuple (base, suffix). If no underscore is found, suffix is an empty string.
    """
    if '_' in col:
        base, suffix = col.rsplit('_', 1)
    else:
        base, suffix = col, ''
    return base, suffix


def process_boolean_columns(df: pd.DataFrame,
                            ignore_cols: List[str] = [
                                "Link", "Website_active"],
                            selected_bases: Optional[List[str]] = None
                            ) -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Processes boolean-related columns in a DataFrame by converting them to boolean (1/0)
    and filtering based on provided parameters.

    This function skips columns listed in ignore_cols and optionally filters to keep only
    those columns whose base (derived from column name) is in selected_bases. It returns a data matrix,
    the corresponding base names, and suffixes.

    Parameters:
    - df: The input pandas DataFrame.
    - ignore_cols: List of columns to skip from processing.
    - selected_bases: Optional list of base names to include. If None, all columns (except ignored) are used.

    Returns:
    - data_matrix: NumPy array of ints where True -> 1 and False -> 0.
    - bases: List of base names for each processed column.
    - suffixes: List of suffixes for each processed column.
    """
    bool_cols_all = [col for col in df.columns if col not in ignore_cols]

    df[bool_cols_all] = df[bool_cols_all].replace(
        {'True': True, 'False': False}).astype(bool)

   # Convert values to boolean (if stored as strings)
    # df.loc[:, bool_cols_all] = df.loc[:, bool_cols_all].astype(bool)

    # Extract base and suffix for each column
    bases_all, suffixes_all = zip(
        *[extract_base_suffix(col) for col in bool_cols_all])
    bases_all = list(bases_all)
    suffixes_all = list(suffixes_all)

    if selected_bases is None:
        bool_cols = bool_cols_all
        bases = bases_all
        suffixes = suffixes_all
    else:
        indices = [i for i, base in enumerate(
            bases_all) if base in selected_bases]
        indices.sort(key=lambda i: selected_bases.index(bases_all[i]))
        bool_cols = [bool_cols_all[i] for i in indices]
        bases = [bases_all[i] for i in indices]
        suffixes = [suffixes_all[i] for i in indices]

    data_matrix = df[bool_cols].astype(int).to_numpy()

    return data_matrix, bases, suffixes


def generate_color_map(suffixes: List[str]) -> Tuple[Dict[str, tuple], List[tuple]]:
    """
    Generates a color map for a list of suffixes, assigning an RGBA color to each unique suffix.

    Depending on the number of unique suffixes, colors are chosen from matplotlib's 'tab10' or 'tab20' colormap.
    Also returns a list of colors mapped in the input order of suffixes.

    Parameters:
    - suffixes: A list of suffix strings.

    Returns:
    - color_map: A dictionary mapping each unique suffix to its RGBA color.
    - column_colors: A list of RGBA colors corresponding to each suffix in the input order.
    """
    unique_suffixes = sorted(set(suffixes))
    num_suffixes = len(unique_suffixes)
    cmap = plt.cm.get_cmap('tab10' if num_suffixes <=
                           10 else 'tab20', num_suffixes)
    color_map = {suffix: to_rgba(cmap(i))
                 for i, suffix in enumerate(unique_suffixes)}
    column_colors = [color_map[sfx] for sfx in suffixes]
    return color_map, column_colors


def create_boolean_image(data_matrix: np.ndarray,
                         column_colors: List[tuple],
                         bg_color: tuple = (240/255, 248/255, 1, 1.0)) -> np.ndarray:
    """
    Create an image (NumPy array) representing boolean data using a custom background color.
    For each boolean column, cells with True are colored as specified in column_colors.
    The final image has shape (n_boolean_columns, n_rows, 4).

    Parameters:
    - data_matrix: A boolean (or int) matrix with shape (n_rows, n_columns).
    - column_colors: A list of RGBA tuples for each column.
    - bg_color: RGBA tuple for the background (default is Alice Blue: (240, 248, 255, 1.0)).

    Returns:
    - img: Numpy array with shape (n_columns, n_rows, 4) representing the colored boolean image.
    """
    n_rows, n_cols = data_matrix.shape
    img = np.full((n_cols, n_rows, 4), bg_color, dtype=float)
    for col_idx, col_color in enumerate(column_colors):
        img[col_idx, data_matrix[:, col_idx] == 1, :] = col_color
    return img


def create_website_active_image(df: pd.DataFrame,
                                col_name: str = "Website_active") -> np.ndarray:
    """
    Create an image (NumPy array) for displaying website active information.

    This function converts the specified "Website_active" column values to colors:
    - "yes" (case-insensitive) becomes darkslategrey.
    - Any other value becomes darkorange.

    Parameters:
    - df: The pandas DataFrame containing website activity data.
    - col_name: The column name representing the website active status.

    Returns:
    - img_active: NumPy array of shape (1, n_rows, 4) representing the active status colors.
    """
    active_vals = df[col_name].astype(str).str.lower().str.strip()
    colors = [to_rgba(SECONDARY_DARK_COLOR) if val == "yes" else to_rgba(
        'darkorange') for val in active_vals]
    img_active = np.array([colors], dtype=float)
    return img_active


def plot_heatmap(img_full: np.ndarray,
                 row_labels: List[str],
                 column_colors: List[tuple],
                 color_map: Dict[str, tuple]) -> None:
    """
    Plots a heatmap composed of boolean and website activity images.

    The heatmap displays the combined image (img_full) with y-axis labels. Boolean rows have their
    labels colored according to column_colors, and a legend is created to indicate the color-code.

    Parameters:
    - img_full: A NumPy array representing the full combined image.
    - row_labels: List of strings used as labels for the corresponding rows.
    - column_colors: List of RGBA tuples for coloring the boolean rows' labels.
    - color_map: Dictionary mapping suffixes to RGBA colors, used for the legend.
    """
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_xlabel('I N D E X', fontsize=8)
    ax.xaxis.set_label_coords(0.02, -0.04)
    ax.imshow(img_full, aspect='auto', interpolation='none', origin='upper')

    n_rows_total = img_full.shape[0]
    ax.set_yticks(np.arange(n_rows_total))
    ax.set_yticklabels(row_labels, fontsize=10)
    [label.set_va("center") for label in ax.get_yticklabels()]

    # Color the boolean row labels.
    for tick_label, col_color in zip(ax.get_yticklabels()[:-1], column_colors):
        tick_label.set_color(col_color)
    # Color the Website_active label.
    ax.get_yticklabels()[-1].set_color(SECONDARY_DARK_COLOR)

    plt.suptitle('MISSING VALUES COMPARISON', fontsize=16)
    fig.text(0.5, 0.94, 'This tool helps compare datasets relative to their missing values',
             ha='center', fontsize=10, color=PRIMARY_DARK_COLOR, fontstyle='italic', alpha=0.6)

    # Build legend (from color map and website active status).
    legend_handles = [
        mpatches.Patch(color=color, label=(
            suffix.replace('.csv', '') if suffix else 'default'))
        for suffix, color in color_map.items()
    ]
    legend_handles.append(mpatches.Patch(color='none', label=''))
    legend_handles.append(mpatches.Patch(color='none', label='LINK ACTIVE'))
    legend_handles.extend([
        mpatches.Patch(color=SECONDARY_DARK_COLOR, label='yes'),
        mpatches.Patch(color='darkorange', label='no')
    ])
    plt.legend(handles=legend_handles, title='DATASETS  ',
               frameon=False, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()

    if params.SAVE_PLOT_AS_FILE:
        plt.savefig(params.PLOT_FILENAME)
    if params.DISPLAY_PLOT:
        plt.show()

    plt.close(fig)



# ---------------------------------------------------------------------------
# Main Code
def main(df: pd.DataFrame,
         selected_bases: Optional[List[str]] = None,
         save_missing_report: bool = False,
         missing_report_filename: Optional[str] = None) -> None:
    """
    Main function to process an in-memory DataFrame,
    convert specific columns to boolean representations, and generate
    a missing values visualization.

    Parameters:
    - df: The in-memory pandas DataFrame containing your report.
    - selected_bases: Optional list of base column names to filter which columns to process.
    - save_missing_report: Optional; if True, saves the missing report as a CSV file.
    - missing_report_filename: Optional; filename to save the missing report.
    """
    data_matrix, bases, suffixes = process_boolean_columns(
        df, ignore_cols=["Link", "Website_active"], selected_bases=selected_bases)
    color_map, column_colors = generate_color_map(suffixes)
    img_bool = create_boolean_image(data_matrix, column_colors)
    img_active = create_website_active_image(df, col_name="Website_active")
    img_full = np.vstack([img_bool, img_active])
    row_labels = bases + ['link active']
    plot_heatmap(img_full, row_labels, column_colors, color_map)

    # Save the missing report if the flag is set.
    if save_missing_report and missing_report_filename:
        df.to_csv(missing_report_filename, index=False)


if __name__ == '__main__':
    # Specify filename in case you run it directly from this .py file
    df = pd.read_csv(params.MISSING_FLAGS_FILENAME)
    if params.SORT_DF:
        df.sort_values(by=[params.SORT_COLUMN])
    main(df, save_missing_report=True,
         missing_report_filename=params.MISSING_FLAGS_FILENAME)
