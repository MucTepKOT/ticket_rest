import redis

r =redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def create_redis_ticket(ticket):
    print(ticket)
    print(type(ticket))
    ticket_id = ticket['id']
    ticket['comments'] = str(ticket['comments'])
    r.hset(ticket_id, None, None, ticket)
    return 'ok'

def update_redis_ticket_status(ticket_id, status):
    r.hset(ticket_id, "status", status)
    return 'ok'

def get_redis_ticket(ticket_id):
    ticket = r.hgetall(ticket_id)
    return ticket

