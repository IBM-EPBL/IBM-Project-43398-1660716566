# Docker File

FROM python:3
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3","app.py" ]
