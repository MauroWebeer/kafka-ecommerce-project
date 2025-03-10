import subprocess

def create_topic():
    try:
        topic_name = "user_activity_events"  # Adjust this for each topic

        # Running the kafka-topics command inside the Docker container
        subprocess.run([
            'docker', 'exec', '-it', 'kafka-ecommerce-project-kafka-1', 
            'kafka-topics', '--create', '--topic', topic_name, '--bootstrap-server', 'localhost:9092', '--partitions', '1', '--replication-factor', '1'
        ], check=True)

        print(f"Topic '{topic_name}' created successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error creating topic: {e}")

if __name__ == "__main__":
    create_topic()
