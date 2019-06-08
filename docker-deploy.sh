#!/bin/bash

version=`python -c "import hermes; print(hermes.__version__)"`

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "dev" ]];then
    echo "Docker build on dev started"

    docker build -t registry.entrydsm.hs.kr/hermes:dev .

    docker push registry.entrydsm.hs.kr/hermes:dev
elif [[ "$1" == "master" ]];then
    echo "Docker build on master started"

    docker build -t registry.entrydsm.hs.kr/hermes:${version} .

    docker tag registry.entrydsm.hs.kr/hermes:${version} registry.entrydsm.hs.kr/hermes:latest

    docker push registry.entrydsm.hs.kr/hermes:${version}
    docker push registry.entrydsm.hs.kr/hermes:latest

fi

exit