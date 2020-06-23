## Python3 install
FROM python:3.7

# cd /usr/source/app
WORKDIR /usr/source/app

## copy source code
COPY . .

## package install
RUN pip install -r requirements.txt

## access from port5000
EXPOSE 5000

## run python
CMD [ "python3", "app.py" ]
