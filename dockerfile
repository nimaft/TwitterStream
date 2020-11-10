FROM python:3.10.0a2-alpine3.12
COPY requirements.txt ./
RUN echo Installing dependencies...
RUN pip install -r ./requirements.txt
COPY . .
RUN rm -rf /var/cache/apk/*
ENV BEARER='AAAAAAAAAAAAAAAAAAAAAAONJQEAAAAA1wHsP7ozvwm0FPeVGgzqODg0Dhs%3DppJgXkaWKv3w2knqe7FSF2GquoVHzW4mTtPYYZotzeibD5OdSk'
RUN echo Starting python and starting the Flask service...
ENTRYPOINT ["waitress-serve","--call","TwiApp:create_app"]
