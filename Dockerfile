FROM python:3.10-slim as image_base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    wget \
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

COPY . .
# USER appuser

FROM image_base as image_django

ENTRYPOINT ["sh", "./entrypoint.sh" ]


FROM nginx:1.23-alpine as image_nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d