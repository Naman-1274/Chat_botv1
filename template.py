import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
project_name = "hey_bot"

List_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/vscode/__init__.py",
    f"src/{project_name}/vscode/settings.json",
    f"src/{project_name}/app/__init__.py",
    f"src/{project_name}/app/M_app.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/models.py",
    ".env",
    "requirements.txt",
    "README.md",
    "run_app.py",
 
    
]

for fp in List_of_files:
    filepath = Path(fp)
    filedir , filename = os.path.split(filepath)
    
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")
        
    if (not os.path.exists(filepath) or (os.path.getsize(filepath) == 0)):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
            
    else:
        logging.info(f"File already exists: {filepath}")