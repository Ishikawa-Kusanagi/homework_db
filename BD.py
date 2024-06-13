import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, Sale, Stock, Shop, Book, Publisher

DSN = "postgresql://postgres:postgres@localhost:5432/homework_db"
engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Пушкин')

book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher1)
book3 = Book(title='Евгений Онегин', publisher=publisher1)

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')

stock1 = Stock(count=1, book=book1, shop=shop1)
stock2 = Stock(count=1, book=book2, shop=shop1)
stock3 = Stock(count=1, book=book1, shop=shop2)
stock4 = Stock(count=1, book=book3, shop=shop3)
stock5 = Stock(count=1, book=book1, shop=shop1)
# загуглить почему эта херня с датой не работает!!!!!!!!!!!!!!!!
sale1 = Sale(price=600,
             date_sale=datetime.datetime.strptime('09-11-2022', '%d-%m-%Y'),
             count=1, stock=stock1)
sale2 = Sale(price=580,
             date_sale=datetime.datetime.strptime('08-11-2022', '%d-%m-%Y'),
             count=1, stock=stock2)
sale3 = Sale(price=580,
             date_sale=datetime.datetime.strptime('05-11-2022', '%d-%m-%Y'),
             count=1, stock=stock3)
sale4 = Sale(price=490,
             date_sale=datetime.datetime.strptime('02-11-2022', '%d-%m-%Y'),
             count=1, stock=stock4)
sale5 = Sale(price=600,
             date_sale=datetime.datetime.strptime('26-10-2022', '%d-%m-%Y'),
             count=1, stock=stock5)

session.add_all(
    [publisher1, book1, book2, book3, shop1, shop2, shop3, stock1, stock2,
     stock3, stock4, stock5, sale1, sale2, sale3, sale4, sale5])
session.commit()
session.close()


def get_sales_by_publisher(publisher_name):
    publisher = session.query(Publisher).filter(
        Publisher.name == publisher_name).one_or_none()
    if not publisher:
        print("Издатель не найден")
        return

    results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Stock, Book.id == Stock.id_book) \
        .join(Sale, Stock.id == Sale.id_stock) \
        .join(Shop, Stock.id_shop == Shop.id) \
        .filter(Book.id_publisher == publisher.id) \
        .all()

    for title, shop_name, price, date_sale in results:
        print(
            f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    publisher_name = input("Введите имя издателя: ")
    get_sales_by_publisher(publisher_name)
