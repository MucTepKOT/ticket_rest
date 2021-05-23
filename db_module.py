import yaml
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

with open('/home/muctepkot/ticket_rest/config.yml', 'r') as yaml_config:
    config = yaml.safe_load(yaml_config)

engine = create_engine(config['postgresql_engine'], echo=True, echo_pool='debug')

Session = sessionmaker(engine)
session = Session()

Base = declarative_base()

class TicketsTable(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    update_date = Column(DateTime)
    topic = Column(String(500), nullable=False)
    text = Column(String(2000), nullable=False)
    email = Column(String(200), nullable=False)
    status = Column(String(100), nullable=False, default='открыт')
    def __repr__(self):
        return "<TicketsTable('%s','%s','%s','%s','%s','%s')>" % (self.create_date, self.update_date, self.topic, self.text, self.email, self.status)

class TicketsCommentsTable(Base):
    __tablename__ = 'tickets_comments'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    email = Column(String(200), nullable=False)
    text = Column(String(3000), nullable=False)
    def __repr__(self):
        return "<TicketsCommentsTable('%s','%s','%s','%s')>" % (self.ticket_id, self.create_date, self.email, self.text)

def get_tickets_count():
    '''Получение кол-ва тикетов в postgresql'''
    tickets = session.query(TicketsTable).count()
    return tickets 

def create_ticket(topic, text, email):
    '''Создание тикета в postgresql'''
    ticket = TicketsTable(topic=topic, text=text, email=email)
    session.add(ticket)
    try:
        session.commit()
        return get_ticket(ticket.id)
    except:
        session.rollback()
        raise

def get_ticket(ticket_id):
    '''Получение тикета из postgresql'''
    query = session.query(TicketsTable).filter(TicketsTable.id == ticket_id)
    ticket = query.first()
    if ticket:
        ticket_dict = {'id':ticket.id,
                    'topic':ticket.topic,
                    'text':ticket.text,
                    'email':ticket.email,
                    'status':ticket.status,
                    'create_date':str(ticket.create_date),
                    'update_date':str(ticket.update_date)}
        comments = get_comments(ticket_id)
        ticket_dict['comments'] = comments       
        return ticket_dict
    else:
        return None

def update_ticket_status(ticket_id, new_status):
    '''Обновление статуса тикета в postgresql'''
    query = session.query(TicketsTable).filter(TicketsTable.id == ticket_id)
    ticket = query.first()
    ticket.status = new_status
    ticket.update_date = datetime.now()
    try:
        session.commit()
        return ticket
    except:
        session.rollback()
        raise

def check_ticket(ticket_id):
    '''Проверка, существует ли тикет в postgresql'''
    query = session.query(TicketsTable).filter(TicketsTable.id == ticket_id)
    res = session.query(query.exists()).scalar()
    return res

def add_comment(ticket_id, text, email):
    '''Создание комментария для тикета в postgresql'''
    ticket_comment = TicketsCommentsTable(ticket_id=ticket_id, text=text, email=email)
    try:
        session.add(ticket_comment)
        session.commit()
        return ticket_comment.ticket_id
    except:
        session.rollback()
        raise
    
def get_comments(ticket_id):
    '''Получение комментария для тикета в postgresql'''
    query = session.query(TicketsCommentsTable).filter(TicketsCommentsTable.ticket_id == ticket_id)
    comments = query.all()
    tasks_comments = []
    for comment in comments:
        comment_dict = {'id':comment.id,
                    'text':comment.text,
                    'email':comment.email,
                    'create_date':str(comment.create_date)}
        tasks_comments.append(comment_dict)
    return tasks_comments
