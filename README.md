# Hawaii Climate Analysis

This project analyzes climate data from Hawaii using SQLAlchemy and Flask. The analysis includes:

### 1. Precipitation analysis
### 2. Station analysis
### 3. Temperature analysis

### Data Source

The data is stored in an SQLite database located in Resources/hawaii.sqlite. The database includes two tables: Measurement and Station.

### Dependencies

The following libraries are required to run the code:

matplotlib

numpy

pandas

datetime

sqlalchemy

flask

flask_sqlalchemy

### Files

climate_analysis.ipynb: Jupyter notebook with the data analysis code

app.py: Flask app that displays the results of the analysis

Resources/: directory containing the SQLite database and CSV files

### Usage

To run the Flask app:

Open the project in Visual Studio Code.

Run app.py in the terminal using the command python app.py.

Open a web browser and navigate to http://localhost:5000/.

Use the available endpoints to retrieve data from the database:

http://localhost:5000/api/v1.0/precipitation

http://localhost:5000/api/v1.0/stations

http://localhost:5000/api/v1.0/tobs

http://localhost:5000/api/v1.0/<start_date>

http://localhost:5000/api/v1.0/<start_date>/<end_date>

Use the returned data to perform further analysis or visualization as needed.

### Results

The Flask app displays the following information:

Precipitation data for the last 12 months

The most active weather station and its temperature data

Temperature data for the most active station in the last 12 months

Returns the min, max, and average temperatures calculated from the given start date to the given end date

### Contact

If you have any questions or feedback about this script, please feel free to contact me at param.birdi@utoronto.ca.

### Acknowledgments

This code was written by Paramdeep Singh Birdi as part of a project for a data analysis course. Most of the data used in this project was provided by the course instructors.
