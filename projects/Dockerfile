############################
# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/projects

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add additional alpine download url in dockerfile
RUN echo -e "http://dl-4.alpinelinux.org/alpine/v3.12/main\nhttp://dl-4.alpinelinux.org/alpine/v3.12/community" > /etc/apk/repositories

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN cd /usr/src/projects/
RUN pip install pipenv
COPY ./Pipfile /usr/src/projects/
COPY ./Pipfile.lock /usr/src/projects/
RUN pipenv install --system --deploy --ignore-pipfile


# copy project
COPY . /usr/src/projects/

RUN ls

# migrate
ENTRYPOINT ["sh", "/usr/src/projects/entrypoint.sh"]