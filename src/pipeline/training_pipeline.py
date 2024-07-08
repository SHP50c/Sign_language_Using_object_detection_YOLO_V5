import sys,os
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

from src.entity.config_entity import (DataIngestionConfig,
                                      DataValidationConfig)
from src.entity.artifacts_entity import (DataIngestionArtifact,
                                         DataValidationArtifact)



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


    def start_data_ingestion(self)-> DataIngestionArtifact:
        try: 
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)
        


    def start_data_validation(
            self,data_ingestion_artifact: DataIngestionArtifact
            )-> DataValidationArtifact:
        logging.info("Entered the fn:start_data_validation of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("performed the data validation operation")
            logging.info("Exiting the fn:start_data_validation of TrainPipeline class")
            return data_validation_artifact

        except CustomException as e:
            logging.info("Exception occured in fn:start_data_validation of Trainpipelin class file:training_pipeline.py")
            raise CustomException(e,sys)



    def run_pipeline(self)-> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise CustomException(e,sys)