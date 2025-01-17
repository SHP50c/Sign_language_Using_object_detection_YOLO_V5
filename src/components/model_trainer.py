import os
import sys
import yaml
from src.utils import read_yaml_file
from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifacts_entity import ModelTrainerArtifact
from src.constant.training_pipeline import DATA_DOWNLOAD_URL



class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config
        

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered fn:initiate_model_trainer of ModelTrainer class")
        try:
            logging.info("Unziping data")
            file_name=DATA_DOWNLOAD_URL.split('/')[-2]+'.zip'
            print(file_name)
            os.system(f"unzip {file_name}")
            os.system(f"rm {file_name}")

            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")

            config['nc'] = int(num_classes)

            with open(f'yolov5/models/custom_{model_config_file_name}.yaml','w') as f:
                yaml.dump(config,f)

            os.system(f"cd yolov5/ && python train.py --img 640 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_ephochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results --cache")
            os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir,exist_ok=True)
            os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            os.system("rm -rf yolov5/runs")
            os.system("rm -rf train")
            os.system("rm -rf test")
            os.system("rm -rf valid")
            os.system("rm -rf data.yaml")
            os.system("rm -rf README.dataset.txt")
            os.system("rm -rf README.roboflow.txt")

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path="yolov5/best.pt")

            logging.info("Exiting fn:initiate_model_trainer of model trainer class")
            logging.info(f"Model trainer artifacts: {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            logging.info("Exception occured in fn:initiate_model_trainer of ModelTrainer class")
            raise CustomException(e,sys)
