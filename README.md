# Final Project
The Python RSS Reader is an application designed to fetch, parse, and display RSS feeds in a user-friendly format. 
Built using Python 3.9, this application not only retrieves live RSS feeds from specified URLs but also offers
caching mechanism powered by PySpark. 
This feature allows users to access previously fetched RSS feeds without an internet connection, filtered by publication date.



## Project Structure

```
final-proj/
├── src/                    
│   ├── main/               
│   │   ├── entity/         
│   │   └── utils/          
│   └── test/               
├── pytest.ini              
├── README.md               
├── requirements.txt        
├── setup.cfg               
└── setup.py                
```

## Installation

1. **Install Apache Spark 3.1.2**: Ensure you have Apache Spark 3.1.2 installed.

2. **Install Python 3.9**: Ensure you have Python 3.9 installed.

3. **Install setuptools**: Ensure you have setuptools installed.
    ```bash
   pip install setuptools
   ```

1. Clone the repository:
   ```bash
   git clone https://github.com/TsariwOleg/Python-for-Data-developers-Part2.git
   ```

3. Install the library:
   ```bash
   pip install .
   ```
   


## Running the Program

To run the program, use the following command:

```bash
spark-submit src\main\main.py https://www.rssboard.org/files/rss-2.0-sample.xml --json --limit 2
```

### Parameters:

- `--source`: URL of the RSS feed (optional if using --date with cached data).
- `--json`: Outputs the result in JSON format.
- `--limit LIMIT`: Limits the number of news items displayed.
- `--date YYYYMMDD`: Fetches news from the local cache for a specific publication date.



## Code Style
To check the code style using pycodestyle, follow these steps:

```bash
pycodestyle .
```

## Running Tests

To run tests, use the following command:

```bash
pytest
```

### Generating Coverage Report

To generate a coverage report, use:

```bash
pytest --cov=src/main --cov-report=html:coverage_report
```
