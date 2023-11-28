FROM python:3.11

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    brotli \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wait-for-it


# System deps:
RUN pip install 'poetry'

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Creating folders, and files for a project:
COPY . /code

RUN cp ./onStartup.sh /tmp
RUN chmod +x /tmp/onStartup.sh

CMD ["/tmp/onStartup.sh"]
