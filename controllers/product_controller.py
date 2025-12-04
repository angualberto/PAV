from db import SessionLocal
from models import Product, Inventory, OrderItem

class ProductController:
    def create_product(self, sku, name, price, quantity=0):
        if price <= 0:
            raise Exception("Preço deve ser maior que zero")
        session = SessionLocal()
        try:
            if session.query(Product).filter(Product.sku == sku, Product.active == True).first():
                raise Exception("SKU já existe")
            p = Product(sku=sku, name=name, price=price)
            session.add(p)
            session.flush()
            inv = Inventory(product_id=p.id, quantity=quantity)
            session.add(inv)
            session.commit()
            return p
        finally:
            session.close()

    def update_product(self, pid, sku, name, price, quantity):
        session = SessionLocal()
        try:
            p = session.query(Product).get(pid)
            if not p or not p.active:
                raise Exception("Produto não encontrado")
            if price <= 0:
                raise Exception("Preço inválido")
            p.sku = sku
            p.name = name
            p.price = price
            if p.inventory:
                p.inventory.quantity = quantity
            else:
                inv = Inventory(product_id=p.id, quantity=quantity)
                session.add(inv)
            session.commit()
            return p
        finally:
            session.close()

    def delete_product(self, pid):
        session = SessionLocal()
        try:
            p = session.query(Product).get(pid)
            if not p:
                raise Exception("Produto não encontrado")
            if session.query(OrderItem).filter(OrderItem.product_id == pid).first():
                raise Exception("Produto referenciado em pedidos. Remoção não permitida.")
            p.active = False
            session.commit()
            return True
        finally:
            session.close()
