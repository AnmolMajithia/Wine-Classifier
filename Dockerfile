FROM python:3.8

LABEL maintainer="jatinsaini580@gmail.com"

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN python -c "import nltk;nltk.download('punkt');nltk.download('stopwords');nltk.download('wordnet')"

EXPOSE 8050

CMD ["python", "app.py"]
