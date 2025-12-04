from db import SessionLocal
from models import Order, OrderItem, Inventory, Product
from validations import can_process_order

class OrderController:
    def create_order(self, customer_id, items, seller=None):
        session = SessionLocal()
        try:
            # construir lookup
            inventory_lookup = {inv.product_id: inv.quantity for inv in session.query(Inventory).all()}
            ok, msg = can_process_order(items, inventory_lookup)
            if not ok:
                raise Exception(msg)
            order = Order(customer_id=customer_id, seller=seller)
            session.add(order)
            session.flush()
            total = 0.0
            for it in items:
                prod = session.query(Product).get(it['product_id'])
                if not prod or not prod.active:
                    raise Exception(f"Produto {it['product_id']} inválido")
                unit = prod.price
                oi = OrderItem(order_id=order.id, product_id=prod.id, unit_price=unit, quantity=it['quantity'])
                session.add(oi)
                total += unit * it['quantity']
                inv = session.query(Inventory).filter_by(product_id=prod.id).first()
                inv.quantity -= it['quantity']
                if inv.quantity < 0:
                    raise Exception(f"Estoque insuficiente para produto id {prod.id}")
            order.total = total
            order.status = 'PAID'
            session.commit()
            return order
        finally:
            session.close()
