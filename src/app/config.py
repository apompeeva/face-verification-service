import os

from dotenv import load_dotenv

load_dotenv()

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')
TOPIC = os.environ.get('TOPIC')
