# params.py
"""
Project Configuration
=====================

This module defines the project configuration.
----------------------------------------------
        ♫ Svaneborg Kardyb - Cycles ♪
"""

from pathlib import Path
from typing import List

class Config:
    """
    Project configuration.

    Attributes:
        DISPLAY_PLOT (bool): Whether to display the plot.
        SAVE_PLOT_AS_FILE (bool): Whether to save the plot as a file.
        SORT_DF (bool): Whether to sort the missing flags data by a specific column.
        EXPORT_MISSING_FLAGS_TO_CSV (bool): Whether to export missing flags to a CSV file.
    """

    DISPLAY_PLOT: bool = True
    """Whether to display the plot."""
    SAVE_PLOT_AS_FILE: bool = True
    """Whether to save the plot as a file."""
    SORT_DF: bool = False
    """Whether to sort the missing flags data by a specific column."""
    EXPORT_MISSING_FLAGS_TO_CSV: bool = True
    """Whether to export missing flags to a CSV file."""


    def __init__(self):
        """
        Initialize the configuration.
        """
        self.BASE_DIR: Path = Path(__file__).parent
        """The base directory of the project."""
        self.PLOT_FOLDER: Path = self.BASE_DIR / 'consolidation_analysis'
        """The plot-related folder."""
        self.PLOT_FOLDER.mkdir(parents=True, exist_ok=True)

        self.DATA_FOLDER: str = str(self.BASE_DIR / 'datasets')
        """The source datasets folder."""
        self.CONSOLIDATED_FILENAME: str = 'consolidated_dataset.csv'
        """The consolidated filename."""

        self.MISSING_FLAGS_FILENAME: str = str(self.PLOT_FOLDER / 'dummy_dataset.csv')
        """The missing flags filename."""
        self.PLOT_FILENAME: str = str(self.PLOT_FOLDER / 'missing_values_comparison.png')
        """The plot filename."""
        
        self.SORT_COLUMN: str = 'Link'
        """A column name."""

        self.HEADERS: List[str] = [
            'Title', 'Link', 'Add Date', 'Last Modified',
            'last_checked', 'Active', 'h1', 'p', 'meta_description'
        ]
        """The headers."""


