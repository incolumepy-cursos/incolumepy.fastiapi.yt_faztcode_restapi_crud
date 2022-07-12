FROM python:3.10.5-alpine3.15 as stage1

WORKDIR /app

COPY ./* /app/
RUN pip install poetry && poetry export --without-hashes -o requirements.txt


FROM python:3.10.5-alpine3.15

WORKDIR /app

COPY --from=stage1 /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -Ur requirements.txt

COPY . /app/

CMD ["uvicorn", 'main:app', '--host', '0.0.0.0', '--port', '80']
