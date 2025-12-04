from flask_restful import Resource, reqparse
from flask import request
from db import SessionLocal
from controllers.order_controller import OrderController

parser = reqparse.RequestParser()
parser.add_argument('customer_id', type=int, required=True)
parser.add_argument('items', type=list, location='json', required=True)
parser.add_argument('seller', type=str, required=False)

class OrderListResource(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per = int(request.args.get('per', 20))
        session = SessionLocal()
        try:
            q = session.query(OrderController().__class__)  # placeholder to avoid unused import - actual listing below
            # list orders
            from models import Order
            q = session.query(Order).filter(Order.active==True).offset((page-1)*per).limit(per).all()
            res = []
            for o in q:
                res.append({'id':o.id,'customer_id':o.customer_id,'total':o.total,'status':o.status,'seller':o.seller})
            return res, 200
        finally:
            session.close()

    def post(self):
        args = request.get_json(force=True)
        customer_id = args.get('customer_id')
        items = args.get('items', [])
        seller = args.get('seller')
        try:
            controller = OrderController()
            order = controller.create_order(customer_id, items, seller)
            return {'id': order.id, 'message': 'Pedido criado', 'total': order.total}, 201
        except Exception as e:
            return {'message': str(e)}, 400

class OrderResource(Resource):
    def get(self, order_id):
        session = SessionLocal()
        try:
            from models import Order, OrderItem
            o = session.query(Order).get(order_id)
            if not o or not o.active:
                return {'message':'Pedido não encontrado'}, 404
            items = []
            for it in o.items:
                items.append({'product_id': it.product_id, 'quantity': it.quantity, 'unit_price': it.unit_price})
            return {'id':o.id,'customer_id':o.customer_id,'items':items,'total':o.total,'status':o.status}, 200
        finally:
            session.close()
