FROM python:3.10-alpine3.17 as builder

RUN python3 -m venv /fastapi_app
RUN /fastapi_app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN /fastapi_app/bin/pip install -Ur /mnt/requirements.txt --no-cache-dir --prefer-binary


FROM python:3.10-alpine3.17 as fastapi_app

WORKDIR /fastapi_app

COPY --from=builder /fastapi_app /fastapi_app
COPY . .

EXPOSE 8000