import pandas as pd
from collections import Counter, defaultdict

import pandas as pd
from collections import Counter, defaultdict

class CSVProcessor:
    __author__ = "Yogesh Chaudhari"
    __copyright__ = "Copyright 2023, Yogesh Chaudhari"
    __credits__ = ["https://www.educative.io/path/python-for-data-analysis"]
    __license__ = "GPLv3"
    __version__ = "0.0.1"
    __maintainer__ = "Yogesh Chaudhari"
    __email__ = "mr.yogesh@gmail.com"
    __status__ = "Development"
    
    """
    This class used to process CSV files containing user interaction data.

    ...

    Attributes
    ----------
    input_file : str
        Path to the input CSV file. It is assumed that CSV has following in header: 
            1. User ID
            2. Timestamp
            3. URL visited
            4. Page view duration (in seconds)
    
    output_file : str
        Path to the output CSV file. It will contain following in header:
            1. Total Interactions
            2. Total Unique Users
            3. Most Visited URL
            4. Average Time Spent on Each URLa formatted string to determine the file path for output

    chunksize : int
        number of data points processed at a time(nos of rows per chunk)

    Methods
    -------
    process_large_csv_perf()
        Processes the CSV file in chunks and outputs interaction information. 
    """

    def __init__(self, input_file, output_file, chunksize=1000):
        self.input_file = input_file
        self.output_file = output_file
        self.chunksize = chunksize

    def process_large_csv_perf(self):
        """
        Processes the CSV file in chunks and outputs interaction information.
        (Assumptions -> CSV file is well-formed and contains no errors.)
        """
        # Initialize variables
        total_interactions = 0
        total_unique_users = set()
        url_counts = Counter()
        total_duration = defaultdict(float)
        url_visits = defaultdict(int)
        # Process each chunk of the CSV file
        for chunk in pd.read_csv(self.input_file, chunksize=self.chunksize):
            total_interactions += len(chunk)
            total_unique_users.update(chunk['user_id'])
            url_counts.update(chunk['url'])
            for url, duration in zip(chunk['url'], chunk['page_view_duration']):
                total_duration[url] += duration
                url_visits[url] += 1
        # Calculate the most visited URL
        most_visited_url = url_counts.most_common(1)[0][0]
        # Calculate the average time spent on each URL
        average_time_spent = {url: total_duration[url] / url_visits[url] for url in total_duration}
        # Create a DataFrame for the output data
        output_df = pd.DataFrame({
            'Total Interactions': [total_interactions],
            'Total Unique Users': [len(total_unique_users)],
            'Most Visited URL': [most_visited_url],
            'Average Time Spent on Each URL': [average_time_spent]
        })
        # Write the output DataFrame to a CSV file
        output_df.to_csv(self.output_file, index=False)

if __name__ == "__main__":
    processor = CSVProcessor('data/user_visited.csv', 'data/output_large_perf_class.csv')
    processor.process_large_csv_perf()
