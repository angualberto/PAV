import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

BASE = "http://127.0.0.1:5000/api"

class ProductGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Padaria - Produtos")
        self.geometry("700x450")
        self.listbox = tk.Listbox(self, width=100)
        self.listbox.pack(pady=10)
        frame = tk.Frame(self)
        frame.pack()
        tk.Button(frame, text="Novo", command=self.create).pack(side="left", padx=5)
        tk.Button(frame, text="Editar", command=self.edit).pack(side="left", padx=5)
        tk.Button(frame, text="Excluir", command=self.delete).pack(side="left", padx=5)
        tk.Button(frame, text="Atualizar", command=self.refresh).pack(side="left", padx=5)
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        r = requests.get(f"{BASE}/products")
        if r.ok:
            for p in r.json():
                self.listbox.insert(tk.END, f"{p['id']}|{p['sku']}|{p['name']}|R${p['price']:.2f}|Q:{p['quantity']}")
        else:
            messagebox.showerror("Erro", r.text)

    def create(self):
        sku = simpledialog.askstring("SKU","SKU:")
        name = simpledialog.askstring("Nome","Nome:")
        price = simpledialog.askfloat("Preço","Preço:")
        qty = simpledialog.askinteger("Quantidade","Quantidade:",initialvalue=0)
        headers = {'X-API-KEY':'minha_chave_secreta'}
        r = requests.post(f"{BASE}/products", json={"sku":sku,"name":name,"price":price,"quantity":qty}, headers=headers)
        if r.status_code == 201:
            messagebox.showinfo("Sucesso","Produto criado")
            self.refresh()
        else:
            try:
                msg = r.json().get('message', r.text)
            except:
                msg = r.text
            messagebox.showerror("Erro", msg)

    def edit(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Selecione","Selecione um produto")
            return
        line = self.listbox.get(sel[0])
        pid = int(line.split("|")[0])
        name = simpledialog.askstring("Nome","Novo nome:")
        price = simpledialog.askfloat("Preço","Novo preço:")
        qty = simpledialog.askinteger("Quantidade","Nova quantidade:")
        headers = {'X-API-KEY':'minha_chave_secreta'}
        r = requests.put(f"{BASE}/products/{pid}", json={"sku":"SAME","name":name,"price":price,"quantity":qty}, headers=headers)
        if r.ok:
            messagebox.showinfo("OK","Atualizado")
            self.refresh()
        else:
            try:
                msg = r.json().get('message', r.text)
            except:
                msg = r.text
            messagebox.showerror("Erro", msg)

    def delete(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Selecione","Selecione um produto")
            return
        line = self.listbox.get(sel[0])
        pid = int(line.split("|")[0])
        if messagebox.askyesno("Confirma","Deseja excluir?"):
            headers = {'X-API-KEY':'minha_chave_secreta'}
            r = requests.delete(f"{BASE}/products/{pid}", headers=headers)
            if r.ok:
                messagebox.showinfo("OK","Removido")
                self.refresh()
            else:
                try:
                    msg = r.json().get('message', r.text)
                except:
                    msg = r.text
                messagebox.showerror("Erro", msg)

if __name__ == "__main__":
    app = ProductGUI()
    app.mainloop()
