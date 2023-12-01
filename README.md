# Financial Statement Analyzer

The Financial Statement Analyzer is a Python script designed for analyzing and visualizing financial transactions from a CSV file. This script allows users to gain insights into their spending patterns by categorizing transactions, generating charts, and providing specific details based on user input.

## Key Features:

- **Transaction Sorting**: View all financial transactions sorted by category, providing a clear overview of spending habits.
- **Date Range Analysis**: Analyze transactions within a specified date range for a chosen category and visualize the data using a line chart.
- **Monthly Overview**: Explore transactions for a specific month and generate a pie chart to visualize the distribution of spending across different categories.
- **Overall Spending Analysis**: Obtain insights into spending patterns across various categories over all recorded months through a pie chart.
- **Monthly Bills and Payments**: Visualize monthly bills and payments trends using a bar chart, offering a comprehensive view of financial trends.
- **Balance Evolution Over Time**: Track the evolution of the balance over time with a line graph, helping users understand their financial history.

## Dependencies:

- **plotly:** Used for generating interactive plots.
- **pandas:** Provides data structures for efficient data manipulation.
- **Other:** standard Python libraries.

## How to Use:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ahayat10/VisualizingFinancialData.git
2.  **Navigate to the Project Directory**:
   ```cd VisualizingFinancialData```
3. **Update the Path on Line 278 in refactored.py to your path to the file**:
   ```transactions = readTransactions("/your/path/M.csv")```
4.  **Run The Script**:
   ```python script.py```


