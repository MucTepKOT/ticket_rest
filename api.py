from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy.sql.expression import text
import db_module

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


parser.add_argument('comment', type=str)


class MainPage(Resource):
    def get(self):
        return ('Hi')

class Tickets(Resource):
    def get(self):
        tickets_count = db_module.get_tickets_count()
        return({"tickets_count":tickets_count})
    def post(self):
        parser.add_argument('topic', type=str, required=True)
        parser.add_argument('text', type=str, required=True)
        parser.add_argument('email',  type=str, required=True)
        # user_ticket = request.json
        # print(user_ticket)
        args = parser.parse_args()
        topic = args['topic']
        text = args['text']
        email = args['email']
        ticket_id = db_module.create_ticket(topic, text, email)
        return ticket_id, 200
        # try:
        #     topic = user_ticket['topic']
        #     text = user_ticket['text']
        #     email = user_ticket['email']
        #     ticket_id = db_module.create_ticket(topic, text, email)
        #     return {"success":f"Тикет id {ticket_id} создан успешно."}
        # except KeyError as key_err:
        #     return {"error":"Недостаточно данных для создания тикета."}

class Ticket(Resource):
    def get(self, ticket_id):
        if ticket_id:
            ticket = db_module.get_ticket(ticket_id)
            print(type(ticket))
            return ticket
    
    def patch(self, ticket_id):
        '''Надо затестить'''
        parser.add_argument('status', type=str, required=True)
        args = parser.parse_args()
        new_status = args['status']
        ticket_status_now = db_module.get_ticket_status(ticket_id)
        if ticket_status_now == 'открыт':
            if new_status == 'отвечен' or 'закрыт':
                db_module.update_status(ticket_id, new_status)
            else:
                return {'status':'неверный статус'}
        elif ticket_status_now == 'отвечен':
            if new_status == 'ожидает ответа' or 'закрыт':
                db_module.update_status(ticket_id, new_status)
            else:
                return {'status':'неверный статус'}
        elif ticket_status_now == 'закрыт':
            return {'status':'таска закрыта, изменить статус нельзя'}

api.add_resource(MainPage, '/')
api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<int:ticket_id>')

if __name__ == '__main__':
    app.run(debug=True)