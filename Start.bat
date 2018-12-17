@echo off
cmd /k "pip install virtualenv & virtualenv youtuber & youtuber\Scripts\activate.bat & pip install --upgrade -r requirements.txt & python uiyt.py & youtuber\Scripts\deactivate.bat"