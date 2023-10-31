import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('csv_files',"train.csv")   # csv_files - folder
    test_data_path: str = os.path.join('csv_files',"test.csv")
    raw_data_path: str = os.path.join('csv_files',"raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()     # the three path will be obtained.
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
           df = pd.read_csv('notebook\data\stud.csv')
           logging.info('Exported the dataset into dataframe')
           
           # Extracts the directory name from path and created the directory
           os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)   

           df.to_csv(self.ingestion_config.raw_data_path,index=False, header = True)

           logging.info("Train test split initiated")
           train_set,test_set = train_test_split(df, test_size=0.2, random_state=42)

           train_set.to_csv(self.ingestion_config.train_data_path,index = False, header = True)

           test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

           logging.info("Ingestion of the data is completed")

           return (
               self.ingestion_config.train_data_path,
               self.ingestion_config.test_data_path
               
           )

        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    path_obj = DataIngestion()
    train_path, test_path = path_obj.initiate_data_ingestion()
    
    data_obj = DataTransformation()
    train_data, test_data = data_obj.initiate_data_transformation(train_path,test_path)


    