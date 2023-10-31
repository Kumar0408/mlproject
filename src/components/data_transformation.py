import sys
from dataclasses import dataclass
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
 preprocessor_obj_file_path = os.path.join('csv_files',"preprocessor.pkl")

class DataTransformation:
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig()
    self.numerical_columns = ["writing_score", "reading_score","math_score"]
    self.categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

  def get_data_transformer_object(self):
    
    """
    Function for preprocessing pipeline and creating the preproccor object.
    """
    try:
      
      num_pipeline = Pipeline(
        steps = [
          ("imputer",SimpleImputer(strategy="median")),
          ("scalar",StandardScaler())
        ]
      )
      
      cat_pipeline = Pipeline(
        steps = [
          ("imputer",SimpleImputer(strategy="most_frequent")),
          ("one_hot_encoder",OneHotEncoder())
        ]
      )

      logging.info("Numerical columns standard scaling completed")

      logging.info("Categorical columns encoding completed")

      preprocessor = ColumnTransformer(
        [
          ("num_pipeline",num_pipeline,self.numerical_columns),
          ("cat_pipeline",cat_pipeline,self.categorical_columns)
        ]
      )

      return preprocessor
    except Exception as e:
      raise CustomException(self,sys)

  def initiate_data_transformation(self, train_path, test_path ):

    try:
      train_df = pd.read_csv(train_path)
      test_df = pd.read_csv(test_path)

      # Adding additional column of average
      
      train_df['average'] = (train_df['math_score'] + train_df['writing_score'] + train_df['reading_score'])/3
      test_df['average'] = (test_df['math_score'] + test_df['writing_score'] + test_df['reading_score'])/3

      logging.info("Adding target data Read Train and test data completed")

      logging.info("Obtaining preprocessing object")
      
      preprocessor_obj = self.get_data_transformer_object()

      # Segregation into feature and targets
      
      target_column_name = "average"
      input_features_train_df = train_df.drop(columns=[target_column_name],axis=1)
      target_features_train_df = train_df[target_column_name]
    
      input_features_test_df = test_df.drop(columns=[target_column_name],axis=1)
      target_features_test_df = test_df[target_column_name]

      logging.info("Apllting preprocessor object on training and testing df")

      input_features_train_arr = preprocessor_obj.fit_transform(input_features_train_df)
      input_features_test_arr = preprocessor_obj.transform(input_features_test_df)  

      train_arr = np.c_[
                input_features_train_arr, np.array(target_features_train_df)
            ]
      test_arr = np.c_[input_features_test_arr, np.array(target_features_test_df)]

      logging.info(f"Saved preprocessing object.")

      save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj

            )
    except Exception as e:
      raise CustomException(e,sys)
      