from flask_restful import Resource, reqparse
from flask import request, current_app
from db import SessionLocal
from models import Product, Inventory
from controllers.product_controller import ProductController
from config import API_KEY

parser = reqparse.RequestParser()
parser.add_argument('sku', type=str, required=True)
parser.add_argument('name', type=str, required=True)
parser.add_argument('price', type=float, required=True)
parser.add_argument('quantity', type=int, required=False, default=0)

def check_api_key():
    key = request.headers.get('X-API-KEY')
    if key != API_KEY:
        return False
    return True

class ProductListResource(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per = int(request.args.get('per', 20))
        session = SessionLocal()
        try:
            q = session.query(Product).filter(Product.active == True).offset((page-1)*per).limit(per).all()
            result = []
            for p in q:
                qty = p.inventory.quantity if p.inventory else 0
                result.append({'id':p.id,'sku':p.sku,'name':p.name,'price':p.price,'quantity':qty})
            return result, 200
        finally:
            session.close()

    def post(self):
        if not check_api_key():
            return {'message':'Unauthorized'}, 401
        args = parser.parse_args()
        try:
            controller = ProductController()
            prod = controller.create_product(args['sku'], args['name'], args['price'], args['quantity'])
            return {'id': prod.id, 'message': 'Produto criado'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

class ProductResource(Resource):
    def get(self, product_id):
        session = SessionLocal()
        try:
            p = session.query(Product).get(product_id)
            if not p or not p.active:
                return {'message':'Produto não encontrado'}, 404
            qty = p.inventory.quantity if p.inventory else 0
            return {'id':p.id,'sku':p.sku,'name':p.name,'price':p.price,'quantity':qty}, 200
        finally:
            session.close()

    def put(self, product_id):
        if not check_api_key():
            return {'message':'Unauthorized'}, 401
        args = parser.parse_args()
        try:
            controller = ProductController()
            controller.update_product(product_id, args['sku'], args['name'], args['price'], args['quantity'])
            return {'message':'Atualizado'}, 200
        except Exception as e:
            return {'message': str(e)}, 400

    def delete(self, product_id):
        if not check_api_key():
            return {'message':'Unauthorized'}, 401
        try:
            controller = ProductController()
            controller.delete_product(product_id)
            return {'message':'Removido'}, 200
        except Exception as e:
            return {'message': str(e)}, 400
