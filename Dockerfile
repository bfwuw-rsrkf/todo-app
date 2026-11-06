FROM python:3.12-alpine AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

WORKDIR /code

COPY --from=builder /install /usr/local
COPY app/ app/

EXPOSE 5000
CMD ["python", "-m", "app.main"]