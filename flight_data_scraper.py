from playwright.sync_api import sync_playwright,TimeoutError
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timedelta
url = "https://matrix.itasoftware.com"
out_path = "output.xlsx"

def origin_input():
    """
    This function takes input from user. Only accepts three digits in chars. Does not check if the input is valid.
    """
    while True:
        
        origin = input("Origin (3 Char IATA Format): ")
    
        if len(origin) == 3 and origin.isalpha():
            break
        else:
            print("Origin input is invalid. Please provide in the suggested form.")
    return origin.upper()

def destination_input():
    """
    This function takes input from user. Only accepts three digits in chars. Does not check if the input is valid.
    """
    while True:
        destination = input("Destination (3 Char IATA Format): ")
    
        if len(destination) == 3 and destination.isalpha():
            break
        else:
            print("Destination input is invalid. Please provide in the suggested form.")
    return destination.upper()

def start_date_input():
    """
    This function takes in date values, checks if the date is valid but does not check if the date is valid.
    It is possible to check if the date is in the past to confirm, and since it is only possible to book for a date in the upcoming 365 days
    this validity check can also be implemented.
    """
    while True:
        date_input = input("Start Date ( Format : MM/DD/YY) ")

        try:
            
            formatted_date = datetime.strptime(date_input, "%m/%d/%y")
            print("Succesful, date you provided is: ", formatted_date.strftime("%m/%d/%y"))
            break
        except ValueError:
            print("Error! Please provide dates in suggested format (MM/DD/YY).")
    return date_input

def end_date_input():
    """
    This function takes in date values, checks if the date is valid but does not check if the date is valid.
    It is possible to check if the date is in the past to confirm, and since it is only possible to book for a date in the upcoming 365 days
    this validity check can also be implemented.
    """
    while True:
        date_input = input("End Date ( Format : MM/DD/YY) ")

        try:
            
            formatted_date = datetime.strptime(date_input, "%m/%d/%y")
            print("Succesful, date you provided is: ", formatted_date.strftime("%m/%d/%y"))
            break
        except ValueError:
            print("Error! Please provide dates in suggested format (MM/DD/YY).")
    return date_input


def wait_for_table_load(page):
    """
    This function will wait for the table objects to be loaded, and catch TimeoutError if it happens.
    
    """
    while True:
        try:
            print("Waiting for tables to load...")
            page.wait_for_selector('div[id="cdk-accordion-child-0"]',timeout=10000)
            print("Tables loaded... Parsing the screen...")
            break
        except TimeoutError:
            print("TimeoutError... Retrying...")
def wait_for_carrier_table_load(page,carrier):
    """
    This function will wait for the table objects to be loaded for each carrier after click action, and catch TimeoutError if it happens.
    
    """
    while True:
        try:
            page.wait_for_selector('thead[class="ng-star-inserted"]',timeout=10000)
            print(f"got the table for {carrier}... ")
            break
        except TimeoutError:
            print(f"a problem occured while loading the tables for {carrier}... Retrying...")

def read_screen(page,starting_date,ending_date,dataframes):
    """
    This function will read the table contents for carriers and return the dataframe objects in a list of dataframes. It will also generate a sheet name representing the first flight date for each query.
    
    """
    new_html = page.content() 
    df = pd.read_html(new_html,attrs = {"role":"table"})
    df=df[0]
    df = df[df["Airline filter_alt"].notnull()]
    df["start_date"] = starting_date
    df["end_date"] = ending_date
    dataframes = pd.concat([dataframes,df],ignore_index= True)
    sheet_name = starting_date.replace("/",".")
    return sheet_name,dataframes
    
def flight_data_scraper(origin,destination,start_date,end_date):
    ## First we initiate our page object from playwright.
    with sync_playwright() as p:
        ## Then we convert our dates to datetime object to create a list of dates in order to iterate through the list,this is for the sake of generating more data.
        start_date_formatted = datetime.strptime(start_date,"%m/%d/%y")
        end_date_formatted = datetime.strptime(end_date,"%m/%d/%y")
        time_delta = end_date_formatted - start_date_formatted
        date_list = pd.date_range(start_date_formatted,start_date_formatted + timedelta(days=3),freq="D") 
   
        for starting_date in date_list:
            #We have to reformat the dates to pass them into form in the webpage.
            #We also calculate the timedelta (time difference between start and end date) to fill the form for future iterations.
            print("Starting Scraper...")
            ending_date_in_dt = starting_date + timedelta(days=time_delta.days)
            ending_date = datetime.strftime(ending_date_in_dt,"%m/%d/%Y")
            starting_date = datetime.strftime(starting_date,"%m/%d/%Y")
            
            while True:
                try:
                    #In this while loop and try/except block, we try to fill the form and click search button.
                    #But sometimes page takes too long to load after searching. So when a TimeoutError occurs we catch it in the except block and close the browser to restart the process.
                    print("Starting Browser...")
                    browser = p.firefox.launch(headless= True,timeout=25000)
                    page =  browser.new_page()
                    page.goto(url)
                    print("Page is now loaded...")
                    page.type("input[id=mat-mdc-chip-list-input-1]",destination.upper())
                    page.type("input[id=mat-mdc-chip-list-input-0]",origin.upper())
                    page.get_by_placeholder("Start Date").fill(starting_date)
                    page.get_by_placeholder("End Date").fill(ending_date)
                    print("Filled parameters...")
                    page.keyboard.down(key="Enter")
                    page.keyboard.up(key="Enter")
                    print("Clicking search button...")
                    page.get_by_role("button", name="Search").click()
                    print("Search completed...")
                    break
                except TimeoutError:
                    print("Loading took longer than expected... Closing the page and retrying...")
                    browser.close()
                    print("Page is now closed... Restarting the process...")
            wait_for_table_load(page)
            #Parsing the screen to get carriers and content in the upper table.
            #When we click the carrier names/images in the upper table we get a seperate table that only includes their prices, so we collect their names in carriers list.
            page_content = page.content()
            soup = BeautifulSoup(page_content,"lxml")
            upper_table_content = soup.find("mat-table",attrs={"role":"table"})
            rows = upper_table_content.find_all("mat-row")    
            headers = upper_table_content.find("mat-header-row")
            list = []
            carriers = []
            #We also create a pandas.dataframe object in order to collect and append all the carriers prices/durations etc.
            dataframes = pd.DataFrame()
            for header_cell in headers.find_all("mat-header-cell"):
                carriers.append(header_cell.text)
            for row in rows:
                cells = row.find_all("mat-cell")
                for cell in cells:
                    list.append(cell.text)
            
            for carrier in carriers[1:]:
            #after we get all the data from upper table, we start to iterate through the carriers list and click them.

                print("Iterating over carriers... Next carrier is: ",carrier)
                page.get_by_role("columnheader", name=f"{carrier} Carrier logo",exact= True).get_by_role("img").click()
                #Pages does not load instantly, so wait for the table object to be present/visible.
                #After screen is loaded we get the table content with pandas'es built in read_html function and concat the dataframe to the placeholder dataframe we created above.
                #Function below will also generate a sheetname for us to use in excel sheets.
                wait_for_carrier_table_load(page,carrier)
                sheet_name,dataframes = read_screen(page,starting_date,ending_date,dataframes)
            #Here, we write all the information collected from parsing the screen to a single sheet.
            with pd.ExcelWriter(out_path,mode="a",engine="openpyxl",if_sheet_exists="replace") as writer:   
                dataframes.to_excel(writer,sheet_name = f"{sheet_name}",index=False)
            print(f"Completed the search for date {sheet_name}... Continuing for the next day...")
            browser.close()
        print("All searches are now completed... Please go ahead and check your excel file...")    
        return dataframes



origin = origin_input()
destination = destination_input()
start_date = start_date_input()
end_date = end_date_input()


flight_data_scraper(origin,destination,start_date,end_date)