import redis
import yaml
import os

with open('/home/muctepkot/ticket_rest/config.yml', 'r') as yaml_config:
    config = yaml.safe_load(yaml_config)

r = redis.Redis(config['redis']['host'], 
                config['redis']['port'], 
                config['redis']['db'], 
                decode_responses=True)

def create_redis_ticket(ticket):
    '''Создание тикета в redis'''
    print(ticket)
    print(type(ticket))
    ticket_id = ticket['id']
    ticket['comments'] = str(ticket['comments'])
    r.hset(ticket_id, None, None, ticket)
    return 'ok'

def update_redis_ticket_status(ticket_id, status):
    '''Обновление статуса тикета в redis'''
    r.hset(ticket_id, "status", status)
    return 'ok'

def get_redis_ticket(ticket_id):
    '''Получение тикета из redis'''
    ticket = r.hgetall(ticket_id)
    return ticket

def check_redis_ticket(ticket_id):
    '''Проверка существования тикета'''
    ticket = r.keys(ticket_id)
    if ticket:
        return True
    else:
        return False
 
