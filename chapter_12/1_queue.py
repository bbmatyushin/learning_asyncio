"""Очереди в asyncio работают по принуипу производитель-потребитель.
Очередь создается одна, но несколько потребителей могут конкурентно обрабатывать
с нее данные."""

import asyncio
from asyncio import Queue
from dataclasses import dataclass
from random import randrange


@dataclass
class Product:
    name: str
    checkout_time: float


@dataclass
class Customer:
    customer_id: int
    products: list[Product]


async def checkout_customer(queue: Queue, cashier_num: int):
    """Сопрограмма для обслуживания одного покупателя"""
    while not queue.empty():  # выбираем покупателя, если в очереди кто-то есть
        customer: Customer = queue.get_nowait()  # забрать данные из начала очереди
        print(f"Кассир {cashier_num} обслуживает покупателя {customer.customer_id}")

        for prod in customer.products:
            print(f"Кассир №{cashier_num} обслуживает покупателя {customer.customer_id}: "
                  f"товар - {prod.name}")
            await asyncio.sleep(prod.checkout_time)

        print(f"Кассир №{cashier_num} закончил обслуживать покупателя {customer.customer_id}")

        print('Queue size:', queue.qsize())
        queue.task_done()  # Сигнал, что обработка текущего элемента данных завершена


async def main():
    customer_queue = Queue()

    all_products = [
        Product('Торт', 1.2),
        Product('Бананы', .5),
        Product('Кофе', .9),
        Product('Хлеб', .2),
    ]

    for i in range(10):  # создаем 10 случайных покупателей со случайным набором товара
        products = [all_products[randrange(len(all_products))] for _ in range(randrange(10))]
        # put_nowait() - неблокирующий метод добавления данных в очередь
        # Если при создании очереди указать параметр maxsize=8, то получим исключение asyncio.queue.QueueFull.
        # Чтобы такого не было, нужно использовать блокирующий метод - put() (см. 1_queue_block.py)
        customer_queue.put_nowait(Customer(i, products))

    # Создание 3х задач-исполнителей, для обслуживания данных (покупателей) из очереди
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, j)) for j in range(3)]

    # Сопрограмма join() блокируется до тех пор, пока очередь не опустеет
    await asyncio.gather(customer_queue.join(), *cashiers)


if __name__ == '__main__':
    asyncio.run(main())
