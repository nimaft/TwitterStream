FROM python:3.10.0a2-alpine3.12
RUN apk add --update py3-pip
COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt
COPY . .
RUN echo Starting python and starting the Flask service...
ENTRYPOINT ["waitress-serve","--call","TwiApp:create_app"]
