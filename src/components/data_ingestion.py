import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.utils import export_collection_as_dataframe


## intilizing the data ingestion configuration

@dataclass
class DataIngestionconfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')
    
    
    
## Create a data ingestion class


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()
        
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion method start')
        
        try:
            df : pd.DataFrame = export_collection_as_dataframe(
                db_name="CCDP_project", collection_name= "CreditCard_Fault"
            ) 
            logging.info('Dataset read as pandas Dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("Raw Data Created")
            
            logging.info("Train test split")
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
                        
            logging.info("Data ingestion completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            logging.info("Error Occured in Data ingestion config")