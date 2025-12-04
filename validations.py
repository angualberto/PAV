import re

def clean_digits(s: str) -> str:
    return re.sub(r'\D', '', s or '')

def is_valid_cpf(cpf: str) -> bool:
    cpf = clean_digits(cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    def calc(cpf_slice, factor):
        total = 0
        for ch in cpf_slice:
            total += int(ch) * factor
            factor -= 1
        r = total % 11
        return '0' if r < 2 else str(11 - r)
    d1 = calc(cpf[:9], 10)
    d2 = calc(cpf[:9] + d1, 11)
    return cpf[-2:] == d1 + d2

def is_valid_email(email: str) -> bool:
    if not email:
        return True
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def can_process_order(items: list, inventory_lookup: dict) -> (bool, str):
    # items = list of dicts with product_id, quantity
    for it in items:
        pid = it.get('product_id')
        qty = it.get('quantity', 0)
        if pid not in inventory_lookup:
            return False, f"Produto id {pid} não existe em estoque"
        if inventory_lookup[pid] < qty:
            return False, f"Estoque insuficiente para produto id {pid}"
    return True, ""

# Nova validação: total da nota deve estar entre 0 e 1_000_000
def validate_order_total(total: float) -> (bool, str):
    """
    Retorna (True,"") se total válido, senão (False, mensagem).
    Uso: OrderController deve chamar antes de confirmar/emitir nota.
    """
    try:
        t = float(total)
    except Exception:
        return False, "Total inválido"
    if t < 0:
        return False, "Total da nota não pode ser negativo"
    if t > 1_000_000:
        return False, "Total da nota excede o limite de R$ 1.000.000"
    return True, ""
