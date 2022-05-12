FROM python:3.8-slim-buster

RUN apt-get install -y bash

RUN python3.8 -m pip install --upgrade pip

RUN ln -s /usr/bin/python3.8 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /simphony/simcmclkinetics
COPY ./LICENCE.md .
COPY ./packageinfo.py .
COPY ./cmcl_logo.png .
COPY ./cmcl.ontology.yml .
COPY ./osp ./osp
COPY ./setup.py .
COPY ./examples ./examples
COPY ./tests ./tests
COPY ./README.md .
COPY ./entrypoint.sh .
COPY ./.env .

ARG KINETICS_AGENT_BASE_URL
ENV KINETICS_AGENT_BASE_URL $KINETICS_AGENT_BASE_URL

RUN python -m pip install .
RUN python -m pip install -r tests/test_requirements.txt
RUN pico install cmcl.ontology.yml

ENTRYPOINT ["./entrypoint.sh"]
CMD ["test"]