FROM python:3.8-slim-buster

# switch working directory
WORKDIR /app

## copy every content from the local file to the image
#COPY . /app

COPY requirements.txt /app
COPY /app /app

# install the dependencies and packages in the requirements file
RUN pip3 --no-cache-dir install -r requirements.txt

# expose our port
EXPOSE 5000

CMD [ "python3", "app.py" ]
