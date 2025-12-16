from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(
    "amqp://guest:guest@217.76.176.93:5672/local",
    exchange_name="report",  # обменник
    queue_name="cmd_order",  # очередь для отправки
    # dead_letter_queue_name="cmd_order_dead"
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


# Модифицируем задачу, добавив расписание с помощью параметра `schedule`.
# Задача будет выполняться каждую минуту.

@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",  # Выражение cron: каждую минуту
            "args": ["Cron_User"],  # Аргументы для функции
            "schedule_id": "greet_every_minute",  # Уникальный ID расписания
        }
    ]
)
async def my_scheduled_task() -> str:
    ...
