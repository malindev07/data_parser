import asyncio
import json

from aiokafka import AIOKafkaProducer


async def send_one(url: str, topic: str):
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        await producer.send(topic=topic, value=url)
        # await producer.commit_transaction()
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


# asyncio.run(send_one(topic="sotohit", url="123"))
# import json
# import random
# import time
# from confluent_kafka import Producer
#
# # конфигурация Producer'а
# config = {
#     "bootstrap.servers": "localhost:9092",  # Список серверов Kafka
#     # Идентификатор группы потребителей
#     # Начальная точка чтения ('earliest' или 'latest')
# }
# producer = Producer(config)
#
#
# # функция для генерации случайных данных
# def generate_data():
#     return {
#         "sensor_id": random.randint(1, 100),
#         "temperature": random.uniform(20.0, 30.0),
#         "humidity": random.uniform(30.0, 50.0),
#         "timestamp": int(time.time()),
#     }
#
#
# # функция для сериализации данных в JSON
# def serialize_data(data):
#     return json.dumps(data)
#
#
# # функция для отправки сообщения
# def send_message(topic, data):
#     producer.produce(topic, value=data)
#     producer.flush()
#
#
# # основной цикл отправки сообщений
# try:
#     while True:
#         # генерируем случайные данные
#         data = generate_data()
#
#         # сериализуем данные
#         serialized_data = serialize_data(data)
#
#         # отправляем данные в Kafka
#         send_message("sensor_data", serialized_data)
#
#         # логирование отправленного сообщения
#         print(f"Sent data: {serialized_data}")
#
#         # пауза между отправками
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Stopped.")
#     # producer.close()
