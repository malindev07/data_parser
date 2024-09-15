import json

from aiokafka import AIOKafkaConsumer
import asyncio

from api.action import create_parser


def deserializer(serialized):
    return json.loads(serialized)


async def consume():
    consumer = AIOKafkaConsumer(
        "sotohit",
        "baucenter",
        bootstrap_servers="localhost:9092",
        group_id="my-group",
        value_deserializer=deserializer,
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()

    try:
        # Consume messages

        async for msg in consumer:

            print(
                "consumed: ",
                msg.topic,
                msg.value,
            )

            res = await create_parser(url=msg.value, topic=msg.topic, data_count=5)
            return res

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


# from confluent_kafka import KafkaException
# from confluent_kafka import Consumer, KafkaException
#
# config = {
#     "bootstrap.servers": "localhost:9092",  # Список серверов Kafka
#     "group.id": "mygroup",  # Идентификатор группы потребителей
#     "auto.offset.reset": "earliest",  # Начальная точка чтения ('earliest' или 'latest')
# }
# consumer = Consumer(config)
# consumer.subscribe(["sensor_data"])
# try:
#     while True:
#         msg = consumer.poll(timeout=1.0)  # ожидание сообщения
#         if msg is None:  # если сообщений нет
#             continue
#         if msg.error():  # обработка ошибок
#             raise KafkaException(msg.error())
#         else:
#             # действия с полученным сообщением
#             print(f"Received message: {msg.value().decode('utf-8')}")
# except KeyboardInterrupt:
#     pass
# finally:
#     consumer.close()  # не забываем закрыть соединение
