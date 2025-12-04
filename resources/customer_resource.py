from flask_restful import Resource, reqparse
from flask import request
from db import SessionLocal
from models import Customer
from validations import is_valid_cpf, is_valid_email

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('cpf', type=str, required=True)
parser.add_argument('email', type=str, required=False)
parser.add_argument('phone', type=str, required=False)

class CustomerListResource(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per = int(request.args.get('per', 20))
        session = SessionLocal()
        try:
            q = session.query(Customer).filter(Customer.active==True).offset((page-1)*per).limit(per).all()
            return [{'id':c.id,'name':c.name,'cpf':c.cpf,'email':c.email} for c in q], 200
        finally:
            session.close()

    def post(self):
        args = parser.parse_args()
        if not is_valid_cpf(args['cpf']):
            return {'message':'CPF inválido'}, 400
        if not is_valid_email(args.get('email')):
            return {'message':'Email inválido'}, 400
        session = SessionLocal()
        try:
            if session.query(Customer).filter(Customer.cpf==args['cpf']).first():
                return {'message':'CPF já cadastrado'}, 400
            c = Customer(name=args['name'], cpf=args['cpf'], email=args.get('email'), phone=args.get('phone'))
            session.add(c)
            session.commit()
            return {'id': c.id, 'message':'Cliente criado'}, 201
        finally:
            session.close()

class CustomerResource(Resource):
    def get(self, customer_id):
        session = SessionLocal()
        try:
            c = session.query(Customer).get(customer_id)
            if not c or not c.active:
                return {'message':'Cliente não encontrado'}, 404
            return {'id':c.id,'name':c.name,'cpf':c.cpf,'email':c.email}, 200
        finally:
            session.close()
