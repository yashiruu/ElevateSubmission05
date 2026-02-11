import utils.extract as extract
import utils.transform as transform
from utils import load
import json

if __name__ == "__main__":
    data = extract.scrape_all_products()
    data_df = transform.transform_products(data)
    print(data_df)
    
    # save dataframe
    load.save_to_csv(data_df)
    
    load.save_to_google_sheets(
        df=data_df,
        spreadsheet_id="1tWZkZovHqIjOPCy7MkupIkFS7DC3f_IdBxCQ-QRHOWQ"
    )
     
    load.save_to_postgresql(
        df=data_df,
        connection_uri="postgresql+psycopg2://postgres:bukangajah@127.0.0.1:5432/db_etl",
        table_name="tb_fashion"
    )