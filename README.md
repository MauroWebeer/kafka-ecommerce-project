# Kafka E-Commerce Event Processing Project

This project simulates an e-commerce platform where events like user activities, transactions, page views, and clicks are produced, consumed, and saved to a PostgreSQL database for further analysis using DBT (Data Build Tool).

## Project Overview

In this project, Kafka is used as a message broker to handle the real-time stream of events. The events are consumed by a Python consumer, processed, and then saved into a PostgreSQL database. DBT is used for the data transformation and analysis phase.

### Technologies Used
- **Kafka**: Real-time stream processing for events.
- **PostgreSQL**: Store the processed events and transactional data.
- **DBT**: Data transformation and analysis.
- **Python**: Consumer script for processing the events and storing data into PostgreSQL.
- **Docker**: Containerize Kafka and Zookeeper for easy setup.

## Project Structure

```bash
.
├── scripts
│   └── create_tables.py
├── topics
│   └── user_activity_events
│      └── create_topic.py
│      └── README.md
│      └── schema.json
│   └── user_login_events
│      └── create_topic.py
│      └── README.md
│      └── schema.json
│   └── user_transaction_events
│      └── create_topic.py
│      └── README.md
│      └── schema.json
├── consumer.py
├── docker-compose.yml
├── producer.py
├── README.md
└── requirements.txt
```

- **docker-compose.yml**: The Docker Compose file to set up Kafka and Zookeeper.
- **scripts/create_tables.py**: Python script to create the PostgreSQL database and tables for storing events and transactions.
- **consumer.py**: Python script to consume events from Kafka topics and save them into PostgreSQL.
- **requirements.txt**: Python dependencies.

- **docker-compose.yml**: The Docker Compose file to set up Kafka and Zookeeper.
- **scripts/create_tables.py**: Python script to create the PostgreSQL database and tables for storing events and transactions.
- **consumer.py**: Python script to consume events from Kafka topics and save them into PostgreSQL.
- **requirements.txt**: Python dependencies.
- **topics/user_activity_events/README.md**: Documentation for the user_activity_events Kafka topic. Explains the purpose of the topic, the data format (e.g., page - views and clicks), and usage instructions.
- **topics/user_activity_events/schema.json**: JSON schema that defines the structure and data types of events in the user_activity_events Kafka topic.
- **topics/user_login_events/README.md**: Documentation for the user_login_events Kafka topic. Describes the structure and usage of login events.
- **topics/user_login_events/schema.json**: JSON schema that defines the structure and data types of events in the user_login_events Kafka topic.
- **topics/user_transaction_events/README.md**: Documentation for the user_transaction_events Kafka topic. Provides details on transaction events (e.g., purchases) and usage.
- **topics/user_transaction_events/schema.json**: JSON schema that defines the structure and data types of events in the user_transaction_events Kafka topic.

## Setup

Follow these steps to set up the project locally:

### Prerequisites

- Docker and Docker Compose installed.
- Python 3.7+ and virtual environment (venv) installed.

### 1. Set up Kafka and Zookeeper with Docker

Run the following command to start Kafka and Zookeeper using Docker Compose:

```bash
docker-compose up -d
```

This will set up Kafka and Zookeeper in the background. Kafka will be available on `localhost:9092`.

### 2. Install Python Dependencies

Create a virtual environment and install the necessary Python packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database

Run the script `create_tables.py` to set up the PostgreSQL database and tables:

```bash
python3 scripts/create_tables.py
```

This will:
- Create a database called `ecommerce` in PostgreSQL.
- Create tables for users, events, page views, clicks, and transactions.

### 4. Produce Events

Use the provided **producer** script or a separate Python script to simulate the production of e-commerce events (page views, clicks, and transactions). These events will be sent to Kafka topics:
- `user_activity_events`
- `user_login_events`
- `user_transaction_events`

Each event has a corresponding JSON format (with fields like `event_name`, `event_id`, `user_id`, `timestamp`, etc.).

### 5. Consume Events

Run the **consumer** script to consume the events from Kafka and store them into PostgreSQL:

```bash
python3 scripts/consumer.py
```

This will consume events from the Kafka topics and insert them into the corresponding PostgreSQL tables.

### 6. Run DBT for Data Analysis

DBT is used to transform and analyze the data stored in PostgreSQL. Set up your DBT models and run the DBT commands to generate metrics and reports.

To get started with DBT:
- Set up your `dbt_project.yml` and configure the connection to PostgreSQL in the `profiles.yml` file.
- Write your DBT models in the `models/` directory.
- Run DBT transformations:

```bash
dbt run
```

## Environment Variables

You can store sensitive information (like database credentials) in a `.env` file. Here's an example:

```env
DB_HOST=localhost
DB_NAME=ecommerce
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432
```

Ensure the consumer and DBT configuration are set up to use these environment variables.

## Kafka Topics

The following Kafka topics are used in this project:

1. **user_activity_events**: User activities such as page views and clicks.
2. **user_login_events**: User login events.
3. **user_transaction_events**: Transaction events such as purchases.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### What’s in the README:

- **Project overview**: High-level description of the project.
- **Technologies used**: List of the main technologies involved.
- **Project structure**: Layout of the project files and folders.
- **Setup instructions**: Detailed steps to get the project up and running.
- **Environment variables**: How to configure sensitive information securely.
- **Kafka topics**: Description of the event types handled by Kafka.

You can modify any sections if necessary and fill in more details related to your DBT setup or other specific configurations. Let me know if you need any further adjustments!