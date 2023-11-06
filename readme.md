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

## Microservices

Each service consists of REST API, consumer and business logic.

### Upload Service
Bold denotes parameter and it's applicable type.
- GET /images
- POST /images
- GET /images/**string:uuid**
- DELETE /images/**string:uuid**
- GET /health

### Dithering service
- GET /images
- GET /images/**string:uuid**
- POST /images/**string:uuid**/**int:channels**
- GET /health

## Messages
As it's message-driven system each message consists of:
- header
- body
- destination

Each header carries information about completed action.
```python
header = [
    ("message_type", b"IMAGE_UPLOADED"),
    ("version", b"1.0.0"),
]
```

### Headers
- produced by uplaod service: IMAGE_UPLOADED, IMAGE_DELETED
- produced by dither service: DITHER_UPLOADED

TODO: update as soon as APIs get fully implemented.

### Body
Each service sends different information 
1. Image Service => dithering service
- uuid
- url 
- filename

Each one in respect to original image

2. Dithreing service => upload service
- uuid (of original image)
- url_dither

## Communication between microservices
There are two basic approaches of communications between distributed systems: event-driven and message-driven.

In a shorthand Event-driven commucation can be described as:
1. Service A does some action.
2. Service A publishes an event E.
3. Services subscribed to an event E receive message.

Message-driven communication can be described as:
1. Service A does some action.
2. Service A sends message M to a queue Q.
3. Services subscribed to a queue Q receive message.

In essence events have broadcast nature, whereas messages are more directed.

## Kafka
Firstly topic must be created. Then any existing consumer is able to subscribe to it. Typical command:  
```text
docker exec queue-kafka-1 kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic users
```

## Tests

There are two approaches I considered:
1. using separate docker-compose-test_level.yml files
2. using [python-testcontainers](https://testcontainers-python.readthedocs.io/en/latest/README.html) package

Pros and cons of each solution
1. docker-compose-test_level.yml
   - pros:
     - easy to setup
     - test are being run in separate environment
   - cons:
     - manual cleanup of unused containers
2. testcontainers
   - pros:
     - automatic cleanup
     - test are being run in separate environment
   - cons:
     - creating containers within containers is slower
     - harder to setup
### Test structure
```text
tests/
├── conftest.py
├── test_api.py
.
.
.
└── requirements.txt
```

## Other
1. I'm using free tier PostgreSQL cloud solutions. Project started it's existence on [ElephantSQL](https://www.elephantsql.com/), but limit of 5 concurrent connections quickly made the project buggy. Now I'm using [Neon.tech](https://neon.tech/) as it allows up to 100 simultaneous connections by default 💀 With usage of connection pooler this number can go up to 10000. 
2. Eco tier ($5/mo) on heroku allows up to 20 connections as far as I know. I'm in safe teritory for now.
3. [Cloudinary](https://cloudinary.com/) works flawlessly for now. API is limited to 500 req/h (listing & deleting resources).
4. [CloudKaraka](https://elements.heroku.com/addons/cloudkarafka) is the service I'm going to use in deployment. I'm not paying $100/mo for [that](https://elements.heroku.com/addons/heroku-kafka)
5. API Gateway in my case could be used to get more coherent API thanks to one entry point to many APIs. Without it client app has to connect to different host for each service. It's possible to deploy [WSO2](https://elements.heroku.com/buttons/wso2/cloud-heroku-api-gateway) as a Heroku dyno. I'm not sure whether I'll use it yet.
More complex solutions provide also another services by default. NGINX Plus on Enterprise level provides:
- load balancing
- API Gateway
- Content Cache
- Web Application Firewall
- protection against Denial of Service
  
You can download useful books at a small price of your personal data from [nginx.com](https://www.nginx.com/resources/library/). 
