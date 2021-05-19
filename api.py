from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from sqlalchemy.sql.expression import text
import db_module

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('comment', type=str)

class MainPage(Resource):
    def get(self):
        return ('Hi, this is awesome ticket system')

class Tickets(Resource):
    def get(self):
        tickets_count = db_module.get_tickets_count()
        return({"tickets_count":tickets_count})
    def post(self):
        parser.add_argument('topic', type=str, required=True, help='Тикет не может быть создан без темы')
        parser.add_argument('text', type=str, required=True, help='Тикет не может быть пустым')
        parser.add_argument('email',  type=str, required=True, help='Тикет не может быть создан без указания email создателя тикета')
        args = parser.parse_args()
        topic = args['topic']
        text = args['text']
        email = args['email']
        ticket_creation_result = db_module.create_ticket(topic, text, email)
        return ticket_creation_result, 201

class Ticket(Resource):
    def get(self, ticket_id):
        if ticket_id:
            ticket = db_module.get_ticket(ticket_id)
            print(type(ticket))
            return ticket
        else:
            abort(404, description='Тикет не найден')
    
    def patch(self, ticket_id):
        '''Надо затестить'''
        print(request.json)
        parser.add_argument('status', type=str, required=True)
        args = parser.parse_args()
        new_status = args['status']
        print(f'Новый статус: {new_status}')

        if db_module.check_ticket(ticket_id) == True:
            ticket = db_module.get_ticket(ticket_id)
            ticket_status_now = ticket['status']
            print(ticket_status_now)
            if ticket_status_now == 'открыт':
                if new_status == 'отвечен' or 'закрыт':
                    db_module.update_ticket_status(ticket_id, new_status)
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - ОТКРЫТ')
            elif ticket_status_now == 'отвечен':
                if new_status == 'ожидает ответа' or 'закрыт':
                    db_module.update_ticket_status(ticket_id, new_status)
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - ОТВЕЧЕН')
            elif ticket_status_now == 'ожидает ответа':
                if new_status == 'отвечен' or 'закрыт':
                    db_module.update_ticket_status(ticket_id, new_status)
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - ОЖИДАЕТ ОТВЕТА')
            elif ticket_status_now == 'закрыт':
                abort(422, description='Нельзя редактировать тикет со статусом ЗАКРЫТ')
        else:
            abort(404, description=f'Тикет с id {ticket_id} не найден')
                
class Comments(Resource):
    def post(self, ticket_id):
        parser.add_argument('text', type=str, required=True, help='Комментарий не может быть пустым')
        parser.add_argument('email', type=str, required=True, help='Комментарий не может быть создан без указания email комментатора')
        args = parser.parse_args()
        text = args['text']
        email = args['email']

        if db_module.check_ticket(ticket_id) == True:
            ticket = db_module.get_ticket(ticket_id)
            ticket_status = ticket['status']
            print(ticket)
            if ticket_status == 'закрыт':
                abort(422, description='Нельзя комментировать тикет со статусом ЗАКРЫТ')
            else:
                comment_creation_result = db_module.add_comment(ticket_id, text, email)
                if comment_creation_result:
                    return f"Для тикета id {comment_creation_result} успешно создан комментарий", 201
                else:
                    abort(400, description='Создание клмментария произошло с ошибкой. Попробуйте повторить позже.')        
        else:
            abort(404, description=f'Тикет с id {ticket_id} не найден')

api.add_resource(MainPage, '/')
api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<int:ticket_id>')
api.add_resource(Comments, '/tickets/<int:ticket_id>/comments')

if __name__ == '__main__':
    app.run(debug=True)