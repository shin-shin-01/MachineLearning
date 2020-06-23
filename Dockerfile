## Python3 install
FROM python:3

# cd /usr/source/app
WORKDIR /usr/source/app

## copy local/requirements.txt
COPY requirements.txt .
## package install
RUN pip install --no-cache-dir -r requirements.txt

## copy source code
COPY . .

## access from port5000
EXPOSE 5000

## run python
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
