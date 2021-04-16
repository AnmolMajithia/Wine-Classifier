FROM python:3.8

LABEL maintainer="jatinsaini580@gmail.com"

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python -m nltk.downloader punkt stopwords wordnet


EXPOSE 8050

CMD ["python", "app.py"]
