FROM python:3.8

# install pipenv and create pip requirements file
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

# copy files, and install telegramtogo
COPY . /app
WORKDIR /app
RUN pip install .

# run app
CMD telegramtogo