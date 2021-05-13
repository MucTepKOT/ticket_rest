from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine
# from sqlalchemy.sql import select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@localhost/tickets_db', echo=True)
# Флаг echo включает ведение лога через стандартный модуль logging Питона.

Base = declarative_base()

class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    create_date = Column(Date, nullable=False, default=date.today())
    update_date = Column(Date)
    topic = Column(String(500), nullable=False)
    text = Column(String(2000), nullable=False)
    email = Column(String(200), nullable=False)
    status = Column(String(100), nullable=False, default='открыт')
    # def __init__(self, topic, text, email):
    #     self.topic = topic
    #     self.text = text
    #     self.email = email
    def __repr__(self):
        return "<Tickets('%s','%s','%s','%s','%s','%s')>" % (self.create_date, self.update_date, self.topic, self.text, self.email, self.status)


class TicketsComments(Base):
    __tablename__ = 'tickets_comments'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    create_date = Column(Date, nullable=False, default=date.today())
    email = Column(String(200), nullable=False)
    text = Column(String(3000), nullable=False)
    # def __init__(self, ticket_id, email, text):
    #     self.ticket_id = ticket_id
    #     self.email = email
    #     self.text = text
    def __repr__(self): 
        return "<TicketsComments('%s','%s','%s','%s')>" % (self.ticket_id, self.create_date, self.email, self.text)

# Base.metadata.create_all(engine)

def create_ticket(topic, text, email):
    ticket = Tickets(topic, text, email)
    session.add(ticket)
    # print(ticket.id)
    session.commit()
    # print(ticket.id)
    return ticket.id


def update_status(ticket_id, status):
    query = session.query(Tickets).filter(Tickets.id == ticket_id)
    ticket = query.first()
    ticket.status = status
    session.commit()
    print(ticket)
    return ticket.id

def get_ticket(ticket_id):
    query = session.query(Tickets).filter(Tickets.id == ticket_id)
    ticket = query.first()
    # print(ticket)
    return ticket

def add_comment(text, email, ticket_id):
    ticket_comment = TicketsComments()
    

Session = sessionmaker(engine)
session = Session()

# ticket = Tickets(topic='второй тестовый тикет', text='Какой-то текст второго тестового тикета бла бла', email='555@test.ru')

# print(create_ticket(topic='третий тестовый тикет', text='Какой-то текст третьего тестового тикета бла бла', email='566@test.ru'))
# print(update_status(ticket_id=2, status='ожидает ответа'))
print(get_ticket(3))

# session.add(first_ticket)
# session.commit()
