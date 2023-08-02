#! /bin/sh
echo "========================================================================================================"
echo "Welcome to the setup. First it will set up the local virtual environment."
echo "Then it will install all the required libraries from the requirements.txt file."
echo "--------------------------------------------------------------------------------------------------------"

if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip."
else
    echo "creating .env folder and installing using pip."
    python -m venv .env
fi

Activate virtual environment
. .env/bin/activate

# Upgrade pip
pip install --upgrade pip
pip install -r requirements.txt
# Deactivate the virtual environment
deactivate