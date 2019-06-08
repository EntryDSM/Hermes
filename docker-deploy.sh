#!/bin/bash

version=`python -c "import hermes; print(hermes.__version__)"`
branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "${branch}" == "dev" ]];then
    docker build -t registry.entrydsm.hs.kr/hermes:dev .

    docker push registry.entrydsm.hs.kr/hermes:dev
elif [[ "${branch}" == "master" ]];then
    image_id=`docker build -t registry.entrydsm.hs.kr/hermes:${version} .`

    docker tag ${image_id} registry.entrydsm.hs.kr/hermes:latest

    docker push registry.entrydsm.hs.kr/hermes:${version}
    docker push registry.entrydsm.hs.kr/hermes:latest
fi

exit