FROM python:3.7-alpine
MAINTAINER Seonghyeon Kim "seonghyeon@entrydsm.hs.kr"
ENV GITHUB_TOKEN $GITHUB_TOKEN
ENV RUN_ENV prod
ENV SERVICE_NAME hermes
COPY . .
WORKDIR .
RUN apk add --no-cache \
        gcc \
        make \
        musl-dev \
        libressl-dev \
        libffi-dev \
    && pip install -r requirements.txt \
    && apk del \
        gcc \
        make \
        musl-dev \
        libressl-dev \
        libffi-dev
EXPOSE 8888
ENTRYPOINT ["python"]
CMD ["-m", "hermes"]