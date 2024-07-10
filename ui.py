import tkinter as tk
from tkinter import ttk, messagebox
import database as db

def main():
    root = tk.Tk()
    app = ControlePacientesApp(root)
    root.mainloop()

class ControlePacientesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Pacientes")

        # Frame para cadastro de pacientes
        self.frame_cadastro = tk.Frame(self.root)
        self.frame_cadastro.pack(pady=10)
        
        tk.Label(self.frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = tk.Entry(self.frame_cadastro)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame_cadastro, text="Data de Nascimento:").grid(row=1, column=0, padx=5, pady=5)
        self.data_nascimento_entry = tk.Entry(self.frame_cadastro)
        self.data_nascimento_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.frame_cadastro, text="Cadastrar Paciente", command=self.cadastrar_paciente).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para listar pacientes
        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.pack(pady=10)
        
        self.tree = ttk.Treeview(self.frame_lista, columns=("ID", "Nome", "Data de Nascimento"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data de Nascimento", text="Data de Nascimento")
        self.tree.pack()
        
        # Botão para exclusão de paciente
        self.btn_excluir = tk.Button(self.frame_lista, text="Excluir Paciente", command=self.excluir_paciente)
        self.btn_excluir.pack(pady=10)

        self.carregar_pacientes()  # Carrega inicialmente os pacientes na lista

        # Frame para adicionar produtos
        self.frame_produtos = tk.Frame(self.root)
        self.frame_produtos.pack(pady=10)
        
        tk.Label(self.frame_produtos, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        self.produto_entry = tk.Entry(self.frame_produtos)
        self.produto_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_produtos, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5)
        self.quantidade_entry = tk.Entry(self.frame_produtos)
        self.quantidade_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.frame_produtos, text="Data:").grid(row=1, column=0, padx=5, pady=5)
        self.data_entry = tk.Entry(self.frame_produtos)
        self.data_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.frame_produtos, text="Adicionar Produto", command=self.adicionar_produto).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.frame_lista, text="Ver Produtos", command=self.ver_produtos_paciente).pack(pady=10)


    def cadastrar_paciente(self):
        nome = self.nome_entry.get()
        data_nascimento = self.data_nascimento_entry.get()
        if nome and data_nascimento:
            db.add_paciente(nome, data_nascimento)
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            self.nome_entry.delete(0, tk.END)
            self.data_nascimento_entry.delete(0, tk.END)
            self.carregar_pacientes()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def carregar_pacientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for paciente in db.get_pacientes():
            self.tree.insert('', 'end', values=paciente)
    
    def excluir_paciente(self):
        selected_item = self.tree.selection()
        if selected_item:
            paciente_id = self.tree.item(selected_item)["values"][0]
            confirmar = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este paciente?")
            if confirmar:
                db.delete_paciente(paciente_id)
                messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
                self.carregar_pacientes()  # Atualiza a lista de pacientes após exclusão
        else:
            messagebox.showerror("Erro", "Por favor, selecione um paciente na lista.")

        # Limpar treeview antes de carregar novos dados
        for item in tree_produtos.get_children():
            tree_produtos.delete(item)

        # Obter produtos do paciente por data
        produtos = db.get_produtos(paciente_id)
        for produto in produtos:
            tree_produtos.insert('', 'end', values=(produto[2], produto[3], produto[4]))  # (produto, data)

    def adicionar_produto(self):
        selected_item = self.tree.selection()
        if selected_item:
            paciente_id = self.tree.item(selected_item)["values"][0]
            produto = self.produto_entry.get()
            quantidade = self.quantidade_entry.get()
            data = self.data_entry.get()
            if produto and quantidade and data:
                db.add_produto(paciente_id, produto, quantidade, data)
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                self.produto_entry.delete(0, tk.END)
                self.quantidade_entry.delete(0, tk.END)
                self.data_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione um paciente na lista.")

    def ver_produtos_paciente(self):
        selected_item = self.tree.selection()
        if selected_item:
            paciente_id = self.tree.item(selected_item)["values"][0]
            paciente_nome = self.tree.item(selected_item)["values"][1]

            # Abrir uma nova janela para listar os produtos do paciente
            self.produtos_window = tk.Toplevel(self.root)
            self.produtos_window.title(f"Produtos do Paciente {paciente_nome}")

            # Frame para listar produtos (usando grid para consistência)
            frame_produtos_paciente = tk.Frame(self.produtos_window)
            frame_produtos_paciente.pack(padx=20, pady=10)

            tk.Label(frame_produtos_paciente, text=f"Produtos do Paciente {paciente_nome}").grid(row=0, column=0, columnspan=2, pady=10)

            # Treeview para listar produtos por data
            tree_produtos = ttk.Treeview(frame_produtos_paciente, columns=("Produto", "Quantidade", "Data"), show='headings')
            tree_produtos.heading("Produto", text="Produto")
            tree_produtos.heading("Quantidade", text="Quantidade")
            tree_produtos.heading("Data", text="Data")
            tree_produtos.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            # Botão para voltar para a tela de lista de pacientes
            tk.Button(self.produtos_window, text="Voltar", command=self.produtos_window.destroy).pack(pady=10)

            # Carregar produtos do paciente selecionado
            self.carregar_produtos_paciente(tree_produtos, paciente_id)
        else:
            messagebox.showerror("Erro", "Por favor, selecione um paciente na lista.")

    def carregar_produtos_paciente(self, tree_produtos, paciente_id):
        # Limpar treeview antes de carregar novos dados
        for item in tree_produtos.get_children():
            tree_produtos.delete(item)

        # Obter produtos do paciente por data
        produtos = db.get_produtos(paciente_id)
        for produto in produtos:
            tree_produtos.insert('', 'end', values=(produto[2], produto[3], produto[4]))  # (produto, quantidade, data)

if __name__ == "__main__":
    main()
