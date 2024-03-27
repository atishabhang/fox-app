FROM python:alpine

RUN apk add make
WORKDIR /app
COPY . .

RUN make build
ENTRYPOINT ["python"]
