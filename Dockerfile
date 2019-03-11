FROM python:3.6

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /InvestingCalculator

COPY config.py /InvestingCalculator
COPY manage.py /InvestingCalculator
ADD calculator /InvestingCalculator/calculator
ADD InvestingCalculator /InvestingCalculator/InvestingCalculator

#COPY pycharm-debug-py3k.egg /
#COPY pycharm-debug-py3k.egg /flask_test

WORKDIR /InvestingCalculator
CMD ["python3", "./manage.py", "makemigrations"]
CMD ["python3", "./manage.py", "migrate"]
CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]