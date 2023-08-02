#! /bin/sh
echo "========================================================================================================"
echo "Welcome to the setup. First it will set up the local virtual environment."
echo "Then it will install all the required libraries from the requirements.txt file."
echo "--------------------------------------------------------------------------------------------------------"

if [ -d ".env" ];
then
    echo "Enabling virtual environment."
else
    echo "No Virtual env. Please run local_setup.sh first."
    exit N
fi

# Activate virtual env
. .env/bin/activate
export ENV=development
python main.py
deactivate
npm run serve