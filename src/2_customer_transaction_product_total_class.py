import pandas as pd

class CustomerTransactions:
    """
    This class used to process CSV files containing customer transaction data.

    ...

    Attributes
    ----------
    input_file : str
        Path to the input CSV file. It is assumed that CSV has following in header: 
            1. transaction_id (int): Unique identifier for each transaction.
            2. customer_id (int): Unique identifier for each customer.
            3. timestamp (str): Timestamp of when the transaction was made in the format 'YYYY-MM-DD HH:MM:SS'.
            4. product_name (str): Name of the product purchased.
            5. product_category (str): Category of the product purchased.
            6. product_price (float): Price of the product purchased.
            7. quantity (int): Quantity of the product purchased.
    
    output_file : str
        Path to the output CSV file. It will contain following in header:
            1. date (str): Date of the transaction in the format 'YYYY-MM-DD'.
            2. customer_id (int): Unique identifier for each customer.
            3. total_spent (float): Total amount spent by the customer on that date.

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

    def process(self):
        # Read CSV in chunks for arbitrarly large file
        reader = pd.read_csv(self.input_file, chunksize=self.chunksize)

        output_list = [] # To store chunks of processed data

        for chunk in reader:
            chunk['timestamp'] = pd.to_datetime(chunk['timestamp'])
            chunk['date'] = chunk['timestamp'].dt.date
            chunk['total_spent'] = chunk['product_price'] * chunk['quantity']
            grouped = chunk.groupby(['date', 'customer_id'])['total_spent'].sum().reset_index()

            output_list.append(grouped)

        # Concatenate all chunks and group again in case data for a single day/customer is split across chunks
        output_df = pd.concat(output_list)
        final_output = output_df.groupby(['date', 'customer_id'])['total_spent'].sum().reset_index()

        # Save to CSV
        final_output.to_csv(self.output_file, index=False)


if __name__ == "__main__":
    transactions = CustomerTransactions('data/customer_input.csv', 'data/customer_output.csv')
    transactions.process()
