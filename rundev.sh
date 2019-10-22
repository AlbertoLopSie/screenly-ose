#!/bin/bash
docker run --rm -it \
       --name=screenly-dev \
       -e 'LISTEN=0.0.0.0' \
       -e 'SWAGGER_HOST=127.0.0.1:8080' \
       -p 8080:8080 \
       -v $(pwd):/home/pi/screenly \
       albertols/screenly-ose-dev-server