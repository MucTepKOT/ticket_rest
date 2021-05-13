from flask import Flask, request
from flask_restful import Resource, Api
# import db_module

app = Flask(__name__)
api = Api(app)

class Tickets(Resource):
    def post(self):
        pass

class Ticket(Resource):
    def get(self, ticket_id):
        pass

    def put(self, ticket_id):
        pass


api.add_resource(Tickets, '/tickets')
api.add_resource(Ticket, '/tickets/<ticket_id>')

if __name__ == '__main__':
    app.run(debug=True)