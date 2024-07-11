import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s')

source = "src"


list_of_files = [
    "data/.gitkeep",
    f"{source}/__init__.py",
    f"{source}/components/__init__.py",
    f"{source}/components/data_ingestion.py",
    f"{source}/components/data_validation.py",
    f"{source}/components/model_trainer.py",
    f"{source}/components/model_pusher.py",
    f"{source}/configuration/__init__.py",
    f"{source}/configuration/s3_operations.py",
    f"{source}/constant/__init__.py",
    f"{source}/constant/training_pipeline/__init__.py",
    f"{source}/constant/application.py",
    f"{source}/entity/__init__.py",
    f"{source}/entity/artifacts_entity.py",
    f"{source}/entity/config_entity.py",
    f"{source}/exception.py",
    f"{source}/logger.py",
    f"{source}/pipeline/__init__.py",
    f"{source}/pipeline/training_pipeline.py",
    f"{source}/utils.py",
    "templates/index.html",
    ".dockerignore",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    
    if(not os.path.exists(filename)) or (os.path.getsize(filename) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating empty file: {filename}")

    
    else:
        logging.info(f"{filename} is already created")