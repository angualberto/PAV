from flask import Flask
from flask_restful import Api
from models import Base
from db import engine

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    api = Api(app)

    from resources.product_resource import ProductListResource, ProductResource
    from resources.customer_resource import CustomerListResource, CustomerResource
    from resources.order_resource import OrderListResource, OrderResource

    api.add_resource(ProductListResource, '/api/products')
    api.add_resource(ProductResource, '/api/products/<int:product_id>')
    api.add_resource(CustomerListResource, '/api/customers')
    api.add_resource(CustomerResource, '/api/customers/<int:customer_id>')
    api.add_resource(OrderListResource, '/api/orders')
    api.add_resource(OrderResource, '/api/orders/<int:order_id>')

    return app

if __name__ == "__main__":
    app = create_app()
    # criar tabelas
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
