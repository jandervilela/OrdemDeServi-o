import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from tkinter import font
import re

# Função para criar o banco de dados e tabelas (se ainda não existir)
def criar_banco():
    conn = sqlite3.connect('ordem_servico.db')
    c = conn.cursor()
    
    # Criação da tabela de usuários
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    cpf TEXT,
                    endereco TEXT,
                    telefone TEXT,
                    email TEXT,
                    data_nascimento TEXT,
                    is_admin BOOLEAN)''')

    # Outras tabelas (clientes, produtos, ordens de serviço) seguem aqui...
    # ...

    conn.commit()
    conn.close()

# Função para adicionar um novo usuário ao banco de dados
def adicionar_usuario(username, senha, cpf, endereco, telefone, email, data_nascimento, is_admin):
    password_hash = hashlib.sha256(senha.encode()).hexdigest()  # Criptografando a senha
    
    # Conectar ao banco de dados e adicionar o usuário
    conn = sqlite3.connect('ordem_servico.db')
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO usuarios (username, password, cpf, endereco, telefone, email, data_nascimento, is_admin)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (username, password_hash, cpf, endereco, telefone, email, data_nascimento, is_admin))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:  # Caso o nome de usuário já exista
        messagebox.showerror("Erro", "Erro ao cadastrar usuário. Verifique se o nome de usuário já existe.")
    
    conn.close()

# Função para abrir a janela de cadastro de novo usuário
def abrir_janela_usuario():
    janela_usuario = tk.Toplevel()
    janela_usuario.title("Cadastro de Usuário")
    janela_usuario.geometry("1024x800")
    
    font_padrao = font.Font(family="Arial", size=14)
    
    # Labels e campos de entrada para cadastro de usuário
    tk.Label(janela_usuario, text="Nome de Usuário", font=font_padrao).pack(pady=10)
    entry_username = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_username.pack(pady=10)

    tk.Label(janela_usuario, text="Senha", font=font_padrao).pack(pady=10)
    entry_senha = tk.Entry(janela_usuario, font=font_padrao, show="*", width=30)
    entry_senha.pack(pady=10)

    tk.Label(janela_usuario, text="CPF", font=font_padrao).pack(pady=10)
    entry_cpf = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_cpf.pack(pady=10)

    tk.Label(janela_usuario, text="Endereço", font=font_padrao).pack(pady=10)
    entry_endereco = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_endereco.pack(pady=10)

    tk.Label(janela_usuario, text="Telefone", font=font_padrao).pack(pady=10)
    entry_telefone = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_telefone.pack(pady=10)

    tk.Label(janela_usuario, text="Email", font=font_padrao).pack(pady=10)
    entry_email = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_email.pack(pady=10)

    tk.Label(janela_usuario, text="Data de Nascimento", font=font_padrao).pack(pady=10)
    entry_data_nascimento = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_data_nascimento.pack(pady=10)

    tk.Label(janela_usuario, text="Administrador (Sim/Nao)", font=font_padrao).pack(pady=10)
    entry_is_admin = tk.Entry(janela_usuario, font=font_padrao, width=30)
    entry_is_admin.pack(pady=10)
    
    # Função para salvar o usuário
    def salvar_usuario():
        username = entry_username.get()
        senha = entry_senha.get()
        cpf = entry_cpf.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        data_nascimento = entry_data_nascimento.get()
        is_admin = entry_is_admin.get().lower() == "true"  # Converte a entrada para booleano
        
        if username and senha and cpf and endereco and telefone and email and data_nascimento:
            adicionar_usuario(username, senha, cpf, endereco, telefone, email, data_nascimento, is_admin)
            janela_usuario.destroy()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    # Botão de salvar
    tk.Button(janela_usuario, text="Salvar", command=salvar_usuario, bg="#4CAF50", fg="white", font=font_padrao).pack(pady=20)

# Tela de login e tela principal seguem aqui...

# Função da tela principal (exemplo)
def tela_principal():
    janela_principal = tk.Tk()
    janela_principal.title("Sistema NextPlanejados")
    janela_principal.geometry("1024x800")
    janela_principal.config(bg="#f0f0f0")

    # Botão para abrir a janela de cadastro de usuário
    btn_novo_usuario = tk.Button(janela_principal, text="Cadastrar Novo Usuário", command=abrir_janela_usuario, width=20, height=2, bg="#4CAF50", fg="white")
    btn_novo_usuario.pack(pady=20)

    janela_principal.mainloop()

# Criar banco de dados
criar_banco()  # Cria o banco de dados e as tabelas
tela_principal()  # Abre a tela principal

# Função para criar o banco de dados e tabelas (se ainda não existir)
def criar_banco():
    conn = sqlite3.connect('ordem_servico.db')
    c = conn.cursor()
    
    # Criação da tabela de usuários com mais campos
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    cpf TEXT,
                    endereco TEXT,
                    telefone TEXT,
                    email TEXT,
                    data_nascimento TEXT,
                    is_admin BOOLEAN)''')

    # Criação da tabela de clientes
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    telefone TEXT,
                    email TEXT,
                    cpf Text)''')

    # Criação da tabela de produtos
    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    quantidade INTEGER,
                    preco REAL)''')

    # Criação da tabela de ordens de serviço
    c.execute('''CREATE TABLE IF NOT EXISTS ordens_servico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    produto_id INTEGER,
                    data_inicio TEXT,
                    status TEXT,
                    FOREIGN KEY(cliente_id) REFERENCES clientes(id),
                    FOREIGN KEY(produto_id) REFERENCES produtos(id))''')
    
    conn.commit()
    conn.close()

# Função para verificar o login
def verificar_login(username, password):
    conn = sqlite3.connect('ordem_servico.db')
    c = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user

# Função para a tela de login
def tela_login():
    janela_login = tk.Tk()
    janela_login.title("NextPlanejados")
    janela_login.geometry("800x500")
    janela_login.config(bg="#f0f0f0")

    # Fonte de textos
    font_padrao = font.Font(family="Arial", size=14)

    # Labels e campos de entrada para login
    tk.Label(janela_login, text="Usuário", font=font_padrao, bg="#f0f0f0").pack(pady=10)
    entry_username = tk.Entry(janela_login, font=font_padrao, width=30)
    entry_username.pack(pady=10)

    tk.Label(janela_login, text="Senha", font=font_padrao, bg="#f0f0f0").pack(pady=10)
    entry_password = tk.Entry(janela_login, font=font_padrao, show="*", width=30)
    entry_password.pack(pady=10)

    # Função de login
    def login():
        username = entry_username.get()
        password = entry_password.get()
        user = verificar_login(username, password)
        if user:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            janela_login.destroy()
            tela_principal()  # Abre a tela principal
        else:
            messagebox.showerror("Login", "Usuário ou senha inválidos.")

    # Botão de login
    btn_login = tk.Button(janela_login, text="Entrar", command=login, bg="#4CAF50", fg="white", font=font_padrao, width=20, height=2)
    btn_login.pack(pady=20)

    janela_login.mainloop()

# Função para a tela principal
def tela_principal():
    janela_principal = tk.Tk()
    janela_principal.title("Sistema NextPlanejados")
    janela_principal.geometry("1024x800")
    janela_principal.config(bg="#f0f0f0")

    # Definir fontes
    font_padrao = font.Font(family="Arial", size=14)
    font_titulo = font.Font(family="Arial", size=18, weight="bold")

    # Criar o Notebook (abas)
    notebook = ttk.Notebook(janela_principal)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Criar frames para as abas
    frame_clientes = ttk.Frame(notebook)
    frame_produtos = ttk.Frame(notebook)
    frame_ordens_servico = ttk.Frame(notebook)

    # Adicionar frames no notebook (abas)
    notebook.add(frame_clientes, text="Clientes")
    notebook.add(frame_produtos, text="Produtos")
    notebook.add(frame_ordens_servico, text="Ordens de Serviço")

    # ----------------- Tela de Clientes -----------------
    clientes_label = tk.Label(frame_clientes, text="Clientes Cadastrados", font=font_titulo)
    clientes_label.pack(pady=20)

    # Treeview para exibir os clientes
    treeview_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nome", "Telefone", "Email", "cpf"), show="headings")
    treeview_clientes.heading("ID", text="ID")
    treeview_clientes.heading("Nome", text="Nome")
    treeview_clientes.heading("Telefone", text="Telefone")
    treeview_clientes.heading("Email", text="Email")
    treeview_clientes.heading("cpf", text="cpf")

    treeview_clientes.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_clientes():
        clientes = carregar_clientes()
        for row in treeview_clientes.get_children():
            treeview_clientes.delete(row)
        if not clientes:
            treeview_clientes.insert("", "end", values=("Nenhum cliente cadastrado.", "", "", "", "", ""))
        for cliente in clientes:
            treeview_clientes.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3],cliente[4]))

    def carregar_clientes():
        conn = sqlite3.connect('ordem_servico.db')
        c = conn.cursor()
        c.execute("SELECT * FROM clientes")
        clientes = c.fetchall()
        conn.close()
        return clientes

    mostrar_clientes()

    # Função para abrir janela de cadastro de cliente
    def abrir_janela_cliente():
        janela_cliente = tk.Toplevel(janela_principal)
        janela_cliente.title("Cadastro de Cliente")
        janela_cliente.geometry("600x500")
        
        tk.Label(janela_cliente, text="Nome", font=font_padrao).pack(pady=10)
        entry_nome = tk.Entry(janela_cliente, font=font_padrao, width=30)
        entry_nome.pack(pady=10)

        tk.Label(janela_cliente, text="Telefone", font=font_padrao).pack(pady=10)
        entry_telefone = tk.Entry(janela_cliente, font=font_padrao, width=30)
        entry_telefone.pack(pady=10)

        tk.Label(janela_cliente, text="Email", font=font_padrao).pack(pady=10)
        entry_email = tk.Entry(janela_cliente, font=font_padrao, width=30)
        entry_email.pack(pady=10)

        tk.Label(janela_cliente, text="cpf", font=font_padrao).pack(pady=10)
        entry_cpf = tk.Entry(janela_cliente, font=font_padrao, width=30)
        entry_cpf.pack(pady=10)

        

        def salvar_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            email = entry_email.get()
            cpf = entry_cpf.get()
            if nome and telefone and email:
                conn = sqlite3.connect('ordem_servico.db')
                c = conn.cursor()
                c.execute("INSERT INTO clientes (nome, telefone, email, cpf) VALUES (?, ?, ?, ?)", (nome, telefone, email, cpf))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                mostrar_clientes()
                janela_cliente.destroy()
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

        # Botão de salvar
        tk.Button(janela_cliente, text="Salvar", command=salvar_cliente, bg="#4CAF50", fg="white", font=font_padrao).pack(pady=20)

    # Botão para abrir a janela de cadastro de cliente
    btn_novo_cliente = tk.Button(frame_clientes, text="Cadastrar Novo Cliente", command=abrir_janela_cliente, width=20, height=2, bg="#4CAF50", fg="white", font=font_padrao)
    btn_novo_cliente.pack(pady=20)

    # ----------------- Tela de Produtos -----------------
    produtos_label = tk.Label(frame_produtos, text="Produtos Cadastrados", font=font_titulo)
    produtos_label.pack(pady=20)

    # Treeview para exibir os produtos
    treeview_produtos = ttk.Treeview(frame_produtos, columns=("ID", "Nome", "Quantidade", "Preço"), show="headings")
    treeview_produtos.heading("ID", text="ID")
    treeview_produtos.heading("Nome", text="Nome")
    treeview_produtos.heading("Quantidade", text="Quantidade")
    treeview_produtos.heading("Preço", text="Preço")
    treeview_produtos.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_produtos():
        produtos = carregar_produtos()
        for row in treeview_produtos.get_children():
            treeview_produtos.delete(row)
        if not produtos:
            treeview_produtos.insert("", "end", values=("Nenhum produto cadastrado.", "", "", ""))
        for produto in produtos:
            treeview_produtos.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3]))

    def carregar_produtos():
        conn = sqlite3.connect('ordem_servico.db')
        c = conn.cursor()
        c.execute("SELECT * FROM produtos")
        produtos = c.fetchall()
        conn.close()
        return produtos

    mostrar_produtos()

    # Função para abrir janela de cadastro de produto
    def abrir_janela_produto():
        janela_produto = tk.Toplevel(janela_principal)
        janela_produto.title("Cadastro de Produto")
        janela_produto.geometry("600x500")

        tk.Label(janela_produto, text="Nome do Produto", font=font_padrao).pack(pady=10)
        entry_nome_produto = tk.Entry(janela_produto, font=font_padrao, width=30)
        entry_nome_produto.pack(pady=10)

        tk.Label(janela_produto, text="Quantidade", font=font_padrao).pack(pady=10)
        entry_quantidade = tk.Entry(janela_produto, font=font_padrao, width=30)
        entry_quantidade.pack(pady=10)

        tk.Label(janela_produto, text="Preço", font=font_padrao).pack(pady=10)
        entry_preco = tk.Entry(janela_produto, font=font_padrao, width=30)
        entry_preco.pack(pady=10)

        def salvar_produto():
            nome_produto = entry_nome_produto.get()
            quantidade = entry_quantidade.get()
            preco = entry_preco.get()
            if nome_produto and quantidade.isdigit() and preco.replace('.', '', 1).isdigit():
                conn = sqlite3.connect('ordem_servico.db')
                c = conn.cursor()
                c.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome_produto, int(quantidade), float(preco)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                mostrar_produtos()
                janela_produto.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

        # Botão de salvar
        tk.Button(janela_produto, text="Salvar", command=salvar_produto, bg="#4CAF50", fg="white", font=font_padrao).pack(pady=20)

    # Botão para abrir a janela de cadastro de produto
    btn_novo_produto = tk.Button(frame_produtos, text="Cadastrar Novo Produto", command=abrir_janela_produto, width=20, height=2, bg="#4CAF50", fg="white", font=font_padrao)
    btn_novo_produto.pack(pady=20)

    # ----------------- Tela de Ordens de Serviço -----------------
    ordens_label = tk.Label(frame_ordens_servico, text="Ordens de Serviço Cadastradas", font=font_titulo)
    ordens_label.pack(pady=20)

    # Treeview para exibir as ordens de serviço
    treeview_ordens_servico = ttk.Treeview(frame_ordens_servico, columns=("ID", "Cliente", "Produto", "Data", "Status"), show="headings")
    treeview_ordens_servico.heading("ID", text="ID")
    treeview_ordens_servico.heading("Cliente", text="Cliente")
    treeview_ordens_servico.heading("Produto", text="Produto")
    treeview_ordens_servico.heading("Data", text="Data")
    treeview_ordens_servico.heading("Status", text="Status")
    treeview_ordens_servico.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_ordens():
        ordens = carregar_ordens()
        for row in treeview_ordens_servico.get_children():
            treeview_ordens_servico.delete(row)
        if not ordens:
            treeview_ordens_servico.insert("", "end", values=("Nenhuma ordem cadastrada.", "", "", "", ""))
        for ordem in ordens:
            treeview_ordens_servico.insert("", "end", values=(ordem[0], ordem[1], ordem[2], ordem[3], ordem[4]))

    def carregar_ordens():
        conn = sqlite3.connect('ordem_servico.db')
        c = conn.cursor()
        c.execute("SELECT ordens_servico.id, clientes.nome, produtos.nome, ordens_servico.data_inicio, ordens_servico.status FROM ordens_servico JOIN clientes ON ordens_servico.cliente_id = clientes.id JOIN produtos ON ordens_servico.produto_id = produtos.id")
        ordens = c.fetchall()
        conn.close()
        return ordens

    mostrar_ordens()

    # Função para abrir janela de cadastro de ordem de serviço
    def abrir_janela_ordem_servico():
        janela_ordem = tk.Toplevel(janela_principal)
        janela_ordem.title("Cadastro de Ordem de Serviço")
        janela_ordem.geometry("600x500")

        tk.Label(janela_ordem, text="Cliente", font=font_padrao).pack(pady=10)
        entry_cliente = tk.Entry(janela_ordem, font=font_padrao, width=30)
        entry_cliente.pack(pady=10)

        tk.Label(janela_ordem, text="Produto", font=font_padrao).pack(pady=10)
        entry_produto = tk.Entry(janela_ordem, font=font_padrao, width=30)
        entry_produto.pack(pady=10)

        tk.Label(janela_ordem, text="Data de Início", font=font_padrao).pack(pady=10)
        entry_data_inicio = tk.Entry(janela_ordem, font=font_padrao, width=30)
        entry_data_inicio.pack(pady=10)

        tk.Label(janela_ordem, text="Status", font=font_padrao).pack(pady=10)
        entry_status = tk.Entry(janela_ordem, font=font_padrao, width=30)
        entry_status.pack(pady=10)

        def salvar_ordem_servico():
            cliente = entry_cliente.get()
            produto = entry_produto.get()
            data_inicio = entry_data_inicio.get()
            status = entry_status.get()
            if cliente and produto and data_inicio and status:
                conn = sqlite3.connect('ordem_servico.db')
                c = conn.cursor()
                c.execute('''INSERT INTO ordens_servico (cliente_id, produto_id, data_inicio, status)
                             VALUES ((SELECT id FROM clientes WHERE nome=?), 
                                     (SELECT id FROM produtos WHERE nome=?), 
                                     ?, ?)''', (cliente, produto, data_inicio, status))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Ordem de serviço cadastrada com sucesso!")
                mostrar_ordens()
                janela_ordem.destroy()
            else:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

        # Botão de salvar
        tk.Button(janela_ordem, text="Salvar", command=salvar_ordem_servico, bg="#4CAF50", fg="white", font=font_padrao).pack(pady=20)

    # Botão para abrir a janela de cadastro de ordem de serviço
    btn_nova_ordem_servico = tk.Button(frame_ordens_servico, text="Nova Ordem de Serviço", command=abrir_janela_ordem_servico, width=20, height=2, bg="#4CAF50", fg="white", font=font_padrao)
    btn_nova_ordem_servico.pack(pady=20)

    janela_principal.mainloop()

# Iniciar a aplicação
criar_banco()
tela_login()
