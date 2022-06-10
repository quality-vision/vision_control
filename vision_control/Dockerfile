FROM python:3.10

# There is no reason to generate .pyc files inside the container.
ENV PYTHONDONTWRITEBYTECODE=1

# Buffering causes issues for container logging.
ENV PYTHONUNBUFFERED=1

# Install Poetry.
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Add Poetry to path.
ENV PATH="${PATH}:/root/.poetry/bin"

# Copy files and install dependencies.
WORKDIR /backend
COPY pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
