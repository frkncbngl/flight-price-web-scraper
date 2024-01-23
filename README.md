# Flight Data Scraper

This Python script utilizes [Playwright](https://playwright.dev/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to scrape flight data from the [ITA Matrix](https://matrix.itasoftware.com) website. The scraped data is then stored in an Excel file.

## Prerequisites

- [Playwright](https://playwright.dev/) - A browser automation library.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - A library for pulling data out of HTML and XML files.
- [pandas](https://pandas.pydata.org/) - A data manipulation and analysis library for Python.

## How to Use

1. Install the required Python libraries:

   ```bash
   pip install playwright beautifulsoup4 pandas openpyxl
   ```

2. Provide Input:

Follow the prompts to input the required information:

- **Origin (3 Char IATA Format)**
- **Destination (3 Char IATA Format)**
- **Start Date (Format: MM/DD/YY)**
- **End Date (Format: MM/DD/YY)**

The script will then launch a browser, navigate to the ITA Matrix website, input the provided parameters, and initiate the flight data scraping process.
![](https://www.gstatic.com/flights/airline_logos/35px/TK.png)
