import pandas as pd

def process_csv(input_file, output_file):
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
    
    Assumptions -> CSV file is well-formed and contains no errors.
    """
    
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(input_file)
    
    # Calculate the total number of interactions in the file
    total_interactions = df.shape[0]
    
    # Calculate the total number of unique users in the file
    total_unique_users = df['user_id'].nunique()
    
    # Calculate the most visited URL in the file
    most_visited_url = df['url'].value_counts().idxmax()
    
    # Calculate the average time spent on each URL
    average_time_spent = df.groupby('url')['page_view_duration'].mean()
    
    # Create a DataFrame for the output data
    output_df = pd.DataFrame({
        'Total Interactions': [total_interactions],
        'Total Unique Users': [total_unique_users],
        'Most Visited URL': [most_visited_url],
        'Average Time Spent on Each URL': [average_time_spent]
    })
    
    # Write the output DataFrame to a CSV file
    output_df.to_csv(output_file, index=False)


process_csv('data/user_visited.csv', 'data/output_simplified.csv')
