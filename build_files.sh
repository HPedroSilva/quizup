echo "QUIZUP - BUILD STARTED"
python3.12 -m ensurepip
python3.12 -m pip install pipenv
python3.12 -m pipenv install
python3.12 -m pipenv run collectstatic
python3.12 -m pipenv run migrate
echo "QUIZUP - BUILD ENDED"