FROM python:3.7
MAINTAINER Seonghyeon Kim "seonghyeon@entrydsm.hs.kr"
RUN apt-get update -y
ENV GITHUB_TOKEN $GITHUB_TOKEN
ENV RUN_ENV prod
ENV SERVICE_NAME hermes
COPY . .
WORKDIR .
RUN pip install -r requirements.txt
EXPOSE 8888
ENTRYPOINT ["python"]
CMD ["-m", "hermes"]