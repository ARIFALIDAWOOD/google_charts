IF NOT EXIST .Env/Scripts/activate.bat (
    echo Creating .Env directory...
    python -m venv .Env
    echo Installing required packages...
    call .Env/Scripts/activate.bat && pip install -r config/req.txt
)

REM Activate the virtual environment
call .Env/Scripts/activate.bat

REM Run create_json.py
python create_json.py
