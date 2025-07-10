# Meteor Dashboard

This project provides an interactive dashboard built with [Streamlit](https://streamlit.io/) for exploring meteorite landings. It loads the **Meteorite_Landings.csv** dataset and offers visualisations, tables and statistics about meteorites discovered around the world.

## Setup

1. Install Python 3.
2. Install the required libraries:
   ```bash
   pip install streamlit pandas pydeck
   ```
3. Place `Meteorite_Landings.csv` in the repository root. The dataset follows the [NASA Meteorite Landings](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh) format and must include columns such as `name`, `id`, `mass (g)`, `year`, `reclat` and `reclong`.

## Running the Dashboard

Run Streamlit from the repository directory:

```bash
streamlit run app.py
```

Streamlit will print a local URL. Open that URL in your browser to use the dashboard. You can filter meteorites by year, mass and class, switch between maps, charts, data tables and view key insights.

## Usage

- **Overview**: Shows a map of meteor landings and key statistics.
- **Charts**: Displays bar and line charts for top classes and mass statistics.
- **Data Tables**: Lists heaviest meteorites, common classes and other tables.
- **Key Insights**: Highlights interesting observations from the entire dataset.

Ensure the dataset is present before running, otherwise the app will fail to load the data.


