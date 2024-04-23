FROM python:3.10-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*


# ARG UID=10001
# # RUN adduser \
# #     --disabled-password \
# #     --gecos "" \
# #     --home "/nonexistent" \
# #     --shell "/sbin/nologin" \
# #     --no-create-home \
# #     --uid "${UID}" \
# #     appuser

ENV POETRY_VERSION=1.5.1
RUN pip3 install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock /app/
RUN poetry export -f requirements.txt --output requirements.txt

RUN pip3 install -r requirements.txt

# USER appuser

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh" ]
