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
    while True:
        customer: Customer = await queue.get()  # блокирует выполнение, если в очереди нет данных (покупателей)
        print(f"Кассир {cashier_num} обслуживает покупателя {customer.customer_id}")

        for prod in customer.products:
            print(f"Кассир №{cashier_num} обслуживает покупателя {customer.customer_id}: "
                  f"товар - {prod.name}")
            await asyncio.sleep(prod.checkout_time)

        print(f"Кассир №{cashier_num} закончил обслуживать покупателя {customer.customer_id}")

        queue.task_done()  # Сигнал, что обработка текущего элемента данных завершена


def generate_customer(customer_id: int) -> Customer:
    """Генерация случайног покупателя"""
    all_products = [
        Product('Торт', 8.2),
        Product('Бананы', 3.5),
        Product('Кофе', 4.9),
        Product('Хлеб', 2.2),
    ]
    products = [all_products[randrange(len(all_products))] for _ in range(randrange(10))]

    return Customer(customer_id, products)


async def generate_customer_count(queue: Queue):
    """Генерировать нескольк случайных покупателей в секунду"""
    customer_count: int = 0

    while True:
        customers = [generate_customer(i) for i in range(customer_count, customer_count + randrange(5))]

        for cust in customers:
            print(f'Ожидается возможность поставить покупателя {cust.customer_id} в очередь...')
            await queue.put(cust)  # Если очередь будет переполнена, то ждем пока размер ее уменьшится на 1
            print(f"Покупатель {cust.customer_id} поставлен в очередь")

        customer_count += len(customers)
        await asyncio.sleep(1)


async def main():
    customer_queue = Queue(5)

    customer_producer = asyncio.create_task(generate_customer_count(customer_queue))

    # Создание 3х задач-исполнителей, для обслуживания данных (покупателей) из очереди
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, j)) for j in range(3)]

    # Сопрограмма join() блокируется до тех пор, пока очередь не опустеет
    await asyncio.gather(customer_producer, *cashiers)


if __name__ == '__main__':
    asyncio.run(main())
