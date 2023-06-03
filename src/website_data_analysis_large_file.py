import pandas as pd

def process_large_csv(input_file, output_file, chunksize=10000):
    """
    Function to process a website URL related CSV file and generate output CSV file.
    
    Args:
    input_file: Path to the input CSV file. It is assumed that CSV has following in header: 
    1. User ID
    2. Timestamp
    3. URL visited
    4. Page view duration (in seconds)
    output_file: Path to the output CSV file. It will contain following in header:
    1. Total Interactions
    2. Total Unique Users
    3. Most Visited URL
    4. Average Time Spent on Each URL
    chunksize: number of data points processed at a time(nos of rows per chunk)
    Assumptions -> CSV file is well-formed and contains no errors.
    """
    
    # Initialize variables
    total_interactions = 0
    total_unique_users = set()
    url_counts = {}
    total_duration = {}
    url_visits = {}

    # Process each chunk of the CSV file
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Update the total number of interactions
        total_interactions += len(chunk)
        
        # Update the set of unique users
        total_unique_users.update(chunk['user_id'])
        
        # Update the count of visits to each URL
        for url in chunk['url']:
            url_counts[url] = url_counts.get(url, 0) + 1
        
        # Update the total duration and count of visits for each URL
        for url, duration in zip(chunk['url'], chunk['page_view_duration']):
            total_duration[url] = total_duration.get(url, 0) + duration
            url_visits[url] = url_visits.get(url, 0) + 1

    # Calculate the most visited URL
    most_visited_url = max(url_counts, key=url_counts.get)

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
    output_df.to_csv(output_file, index=False)

process_large_csv('data/user_visited.csv', 'data/output_large.csv', 10)
