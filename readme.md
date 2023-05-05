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


## Env variables
| Name                  | Description   |
| --------------------- | ------------- |
| KAFKA_SERVER          | HOSTNAME+PORT |
| KAFKA_IMAGE_TOPIC     |               |
| KAFKA_DITHER_TOPIC    |               |
| CLOUDINARY_CLOUD_NAME |               |
| CLOUDINARY_API_KEY    |               |
| CLOUDINARY_API_SECRET |               |
| POSTGRES_DB           | DB NAME       |
| POSTGRES_PASSWORD     |               |
| POSTGRES_USER         |               |
| POSTGRES_PORT         |               |
| POSTGRES_HOST         | HOSTNAME      |





## Upload Service
- GET /images -
- POST /images
- GET /images/<string:uuid>
- DELETE /images/<string:uuid>
- GET /health

### Messages sent to dithering service
- uuid
- url
- filename

## Dithering service
- GET /images
- GET /images/<string:uuid>
- POST /images/<string:uuid>/<int:channels>
- GET /health


### Message sent to upload service
- uuid
- url_dither




## Kafka
```text
docker exec queue-kafka-1 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic users
```