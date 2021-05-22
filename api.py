import logging
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import db_module

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class Tickets(Resource):
    def get(self):
        '''Получить общее кол-во тикетов'''
        tickets_count = db_module.get_tickets_count()
        return({"tickets_count":tickets_count})
    def post(self):
        '''Создать тикет'''
        parser_copy = parser.copy()
        parser_copy.add_argument('topic', type=str, required=True, help='Тикет не может быть создан без темы')
        parser_copy.add_argument('text', type=str, required=True, help='Тикет не может быть пустым')
        parser_copy.add_argument('email',  type=str, required=True, help='Тикет не может быть создан без указания email создателя тикета')
        args = parser_copy.parse_args()
        topic = args['topic']
        text = args['text']
        email = args['email']
        ticket_creation_result = db_module.create_ticket(topic, text, email)
        
        return {'ticket_id':ticket_creation_result,
                'info':'Тикет создан'}, 201

class Ticket(Resource):
    def get(self, ticket_id):
        '''Получить тикет по id'''
        if ticket_id:
            ticket = db_module.get_ticket(ticket_id)
            return ticket
        else:
            abort(404, description='Тикет не найден')
    
    def patch(self, ticket_id):
        '''Обновить статус тикета'''
        if db_module.check_ticket(ticket_id) == True:
            parser_copy = parser.copy()
            parser_copy.add_argument('status', type=str, required=True)
            args = parser_copy.parse_args()
            new_status = args['status']
            ticket = db_module.get_ticket(ticket_id)
            ticket_status_now = ticket['status']
            if ticket_status_now == 'открыт':
                if new_status in {'отвечен', 'закрыт'}:
                    db_module.update_ticket_status(ticket_id, new_status)
                    return {'ticket_id':ticket_id,
                            'info':'Статус обновлен'}, 200
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - {ticket_status_now}')
            elif ticket_status_now == 'отвечен':
                if new_status in {'ожидает ответа', 'закрыт'}:
                    db_module.update_ticket_status(ticket_id, new_status)
                    return {'ticket_id':ticket_id,
                            'info':'Статус обновлен'}, 200
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - {ticket_status_now}')
            elif ticket_status_now == 'ожидает ответа':
                if new_status in {'отвечен', 'закрыт'}:
                    db_module.update_ticket_status(ticket_id, new_status)
                    return {'ticket_id':ticket_id,
                            'info':'Статус обновлен'}, 200
                else:
                    abort(422, description=f'Передан некорректный статус. Текущий статус - {ticket_status_now}')
            elif ticket_status_now == 'закрыт':
                abort(422, description=f'Нельзя редактировать тикет со статусом {ticket_status_now}')
        else:
            abort(404, description=f'Тикет с id {ticket_id} не найден')
                
class Comments(Resource):
    def post(self, ticket_id):
        '''Добавить комментарий к тикету'''
        if db_module.check_ticket(ticket_id) == True:
            parser_copy = parser.copy()
            parser_copy.add_argument('text', type=str, required=True, help='Комментарий не может быть пустым')
            parser_copy.add_argument('email', type=str, required=True, help='Комментарий не может быть создан без указания email комментатора')
            args = parser_copy.parse_args()
            text = args['text']
            email = args['email']
            ticket = db_module.get_ticket(ticket_id)
            ticket_status = ticket['status']
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

api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<int:ticket_id>')
api.add_resource(Comments, '/tickets/<int:ticket_id>/comments')

if __name__ == '__main__':
    app.run(debug=True)