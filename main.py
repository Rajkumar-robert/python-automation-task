import subprocess
import scrapper
import report_insert

def webScrapping():
    try:
        scrapper.main()
        print("Web scraping completed")
    except Exception as e:
        print("An error occurred during web scraping:", e)

def excel_to_database():
    try:
        report_insert.main()
        print("Excel to database operation completed")
    except Exception as e:
        print("An error occurred during excel to database operation:", e)

def main():
    webScrapping()
    excel_to_database()
    
if __name__ == "__main__":
    main()
