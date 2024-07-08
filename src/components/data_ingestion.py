import os
import sys
import shutil
import gdown
from six.moves import urllib
import zipfile
import aspose.zip as az
from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifacts_entity import DataIngestionArtifact



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            logging.info("Initialising DataIngestionConfig class from config_entity.py")
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            logging.info("Exception occured in fn:__init__ of DataIngetion (data_ingestion.py)")
            raise CustomException(e,sys)
        

    def download_data(self)-> str:
        '''
        Fetch the data from the url
        '''
        try:
            logging.info("Entered fn: download_data of class DataIngestion")
            dataset_url=self.data_ingestion_config.data_download_url
            file_id=dataset_url.split("/")[-2]
            data_file_name=f'{file_id}.zip'
            prefix='https://drive.google.com/uc?/export=download&id='
            zip_download_dir=self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir,exist_ok=True)
            zip_file_path=os.path.join(zip_download_dir,data_file_name)
            
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
            gdown.download(prefix+file_id,zip_file_path,quiet=False)
            logging.info(f"Downloaded data from {dataset_url} into filr {zip_file_path}")
            
            return  zip_file_path
        
        except Exception as e:
            raise CustomException(e,sys)


    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        Extracts the zip file into the data directory.
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")
            os.makedirs(feature_store_path, exist_ok=True)
            with az.Archive(zip_file_path) as archive:
                archive.extract_to_directory(feature_store_path)
            #with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            #    zip_ref.extractall(path=feature_store_path)

            return feature_store_path
        except Exception as e:
            raise CustomException(e, sys)


        

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)