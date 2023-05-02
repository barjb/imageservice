# App
## Structure
- API
  - fast
  - one and only responsibility is handling requests & calling other services
- Upload Service
  - Upload images onto a storage,
- Dithering Service
  - does the work
- Notification Service (future)
  - Send email containing link to processed image

## Upload Service
- GET /id -
- POST /upload

### Messages sent to dithering service
- uuid
- url
- filename

## Dithering service
- GET /health


### Message sent to upload service
- uuid
- url_dither


## Kafka
```text
docker exec queue-kafka-1 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic users
```