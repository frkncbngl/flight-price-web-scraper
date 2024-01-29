# Flight Data Scraper

This Python script utilizes [Playwright](https://playwright.dev/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to scrape flight data from the [ITA Matrix](https://matrix.itasoftware.com) website. The scraped data is then stored in an Excel file.

## Prerequisites

- [Playwright](https://playwright.dev/) - A browser automation library.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - A library for pulling data out of HTML and XML files.
- [pandas](https://pandas.pydata.org/) - A data manipulation and analysis library for Python.


   ```bash
   pip install playwright beautifulsoup4 pandas openpyxl
   ```
#Ver 1.1
-Added some extra code to catch the TimeoutErrors. And hopefully to keep the program running.


## Usage
1. Run the script in your terminal or IDE.
2. Follow the prompts to input the origin, destination, start date, and end date in the specified format.

## Code Overview
- The script uses Playwright to automate interactions with the ITA Matrix website and collect flight data.
- User inputs for origin, destination, start date, and end date are validated.
- The script iterates over a date range, fills out the ITA Matrix search form, and collects data for each date.
- The collected data is organized into pandas dataframes and saved to an Excel file with separate sheets for each date.

## Script Details
- `origin_input()`: Takes user input for the origin airport in 3-char IATA format.
- `destination_input()`: Takes user input for the destination airport in 3-char IATA format.
- `start_date_input()`: Takes user input for the start date in MM/DD/YY format.
- `end_date_input()`: Takes user input for the end date in MM/DD/YY format.
- `wait_for_table_load(page)`: Waits for the main table to load on the webpage.
- `wait_for_carrier_table_load(page,carrier)`: Waits for carrier-specific table to load after clicking on a carrier.
- `read_screen(page,starting_date,ending_date,dataframes)`: Reads the table contents for carriers and returns dataframe objects.
- `flight_data_scraper(origin,destination,start_date,end_date)`: Main function to initiate the web scraping process.

**Note:** The scraped data is saved to an Excel file named `output.xlsx`. Make sure to check the generated Excel file for the collected flight information.

Feel free to customize the script according to your needs or contribute to its improvement!
