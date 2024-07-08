import os
import sys
import shutil
from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataValidationConfig
from src.entity.artifacts_entity import (DataIngestionArtifact,
                                         DataValidationArtifact)


class DataValidation:
    def __init__(
            self,
            data_ingestion_artifact: DataIngestionArtifact,
            data_validation_config: DataValidationConfig
    ):
        try:
            #Getting the Directory path from constant via config_entity.py & artifact_entity.py
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            logging.info("Exception occured in fn:__init__ of class DataValidation file:data_validation.py")
            raise CustomException(e,sys)
        

    
    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None
            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)
            logging.info(f"Checking the existing file and validating the required file in {self.data_ingestion_artifact.feature_store_path}")
            for file in all_files:
                if file not in self.data_validation_config.required_file_list:
                    validation_status = False
                    os.makedirs(self.data_validation_config.data_validation_dir,exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

                else:
                    validation_status = True
                    os.makedirs(self.data_validation_config.data_validation_dir,exist_ok=True)
                    with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            logging.info("Exception occured in fn:validate_all_files_exist of class DataValidation file:data_validation.py")
            raise CustomException(e,sys)
        


    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entered fn:initiate_data_validation of data validation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)
            
            logging.info("Exiting fn:initiate_data_validation of DataValidation class")
            logging.info(f"Data validation artifact:{data_validation_artifact}")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())
            
            return data_validation_artifact
        
        except Exception as e:
            logging.info("Exception occured in fn:intiate_data_validation of DataValidation class file:data_validation.py")
            raise CustomException(e,sys)