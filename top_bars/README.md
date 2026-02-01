[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erickgl1003/funky-scripts/blob/main/top_bars/jupyter_notebook.ipynb?forcereload=1)
# Top Bars

A collection of scripts for fetching [The World's 50 Best Bars](https://www.theworlds50best.com/bars/list/1-50) data.

## Files

### `top_bars.py`
The main Python script that processes top bars data. This script handles data extraction & transformation by leveraging Selenium.

### `jupyter_notebook.ipynb`
An interactive Jupyter Notebook for exploratory data analysis and visualization of top bars data. Open this in Jupyter or VS Code's notebook viewer to run cells interactively.

### `data/top_bars_{year}.txt`
The input data file containing top bars information for a given year, created in `top_bars.py`. This text file serves as the primary dataset used by the Jupyter Notebook.

## Usage

1. **For updating the dataset**: Run `python top_bars.py` from the terminal
2. **For interactive exploration**: Open `jupyter_notebook.ipynb` in Jupyter or VS Code
3. **Data**: Ensure `data/top_bars_{year}.txt` exists and contains the necessary data before running scripts
