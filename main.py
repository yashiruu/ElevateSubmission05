import utils.extract as extract
import utils.transform as transform
from utils import load
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

if __name__ == "__main__":
    # ===============================
    # Extract Data
    # ===============================
    data = extract.scrape_all_products()
    
    # ===============================
    # Transform Data
    # ===============================
    data_df = transform.transform_products(data)
    
    # ===============================
    # Load Data
    # ===============================
    load.save_to_csv(data_df)
    
    load.save_to_google_sheets(
        df=data_df,
        spreadsheet_id=os.getenv("GOOGLE_SPREADSHEET_ID")
    )
     
    load.save_to_postgresql(
        df=data_df,
        connection_uri=os.getenv("DB_URI"),
        table_name="tb_fashion"
    )