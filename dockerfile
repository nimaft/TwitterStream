FROM python:3.10.0a2-alpine3.12
COPY requirements.txt ./
RUN echo Installing dependencies...
RUN pip install -r ./requirements.txt
COPY . .
RUN rm -rf /var/cache/apk/*
RUN echo Starting python and starting the Flask service...
ENTRYPOINT ["waitress-serve","--port","80","--call","TwiApp:create_app"]
