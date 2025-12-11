from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError
from models import User, Address, Product, Order, Base
import random


engine = create_engine("postgresql://postgres:postgres@localhost/postgres")
Session = sessionmaker(bind=engine)
session = Session()


def populate_database():
    """Заполнение базы данных данными"""
    print("\nНачинаем заполнение базы данных...")

    # Создание пользователей
    users = []
    emails = [f"user{i+1}@example.com" for i in range(5)]

    # Проверяем существующих пользователей
    existing_users = session.query(User).filter(User.email.in_(emails)).all()
    existing_emails = [user.email for user in existing_users]

    if existing_emails:
        print(f"Найдены существующие пользователи с email: {existing_emails}")
        return

    try:
        for i in range(5):
            user = User(
                name=f"User{i+1}",
                email=f"user{i+1}@example.com",
                description=f"Description for user{i+1}",
            )
            session.add(user)
            users.append(user)
            print(f"Создан пользователь: {user.name}")

        session.commit()
        print("Пользователи сохранены в БД")

        # Создание адресов
        addresses = []
        for i, user in enumerate(users):
            address = Address(
                user_id=user.id,
                street=f"Street {i+1}",
                city=f"City {i+1}",
                postal_code=f"1234{i+1}",
            )
            session.add(address)
            addresses.append(address)
            print(f"Создан адрес для {user.name}")

        session.commit()
        print("Адреса сохранены в БД")

        # Создание продуктов
        products = []
        product_names = [f"Product{i+1}" for i in range(5)]

        # Проверяем существующие продукты
        existing_products = (
            session.query(Product).filter(Product.name.in_(product_names)).all()
        )
        if existing_products:
            print(f"Продукты уже существуют. Используем существующие.")
            products = existing_products
        else:
            for i in range(5):
                product = Product(
                    name=f"Product{i+1}",
                    price=random.randint(100, 1000),
                    description=f"Description for product{i+1}",
                )
                session.add(product)
                products.append(product)
                print(f"Создан продукт: {product.name}")

            session.commit()
            print("Продукты сохранены в БД")

        # Создание заказов
        for i in range(5):
            # Проверяем, существует ли уже такой заказ
            existing_order = (
                session.query(Order)
                .filter(
                    Order.user_id == users[i].id, Order.address_id == addresses[i].id
                )
                .first()
            )

            if existing_order:
                print(f"Заказ для {users[i].name} уже существует, пропускаем...")
                continue

            order = Order(
                user_id=users[i].id,
                address_id=addresses[i].id,
                total_amount=random.randint(1000, 5000),
            )

            order_products = random.sample(products, random.randint(2, 3))
            order.products.extend(order_products)

            session.add(order)
            print(f"Создан заказ для {users[i].name}")

        session.commit()
        print("Заказы сохранены в БД")
        print("\n" + "=" * 50)
        print("База данных успешно заполнена!")
        print("=" * 50)

    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка целостности данных: {e}")
        print("Возможно, некоторые данные уже существуют в базе.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при заполнении базы данных: {e}")


def query_related_data():
    """Запрос и вывод связанных данных"""
    print("\nЗапрос связанных данных...")

    try:
        # Исправленный запрос с joinedload
        users = (
            session.query(User)
            .options(
                joinedload(User.addresses),
                joinedload(User.orders).joinedload(Order.delivery_address),
                joinedload(User.orders).joinedload(Order.products),
            )
            .all()
        )

        if not users:
            print("В базе данных нет пользователей!")
            return

        print(f"\nНайдено пользователей: {len(users)}")

        for user in users:
            print(f"\n{'='*60}")
            print(f"Пользователь: {user.name}")
            print(f"Email: {user.email}")
            print(f"Описание: {user.description}")

            if user.addresses:
                print("\nАдреса:")
                for address in user.addresses:
                    print(f"  - {address.street}, {address.city}")
            else:
                print("\nАдреса: нет")

            if user.orders:
                print("\nЗаказы:")
                for order in user.orders:
                    print(f"  - Заказ #{order.id}, Сумма: {order.total_amount}")
                    if order.delivery_address:
                        print(f"    Адрес доставки: {order.delivery_address.street}")
                    if order.products:
                        print("    Продукты:")
                        for product in order.products:
                            print(f"      * {product.name} - {product.price} руб.")
            else:
                print("\nЗаказы: нет")

        print(f"\n{'='*60}")

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")


if __name__ == "__main__":
    try:
        # Проверяем подключение
        with engine.connect() as conn:
            print("Подключение к базе данных успешно!")
        # Заполнение базы данных
        populate_database()

        # Выполнение запросов
        query_related_data()

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        session.close()
        print("\nСессия закрыта.")
