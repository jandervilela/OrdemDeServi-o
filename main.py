import tkinter as tk
from tkinter import ttk
import requests
import json
from tkinter import messagebox
import re  # Importa o módulo de expressões regulares
from tkinter import messagebox
import locale
import sqlite3
from datetime import datetime
from ttkthemes import ThemedTk
import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow
import calendar
from datetime import datetime, date
#from tkwidgets import MaskedEntry

modo_edicao_cliente = False
id_cliente_editando = None

def criar_tabela_produtos(): #já conferido
    """
    Cria a tabela 'produtos' no banco de dados 'banco_de_dados.db'
    se ela ainda não existir.
    """
    # Estabelece uma conexão com o banco de dados SQLite chamado 'banco_de_dados.db'.
    # Se o arquivo não existir, ele será criado.
    conn = sqlite3.connect('banco_de_dados.db')

    # Cria um objeto cursor, que permite executar comandos SQL.
    cursor = conn.cursor()

    # Executa um comando SQL para criar a tabela 'produtos' se ela não existir ('IF NOT EXISTS').
    # Define as colunas da tabela e seus respectivos tipos de dados e restrições:
    # - id: INTEGER, chave primária ('PRIMARY KEY') e auto-incrementável ('AUTOINCREMENT').
    # - nome: TEXT, não pode ser nulo ('NOT NULL').
    # - descricao: TEXT, não pode ser nulo ('NOT NULL').
    # - categoria: TEXT, não pode ser nulo ('NOT NULL').
    # - tipo_codigo_barras: TEXT, pode ser nulo.
    # - codigo_barras: TEXT, pode ser nulo.
    # - preco_custo: REAL, não pode ser nulo ('NOT NULL').
    # - preco_venda: REAL, não pode ser nulo ('NOT NULL').
    # - estoque: INTEGER, não pode ser nulo ('NOT NULL').
    # - unidade: TEXT, pode ser nulo.
    # - sku: TEXT, pode ser nulo.
    # - fornecedor: TEXT, pode ser nulo.
    # - margem_lucro: REAL, pode ser nulo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo_codigo_barras TEXT,
            codigo_barras TEXT,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            estoque INTEGER NOT NULL,
            unidade TEXT,
            sku TEXT,
            fornecedor TEXT,
            margem_lucro REAL
        )
    """)

    # Confirma as alterações feitas no banco de dados.
    conn.commit()

    # Fecha a conexão com o banco de dados, liberando os recursos.
    conn.close()

def criar_tabela_servicos():
    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        descricao TEXT
    )
    """)
    conn.commit()
    conn.close()

def criar_tabela_clientes(): #já conferido
    """
    Cria a tabela 'clientes' no banco de dados 'banco_de_dados.db'
    se ela ainda não existir.
    """
    # Estabelece uma conexão com o banco de dados SQLite chamado 'banco_de_dados.db'.
    # Se o arquivo não existir, ele será criado.
    conn = sqlite3.connect('banco_de_dados.db')

    # Cria um objeto cursor, que permite executar comandos SQL.
    cursor = conn.cursor()

    # Executa um comando SQL para criar a tabela 'clientes' se ela não existir ('IF NOT EXISTS').
    # Define as colunas da tabela e seus respectivos tipos de dados e restrições:
    # - id: INTEGER, chave primária ('PRIMARY KEY') e auto-incrementável ('AUTOINCREMENT').
    # - nome: TEXT, não pode ser nulo ('NOT NULL').
    # - cpf_cnpj: TEXT, deve ser único ('UNIQUE'), pode ser nulo.
    # - telefone: TEXT, pode ser nulo.
    # - email: TEXT, pode ser nulo.
    # - cep: TEXT, pode ser nulo.
    # - rua: TEXT, pode ser nulo.
    # - numero: TEXT, pode ser nulo.
    # - complemento: TEXT, pode ser nulo.
    # - bairro: TEXT, não pode ser nulo ('NOT NULL').
    # - cidade: TEXT, não pode ser nulo ('NOT NULL').
    # - estado: TEXT, não pode ser nulo ('NOT NULL').
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT UNIQUE,
            telefone TEXT,
            email TEXT,
            cep TEXT,
            rua TEXT,
            numero TEXT,
            complemento TEXT,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    # Confirma as alterações feitas no banco de dados.
    conn.commit()

    # Fecha a conexão com o banco de dados, liberando os recursos.
    conn.close()

def buscar_tipos_servico():
    """Busca os nomes de todos os serviços cadastrados no banco de dados."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM servicos")
        tipos_servico = [row[0] for row in cursor.fetchall()]
        return tipos_servico
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Buscar Serviços", f"Ocorreu um erro ao buscar os tipos de serviço: {e}")
        return []
    finally:
        if conn:
            conn.close()

def buscar_clientes_por_prefixo(prefixo):
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM clientes WHERE nome LIKE ? ORDER BY nome", (prefixo + '%',))
        clientes = [row[0] for row in cursor.fetchall()]
        print(f"Buscar Clientes: Prefixo = '{prefixo}', Resultados = {clientes}")
        return clientes
    except sqlite3.Error as e:
        print(f"Erro ao buscar clientes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def mostrar_calendario(frame, ano=datetime.now().year, mes=datetime.now().month, entry_data_inicial_os=None, janela_principal=None):
    style = ttk.Style()
    print(style.theme_use())
    print(style.layout("TButton"))
    print(style.configure("TButton"))

    # Limpa o frame de calendário se já houver algo nele
    for widget in frame.winfo_children():
        widget.destroy()

    cal = calendar.monthcalendar(ano, mes)
    dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    hoje = datetime.now().date()

    # Estilo para o dia atual
    estilo_dia_atual = ttk.Style()
    estilo_dia_atual.configure("DiaAtual.TButton",
                               background="yellow",
                               foreground="black",
                               font=('Arial', 9, 'bold'))
    estilo_dia_atual.map("DiaAtual.TButton",
                         background=[('active', 'orange')],
                         foreground=[('active', 'black')])

    # Cabeçalho dos dias da semana
    for i, dia in enumerate(dias_semana):
        lbl_dia_semana = ttk.Label(frame, text=dia, width=3)
        lbl_dia_semana.grid(row=0, column=i, padx=2, pady=2)

    # Dias do mês
    for semana_index, semana in enumerate(cal):
        for dia_index, dia in enumerate(semana):
            if dia != 0:
                data_celula = date(ano, mes, dia)
                if data_celula == hoje:
                    btn_dia = ttk.Button(frame, text=dia, width=3,
                                       command=lambda d=dia: selecionar_data_os(d, ano, mes, entry_data_inicial_os, janela_principal),
                                       style="DiaAtual.TButton")
                else:
                    btn_dia = ttk.Button(frame, text=dia, width=3,
                           command=lambda d=dia: selecionar_data_os(d, ano, mes, entry_data_inicial_os, janela_principal))
                btn_dia.grid(row=semana_index + 1, column=dia_index, padx=2, pady=2)

    # Botões de navegação (mês anterior e próximo)
    frame_nav = ttk.Frame(frame)
    frame_nav.grid(row=len(cal) + 1, column=0, columnspan=7, pady=5)

    btn_prev = ttk.Button(frame_nav, text="<", width=3, command=lambda: mostrar_calendario(frame, ano - 1 if mes == 1 else ano, mes - 1 if mes > 1 else 12, entry_data_inicial_os, janela_principal))
    btn_prev.pack(side=tk.LEFT)

    lbl_mes_ano = ttk.Label(frame_nav, text=f"{calendar.month_name[mes]} {ano}")
    lbl_mes_ano.pack(side=tk.LEFT, padx=10)

    btn_next = ttk.Button(frame_nav, text=">", width=3, command=lambda: mostrar_calendario(frame, ano + 1 if mes == 12 else ano, mes + 1 if mes < 12 else 1, entry_data_inicial_os, janela_principal))
    btn_next.pack(side=tk.LEFT)

def selecionar_data_os(dia, ano, mes, entry_widget, janela_principal):
    data_selecionada = f"{dia:02d}/{mes:02d}/{ano}"
    if entry_widget:
        entry_widget.config(state=tk.NORMAL)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, data_selecionada)
        entry_widget.config(state='readonly')
        global frame_calendario_visivel
        # Encontre a janela Toplevel do calendário e destrua-a
        toplevel_calendario = None
        for widget in janela_principal.winfo_children(): # Use janela_principal aqui
            if isinstance(widget, tk.Toplevel) and widget.title() == "Selecionar Data":
                toplevel_calendario = widget
                break
        if toplevel_calendario:
            toplevel_calendario.destroy()
            frame_calendario_visivel = False

def abrir_calendario_os(janela_principal): # 'janela_principal' agora recebe a referência de 'root'
    global frame_calendario_visivel, btn_calendario_inicial_os

    if 'frame_calendario_visivel' not in globals():
        frame_calendario_visivel = False

    if frame_calendario_visivel:
        # Se já estiver visível, podemos fechar a janela (se for um Toplevel)
        for widget in janela_principal.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.title() == "Selecionar Data":
                widget.destroy()
                frame_calendario_visivel = False
                return

    nova_janela_calendario = tk.Toplevel(janela_principal) # Use 'janela_principal' aqui
    nova_janela_calendario.title("Selecionar Data")
    frame_calendario = ttk.Frame(nova_janela_calendario)
    frame_calendario.pack()
    
    mostrar_calendario(frame_calendario, entry_data_inicial_os=entry_data_inicial_os, janela_principal=janela_principal)
    # Obtenha a posição do botão "Data" na tela
    x_botao_global = btn_calendario_inicial_os.winfo_rootx()
    y_botao_global = btn_calendario_inicial_os.winfo_rooty() + btn_calendario_inicial_os.winfo_height()

    # Posicione a janela do calendário abaixo do botão
    nova_janela_calendario.geometry(f"+{x_botao_global}+{y_botao_global}")
    nova_janela_calendario.transient(janela_principal) # Use 'janela_principal' aqui
    nova_janela_calendario.grab_set() # Focar nesta janela

    frame_calendario_visivel = True
           
def criar_aba_ordens_servico(notebook, janela_principal):
    aba_os = ttk.Frame(notebook)
    notebook.add(aba_os, text="Ordens de Serviço")

    global frame_cadastro_os_global
    frame_cadastro_os_global = ttk.LabelFrame(aba_os, text="Nova Ordem de Serviço")
    frame_cadastro_os_global.pack(padx=10, pady=10, fill='x', expand=False)
    frame_cadastro_os_global.columnconfigure(0, weight=1)
    frame_cadastro_os_global.columnconfigure(1, weight=2)

    # --- Data Inicial (Automática) ---
    lbl_data_inicial_os = ttk.Label(frame_cadastro_os_global, text="Data Inicial:")
    lbl_data_inicial_os.grid(row=4, column=0, padx=5, pady=5, sticky='w')

    global entry_data_inicial_os  # Declare como global aqui
    entry_data_inicial_os = ttk.Entry(frame_cadastro_os_global, state='readonly')
    entry_data_inicial_os.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    # --- Cliente (Com Auto-Complete) ---
    lbl_cliente_os = ttk.Label(frame_cadastro_os_global, text="Cliente*:")
    lbl_cliente_os.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_cliente_os = ttk.Entry(frame_cadastro_os_global)
    entry_cliente_os.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    listbox_sugestoes_cliente = tk.Listbox(frame_cadastro_os_global, height=5)
    listbox_sugestoes_cliente.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
    listbox_sugestoes_cliente.lower()

    def buscar_clientes_por_prefixo(prefixo):
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM clientes WHERE nome LIKE ? ORDER BY nome", (prefixo + '%',))
            clientes = [row[0] for row in cursor.fetchall()]
            return clientes
        except sqlite3.Error as e:
            print(f"Erro ao buscar clientes: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def atualizar_sugestoes_cliente(event):
        texto_digitado = entry_cliente_os.get()
        if len(texto_digitado) >= 2:
            sugestoes = buscar_clientes_por_prefixo(texto_digitado)
            listbox_sugestoes_cliente.delete(0, tk.END)
            for sugestao in sugestoes:
                listbox_sugestoes_cliente.insert(tk.END, sugestao)
            if sugestoes:
                listbox_sugestoes_cliente.lift(entry_cliente_os)
            else:
                listbox_sugestoes_cliente.lower()
        else:
            listbox_sugestoes_cliente.lower()

    def selecionar_cliente(event):
        try:
            selecao_indices = listbox_sugestoes_cliente.curselection()
            if selecao_indices:
                selecao = listbox_sugestoes_cliente.get(selecao_indices[0])
                entry_cliente_os.delete(0, tk.END)
                entry_cliente_os.insert(0, selecao)
                listbox_sugestoes_cliente.lower()
                entry_cliente_os.focus_set()
        except tk.TclError:
            pass

    entry_cliente_os.bind("<KeyRelease>", atualizar_sugestoes_cliente)
    listbox_sugestoes_cliente.bind("<Double-Button-1>", selecionar_cliente)
    listbox_sugestoes_cliente.bind("<Return>", selecionar_cliente)

    # --- Técnico Responsável (Combobox) ---
    lbl_tecnico_os = ttk.Label(frame_cadastro_os_global, text="Técnico Responsável:")
    lbl_tecnico_os.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    combo_tecnico_os = ttk.Combobox(frame_cadastro_os_global, values=[""])
    combo_tecnico_os.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    def carregar_tecnicos_os(combobox):
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM tecnicos ORDER BY nome",)
            tecnicos = [row[0] for row in cursor.fetchall()]
            combobox['values'] = tecnicos
            if conn:
                conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Erro ao Carregar Técnicos", f"Ocorreu um erro ao carregar os técnicos: {e}")
            combobox['values'] = []

    carregar_tecnicos_os(combo_tecnico_os)

    # --- Status ---
    lbl_status_os = ttk.Label(frame_cadastro_os_global, text="Status*:")
    lbl_status_os.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    combo_status_os = ttk.Combobox(frame_cadastro_os_global, values=["Aberto", "Em Andamento", "Fechado"])
    combo_status_os.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

    # --- Data Inicial (Automática) ---
    lbl_data_inicial_os = ttk.Label(frame_cadastro_os_global, text="Data Inicial:")
    lbl_data_inicial_os.grid(row=4, column=0, padx=5, pady=5, sticky='w')

    entry_data_inicial_os = ttk.Entry(frame_cadastro_os_global, state='readonly')
    entry_data_inicial_os.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    # --- Tipo de Ordem de Serviço (Com Auto-Complete) ---
    lbl_tipo_os = ttk.Label(frame_cadastro_os_global, text="Tipo de Serviço*:")
    lbl_tipo_os.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    entry_tipo_os = ttk.Entry(frame_cadastro_os_global)
    entry_tipo_os.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    listbox_sugestoes_tipo_os = tk.Listbox(frame_cadastro_os_global, height=5)
    listbox_sugestoes_tipo_os.grid(row=6, column=1, padx=5, pady=2, sticky='ew')
    listbox_sugestoes_tipo_os.lower()

    def buscar_tipos_servico_por_prefixo(prefixo):
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM servicos WHERE nome LIKE ? ORDER BY nome", (prefixo + '%',))
            tipos = [row[0] for row in cursor.fetchall()]
            return tipos
        except sqlite3.Error as e:
            print(f"Erro ao buscar tipos de serviço: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def atualizar_sugestoes_tipo_os(event):
        texto_digitado = entry_tipo_os.get()
        if len(texto_digitado) >= 2:
            sugestoes = buscar_tipos_servico_por_prefixo(texto_digitado)
            listbox_sugestoes_tipo_os.delete(0, tk.END)
            for sugestao in sugestoes:
                listbox_sugestoes_tipo_os.insert(tk.END, sugestao)
            if sugestoes:
                listbox_sugestoes_tipo_os.lift(entry_tipo_os)
            else:
                listbox_sugestoes_tipo_os.lower()
        else:
            listbox_sugestoes_tipo_os.lower()

    def selecionar_tipo_os(event):
        try:
            selecao_indices = listbox_sugestoes_tipo_os.curselection()
            if selecao_indices:
                selecao = listbox_sugestoes_tipo_os.get(selecao_indices[0])
                entry_tipo_os.delete(0, tk.END)
                entry_tipo_os.insert(0, selecao)
                listbox_sugestoes_tipo_os.lower()
                entry_tipo_os.focus_set()
        except tk.TclError:
            pass

    entry_tipo_os.bind("<KeyRelease>", atualizar_sugestoes_tipo_os)
    listbox_sugestoes_tipo_os.bind("<Double-Button-1>", selecionar_tipo_os)
    listbox_sugestoes_tipo_os.bind("<Return>", selecionar_tipo_os)

    # --- Orçamento Checkbutton ---
    check_orcamento_var_os = tk.BooleanVar()
    check_orcamento_os = ttk.Checkbutton(frame_cadastro_os_global, text="Orçamento", variable=check_orcamento_var_os)
    check_orcamento_os.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    # --- Frame para Listagem de Ordens de Serviço ---
    frame_lista_os = ttk.LabelFrame(aba_os, text="Ordens de Serviço Cadastradas")
    frame_lista_os.pack(padx=10, pady=10, fill='both', expand=True)

    return aba_os

# Chamada da função para criar a tabela de clientes na inicialização do programa.
criar_tabela_clientes()

# Chamada da função para criar a tabela de produtos na inicialização do programa.
criar_tabela_produtos()

# Define a localidade para o Brasil (se não estiver definida)
try: #já conferido
    # Tenta configurar a localidade para português do Brasil com codificação UTF-8.
    # UTF-8 é uma codificação de caracteres amplamente utilizada e recomendada.
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Se a primeira tentativa falhar (a localidade 'pt_BR.UTF-8' pode não estar instalada no sistema),
    # tenta configurar para português do Brasil sem especificar a codificação.
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except locale.Error:
        # Se a segunda tentativa também falhar (a localidade 'pt_BR' base pode não estar instalada),
        # exibe uma mensagem de erro no terminal.
        # Finalmente, tenta usar a localidade padrão do sistema operacional.
        locale.setlocale(locale.LC_ALL, '')

def salvar_produto(entry_nome_produto, entry_descricao_produto, entry_categoria, #já conferido
                   combo_tipo_codigo_barras, entry_codigo_barras,
                   entry_preco_custo, entry_preco_venda,
                   entry_estoque_atual, entry_estoque_minimo,
                   entry_unidade, entry_sku, entry_fornecedor,
                   entry_margem_lucro,
                   lbl_erro_nome_produto, lbl_erro_descricao_produto,
                   lbl_erro_categoria, lbl_erro_codigo_barras,
                   lbl_erro_preco_custo, lbl_erro_preco_venda,
                   lbl_erro_estoque_atual, lbl_erro_estoque_minimo,
                   lbl_erro_unidade, lbl_erro_sku, lbl_erro_fornecedor,
                   lbl_erro_margem_lucro, limpar_campos_produtos):
    """
    Salva os dados de um novo produto no banco de dados 'banco_de_dados.db'.
    Realiza a validação dos campos antes de inserir os dados.
    """
    # Obtém os valores dos campos de entrada e remove espaços em branco.
    nome = entry_nome_produto.get().strip()
    descricao = entry_descricao_produto.get().strip()
    categoria = entry_categoria.get().strip()
    tipo_codigo_barras = combo_tipo_codigo_barras.get()
    codigo_barras = entry_codigo_barras.get().strip()
    unidade = entry_unidade.get().strip()
    sku = entry_sku.get().strip()
    fornecedor = entry_fornecedor.get().strip()

    # Tenta converter os campos numéricos para o tipo correto, tratando vírgulas e pontos.
    preco_custo_str = entry_preco_custo.get().replace('R$', '').strip().replace('.', '').replace(',', '.') if entry_preco_custo.get() else '0.00'
    preco_venda_str = entry_preco_venda.get().replace('R$', '').strip().replace('.', '').replace(',', '.') if entry_preco_venda.get() else '0.00'
    margem_lucro_str = entry_margem_lucro.get().replace('%', '').strip().replace('.', '').replace(',', '.') if entry_margem_lucro.get() else '0.00'

    try:
        preco_custo = float(preco_custo_str)
        preco_venda = float(preco_venda_str)
        margem_lucro = float(margem_lucro_str)
        estoque_atual = int(entry_estoque_atual.get()) if entry_estoque_atual.get().isdigit() else 0
        estoque_minimo = int(entry_estoque_minimo.get()) if entry_estoque_minimo.get().isdigit() else 0
    except ValueError:
        messagebox.showerror("Erro de Conversão", "Por favor, insira valores numéricos válidos para preço, margem e estoque.")
        return

    # --- Validação dos campos ---
    erros = False
    if not nome:
        lbl_erro_nome_produto.config(text="Nome do produto é obrigatório.")
        erros = True
    else:
        lbl_erro_nome_produto.config(text="")

    if not descricao:
        lbl_erro_descricao_produto.config(text="Descrição do produto é obrigatória.")
        erros = True
    else:
        lbl_erro_descricao_produto.config(text="")

    if not categoria:
        lbl_erro_categoria.config(text="Categoria do produto é obrigatória.")
        erros = True
    else:
        lbl_erro_categoria.config(text="")

    if preco_custo < 0:
        lbl_erro_preco_custo.config(text="Preço de custo inválido.")
        erros = True
    else:
        lbl_erro_preco_custo.config(text="")

    if preco_venda < 0:
        lbl_erro_preco_venda.config(text="Preço de venda inválido.")
        erros = True
    else:
        lbl_erro_preco_venda.config(text="")

    if estoque_atual < 0:
        lbl_erro_estoque_atual.config(text="Estoque atual inválido.")
        erros = True
    else:
        lbl_erro_estoque_atual.config(text="")

    if estoque_minimo < 0:
        lbl_erro_estoque_minimo.config(text="Estoque mínimo inválido.")
        erros = True
    else:
        lbl_erro_estoque_minimo.config(text="")

    if not unidade:
        lbl_erro_unidade.config(text="Unidade de medida é obrigatória.")
        erros = True
    else:
        lbl_erro_unidade.config(text="")

    lbl_erro_sku.config(text="") # SKU não é obrigatório
    lbl_erro_fornecedor.config(text="") # Fornecedor não é obrigatório

    if margem_lucro < 0:
        lbl_erro_margem_lucro.config(text="Margem de lucro inválida.")
        erros = True
    else:
        lbl_erro_margem_lucro.config(text="")

    if erros:
        return

    # --- Conectar e salvar no banco de dados ---
    try:
        # Estabelece a conexão com o banco de dados 'banco_de_dados.db'.
        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        # Executa a query SQL para inserir os dados do novo produto na tabela 'produtos'.
        cursor.execute("""
            INSERT INTO produtos (nome, descricao, categoria, tipo_codigo_barras, codigo_barras,
                                 preco_custo, preco_venda, estoque, unidade, sku,
                                 fornecedor, margem_lucro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, descricao, categoria, tipo_codigo_barras, codigo_barras,
              preco_custo, preco_venda, estoque_atual, unidade, sku,
              fornecedor, margem_lucro))

        # Confirma as alterações no banco de dados.
        conn.commit()
        # Fecha a conexão com o banco de dados.
        conn.close()
        # Exibe uma mensagem de sucesso para o usuário.
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
        # Chama a função para limpar os campos do formulário após o sucesso.
        limpar_campos_produtos(entry_nome_produto, entry_descricao_produto, entry_categoria,
                               entry_codigo_barras,
                               entry_preco_custo, entry_preco_venda,
                               entry_estoque_atual,
                               entry_unidade, entry_sku, entry_fornecedor, entry_margem_lucro,
                               lbl_erro_nome_produto, lbl_erro_descricao_produto,
                               lbl_erro_categoria, lbl_erro_codigo_barras,
                               lbl_erro_preco_custo, lbl_erro_preco_venda,
                               lbl_erro_estoque_atual,
                               lbl_erro_unidade, lbl_erro_sku, lbl_erro_fornecedor,
                               lbl_erro_margem_lucro)

    except sqlite3.Error as e:
        # Se ocorrer algum erro ao interagir com o banco de dados, exibe uma mensagem de erro.
        messagebox.showerror("Erro no Banco de Dados", f"Erro ao salvar o produto: {e}")

# Você precisará chamar esta função criar_tabela_produtos() em algum lugar
# na inicialização do seu programa para garantir que a tabela exista.
# Por exemplo, logo após a definição da função ou dentro da sua função
# de inicialização da janela principal.

# Exemplo de chamada (coloque isso no seu arquivo principal):
# criar_tabela_produtos()
# Você também precisará criar a função limpar_campos_produtos
def criar_tabela_produtos(): #já conferido
    """
    Cria a tabela 'produtos' no banco de dados 'banco_de_dados.db'
    se ela ainda não existir.
    """
    # Estabelece uma conexão com o banco de dados SQLite chamado 'banco_de_dados.db'.
    # Se o arquivo não existir, ele será criado.
    conn = sqlite3.connect('banco_de_dados.db')
    # Cria um objeto cursor para executar comandos SQL.
    cursor = conn.cursor()
    # Executa o comando SQL para criar a tabela 'produtos' com as seguintes colunas:
    # - id: INTEGER (chave primária, auto-incrementável)
    # - nome: TEXT (obrigatório)
    # - descricao: TEXT (obrigatório)
    # - categoria: TEXT (obrigatório)
    # - tipo_codigo_barras: TEXT (opcional)
    # - codigo_barras: TEXT (opcional)
    # - preco_custo: REAL (obrigatório)
    # - preco_venda: REAL (obrigatório)
    # - estoque: INTEGER (obrigatório)
    # - unidade: TEXT (opcional)
    # - sku: TEXT (opcional)
    # - fornecedor: TEXT (opcional)
    # - margem_lucro: REAL (opcional)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo_codigo_barras TEXT,
            codigo_barras TEXT,
            preco_custo REAL NOT NULL,
            preco_venda REAL NOT NULL,
            estoque INTEGER NOT NULL,
            unidade TEXT,
            sku TEXT,
            fornecedor TEXT,
            margem_lucro REAL
        )
    """)
    # Confirma as alterações no banco de dados.
    conn.commit()
    # Fecha a conexão com o banco de dados.
    conn.close()

def criar_tabela_tecnicos():
    """
    Cria a tabela 'tecnicos' no banco de dados 'banco_de_dados.db' (ou o cria se não existir).
    """
    try:
        # Conecta ao banco de dados (cria o arquivo se não existir)
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        # Cria a tabela 'tecnicos' se ela não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                cep TEXT,
                rua TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                telefone TEXT,
                email TEXT,
                funcao TEXT
            );
        """)
        print("Tabela 'tecnicos' criada com sucesso.")

        # Commita as alterações e fecha a conexão
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'tecnicos': {e}")

def limpar_campos_produtos(): #já conferido
    """
    Limpa os campos de entrada e as mensagens de erro na aba de produtos.
    Utiliza variáveis globais para acessar os widgets.
    """
    # Colete todos os seus Entry e Combobox da aba de produtos
    global entry_nome_produto, entry_descricao_produto, entry_categoria, combo_tipo_codigo_barras, entry_codigo_barras
    global entry_preco_custo, entry_preco_venda, entry_estoque_atual, entry_estoque_minimo, entry_unidade, entry_sku, entry_fornecedor, entry_margem_lucro
    global lbl_erro_nome_produto, lbl_erro_descricao_produto, lbl_erro_categoria, lbl_erro_codigo_barras
    global lbl_erro_preco_custo, lbl_erro_preco_venda, lbl_erro_estoque_atual, lbl_erro_estoque_minimo, lbl_erro_unidade, lbl_erro_sku, lbl_erro_fornecedor, lbl_erro_margem_lucro

    # Limpa o texto de cada campo de entrada (Entry).
    entry_nome_produto.delete(0, tk.END)
    entry_descricao_produto.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    # Define o valor do Combobox para "Outro".
    combo_tipo_codigo_barras.set("Outro")
    entry_codigo_barras.delete(0, tk.END)
    entry_preco_custo.delete(0, tk.END)
    entry_preco_venda.delete(0, tk.END)
    entry_estoque_atual.delete(0, tk.END)
    entry_estoque_minimo.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    entry_sku.delete(0, tk.END)
    entry_fornecedor.delete(0, tk.END)
    entry_margem_lucro.delete(0, tk.END)

    # Limpa o texto de cada label de erro, removendo qualquer mensagem exibida.
    lbl_erro_nome_produto.config(text="")
    lbl_erro_descricao_produto.config(text="")
    lbl_erro_categoria.config(text="")
    lbl_erro_codigo_barras.config(text="")
    lbl_erro_preco_custo.config(text="")
    lbl_erro_preco_venda.config(text="")
    lbl_erro_estoque_atual.config(text="")
    lbl_erro_estoque_minimo.config(text="")
    lbl_erro_unidade.config(text="")
    lbl_erro_sku.config(text="")
    lbl_erro_fornecedor.config(text="")
    lbl_erro_margem_lucro.config(text="")

def criar_aba_produtos(notebook, salvar_produto, limpar_campos_produtos, formatar_para_real, formatar_para_porcentagem, calcular_preco_venda): #já conferido
    """
    Cria a aba de produtos dentro do notebook principal.
    Organiza os widgets para entrada de dados de produtos e botões de ação.
    """
    # 1. Criar o Frame principal da aba de produtos
    aba_produtos = ttk.Frame(notebook)
    aba_produtos.columnconfigure(0, weight=1) # Permite que a coluna principal se expanda com a janela

    # 2. Frame para Informações Gerais
    frame_geral = ttk.LabelFrame(aba_produtos, text="Informações Gerais")
    frame_geral.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    frame_geral.columnconfigure(1, weight=1) # Permite que a coluna das entradas se expanda
    frame_geral.columnconfigure(3, weight=1) # Permite que a coluna do combo/entrada se expanda

    # Label e Entry para o nome do produto
    lbl_nome_produto = ttk.Label(frame_geral, text="Nome do Produto:")
    entry_nome_produto = ttk.Entry(frame_geral)
    lbl_erro_nome_produto = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de nome
    lbl_nome_produto.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entry_nome_produto.grid(row=0, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_nome_produto.grid(row=0, column=4, sticky='w', padx=5)

    # Label e Entry para a descrição do produto
    lbl_descricao_produto = ttk.Label(frame_geral, text="Descrição:")
    entry_descricao_produto = ttk.Entry(frame_geral)
    lbl_erro_descricao_produto = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de descrição
    lbl_descricao_produto.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entry_descricao_produto.grid(row=1, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_descricao_produto.grid(row=1, column=4, sticky='w', padx=5)

    # Label e Entry para a categoria do produto, e Label/Combobox para o tipo de código de barras
    lbl_categoria = ttk.Label(frame_geral, text="Categoria:")
    entry_categoria = ttk.Entry(frame_geral)
    lbl_erro_categoria = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de categoria
    lbl_categoria.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    entry_categoria.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
    lbl_tipo_codigo_barras = ttk.Label(frame_geral, text="Tipo de Código de Barras:")
    tipos_codigo_barras = ["EAN-13", "UPC-A", "Code 128", "QR Code", "Outro"]
    combo_tipo_codigo_barras = ttk.Combobox(frame_geral, values=tipos_codigo_barras, state="readonly")
    combo_tipo_codigo_barras.set("Outro") # Define um valor padrão para o Combobox
    lbl_tipo_codigo_barras.grid(row=2, column=2, sticky='w', padx=5, pady=5)
    combo_tipo_codigo_barras.grid(row=2, column=3, sticky='ew', padx=5, pady=5)
    lbl_erro_categoria.grid(row=2, column=4, sticky='w', padx=5)

    # Label e Entry para o código de barras do produto
    lbl_codigo_barras = ttk.Label(frame_geral, text="Código de Barras:")
    lbl_codigo_barras.grid(row=3, column=0, sticky='w', padx=5, pady=5)
    entry_codigo_barras = ttk.Entry(frame_geral)
    lbl_erro_codigo_barras = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de código de barras
    entry_codigo_barras.grid(row=3, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_codigo_barras.grid(row=3, column=4, sticky='w', padx=5)

    # Label e Entry para a unidade de medida do produto
    lbl_unidade = ttk.Label(frame_geral, text="Unidade de Medida:")
    entry_unidade = ttk.Entry(frame_geral)
    lbl_erro_unidade = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de unidade
    lbl_unidade.grid(row=4, column=0, sticky='w', padx=5, pady=5)
    entry_unidade.grid(row=4, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_unidade.grid(row=4, column=4, sticky='w', padx=5)

    # Label e Entry para o SKU do produto
    lbl_sku = ttk.Label(frame_geral, text="SKU:")
    entry_sku = ttk.Entry(frame_geral)
    lbl_erro_sku = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de SKU
    lbl_sku.grid(row=5, column=0, sticky='w', padx=5, pady=5)
    entry_sku.grid(row=5, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_sku.grid(row=5, column=4, sticky='w', padx=5)

    # Label e Entry para o fornecedor do produto
    lbl_fornecedor = ttk.Label(frame_geral, text="Fornecedor:")
    entry_fornecedor = ttk.Entry(frame_geral)
    lbl_erro_fornecedor = ttk.Label(frame_geral, text="", foreground="red") # Label para exibir erros de fornecedor
    lbl_fornecedor.grid(row=6, column=0, sticky='w', padx=5, pady=5)
    entry_fornecedor.grid(row=6, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_fornecedor.grid(row=6, column=4, sticky='w', padx=5)

    # 3. Frame para Preço e Estoque
    frame_preco_estoque = ttk.LabelFrame(aba_produtos, text="Preço e Estoque")
    frame_preco_estoque.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
    frame_preco_estoque.columnconfigure(1, weight=1) # Permite que a coluna das entradas se expanda

    # --- Preço de Custo ---
    lbl_preco_custo = ttk.Label(frame_preco_estoque, text="Preço de Custo:")
    entry_preco_custo = ttk.Entry(frame_preco_estoque)
    lbl_erro_preco_custo = ttk.Label(frame_preco_estoque, text="", foreground="red") # Label para exibir erros de preço de custo
    lbl_preco_custo.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entry_preco_custo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_preco_custo.grid(row=0, column=2, sticky='w', padx=5)
    # Bind para formatar para real, calcular preço de venda e margem ao perder o foco
    entry_preco_custo.bind("<FocusOut>", lambda event: (
        formatar_para_real(event, entry_preco_custo),
        calcular_preco_venda(event, entry_preco_custo, entry_margem_lucro, entry_preco_venda),
        calcular_margem_lucro(event, entry_preco_custo, entry_preco_venda, entry_margem_lucro) # Assumindo que calcular_margem_lucro existe
    ))

    # --- Margem de Lucro ---
    lbl_margem_lucro = ttk.Label(frame_preco_estoque, text="Margem de Lucro (%):")
    entry_margem_lucro = ttk.Entry(frame_preco_estoque)
    lbl_erro_margem_lucro = ttk.Label(frame_preco_estoque, text="", foreground="red") # Label para exibir erros de margem de lucro
    lbl_margem_lucro.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entry_margem_lucro.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_margem_lucro.grid(row=1, column=2, sticky='w', padx=5)
    # Bind para formatar para porcentagem ao digitar e calcular preço de venda ao perder o foco
    entry_margem_lucro.bind("<KeyRelease>", formatar_para_porcentagem)
    entry_margem_lucro.bind("<FocusOut>", lambda event: calcular_preco_venda(event, entry_preco_custo, entry_margem_lucro, entry_preco_venda))

    # --- Preço de Venda ---
    lbl_preco_venda = ttk.Label(frame_preco_estoque, text="Preço de Venda:")
    entry_preco_venda = ttk.Entry(frame_preco_estoque, state='readonly') # Define como somente leitura inicialmente
    lbl_erro_preco_venda = ttk.Label(frame_preco_estoque, text="", foreground="red") # Label para exibir erros de preço de venda
    lbl_preco_venda.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    entry_preco_venda.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_preco_venda.grid(row=2, column=2, sticky='w', padx=5)
    # A formatação para real será aplicada pela função calcular_preco_venda

    # --- Estoque Atual ---
    lbl_estoque_atual = ttk.Label(frame_preco_estoque, text="Estoque Atual:")
    entry_estoque_atual = ttk.Entry(frame_preco_estoque)
    lbl_erro_estoque_atual = ttk.Label(frame_preco_estoque, text="", foreground="red") # Label para exibir erros de estoque atual
    lbl_estoque_atual.grid(row=4, column=0, sticky='w', padx=5, pady=5) # Alterado de row=3 para evitar sobreposição
    entry_estoque_atual.grid(row=4, column=1, sticky='ew', padx=5, pady=5) # Alterado de row=3
    lbl_erro_estoque_atual.grid(row=4, column=2, sticky='w', padx=5) # Alterado de row=3
    entry_estoque_atual.bind("<KeyRelease>", lambda event: lbl_erro_estoque_atual.config(text="")) # Limpa erro ao digitar

    # --- Estoque Mínimo ---
    lbl_estoque_minimo = ttk.Label(frame_preco_estoque, text="Estoque Mínimo:")
    entry_estoque_minimo = ttk.Entry(frame_preco_estoque)
    lbl_erro_estoque_minimo = ttk.Label(frame_preco_estoque, text="", foreground="red") # Label para exibir erros de estoque mínimo
    lbl_estoque_minimo.grid(row=5, column=0, sticky='w', padx=5, pady=5) # Alterado de row=4
    entry_estoque_minimo.grid(row=5, column=1, sticky='ew', padx=5, pady=5) # Alterado de row=4
    lbl_erro_estoque_minimo.grid(row=5, column=2, sticky='w', padx=5) # Alterado de row=4
    entry_estoque_minimo.bind("<KeyRelease>", lambda event: lbl_erro_estoque_minimo.config(text="")) # Limpa erro ao digitar

    # 4. Botões na aba principal
    frame_botoes_produtos = ttk.Frame(aba_produtos)
    frame_botoes_produtos.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
    frame_botoes_produtos.columnconfigure(0, weight=1)
    frame_botoes_produtos.columnconfigure(1, weight=1)
    frame_botoes_produtos.columnconfigure(2, weight=1)

    # Botão Salvar Produto: chama a função salvar_produto com os argumentos corretos
    btn_salvar_produto = ttk.Button(frame_botoes_produtos, text="Salvar Produto", command=lambda: salvar_produto(
        entry_nome_produto, entry_descricao_produto, entry_categoria, combo_tipo_codigo_barras, entry_codigo_barras,
        entry_preco_custo, entry_preco_venda, entry_estoque_atual, entry_estoque_minimo, entry_unidade, entry_sku, entry_fornecedor, entry_margem_lucro,
        lbl_erro_nome_produto, lbl_erro_descricao_produto, lbl_erro_categoria, lbl_erro_codigo_barras,
        lbl_erro_preco_custo, lbl_erro_preco_venda, lbl_erro_estoque_atual, lbl_erro_estoque_minimo,
        lbl_erro_unidade, lbl_erro_sku, lbl_erro_fornecedor, lbl_erro_margem_lucro,
        limpar_campos_produtos
    ))
    btn_salvar_produto.grid(row=0, column=2, sticky='ew', padx=5, pady=5)

    # Botão Novo Produto: chama a função limpar_campos_produtos para resetar o formulário
    btn_novo_produto = ttk.Button(frame_botoes_produtos, text="Novo Produto", command=lambda: limpar_campos_produtos())
    btn_novo_produto.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    # Botão Limpar: também chama a função limpar_campos_produtos para resetar o formulário
    btn_limpar_produto = ttk.Button(frame_botoes_produtos, text="Limpar", command=lambda: limpar_campos_produtos())
    btn_limpar_produto.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    # 5. Adicionar o frame da aba de produtos ao notebook
    notebook.add(aba_produtos, text="Produtos")

def criar_aba_servicos(notebook):
    aba_servicos = ttk.Frame(notebook)
    notebook.add(aba_servicos, text="Serviços")

    frame_cadastro_servico = ttk.LabelFrame(aba_servicos, text="Cadastrar Novo Serviço")
    frame_cadastro_servico.pack(padx=10, pady=10, fill='x', expand=False)

    # Nome do Serviço
    lbl_nome_servico = ttk.Label(frame_cadastro_servico, text="Nome*:")
    entry_nome_servico = ttk.Entry(frame_cadastro_servico)
    lbl_nome_servico.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nome_servico.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    # Preço do Serviço
    lbl_preco_servico = ttk.Label(frame_cadastro_servico, text="Preço*:")
    entry_preco_servico = ttk.Entry(frame_cadastro_servico)
    lbl_preco_servico.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_preco_servico.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    entry_preco_servico.bind("<FocusOut>", lambda event: formatar_para_real(event, entry_preco_servico))

    # Descrição do Serviço
    lbl_descricao_servico = ttk.Label(frame_cadastro_servico, text="Descrição:")
    entry_descricao_servico = ttk.Entry(frame_cadastro_servico)
    lbl_descricao_servico.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_descricao_servico.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    # Botão Salvar Serviço

    btn_salvar_servico = ttk.Button(
        frame_cadastro_servico,
        text="Salvar Serviço",
        command=lambda: salvar_servico_no_banco(
            entry_nome_servico,
            entry_preco_servico,
            entry_descricao_servico,
            btn_salvar_servico,
            exibir_servicos  # Passe a função exibir_servicos como argumento
        )
    )
    btn_salvar_servico.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='ew')


    # --- Área de Busca ---
    frame_busca_servicos = ttk.Frame(aba_servicos)
    frame_busca_servicos.pack(padx=10, pady=5, fill='x', expand=False)

    lbl_buscar_servico = ttk.Label(frame_busca_servicos, text="Buscar Serviço:")
    lbl_buscar_servico.pack(side='left', padx=5)

    entry_buscar_servico = ttk.Entry(frame_busca_servicos)
    entry_buscar_servico.pack(side='left', padx=5, fill='x', expand=True)

    def buscar_servicos():
        termo_busca = entry_buscar_servico.get().strip().lower()

        # Limpar a Treeview
        for item in tree_servicos.get_children():
            tree_servicos.delete(item)

        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, preco, descricao FROM servicos WHERE LOWER(nome) LIKE ?", ('%' + termo_busca + '%',))
            servicos_encontrados = cursor.fetchall()

            for servico in servicos_encontrados:
                tree_servicos.insert("", "end", values=servico)

        except sqlite3.Error as e:
            messagebox.showerror("Erro na Busca", f"Ocorreu um erro durante a busca: {e}")
        finally:
            if conn:
                conn.close()

    btn_buscar_servico = ttk.Button(frame_busca_servicos, text="Buscar", command=buscar_servicos)
    btn_buscar_servico.pack(side='left', padx=5)

    # --- Treeview para listar os serviços ---
    frame_lista_servicos = ttk.LabelFrame(aba_servicos, text="Serviços Cadastrados")
    frame_lista_servicos.pack(padx=10, pady=10, fill='both', expand=True)

    colunas = ("ID", "Nome", "Preço", "Descrição")
    tree_servicos = ttk.Treeview(frame_lista_servicos, columns=colunas, show="headings")

    for coluna in colunas:
        tree_servicos.heading(coluna, text=coluna)
        tree_servicos.column(coluna, width=100, anchor="center")

    tree_servicos.pack(fill='both', expand=True)

    global id_servico_selecionado
    id_servico_selecionado = None
    global modo_edicao
    modo_edicao = False
    global id_edicao
    id_edicao = None

    def selecionar_servico():
        global id_servico_selecionado
        item_selecionado = tree_servicos.selection()
        if item_selecionado:
            id_servico_selecionado = tree_servicos.item(item_selecionado[0])['values'][0]
        else:
            id_servico_selecionado = None

    def excluir_servico():
        global id_servico_selecionado
        if id_servico_selecionado is None:
            messagebox.showerror("Erro", "Selecione um serviço para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este serviço?"):
            try:
                conn = sqlite3.connect("banco_de_dados.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM servicos WHERE id=?", (id_servico_selecionado,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
                exibir_servicos() # Atualizar a lista após a exclusão
                id_servico_selecionado = None # Resetar a seleção
            except sqlite3.Error as e:
                messagebox.showerror("Erro ao Excluir", f"Ocorreu um erro ao excluir o serviço: {e}")
            finally:
                if conn:
                    conn.close()

    def editar_servico():
        global id_servico_selecionado
        if id_servico_selecionado is None:
            messagebox.showerror("Erro", "Selecione um serviço para editar.")
            return

        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome, preco, descricao FROM servicos WHERE id=?", (id_servico_selecionado,))
            servico = cursor.fetchone()
            if servico:
                entry_nome_servico.delete(0, tk.END)
                entry_nome_servico.insert(0, servico[0])
                entry_preco_servico.delete(0, tk.END)
                entry_preco_servico.insert(0, f"R$ {servico[1]:.2f}".replace('.', ','))
                entry_descricao_servico.delete(0, tk.END)
                entry_descricao_servico.insert(0, servico[2] or "") # Insere string vazia se a descrição for None

                # *** Próximo passo: Sinalizar que estamos em modo de edição ***
                global modo_edicao
                modo_edicao = True
                global id_edicao
                id_edicao = id_servico_selecionado
                btn_salvar_servico.config(text="Atualizar Serviço") # Mudar o texto do botão salvar
            else:
                messagebox.showerror("Erro", "Serviço não encontrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro ao Buscar Serviço", f"Ocorreu um erro ao buscar os dados do serviço: {e}")
        finally:
            if conn:
                conn.close()

    tree_servicos.bind("<ButtonRelease-1>", lambda event: selecionar_servico())

    # --- Botões Editar e Excluir ---
    frame_acoes_servicos = ttk.Frame(aba_servicos)
    frame_acoes_servicos.pack(padx=10, pady=5, fill='x', expand=False)

    btn_editar_servico = ttk.Button(frame_acoes_servicos, text="Editar Serviço", command=editar_servico)
    btn_editar_servico.pack(side='left', padx=5)

    btn_excluir_servico = ttk.Button(frame_acoes_servicos, text="Excluir Serviço", command=excluir_servico)
    btn_excluir_servico.pack(side='left', padx=5)

    def exibir_servicos():
       for item in tree_servicos.get_children():
        tree_servicos.delete(item)

       try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, descricao FROM servicos")
        servicos = cursor.fetchall()

        for servico in servicos:
            preco_formatado = f"R$ {servico[2]:.2f}".replace('.', ',') # Formata o preço
            tree_servicos.insert("", "end", values=(servico[0], servico[1], preco_formatado, servico[3]))

       except sqlite3.Error as e:
        messagebox.showerror("Erro ao Carregar Serviços", f"Ocorreu um erro ao carregar os serviços: {e}")
       finally:
        if conn:
            conn.close()

    exibir_servicos() # Carregar os serviços inicialmente

    def buscar_servicos(): # <--- MOVI A DEFINIÇÃO PARA ANTES DO BOTÃO
        termo_busca = entry_buscar_servico.get().strip().lower()

        # Limpar a Treeview
        for item in tree_servicos.get_children():
            tree_servicos.delete(item)

        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, preco, descricao FROM servicos WHERE LOWER(nome) LIKE ?", ('%' + termo_busca + '%',))
            servicos_encontrados = cursor.fetchall()

            for servico in servicos_encontrados:
                tree_servicos.insert("", "end", values=servico)

        except sqlite3.Error as e:
            messagebox.showerror("Erro na Busca", f"Ocorreu um erro durante a busca: {e}")
        finally:
            if conn:
                conn.close()

    return aba_servicos

def formatar_para_real(event, widget): #já conferido
    """
    Formata o texto de um widget Entry para o formato de moeda Real (R$).

    Esta função é projetada para ser usada como um callback para eventos
    de teclado (como KeyRelease) ou perda de foco (FocusOut) em widgets
    Entry onde o usuário digita valores monetários. Ela remove a
    formatação existente, tenta converter o texto para um número float
    e, se bem-sucedido, re-insere o valor formatado como "R$ XX,YY".

    Args:
        event: O objeto de evento Tkinter que disparou a função.
               Embora esteja presente na assinatura, esta função
               geralmente não usa informações específicas do evento.
        widget: O widget Entry que contém o texto a ser formatado.
    """
    # 1. Remove a formatação existente e normaliza separadores decimais:
    #    - Remove o prefixo "R$" (se existir).
    #    - Substitui vírgulas por pontos para permitir a conversão para float.
    texto = widget.get().replace("R$", "").replace(",", ".").strip()

    # 2. Verifica se há algum texto para formatar:
    if texto:
        try:
            # 3. Tenta converter o texto para um número float:
            valor = float(texto)

            # 4. Limpa o conteúdo atual do widget Entry:
            widget.delete(0, tk.END)

            # 5. Formata o valor como "R$ XX,YY" e insere de volta no widget:
            #    - "{:.2f}" formata o float para duas casas decimais.
            #    - .replace(".", ",") substitui o ponto decimal pela vírgula para o padrão brasileiro.
            #    - f"R$ ..." cria a string final com o prefixo "R$".
            widget.insert(0, f"R$ {valor:.2f}".replace(".", ","))

        except ValueError:
            # 6. Se a conversão para float falhar (o texto não é um número válido),
            #    a função tenta remover caracteres inválidos para manter apenas números
            #    e o separador decimal ponto. Isso melhora a experiência do usuário
            #    ao digitar valores.
            novo_texto = ''.join(char for char in texto if char.isdigit() or char == '.')
            widget.delete(0, tk.END)
            widget.insert(0, novo_texto)

# --- Variáveis globais ---
# Variáveis da aba de Serviços
entry_nome_cliente = None
entry_cpf_cliente = None
entry_telefone_cliente = None
entry_email_cliente = None
entry_endereco_cliente = None
entry_numero_os = None
entry_data_abertura = None
entry_data_previsao = None
entry_data_execucao = None
entry_data_fechamento = None
entry_tecnico_responsavel = None
entry_descricao_problema = None
entry_servico_executado = None
entry_pecas_utilizadas = None
entry_valor_total = None
entry_observacoes = None
tree_servicos = None
indice_editando_servico = None
btn_salvar_servico = None # Declarando globalmente



# --- Funções do Banco de Dados ---
def criar_tabelas():
    """Cria as tabelas 'tecnicos' e 'servicos' no banco de dados, se elas não existirem."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                especialidade TEXT NOT NULL,
                cep TEXT NOT NULL,
                rua TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL,
                funcao TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente TEXT NOT NULL,
                cpf_cliente TEXT UNIQUE NOT NULL,
                telefone_cliente TEXT NOT NULL,
                email_cliente TEXT NOT NULL,
                endereco_cliente TEXT NOT NULL,
                numero_os TEXT NOT NULL,
                data_abertura TEXT NOT NULL,
                data_previsao TEXT NOT NULL,
                data_execucao TEXT,
                data_fechamento TEXT,
                tecnico_responsavel INTEGER,
                descricao_problema TEXT NOT NULL,
                servico_executado TEXT,
                pecas_utilizadas TEXT,
                valor_total REAL,
                observacoes TEXT,
                FOREIGN KEY (tecnico_responsavel) REFERENCES tecnicos(id)
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela: {e}")



# --- Funções da aba de Serviços ---
def salvar_servico():
    """Salva os dados do serviço no banco de dados."""
    nome_cliente = entry_nome_cliente.get()
    cpf_cliente = entry_cpf_cliente.get()
    telefone_cliente = entry_telefone_cliente.get()
    email_cliente = entry_email_cliente.get()
    endereco_cliente = entry_endereco_cliente.get()
    numero_os = entry_numero_os.get()
    data_abertura = entry_data_abertura.get()
    data_previsao = entry_data_previsao.get()
    data_execucao = entry_data_execucao.get()
    data_fechamento = entry_data_fechamento.get()
    tecnico_responsavel = entry_tecnico_responsavel.get()  # Aqui precisa pegar o ID do técnico
    descricao_problema = entry_descricao_problema.get()
    servico_executado = entry_servico_executado.get()
    pecas_utilizadas = entry_pecas_utilizadas.get()
    valor_total = entry_valor_total.get()
    observacoes = entry_observacoes.get()

    if not all([nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente, numero_os, data_abertura, data_previsao, tecnico_responsavel, descricao_problema]):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
        return

    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        # Verifica se o CPF do cliente já existe
        cursor.execute("SELECT id FROM servicos WHERE cpf_cliente=?", (cpf_cliente,))
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showerror("Erro", "CPF do Cliente já cadastrado.")
            conn.close()
            return

       # Converte o nome do técnico responsável para o ID do técnico
        cursor.execute("SELECT id FROM tecnicos WHERE nome=?", (tecnico_responsavel,))
        tecnico_id = cursor.fetchone()
        if tecnico_id is None:
            messagebox.showerror("Erro", "Técnico Responsável não encontrado.")
            conn.close()
            return
        tecnico_responsavel_id = tecnico_id[0]

        cursor.execute("""
            INSERT INTO servicos (nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente, numero_os, data_abertura, data_previsao, data_execucao, data_fechamento, tecnico_responsavel, descricao_problema, servico_executado, pecas_utilizadas, valor_total, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente, numero_os, data_abertura, data_previsao, data_execucao, data_fechamento, tecnico_responsavel_id, descricao_problema, servico_executado, pecas_utilizadas, valor_total, observacoes))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        atualizar_lista_servicos()
        limpar_campos_servico()

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar serviço: {e}")

def limpar_campos_servico():
    """Limpa os campos do formulário de serviço."""
    entry_nome_cliente.delete(0, tk.END)
    entry_cpf_cliente.delete(0, tk.END)
    entry_telefone_cliente.delete(0, tk.END)
    entry_email_cliente.delete(0, tk.END)
    entry_endereco_cliente.delete(0, tk.END)
    entry_numero_os.delete(0, tk.END)
    entry_data_abertura.delete(0, tk.END)
    entry_data_previsao.delete(0, tk.END)
    entry_data_execucao.delete(0, tk.END)
    entry_data_fechamento.delete(0, tk.END)
    entry_tecnico_responsavel.delete(0, tk.END)
    entry_descricao_problema.delete(0, tk.END)
    entry_servico_executado.delete(0, tk.END)
    entry_pecas_utilizadas.delete(0, tk.END)
    entry_valor_total.delete(0, tk.END)
    entry_observacoes.delete(0, tk.END)
    btn_salvar_servico.config(text="Salvar", command=salvar_servico)

def excluir_servico():
    """Exclui o serviço selecionado do banco de dados."""
    selecionado = tree_servicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_servico = tree_servicos.item(selecionado[0], 'values')[0]
            cursor.execute("DELETE FROM servicos WHERE id=?", (id_servico,))
            conn.commit()
            conn.close()
            atualizar_lista_servicos()
            messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir serviço: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um serviço para excluir.")

def editar_servico():
    """Edita o serviço selecionado do banco de dados."""
    selecionado = tree_servicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_servico = tree_servicos.item(selecionado[0], 'values')[0]
            cursor.execute("SELECT * FROM servicos WHERE id=?", (id_servico,))
            servico = cursor.fetchone()
            conn.close()

            if servico:
                entry_nome_cliente.delete(0, tk.END)
                entry_nome_cliente.insert(0, servico[1])
                entry_cpf_cliente.delete(0, tk.END)
                entry_cpf_cliente.insert(0, servico[2])
                entry_telefone_cliente.delete(0, tk.END)
                entry_telefone_cliente.insert(0, servico[3])
                entry_email_cliente.delete(0, tk.END)
                entry_email_cliente.insert(0, servico[4])
                entry_endereco_cliente.delete(0, tk.END)
                entry_endereco_cliente.insert(0, servico[5])
                entry_numero_os.delete(0, tk.END)
                entry_numero_os.insert(0, servico[6])
                entry_data_abertura.delete(0, tk.END)
                entry_data_abertura.insert(0, servico[7])
                entry_data_previsao.delete(0, tk.END)
                entry_data_previsao.insert(0, servico[8])
                entry_data_execucao.delete(0, tk.END)
                entry_data_execucao.insert(0, servico[9])
                entry_data_fechamento.delete(0, tk.END)
                entry_data_fechamento.insert(0, servico[10])
                entry_tecnico_responsavel.delete(0, tk.END)
                # Busca o nome do técnico pelo ID
                conn = sqlite3.connect("banco_de_dados.db")
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM tecnicos WHERE id=?", (servico[11],))
                nome_tecnico = cursor.fetchone()
                conn.close()
                if nome_tecnico:
                    entry_tecnico_responsavel.insert(0, nome_tecnico[0])

                entry_descricao_problema.delete(0, tk.END)
                entry_descricao_problema.insert(0, servico[12])
                entry_servico_executado.delete(0, tk.END)
                entry_servico_executado.insert(0, servico[13])
                entry_pecas_utilizadas.delete(0, tk.END)
                entry_pecas_utilizadas.insert(0, servico[14])
                entry_valor_total.delete(0, tk.END)
                entry_valor_total.insert(0, servico[15])
                entry_observacoes.delete(0, tk.END)
                entry_observacoes.insert(0, servico[16])

                global indice_editando_servico
                indice_editando_servico = id_servico
                btn_salvar_servico.config(text="Atualizar", command=atualizar_servico)
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao editar serviço: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um serviço para editar.")

def atualizar_servico():
    """Atualiza os dados do serviço no banco de dados."""
    global indice_editando_servico
    if indice_editando_servico:
        nome_cliente = entry_nome_cliente.get()
        cpf_cliente = entry_cpf_cliente.get()
        telefone_cliente = entry_telefone_cliente.get()
        email_cliente = entry_email_cliente.get()
        endereco_cliente = entry_endereco_cliente.get()
        numero_os = entry_numero_os.get()
        data_abertura = entry_data_abertura.get()
        data_previsao = entry_data_previsao.get()
        data_execucao = entry_data_execucao.get()
        data_fechamento = entry_data_fechamento.get()
        tecnico_responsavel = entry_tecnico_responsavel.get() # Precisa converter para ID
        descricao_problema = entry_descricao_problema.get()
        servico_executado = entry_servico_executado.get()
        pecas_utilizadas = entry_pecas_utilizadas.get()
        valor_total = entry_valor_total.get()
        observacoes = entry_observacoes.get()

        if not all([nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente, numero_os, data_abertura, data_previsao, tecnico_responsavel, descricao_problema]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()

             # Converte o nome do técnico responsável para o ID do técnico
            cursor.execute("SELECT id FROM tecnicos WHERE nome=?", (tecnico_responsavel,))
            tecnico_id = cursor.fetchone()
            if tecnico_id is None:
                messagebox.showerror("Erro", "Técnico Responsável não encontrado.")
                conn.close()
                return
            tecnico_responsavel_id = tecnico_id[0]

            cursor.execute("""
                UPDATE servicos SET 
                    nome_cliente=?, cpf_cliente=?, telefone_cliente=?, email_cliente=?, endereco_cliente=?,
                    numero_os=?, data_abertura=?, data_previsao=?, data_execucao=?, data_fechamento=?,
                    tecnico_responsavel=?, descricao_problema=?, servico_executado=?,
                    pecas_utilizadas=?, valor_total=?, observacoes=?
                WHERE id=?
            """, (nome_cliente, cpf_cliente, telefone_cliente, email_cliente, endereco_cliente, numero_os, data_abertura, data_previsao, data_execucao, data_fechamento, tecnico_responsavel_id, descricao_problema, servico_executado, pecas_utilizadas, valor_total, observacoes, indice_editando_servico))
            conn.commit()
            conn.close()
            atualizar_lista_servicos()
            limpar_campos_servico()
            btn_salvar_servico.config(text="Salvar", command=salvar_servico)
            indice_editando_servico = None
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar serviço: {e}")
    else:
        messagebox.showerror("Erro", "Nenhum serviço para atualizar.")

def atualizar_lista_servicos():
    """Atualiza a Treeview de serviços com os dados do banco de dados."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servicos")
        servicos = cursor.fetchall()
        conn.close()

        for item in tree_servicos.get_children():
            tree_servicos.delete(item)

        for servico in servicos:
            # Busca o nome do técnico responsável pelo ID
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM tecnicos WHERE id=?", (servico[11],))
            nome_tecnico = cursor.fetchone()
            conn.close()
            tecnico_nome = nome_tecnico[0] if nome_tecnico else "N/D"

            tree_servicos.insert("", tk.END, values=(servico[0], servico[1], servico[2], servico[3], servico[4], servico[5], servico[6], servico[7], servico[8], servico[9], tecnico_nome, servico[12], servico[13], servico[14], servico[15], servico[16]))
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao atualizar lista de serviços: {e}")

def buscar_cep_cliente():
    """Busca o CEP do cliente e preenche o campo de endereço."""
    cep = entry_endereco_cliente.get().replace('-', '').strip()
    if not cep or len(cep) != 8 or not cep.isdigit():
        messagebox.showerror("Erro", "CEP inválido.")
        return

    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "erro" in data:
            messagebox.showerror("Erro", "CEP não encontrado.")
        else:
            endereco = f"{data.get('logradouro', '')}, {data.get('bairro', '')}, {data.get('localidade', '')} - {data.get('uf', '')}"
            entry_endereco_cliente.delete(0, tk.END)
            entry_endereco_cliente.insert(0, endereco)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao buscar CEP: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Resposta inválida do servidor de CEP.")

def formatar_cpf_cliente(event):
    """Formata o CPF do cliente no formato XXX.XXX.XXX-XX."""
    texto = entry_cpf_cliente.get().replace('.', '').replace('-', '')
    novo_texto = ''
    i = 0
    for c in texto:
        if i == 3 or i == 6:
            novo_texto += '.'
        elif i == 9:
            novo_texto += '-'
        novo_texto += c
        i += 1
    entry_cpf_cliente.delete(0, tk.END)
    entry_cpf_cliente.insert(0, novo_texto)

def formatar_telefone_cliente(event):
    """Formata o telefone do cliente no formato (XX) XXXXX-XXXX."""
    texto = entry_telefone_cliente.get().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
    novo_texto = ''
    tamanho = len(texto)
    if tamanho > 0:
        novo_texto = '(' + texto[:2]
        if tamanho > 2:
            novo_texto += ') ' + texto[2:7]
        if tamanho > 7:
            novo_texto += '-' + texto[7:]
    entry_telefone_cliente.delete(0, tk.END)
    entry_telefone_cliente.insert(0, novo_texto)
    entry_telefone_cliente.icursor(tk.END)

def validar_data(data):
    """Valida se a data está no formato DD/MM/AAAA."""
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# --- Variáveis globais ---
# Variáveis da aba de Serviços
entry_nome_servico = None
entry_descricao_servico = None
entry_valor_servico = None
tree_servicos = None
indice_editando_servico = None
btn_salvar_servico = None

# --- Funções do Banco de Dados ---
def criar_tabela_servicos():
    """Cria a tabela 'servicos' no banco de dados, se ela não existir ou se a estrutura estiver incorreta."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        # Verifica se a tabela já existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servicos';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Verifica se a tabela tem as colunas corretas
            cursor.execute("PRAGMA table_info(servicos);")
            columns = cursor.fetchall()
            correct_columns = {'id', 'nome', 'descricao', 'valor'}
            existing_columns = {col[1] for col in columns}

            if existing_columns != correct_columns:
                # Recria a tabela se as colunas não estiverem corretas
                cursor.execute("DROP TABLE IF EXISTS servicos;")
                cursor.execute("""
                    CREATE TABLE servicos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT NOT NULL,
                        valor REAL NOT NULL
                    )
                """)
                conn.commit()
                messagebox.showinfo("Info", "Tabela 'servicos' recriada com a estrutura correta.")
        else:
            # Cria a tabela se não existir
            cursor.execute("""
                CREATE TABLE servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL
                )
            """)
            conn.commit()
            messagebox.showinfo("Info", "Tabela 'servicos' criada com sucesso.")
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela: {e}")

# --- Funções da aba de Serviços ---
def salvar_servico():
    """Salva os dados do serviço no banco de dados."""
    global indice_editando_servico
    nome = entry_nome_servico.get()
    descricao = entry_descricao_servico.get()
    valor = entry_valor_servico.get()

    if not nome or not descricao or not valor:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
        return

    # Remove a formatação de Real (R$) e tenta converter para float
    valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        valor_float = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Use o formato: 1000,00")
        return

    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        if indice_editando_servico:
            cursor.execute("UPDATE servicos SET nome=?, descricao=?, valor=? WHERE id=?", (nome, descricao, valor_float, indice_editando_servico))
            conn.commit()
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
            indice_editando_servico = None
            btn_salvar_servico.config(text="Salvar", command=salvar_servico)
        else:
            # Verifica se o nome do serviço já existe
            cursor.execute("SELECT id FROM servicos WHERE nome=?", (nome,))
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showerror("Erro", "Nome do Serviço já cadastrado.")
                conn.close()
                return
            cursor.execute("INSERT INTO servicos (nome, descricao, valor) VALUES (?, ?, ?)", (nome, descricao, valor_float))
            conn.commit()
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        conn.close()
        atualizar_lista_servicos()
        limpar_campos_servico()

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar serviço: {e}")

def limpar_campos_servico():
    """Limpa os campos do formulário de serviço."""
    entry_nome_servico.delete(0, tk.END)
    entry_descricao_servico.delete(0, tk.END)
    entry_valor_servico.delete(0, tk.END)
    btn_salvar_servico.config(text="Salvar", command=salvar_servico)
    global indice_editando_servico
    indice_editando_servico = None

def excluir_servico():
    """Exclui o serviço selecionado do banco de dados."""
    selecionado = tree_servicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_servico = tree_servicos.item(selecionado[0], 'values')[0]
            cursor.execute("DELETE FROM servicos WHERE id=?", (id_servico,))
            conn.commit()
            conn.close()
            atualizar_lista_servicos()
            messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir serviço: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um serviço para excluir.")

def editar_servico():
    """Edita o serviço selecionado do banco de dados."""
    global indice_editando_servico
    selecionado = tree_servicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_servico = tree_servicos.item(selecionado[0], 'values')[0]
            cursor.execute("SELECT * FROM servicos WHERE id=?", (id_servico,))
            servico = cursor.fetchone()
            conn.close()

            if servico:
                entry_nome_servico.delete(0, tk.END)
                entry_nome_servico.insert(0, servico[1])
                entry_descricao_servico.delete(0, tk.END)
                entry_descricao_servico.insert(0, servico[2])
                entry_valor_servico.delete(0, tk.END)
                entry_valor_servico.insert(0, f"R$ {servico[3]:.2f}".replace('.', ',')) # Formata o valor
                indice_editando_servico = id_servico
                btn_salvar_servico.config(text="Atualizar", command=atualizar_servico) # Muda o texto do botão para "Atualizar"
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao editar serviço: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um serviço para editar.")

def atualizar_servico():
    """Atualiza os dados do serviço no banco de dados."""
    global indice_editando_servico
    if indice_editando_servico:
        nome = entry_nome_servico.get()
        descricao = entry_descricao_servico.get()
        valor = entry_valor_servico.get()
        if not nome or not descricao:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

        # Remove a formatação de Real (R$) e tenta converter para float
        valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            valor_float = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Use o formato: 1000,00")
            return

        try:
            conn = sqlite3.connect("banco_de-dados.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE servicos SET nome=?, descricao=?, valor=? WHERE id=?", (nome, descricao, valor_float, indice_editando_servico))
            conn.commit()
            conn.close()
            atualizar_lista_servicos()
            limpar_campos_servico()
            indice_editando_servico = None
            btn_salvar_servico.config(text="Salvar", command=salvar_servico) # Reseta o botão para "Salvar"
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar serviço: {e}")
    else:
        messagebox.showerror("Erro", "Nenhum serviço para atualizar.")

def atualizar_lista_servicos():
    """Atualiza a Treeview de serviços com os dados do banco de dados."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servicos")
        servicos = cursor.fetchall()
        conn.close()

        for item in tree_servicos.get_children():
            tree_servicos.delete(item)

        for servico in servicos:
            # Formata o valor para exibição em Real (R$)
            valor_formatado = f"R$ {servico[3]:.2f}".replace('.', ',')
            tree_servicos.insert("", tk.END, values=(servico[0], servico[1], servico[2], valor_formatado))
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao atualizar lista de serviços: {e}")

def formatar_valor(event):
    """Formata o valor no formato Real (R$)."""
    texto = entry_valor_servico.get().replace("R$", "").replace(".", "").replace(",", "").strip()
    if not texto:
        texto = "0"
    try:
        valor = int(texto) / 100
        texto_formatado = f"R$ {valor:.2f}".replace('.', ',')
        entry_valor_servico.delete(0, tk.END)
        entry_valor_servico.insert(0, texto_formatado)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Use o formato: 1000,00")
        entry_valor_servico.delete(0, tk.END)
        entry_valor_servico.insert(0, "R$ 0,00")

def criar_aba_servicos(notebook):
    """Cria a aba de Serviços na interface."""
    global entry_nome_servico, entry_descricao_servico, entry_valor_servico, tree_servicos, btn_salvar_servico, indice_editando_servico
    indice_editando_servico = None

    aba_servicos = ttk.Frame(notebook)
    notebook.add(aba_servicos, text='Serviços')

    # --- Frame para o formulário de cadastro de serviços ---
    frame_cadastro_servico = ttk.LabelFrame(aba_servicos, text="Cadastro de Serviço", padding=10)
    frame_cadastro_servico.pack(padx=10, pady=10, fill='x')

    # Labels e Entries para o formulário de serviços
    lbl_nome_servico = ttk.Label(frame_cadastro_servico, text="Nome do Serviço:")
    lbl_nome_servico.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nome_servico = ttk.Entry(frame_cadastro_servico)
    entry_nome_servico.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    lbl_descricao_servico = ttk.Label(frame_cadastro_servico, text="Descrição do Serviço:")
    lbl_descricao_servico.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_descricao_servico = ttk.Entry(frame_cadastro_servico)
    entry_descricao_servico.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    lbl_valor_servico = ttk.Label(frame_cadastro_servico, text="Valor do Serviço:")
    lbl_valor_servico.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_valor_servico = ttk.Entry(frame_cadastro_servico)
    entry_valor_servico.insert(0, "R$ 0,00")  # Inicializa com valor zero
    entry_valor_servico.bind("<FocusOut>", formatar_valor)  # Formata ao sair do campo
    entry_valor_servico.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
    # --- Frame para os botões de ação ---
    frame_botoes_servico = ttk.Frame(aba_servicos)
    frame_botoes_servico.pack(pady=10, padx=10, fill='x')

    btn_novo_servico = ttk.Button(frame_botoes_servico, text="Novo", command=limpar_campos_servico)
    btn_novo_servico.pack(side='left', padx=5)

    btn_salvar_servico = ttk.Button(frame_botoes_servico, text="Salvar", command=salvar_servico)
    btn_salvar_servico.pack(side='left', padx=5)

    btn_editar_servico = ttk.Button(frame_botoes_servico, text="Editar", command=editar_servico)
    btn_editar_servico.pack(side='left', padx=5)

    btn_excluir_servico = ttk.Button(frame_botoes_servico, text="Excluir", command=excluir_servico)
    btn_excluir_servico.pack(side='left', padx=5)

    # --- Frame para a listagem de serviços ---
    frame_lista_servicos = ttk.LabelFrame(aba_servicos, text="Serviços Cadastrados", padding=10)
    frame_lista_servicos.pack(padx=10, pady=10, fill='both', expand=True)

    # Treeview para listar os serviços
    tree_servicos = ttk.Treeview(frame_lista_servicos, columns=("ID", "Nome", "Descrição", "Valor"), show='headings')
    tree_servicos.heading("ID", text="ID")
    tree_servicos.heading("Nome", text="Nome")
    tree_servicos.heading("Descrição", text="Descrição")
    tree_servicos.heading("Valor", text="Valor")
    tree_servicos.pack(fill='both', expand=True)

    # Chamando as funções
    criar_tabela_servicos()
    atualizar_lista_servicos()

    return aba_servicos

def formatar_para_porcentagem(event): #já conferido
    """
    Formata o texto de um widget Entry para o formato de porcentagem (XX%).

    Esta função é projetada para ser usada como um callback para eventos
    de teclado (como KeyRelease) em widgets Entry onde o usuário digita
    valores de porcentagem. Ela garante que apenas números e o símbolo
    de porcentagem sejam mantidos no campo.

    Args:
        event: O objeto de evento Tkinter que disparou a função.
               Contém informações sobre o evento, como o widget e a tecla pressionada.
    """
    widget = event.widget
    texto = widget.get()

    # Permite as ações de apagar (Backspace e Delete) sem interferência da formatação.
    if event.keysym in ('BackSpace', 'Delete'):
        return

    # Remove todos os símbolos '%' temporariamente para facilitar a análise numérica.
    texto_sem_porcento = texto.replace('%', '').strip()

    # Permite que o campo fique vazio.
    if texto_sem_porcento == '':
        return

    try:
        # Tenta converter o texto (sem o %) para um float. Isso valida se a entrada é numérica.
        if texto_sem_porcento:
            float(texto_sem_porcento.replace(',', '.'))
            # Adiciona o símbolo '%' apenas se não estiver presente no final do texto do widget.
            if not widget.get().endswith('%'):
                widget.delete(0, tk.END)
                widget.insert(0, f"{texto_sem_porcento}%")
        # Lógica para permitir a digitação direta do símbolo '%' se não estiver no final.
        elif event.keysym == '%' and not widget.get().endswith('%'):
            widget.insert(tk.END, '%')
        # Impede a adição de mais caracteres se já houver um '%' no final (exceto para apagar).
        elif texto and texto.endswith('%') and event.keysym not in ('BackSpace', 'Delete'):
            return
    except ValueError:
        # Se a conversão para float falhar (entrada não numérica), remove o último caractere digitado,
        # a menos que o conteúdo seja apenas '%'.
        widget_conteudo = widget.get()
        if widget_conteudo and widget_conteudo != '%':
            widget.delete(widget_conteudo[:-1])
        # Se o conteúdo for '%' e tiver mais de um caractere, remove o último (outro '%' digitado).
        elif widget_conteudo == '%' and len(widget_conteudo) > 1:
            widget.delete(tk.END)

def calcular_preco_venda(event, entry_preco_custo, entry_margem_lucro, entry_preco_venda):
    preco_custo_str = entry_preco_custo.get().replace('R$', '').strip().replace('.', '').replace(',', '.') if entry_preco_custo.get() else '0.00'
    margem_lucro_str = entry_margem_lucro.get().replace('%', '').strip().replace('.', '').replace(',', '.') if entry_margem_lucro.get() else ''

    try:
        preco_custo = float(preco_custo_str)
        if margem_lucro_str:
            margem_lucro = float(margem_lucro_str) / 100
            preco_venda_calculado = preco_custo * (1 + margem_lucro)

            entry_preco_venda.config(state='normal') # Tornar editável temporariamente
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.insert(0, f'R$ {preco_venda_calculado:.2f}'.replace('.', ','))
            entry_preco_venda.config(state='readonly') # Voltar para somente leitura

        else:
            entry_preco_venda.config(state='normal')
            entry_preco_venda.delete(0, tk.END)
            entry_preco_venda.config(state='readonly')

    except ValueError as e:
        
        entry_preco_venda.delete(0, tk.END)
        entry_preco_venda.insert(0, 'R$ 0,00')
    except Exception as e:
        print(f"Outro Erro: {e}")

def calcular_margem_lucro(event, entry_preco_custo, entry_preco_venda, entry_margem_lucro): #já conferido
    """
    Calcula a margem de lucro em porcentagem com base no preço de custo
    e no preço de venda, e exibe o resultado formatado no widget Entry
    de margem de lucro.

    Args:
        event: O objeto de evento Tkinter que disparou a função.
               Geralmente usado para identificar o widget que perdeu o foco.
        entry_preco_custo: O widget Entry que contém o preço de custo.
        entry_preco_venda: O widget Entry que contém o preço de venda.
        entry_margem_lucro: O widget Entry onde a margem de lucro calculada
                           será exibida (em porcentagem).
    """
    # Obtém o valor do preço de custo, remove formatação e normaliza para float.
    preco_custo_str = entry_preco_custo.get().replace('R$', '').strip().replace('.', '').replace(',', '.') if entry_preco_custo.get() else '0.00'
    # Obtém o valor do preço de venda, remove formatação e normaliza para float.
    preco_venda_str = entry_preco_venda.get().replace('R$', '').strip().replace('.', '').replace(',', '.') if entry_preco_venda.get() else '0.00'

    try:
        # Converte o preço de custo para float.
        preco_custo = float(preco_custo_str)
        # Converte o preço de venda para float.
        preco_venda = float(preco_venda_str)
        # Verifica se o preço de custo é maior que zero para evitar divisão por zero.
        if preco_custo > 0 and preco_venda >= preco_custo:  # Adicionada condição para preço de venda ser maior ou igual ao custo
            # Calcula a margem de lucro: ((Preço de Venda - Preço de Custo) / Preço de Custo) * 100.
            margem = ((preco_venda - preco_custo) / preco_custo) * 100
            # Limpa o conteúdo atual do widget de margem de lucro.
            entry_margem_lucro.delete(0, tk.END)
            # Insere a margem de lucro calculada e formatada (XX.YY%) no widget.
            entry_margem_lucro.insert(0, f'{margem:.2f}%'.replace('.', ','))
        elif preco_custo > 0:
            # Se o preço de custo for maior que zero, mas o preço de venda não for válido
            # para calcular a margem, limpa o campo de margem de lucro.
            entry_margem_lucro.delete(0, tk.END)
            entry_margem_lucro.insert(0, '')
        else:
            # Se o preço de custo for zero ou negativo, limpa o campo de margem de lucro.
            entry_margem_lucro.delete(0, tk.END)
            entry_margem_lucro.insert(0, '')
    except ValueError:
        # Se ocorrer um erro na conversão para float (preço de custo ou venda inválidos),
        # limpa o campo de margem de lucro.
        entry_margem_lucro.delete(0, tk.END)
        entry_margem_lucro.insert(0, '')
    except ZeroDivisionError:
        # Se o preço de custo for zero, exibe uma mensagem de erro no campo de margem.
        entry_margem_lucro.delete(0, tk.END)
        entry_margem_lucro.insert(0, 'Erro: Custo Zero')

def formatar_telefone(event, telefone_entry): #já conferido
    """
    Formata o texto de um widget Entry para o formato de número de telefone brasileiro
    dinamicamente enquanto o usuário digita.

    Esta função é projetada para ser usada como um callback para eventos
    de teclado (como KeyRelease) em widgets Entry destinados à entrada de
    números de telefone. Ela formata o número à medida que o usuário digita,
    aplicando a máscara: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.

    Args:
        event: O objeto de evento Tkinter que disparou a função.
               Embora esteja presente na assinatura, esta função
               geralmente não usa informações específicas do evento,
               apenas o widget que o gerou.
        telefone_entry: O widget Entry que contém o número de telefone
                        sendo digitado.
    """
    # 1. Obtém o texto atual do campo de telefone.
    texto_atual = telefone_entry.get()

    # 2. Mantém apenas os dígitos do texto atual, removendo quaisquer
    #    caracteres não numéricos (como '-', '(', ')', ' ').
    novo_texto = ''.join(filter(str.isdigit, texto_atual))

    # 3. Aplica a formatação com base no comprimento do texto (apenas dígitos):
    if len(novo_texto) <= 2:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto}")
    elif len(novo_texto) == 3:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:]}")
    elif len(novo_texto) == 4:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:]}")
    elif len(novo_texto) == 7:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:7]}")
    elif len(novo_texto) == 8:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:4]}-{novo_texto[4:]}")
    elif len(novo_texto) == 9: # Para telefones com 9 dígitos após o DDD
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:5]}-{novo_texto[5:]}")
    elif len(novo_texto) == 10:
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:6]}-{novo_texto[6:]}")
    elif len(novo_texto) == 11: # Para telefones com DDD + 9 dígitos
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:7]}-{novo_texto[7:]}")
    else:
        # Se o número exceder 11 dígitos, podemos truncar ou manter como está.
        # Aqui, vamos truncar para 11 dígitos formatados.
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, f"({novo_texto[:2]}) {novo_texto[2:7]}-{novo_texto[7:11]}")

    # Observação: A formatação é aplicada a cada evento de teclado,
    # construindo a máscara dinamicamente. O campo é limpo antes de
    # inserir a nova formatação baseada no texto atual (apenas dígitos).

def buscar_endereco_por_cep(cep_entry, rua_entry, bairro_entry, cidade_entry, estado_entry, numero_focus): #já conferido
    """
    Busca informações de endereço a partir de um CEP utilizando a API do ViaCEP.

    Esta função é projetada para ser usada como um callback, geralmente
    associado a um evento (como perder o foco) em um campo de entrada de CEP.
    Ela pega o CEP digitado, faz uma requisição para a API do ViaCEP e,
    se o CEP for válido e encontrado, preenche os campos de rua, bairro,
    cidade e estado correspondentes.

    Args:
        cep_entry: O widget Entry que contém o CEP digitado.
        rua_entry: O widget Entry onde o nome da rua será preenchido.
        bairro_entry: O widget Entry onde o nome do bairro será preenchido.
        cidade_entry: O widget Entry onde o nome da cidade será preenchido.
        estado_entry: O widget Entry onde a sigla do estado (UF) será preenchida.
        numero_focus: Um widget (geralmente um Entry para o número do endereço)
                      que receberá o foco após o CEP ser encontrado.
    """
    # 1. Obtém o CEP digitado, remove o hífen (se houver) e espaços em branco.
    cep = cep_entry.get().replace('-', '').strip()

    # 2. Valida o CEP: verifica se não está vazio, tem 8 dígitos e contém apenas números.
    if not cep or len(cep) != 8 or not cep.isdigit():
        messagebox.showerror("Erro", "CEP inválido.")
        return

    try:
        # 3. Constrói a URL da API do ViaCEP para o CEP fornecido.
        url = f"https://viacep.com.br/ws/{cep}/json/"

        # 4. Faz a requisição GET para a API.
        response = requests.get(url)

        # 5. Verifica se a requisição foi bem-sucedida (status code 2xx).
        response.raise_for_status()

        # 6. Converte a resposta JSON para um dicionário Python.
        data = response.json()

        # 7. Verifica se a API retornou um erro indicando que o CEP não foi encontrado.
        if "erro" in data:
            messagebox.showerror("Erro", "CEP não encontrado.")
        else:
            # 8. Se o CEP foi encontrado, preenche os campos de endereço com os dados da API.
            rua_entry.delete(0, tk.END)
            rua_entry.insert(0, data.get("logradouro", ""))  # Usa .get() com valor padrão para evitar erros

            bairro_entry.delete(0, tk.END)
            bairro_entry.insert(0, data.get("bairro", ""))

            cidade_entry.delete(0, tk.END)
            cidade_entry.insert(0, data.get("localidade", ""))

            estado_entry.delete(0, tk.END)
            estado_entry.insert(0, data.get("uf", ""))

            # 9. Define o foco no próximo campo (geralmente o número do endereço).
            numero_focus.focus_set()

    # 10. Captura exceções que podem ocorrer durante a requisição HTTP (problemas de rede, etc.).
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao buscar CEP: {e}")

    # 11. Captura exceções que podem ocorrer se a resposta do servidor não for um JSON válido.
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Resposta inválida do servidor de CEP.")

def formatar_cpf_cnpj_para_display(cpf_cnpj_numerico): #já conferido
    """
    Formata uma string contendo apenas dígitos de CPF ou CNPJ para uma
    apresentação mais legível com pontos e traço/barra.

    Args:
        cpf_cnpj_numerico: Uma string contendo apenas os dígitos do CPF (11)
                           ou CNPJ (14).

    Returns:
        Uma string formatada do CPF ou CNPJ, ou a string original se o
        comprimento não for 11 ou 14.
    """
    # Verifica se a string numérica tem o comprimento de um CPF (11 dígitos).
    if len(cpf_cnpj_numerico) == 11:
        # Aplica a máscara de CPF: XXX.XXX.XXX-XX
        return f"{cpf_cnpj_numerico[:3]}.{cpf_cnpj_numerico[3:6]}.{cpf_cnpj_numerico[6:9]}-{cpf_cnpj_numerico[9:]}"
    # Verifica se a string numérica tem o comprimento de um CNPJ (14 dígitos).
    elif len(cpf_cnpj_numerico) == 14:
        # Aplica a máscara de CNPJ: XX.XXX.XXX/YYYY-ZZ
        return f"{cpf_cnpj_numerico[:2]}.{cpf_cnpj_numerico[2:5]}.{cpf_cnpj_numerico[5:8]}/{cpf_cnpj_numerico[8:12]}-{cpf_cnpj_numerico[12:]}"
    # Se o comprimento não for de um CPF ou CNPJ padrão, retorna a string original
    # sem formatação.
    return cpf_cnpj_numerico

def formatar_cpf_cnpj(event, cpf_cnpj_entry): #já conferido
    """
    Formata dinamicamente o texto de um widget Entry para o formato de CPF
    (XXX.XXX.XXX-XX) ou CNPJ (XX.XXX.XXX/XXXX-XX) enquanto o usuário digita.

    A formatação é aplicada com base no número de dígitos inseridos. Números
    com até 11 dígitos são formatados como CPF, e números com mais de 11
    (até 14) são formatados como CNPJ.

    Args:
        event: O objeto de evento Tkinter que disparou a função.
               Geralmente não usado diretamente, mas necessário para o callback
               do evento (como <KeyRelease>).
        cpf_cnpj_entry: O widget Entry que contém o CPF ou CNPJ sendo digitado.
    """
    # 1. Obtém o texto atual do campo e mantém apenas os dígitos,
    #    removendo quaisquer outros caracteres que o usuário possa ter digitado.
    texto_atual = ''.join(filter(str.isdigit, cpf_cnpj_entry.get()))
    tamanho = len(texto_atual)
    novo_texto = ''

    # 2. Lógica de formatação para CPF (quando o número de dígitos é até 11):
    if tamanho <= 11:
        if tamanho <= 3:
            # Se houver até 3 dígitos, não adiciona nenhuma máscara.
            novo_texto = texto_atual
        elif tamanho <= 6:
            # Se houver entre 4 e 6 dígitos, adiciona um ponto após o terceiro dígito.
            novo_texto = f"{texto_atual[:3]}.{texto_atual[3:]}"
        elif tamanho <= 9:
            # Se houver entre 7 e 9 dígitos, adiciona um ponto após o terceiro e o sexto dígito.
            novo_texto = f"{texto_atual[:3]}.{texto_atual[3:6]}.{texto_atual[6:]}"
        else:  # tamanho > 9 e <= 11
            # Se houver entre 10 e 11 dígitos, adiciona pontos e um hífen para o formato CPF completo.
            novo_texto = f"{texto_atual[:3]}.{texto_atual[3:6]}.{texto_atual[6:9]}-{texto_atual[9:]}"
    # 3. Lógica de formatação para CNPJ (quando o número de dígitos é maior que 11, até 14):
    else:  # tamanho > 11
        if tamanho <= 2:
            # Se houver até 2 dígitos, não adiciona nenhuma máscara.
            novo_texto = texto_atual
        elif tamanho <= 5:
            # Se houver entre 3 e 5 dígitos, adiciona um ponto após o segundo dígito.
            novo_texto = f"{texto_atual[:2]}.{texto_atual[2:]}"
        elif tamanho <= 8:
            # Se houver entre 6 e 8 dígitos, adiciona pontos após o segundo e o quinto dígito.
            novo_texto = f"{texto_atual[:2]}.{texto_atual[2:5]}.{texto_atual[5:]}"
        elif tamanho <= 12:
            # Se houver entre 9 e 12 dígitos, adiciona pontos e uma barra.
            novo_texto = f"{texto_atual[:2]}.{texto_atual[2:5]}.{texto_atual[5:8]}/{texto_atual[8:]}"
        else:  # tamanho > 12 e <= 14
            # Se houver entre 13 e 14 dígitos, adiciona pontos, barra e hífen para o formato CNPJ completo.
            novo_texto = f"{texto_atual[:2]}.{texto_atual[2:5]}.{texto_atual[5:8]}/{texto_atual[8:12]}-{texto_atual[12:]}"

    # 4. Limpa o conteúdo atual do widget Entry.
    cpf_cnpj_entry.delete(0, tk.END)
    # 5. Insere o novo texto formatado no widget Entry.
    cpf_cnpj_entry.insert(0, novo_texto)

def limpar_campos(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry,  #já conferido
                  cep_entry, rua_entry, numero_entry, complemento_entry,
                  bairro_entry, cidade_entry, estado_entry):
  """
  Limpa o conteúdo de todos os campos de entrada da aba de clientes.

  Args:
      nome_entry: Widget Entry para o nome do cliente.
      cpf_cnpj_entry: Widget Entry para o CPF/CNPJ do cliente.
      telefone_entry: Widget Entry para o telefone do cliente.
      email_entry: Widget Entry para o email do cliente.
      cep_entry: Widget Entry para o CEP do cliente.
      rua_entry: Widget Entry para a rua do cliente.
      numero_entry: Widget Entry para o número do endereço do cliente.
      complemento_entry: Widget Entry para o complemento do endereço do cliente.
      bairro_entry: Widget Entry para o bairro do cliente.
      cidade_entry: Widget Entry para a cidade do cliente.
      estado_entry: Widget Entry para o estado do cliente.
  """
  nome_entry.delete(0, tk.END)
  cpf_cnpj_entry.delete(0, tk.END)
  telefone_entry.delete(0, tk.END)
  email_entry.delete(0, tk.END)
  cep_entry.delete(0, tk.END)
  rua_entry.delete(0, tk.END)
  numero_entry.delete(0, tk.END)
  complemento_entry.delete(0, tk.END)
  bairro_entry.delete(0, tk.END)
  cidade_entry.delete(0, tk.END)
  estado_entry.delete(0, tk.END)

def limpar_campos_produtos(nome_entry, descricao_entry, categoria_entry, codigo_barras_entry, #já conferido
                           preco_custo_entry, preco_venda_entry, estoque_entry,
                           unidade_entry, sku_entry, fornecedor_entry, margem_lucro_entry,
                           erro_nome_label, erro_descricao_label, erro_categoria_label, erro_codigo_barras_label,
                           erro_preco_custo_label, erro_preco_venda_label,
                           erro_estoque_label, erro_unidade_label, erro_sku_label, erro_fornecedor_label,
                           erro_margem_lucro_label, combo_tipo_codigo_barras=None): # Adicionado combobox como argumento opcional
    """
    Limpa o conteúdo dos campos de entrada e as mensagens de erro na aba de produtos.

    Args:
        nome_entry: Widget Entry para o nome do produto.
        descricao_entry: Widget Entry para a descrição do produto.
        categoria_entry: Widget Entry para a categoria do produto.
        codigo_barras_entry: Widget Entry para o código de barras do produto.
        preco_custo_entry: Widget Entry para o preço de custo do produto.
        preco_venda_entry: Widget Entry para o preço de venda do produto.
        estoque_entry: Widget Entry para o estoque atual do produto.
        unidade_entry: Widget Entry para a unidade de medida do produto.
        sku_entry: Widget Entry para o SKU do produto.
        fornecedor_entry: Widget Entry para o fornecedor do produto.
        margem_lucro_entry: Widget Entry para a margem de lucro do produto.
        erro_nome_label: Label para exibir erros no nome do produto.
        erro_descricao_label: Label para exibir erros na descrição do produto.
        erro_categoria_label: Label para exibir erros na categoria do produto.
        erro_codigo_barras_label: Label para exibir erros no código de barras do produto.
        erro_preco_custo_label: Label para exibir erros no preço de custo do produto.
        erro_preco_venda_label: Label para exibir erros no preço de venda do produto.
        erro_estoque_label: Label para exibir erros no estoque atual do produto.
        erro_unidade_label: Label para exibir erros na unidade de medida do produto.
        erro_sku_label: Label para exibir erros no SKU do produto.
        erro_fornecedor_label: Label para exibir erros no fornecedor do produto.
        erro_margem_lucro_label: Label para exibir erros na margem de lucro do produto.
        combo_tipo_codigo_barras: Widget Combobox para o tipo de código de barras (opcional).
    """
    nome_entry.delete(0, tk.END)
    descricao_entry.delete(0, tk.END)
    categoria_entry.delete(0, tk.END)
    codigo_barras_entry.delete(0, tk.END)
    preco_custo_entry.delete(0, tk.END)
    preco_venda_entry.delete(0, tk.END)
    estoque_entry.delete(0, tk.END)
    unidade_entry.delete(0, tk.END)
    sku_entry.delete(0, tk.END)
    fornecedor_entry.delete(0, tk.END)
    margem_lucro_entry.delete(0, tk.END)

    erro_nome_label.config(text="")
    erro_descricao_label.config(text="")
    erro_categoria_label.config(text="")
    erro_codigo_barras_label.config(text="")
    erro_preco_custo_label.config(text="")
    erro_preco_venda_label.config(text="")
    erro_estoque_label.config(text="")
    erro_unidade_label.config(text="")
    erro_sku_label.config(text="")
    erro_fornecedor_label.config(text="")
    erro_margem_lucro_label.config(text="")

    # Se a combobox foi passada como argumento, redefine o valor padrão
    if combo_tipo_codigo_barras:
        combo_tipo_codigo_barras.set("Outro")

def salvar_cliente(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, #já conferido
                   cep_entry, rua_entry, numero_entry, complemento_entry,
                   bairro_entry, cidade_entry, estado_entry,
                   erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                   erro_email_label, erro_numero_label, erro_complemento_label,
                   erro_cep_label, erro_rua_label, erro_bairro_label,
                   erro_cidade_label, erro_estado_label, treeview_clientes):
    global modo_edicao_cliente
    global id_cliente_editando

    #print(f"Modo de edição em salvar_cliente (início): {modo_edicao_cliente}") # ADICIONE ESTA LINHA
    #print(f"ID do cliente editando em salvar_cliente (início): {id_cliente_editando}") # ADICIONE ESTA LINHA

    nome = nome_entry.get().strip()
    cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj_entry.get()))
    telefone = ''.join(filter(str.isdigit, telefone_entry.get()))
    email = email_entry.get().strip()
    cep = ''.join(filter(str.isdigit, cep_entry.get()))
    rua = rua_entry.get().strip()
    numero = numero_entry.get().strip()
    complemento = complemento_entry.get().strip()
    bairro = bairro_entry.get().strip()
    cidade = cidade_entry.get().strip().upper()
    estado = estado_entry.get().strip().upper()

    erros = validar_campos(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry,
                            cep_entry, rua_entry, numero_entry, complemento_entry,
                            bairro_entry, cidade_entry, estado_entry,
                            erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                            erro_email_label, erro_numero_label, erro_complemento_label,
                            erro_cep_label, erro_rua_label, erro_bairro_label,
                            erro_cidade_label, erro_estado_label)

    if erros:
        messagebox.showerror("Erro", "Por favor, corrija os campos inválidos.")
        return

    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    try:
        if modo_edicao_cliente and id_cliente_editando is not None:
            # Verificar duplicidade de CPF/CNPJ, excluindo o cliente atual
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE cpf_cnpj=? AND id != ?", (cpf_cnpj, id_cliente_editando))
            count_cpf_cnpj = cursor.fetchone()[0]

            if count_cpf_cnpj > 0 and cpf_cnpj:
                messagebox.showerror("Erro", f"Já existe outro cliente com o mesmo CPF/CNPJ ('{formatar_cpf_cnpj_para_display(cpf_cnpj)}').")
                return
            else:
                # Atualizar os dados do cliente existente
                cursor.execute("""
                    UPDATE clientes SET nome=?, cpf_cnpj=?, telefone=?, email=?, cep=?, rua=?, numero=?, complemento=?, bairro=?, cidade=?, estado=?
                    WHERE id=?
                """, (nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado, id_cliente_editando))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados do cliente atualizados com sucesso!")
        else: # Modo de cadastro de novo cliente
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE cpf_cnpj=?", (cpf_cnpj,))
            count_cpf_cnpj = cursor.fetchone()[0]
            if count_cpf_cnpj > 0 and cpf_cnpj:
                messagebox.showerror("Erro", f"Já existe um cliente com o mesmo CPF/CNPJ ('{formatar_cpf_cnpj_para_display(cpf_cnpj)}').")
                return
            else:
                cursor.execute("""
                    INSERT INTO clientes (nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dados do cliente salvos no banco de dados!")

        # Limpar os campos e atualizar o Treeview
        limpar_campos(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry,
                     cep_entry, rua_entry, numero_entry, complemento_entry,
                     bairro_entry, cidade_entry, estado_entry)
        atualizar_treeview_clientes(treeview_clientes)
        modo_edicao_cliente = False
        id_cliente_editando = None

    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Salvar/Atualizar", f"Ocorreu um erro ao interagir com o banco de dados: {e}")

    finally:
        if conn:
            conn.close()
    atualizar_treeview_clientes(treeview_clientes)
    
def atualizar_treeview_clientes(treeview): #já conferido
    """
    Limpa e popula o widget Treeview com os dados da tabela 'clientes'
    do banco de dados 'banco_de_Dados.db'.

    Args:
        treeview: O widget Treeview a ser atualizado.
    """
    # Limpa todos os itens atualmente exibidos no Treeview.
    treeview.delete(*treeview.get_children())

    try:
        # Estabelece uma conexão com o banco de dados SQLite.
        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        # Executa uma consulta SQL para selecionar todos os dados da tabela 'clientes'.
        cursor.execute("SELECT id, nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado FROM clientes")

        # Itera sobre cada linha (cliente) retornada pela consulta.
        for row in cursor.fetchall():
            # Insere uma nova linha no Treeview com os valores da linha do banco de dados.
            # tk.END garante que a nova linha seja adicionada ao final.
            treeview.insert("", tk.END, text=row[0], values=row[1:])
            
    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Atualizar Treeview", f"Ocorreu um erro ao ler o banco de dados: {e}")

    finally:
        # Garante que a conexão com o banco de dados seja fechada,
        # mesmo que ocorra um erro.
        if conn:
            conn.close()

    """
    # O código comentado abaixo parece ser uma tentativa inicial de adicionar
    # um único cliente ao Treeview após salvar. A abordagem correta é
    # limpar e recarregar todos os dados do banco de dados para garantir
    # que o Treeview reflita o estado atual do banco de dados, especialmente
    # se houver outras operações que possam ter modificado o banco de dados.
    #
    # # Se não houver duplicidade, adicionar ao Treeview
    # treeview_clientes.insert("", tk.END, values=(nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado))
    # messagebox.showinfo("Sucesso", "Dados do cliente salvos!")
    # limpar_campos_cliente(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry,
    #                        cep_entry, rua_entry, numero_entry, complemento_entry,
    #                        bairro_entry, cidade_entry, estado_entry,
    #                        erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
    #                        erro_email_label, erro_numero_label, erro_complemento_label,
    #                        erro_cep_label, erro_rua_label, erro_bairro_label,
    #                        erro_cidade_label, erro_estado_label)
    """

def validar_campos(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, #já conferido
                   cep_entry, rua_entry, numero_entry, complemento_entry,
                   bairro_entry, cidade_entry, estado_entry,
                   erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                   erro_email_label, erro_numero_label, erro_complemento_label,
                   erro_cep_label, erro_rua_label, erro_bairro_label,
                   erro_cidade_label, erro_estado_label):
    """
    Valida os campos de entrada do formulário de cliente.

    Verifica se os campos obrigatórios estão preenchidos e se os formatos
    de CPF/CNPJ, telefone e e-mail são válidos. Exibe mensagens de erro
    ao lado dos campos inválidos.

    Args:
        nome_entry: Widget Entry para o nome do cliente.
        cpf_cnpj_entry: Widget Entry para o CPF/CNPJ do cliente.
        telefone_entry: Widget Entry para o telefone do cliente.
        email_entry: Widget Entry para o email do cliente.
        cep_entry: Widget Entry para o CEP do cliente.
        rua_entry: Widget Entry para a rua do cliente.
        numero_entry: Widget Entry para o número do endereço do cliente.
        complemento_entry: Widget Entry para o complemento do endereço do cliente.
        bairro_entry: Widget Entry para o bairro do cliente.
        cidade_entry: Widget Entry para a cidade do cliente.
        estado_entry: Widget Entry para o estado do cliente.
        erro_nome_label: Label para exibir erros no nome.
        erro_cpf_cnpj_label: Label para exibir erros no CPF/CNPJ.
        erro_telefone_label: Label para exibir erros no telefone.
        erro_email_label: Label para exibir erros no email.
        erro_numero_label: Label para exibir erros no número.
        erro_complemento_label: Label para exibir erros no complemento.
        erro_cep_label: Label para exibir erros no CEP.
        erro_rua_label: Label para exibir erros na rua.
        erro_bairro_label: Label para exibir erros no bairro.
        erro_cidade_label: Label para exibir erros na cidade.
        erro_estado_label: Label para exibir erros no estado.

    Returns:
        True se houver algum campo inválido, False caso contrário.
    """
    erros = False

    nome = nome_entry.get().strip()
    cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj_entry.get()))
    telefone = ''.join(filter(str.isdigit, telefone_entry.get()))
    email = email_entry.get().strip()
    cep = ''.join(filter(str.isdigit, cep_entry.get()))
    rua = rua_entry.get().strip()
    numero = numero_entry.get().strip()
    bairro = bairro_entry.get().strip()
    cidade = cidade_entry.get().strip()
    estado = estado_entry.get().strip().upper()

    def aplicar_estilo_erro(widget):
        widget.config(highlightbackground="red", highlightthickness=1)

    def remover_estilo_erro(widget):
        widget.config(highlightbackground="", highlightthickness=0)

    if not nome:
        aplicar_estilo_erro(nome_entry)
        erro_nome_label.config(text="O nome é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(nome_entry)
        erro_nome_label.config(text="")

    if cpf_cnpj and len(cpf_cnpj) not in [11, 14]:
        aplicar_estilo_erro(cpf_cnpj_entry)
        erro_cpf_cnpj_label.config(text="CPF deve ter 11 ou CNPJ 14 dígitos.")
        erros = True
    else:
        remover_estilo_erro(cpf_cnpj_entry)
        erro_cpf_cnpj_label.config(text="")

    if telefone and not (10 <= len(telefone) <= 11):
        aplicar_estilo_erro(telefone_entry)
        erro_telefone_label.config(text="Telefone deve ter 10 ou 11 dígitos.")
        erros = True
    else:
        remover_estilo_erro(telefone_entry)
        erro_telefone_label.config(text="")

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        aplicar_estilo_erro(email_entry)
        erro_email_label.config(text="E-mail inválido.")
        erros = True
    else:
        remover_estilo_erro(email_entry)
        erro_email_label.config(text="")

    if not cep:
        aplicar_estilo_erro(cep_entry)
        erro_cep_label.config(text="O CEP é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(cep_entry)
        erro_cep_label.config(text="")

    if not rua:
        aplicar_estilo_erro(rua_entry)
        erro_rua_label.config(text="A rua é obrigatória.")
        erros = True
    else:
        remover_estilo_erro(rua_entry)
        erro_rua_label.config(text="")

    if not numero:
        aplicar_estilo_erro(numero_entry)
        erro_numero_label.config(text="O número é obrigatório.")
        erros = True
    elif not numero.isdigit():
        aplicar_estilo_erro(numero_entry)
        erro_numero_label.config(text="Digite apenas números no número.")
        erros = True
    else:
        remover_estilo_erro(numero_entry)
        erro_numero_label.config(text="")

    if not bairro:
        aplicar_estilo_erro(bairro_entry)
        erro_bairro_label.config(text="O bairro é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(bairro_entry)
        erro_bairro_label.config(text="")

    if not cidade:
        aplicar_estilo_erro(cidade_entry)
        erro_cidade_label.config(text="A cidade é obrigatória.")
        erros = True
    else:
        remover_estilo_erro(cidade_entry)
        erro_cidade_label.config(text="")

    if not estado:
        aplicar_estilo_erro(estado_entry)
        erro_estado_label.config(text="O estado é obrigatório.")
        erros = True
    elif len(estado) != 2:
        aplicar_estilo_erro(estado_entry)
        erro_estado_label.config(text="O estado deve ter 2 caracteres.")
        erros = True
    else:
        remover_estilo_erro(estado_entry)
        erro_estado_label.config(text="")

    return erros

def validar_email(email): #já conferido
  """
  Valida um endereço de e-mail usando uma expressão regular básica.

  Args:
    email: A string contendo o endereço de e-mail a ser validado.

  Returns:
    True se o e-mail corresponder ao padrão, False caso contrário.
  """
  # Padrão de expressão regular para uma validação básica de e-mail:
  # - ^: Início da string.
  # - [a-zA-Z0-9._%+-]+: Um ou mais caracteres alfanuméricos, ponto,
  #                       sublinhado, porcentagem, mais ou menos.
  # - @: O símbolo "@".
  # - [a-zA-Z0-9.-]+: Um ou mais caracteres alfanuméricos, ponto ou hífen.
  # - \.: Um ponto literal (escapado com uma barra invertida).
  # - [a-zA-Z]{2,}: Dois ou mais caracteres alfabéticos (domínio de nível superior).
  # - $: Fim da string.
  padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  return bool(re.match(padrao, email))

def validar_numero_input(event, numero_entry): #já conferido
  """
  Limita a entrada de um widget Entry para aceitar apenas dígitos.

  Esta função é projetada para ser usada como um callback para eventos
  de teclado (como KeyRelease) em widgets Entry onde se espera apenas
  a digitação de números. Ela remove quaisquer caracteres não numéricos
  da entrada do usuário.

  Args:
      event: O objeto de evento Tkinter que disparou a função.
             Embora esteja presente na assinatura, esta função
             geralmente não usa informações específicas do evento.
      numero_entry: O widget Entry que contém o texto a ser validado.
  """
  texto_atual = numero_entry.get()
  novo_texto = ''.join(filter(str.isdigit, texto_atual))
  if novo_texto != texto_atual:
    numero_entry.delete(0, tk.END)
    numero_entry.insert(0, novo_texto)

def aplicar_estilo_erro(widget): #já conferido
  """
  Aplica um estilo visual de erro a um widget Entry (ou similar) usando ttk Style.

  Args:
      widget: O widget Tkinter ao qual o estilo de erro deve ser aplicado.
              Geralmente um widget Entry ou um widget que suporta a opção 'style'.
  """
  widget.config(style="Erro.TEntry")

def remover_estilo_erro(widget): #já conferido
  """
  Remove o estilo de erro de um widget Entry (ou similar), revertendo ao estilo padrão.

  Args:
      widget: O widget Tkinter do qual o estilo de erro deve ser removido.
              Geralmente um widget Entry ou um widget que suporta a opção 'style'.
  """
  widget.config(style="")  # Remove o estilo de erro

def excluir_cliente(treeview): #já conferido
    """
    Exclui o cliente selecionado no Treeview e remove-o do banco de dados.

    Args:
        treeview (ttk.Treeview): O widget Treeview que exibe a lista de clientes.
    """
    selected_item = treeview.selection()
    # Obtém o item selecionado no Treeview. Se nenhum item estiver selecionado,
    # selected_item será uma tupla vazia.

    if not selected_item:
        messagebox.showerror("Erro", "Selecione um cliente para excluir.")
        return
    # Se nenhum cliente estiver selecionado, exibe uma mensagem de erro e sai da função.

    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o cliente selecionado?"):
        # Exibe uma caixa de diálogo de confirmação perguntando ao usuário se ele tem certeza
        # de que deseja excluir o cliente. Retorna True se o usuário clicar em "Sim" e False
        # se clicar em "Não".

        cliente_id = treeview.item(selected_item, 'values')[0] # Supondo que o ID esteja na primeira coluna

        try:
            conn = sqlite3.connect('banco_de_dados.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE rowid=?", (cliente_id,))
            conn.commit()
            treeview.delete(selected_item)
            messagebox.showinfo("Sucesso", "Cliente excluído!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro ao Excluir", f"Ocorreu um erro ao excluir o cliente do banco de dados: {e}")
        finally:
            if conn:
                conn.close()

        # Se o usuário confirmou a exclusão:
        # 1. Excluímos o item selecionado do Treeview.
        # 2. Exibimos uma mensagem de sucesso.

        # *** IMPORTANTE: ***
        # Atualmente, esta função apenas remove o cliente da visualização no Treeview.
        # Para excluir o cliente PERMANENTEMENTE, você precisará adicionar código aqui
        # para interagir com o seu banco de dados e remover o registro correspondente
        # usando o ID do cliente (ou algum outro identificador único).

        # Exemplo de como você pode obter o ID do cliente (assumindo que o ID
        # esteja armazenado em alguma coluna do Treeview - ajuste conforme a sua estrutura):
        # values = treeview.item(selected_item, 'values')
        # cliente_id = values[0] # Assumindo que o ID é o primeiro valor na tupla 'values'
        #
        # # Aqui você adicionaria o código para excluir o cliente do seu banco de dados
        # # usando o 'cliente_id'.
        # print(f"Cliente com ID {cliente_id} seria excluído do banco de dados.")

# Certifique-se de que a sua função limpar_campos_cliente esteja definida para receber todos esses argumentos
def limpar_campos_cliente(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, #já conferido
                           cep_entry, rua_entry, numero_entry, complemento_entry,
                           bairro_entry, cidade_entry, estado_entry,
                           erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                           erro_email_label, erro_numero_label, erro_complemento_label,
                           erro_cep_label, erro_rua_label, erro_bairro_label,
                           erro_cidade_label, erro_estado_label):
    """
    Limpa o conteúdo dos campos de entrada e as mensagens de erro na aba de clientes.

    Args:
        nome_entry (tk.Entry): Widget Entry para o nome do cliente.
        cpf_cnpj_entry (tk.Entry): Widget Entry para o CPF/CNPJ do cliente.
        telefone_entry (tk.Entry): Widget Entry para o telefone do cliente.
        email_entry (tk.Entry): Widget Entry para o email do cliente.
        cep_entry (tk.Entry): Widget Entry para o CEP do cliente.
        rua_entry (tk.Entry): Widget Entry para a rua do cliente.
        numero_entry (tk.Entry): Widget Entry para o número do endereço do cliente.
        complemento_entry (tk.Entry): Widget Entry para o complemento do endereço do cliente.
        bairro_entry (tk.Entry): Widget Entry para o bairro do cliente.
        cidade_entry (tk.Entry): Widget Entry para a cidade do cliente.
        estado_entry (tk.Entry): Widget Entry para o estado do cliente.
        erro_nome_label (tk.Label): Label para exibir erros no nome.
        erro_cpf_cnpj_label (tk.Label): Label para exibir erros no CPF/CNPJ.
        erro_telefone_label (tk.Label): Label para exibir erros no telefone.
        erro_email_label (tk.Label): Label para exibir erros no email.
        erro_numero_label (tk.Label): Label para exibir erros no número.
        erro_complemento_label (tk.Label): Label para exibir erros no complemento.
        erro_cep_label (tk.Label): Label para exibir erros no CEP.
        erro_rua_label (tk.Label): Label para exibir erros na rua.
        erro_bairro_label (tk.Label): Label para exibir erros no bairro.
        erro_cidade_label (tk.Label): Label para exibir erros na cidade.
        erro_estado_label (tk.Label): Label para exibir erros no estado.
    """
    nome_entry.delete(0, tk.END)
    # Limpa o campo de nome.
    cpf_cnpj_entry.delete(0, tk.END)
    # Limpa o campo de CPF/CNPJ.
    telefone_entry.delete(0, tk.END)
    # Limpa o campo de telefone.
    email_entry.delete(0, tk.END)
    # Limpa o campo de email.
    cep_entry.delete(0, tk.END)
    # Limpa o campo de CEP.
    rua_entry.delete(0, tk.END)
    # Limpa o campo de rua.
    numero_entry.delete(0, tk.END)
    # Limpa o campo de número.
    complemento_entry.delete(0, tk.END)
    # Limpa o campo de complemento.
    bairro_entry.delete(0, tk.END)
    # Limpa o campo de bairro.
    cidade_entry.delete(0, tk.END)
    # Limpa o campo de cidade.
    estado_entry.delete(0, tk.END)
    # Limpa o campo de estado.

    erro_nome_label.config(text="")
    # Limpa a mensagem de erro do nome.
    erro_cpf_cnpj_label.config(text="")
    # Limpa a mensagem de erro do CPF/CNPJ.
    erro_telefone_label.config(text="")
    # Limpa a mensagem de erro do telefone.
    erro_email_label.config(text="")
    # Limpa a mensagem de erro do email.
    erro_numero_label.config(text="")
    # Limpa a mensagem de erro do número.
    erro_complemento_label.config(text="")
    # Limpa a mensagem de erro do complemento.
    erro_cep_label.config(text="")
    # Limpa a mensagem de erro do CEP.
    erro_rua_label.config(text="")
    # Limpa a mensagem de erro da rua.
    erro_bairro_label.config(text="")
    # Limpa a mensagem de erro do bairro.
    erro_cidade_label.config(text="")
    # Limpa a mensagem de erro da cidade.
    erro_estado_label.config(text="")
    # Limpa a mensagem de erro do estado.

def validar_campos(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, #já conferido
                        cep_entry, rua_entry, numero_entry, complemento_entry,
                        bairro_entry, cidade_entry, estado_entry,
                        erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                        erro_email_label, erro_cep_label, erro_rua_label,
                        erro_numero_label, erro_complemento_label, erro_bairro_label,
                        erro_cidade_label, erro_estado_label):
    """
    Valida os campos de entrada do formulário de cliente.

    Verifica se os campos obrigatórios estão preenchidos e se os formatos
    de CPF/CNPJ, telefone e e-mail são válidos. Exibe mensagens de erro
    ao lado dos campos inválidos e aplica/remove estilos de erro nos widgets.

    Args:
        nome_entry (tk.Entry): Widget Entry para o nome do cliente.
        cpf_cnpj_entry (tk.Entry): Widget Entry para o CPF/CNPJ do cliente.
        telefone_entry (tk.Entry): Widget Entry para o telefone do cliente.
        email_entry (tk.Entry): Widget Entry para o email do cliente.
        cep_entry (tk.Entry): Widget Entry para o CEP do cliente.
        rua_entry (tk.Entry): Widget Entry para a rua do cliente.
        numero_entry (tk.Entry): Widget Entry para o número do endereço do cliente.
        complemento_entry (tk.Entry): Widget Entry para o complemento do endereço do cliente.
        bairro_entry (tk.Entry): Widget Entry para o bairro do cliente.
        cidade_entry (tk.Entry): Widget Entry para a cidade do cliente.
        estado_entry (tk.Entry): Widget Entry para o estado do cliente (2 caracteres).
        erro_nome_label (tk.Label): Label para exibir erros no nome.
        erro_cpf_cnpj_label (tk.Label): Label para exibir erros no CPF/CNPJ.
        erro_telefone_label (tk.Label): Label para exibir erros no telefone.
        erro_email_label (tk.Label): Label para exibir erros no email.
        erro_cep_label (tk.Label): Label para exibir erros no CEP.
        erro_rua_label (tk.Label): Label para exibir erros na rua.
        erro_numero_label (tk.Label): Label para exibir erros no número.
        erro_complemento_label (tk.Label): Label para exibir erros no complemento.
        erro_bairro_label (tk.Label): Label para exibir erros no bairro.
        erro_cidade_label (tk.Label): Label para exibir erros na cidade.
        erro_estado_label (tk.Label): Label para exibir erros no estado.

    Returns:
        bool: True se houver algum campo inválido, False caso contrário.
    """
    erros = False

    nome = nome_entry.get().strip()
    cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj_entry.get()))
    telefone = ''.join(filter(str.isdigit, telefone_entry.get()))
    email = email_entry.get().strip()
    cep = ''.join(filter(str.isdigit, cep_entry.get()))
    rua = rua_entry.get().strip()
    numero = numero_entry.get().strip()
    bairro = bairro_entry.get().strip()
    cidade = cidade_entry.get().strip()
    estado = estado_entry.get().strip()

    def aplicar_estilo_erro(widget):
        """Aplica o estilo de erro ao widget."""
        widget.config(style="Erro.TEntry")

    def remover_estilo_erro(widget):
        """Remove o estilo de erro do widget."""
        widget.config(style="")

    if not nome:
        aplicar_estilo_erro(nome_entry)
        erro_nome_label.config(text="O nome é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(nome_entry)
        erro_nome_label.config(text="")

    if cpf_cnpj and len(cpf_cnpj) not in [11, 14]:
        aplicar_estilo_erro(cpf_cnpj_entry)
        erro_cpf_cnpj_label.config(text="CPF deve ter 11 ou CNPJ 14 dígitos.")
        erros = True
    else:
        remover_estilo_erro(cpf_cnpj_entry)
        erro_cpf_cnpj_label.config(text="")

    if telefone and not (10 <= len(telefone) <= 11):
        aplicar_estilo_erro(telefone_entry)
        erro_telefone_label.config(text="Telefone deve ter 10 ou 11 dígitos.")
        erros = True
    else:
        remover_estilo_erro(telefone_entry)
        erro_telefone_label.config(text="")

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        aplicar_estilo_erro(email_entry)
        erro_email_label.config(text="E-mail inválido.")
        erros = True
    else:
        remover_estilo_erro(email_entry)
        erro_email_label.config(text="")

    if not cep:
        aplicar_estilo_erro(cep_entry)
        erro_cep_label.config(text="O CEP é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(cep_entry)
        erro_cep_label.config(text="")

    if not rua:
        aplicar_estilo_erro(rua_entry)
        erro_rua_label.config(text="A rua é obrigatória.")
        erros = True
    else:
        remover_estilo_erro(rua_entry)
        erro_rua_label.config(text="")

    if not numero:
        aplicar_estilo_erro(numero_entry)
        erro_numero_label.config(text="O número é obrigatório.")
        erros = True
    elif not numero.isdigit():
        aplicar_estilo_erro(numero_entry)
        erro_numero_label.config(text="Digite apenas números no número.")
        erros = True
    else:
        remover_estilo_erro(numero_entry)
        erro_numero_label.config(text="")

    if not bairro:
        aplicar_estilo_erro(bairro_entry)
        erro_bairro_label.config(text="O bairro é obrigatório.")
        erros = True
    else:
        remover_estilo_erro(bairro_entry)
        erro_bairro_label.config(text="")

    if not cidade:
        aplicar_estilo_erro(cidade_entry)
        erro_cidade_label.config(text="A cidade é obrigatória.")
        erros = True
    else:
        remover_estilo_erro(cidade_entry)
        erro_cidade_label.config(text="")

    if not estado:
        aplicar_estilo_erro(estado_entry)
        erro_estado_label.config(text="O estado é obrigatório.")
        erros = True
    elif len(estado) != 2:
        aplicar_estilo_erro(estado_entry)
        erro_estado_label.config(text="O estado deve ter 2 caracteres.")
        erros = True
    else:
        remover_estilo_erro(estado_entry)
        erro_estado_label.config(text="")

    return erros

def aplicar_estilo_erro(entry_widget): #já conferido
    """
    Aplica um estilo visual de erro a um widget Entry (ou similar) usando ttk Style.

    Args:
        entry_widget (ttk.Entry): O widget Entry ao qual o estilo de erro deve ser aplicado.
                                   Espera-se que o estilo "Erro.TEntry" esteja previamente
                                   configurado usando ttk.Style.
    """
    entry_widget.config(style="Erro.TEntry")

def remover_estilo_erro(entry_widget): #já conferido
    """
    Remove qualquer estilo visual de erro aplicado a um widget Entry (ou similar),
    revertendo-o ao seu estilo padrão.

    Args:
        entry_widget (ttk.Entry): O widget Entry do qual o estilo de erro deve ser removido.
    """
    entry_widget.config(style="")

def exibir_clientes(tree):
    """
    Carrega os clientes do banco de dados e os exibe no Treeview,
    armazenando o ID do cliente na propriedade 'text' de cada item.

    Args:
        tree (ttk.Treeview): O Treeview onde os clientes serão exibidos.
    """
    # Limpa qualquer item existente no Treeview antes de carregar os dados
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cpf_cnpj, telefone, email, cep, rua, numero, complemento, bairro, cidade, estado FROM clientes") # Incluímos o 'id' na consulta
        clientes = cursor.fetchall()

        for cliente in clientes:
            tree.insert("", "end", text=cliente[0], values=cliente[1:]) # Usamos cliente[0] (o id) como 'text' e o resto como 'values'

    except sqlite3.Error as e:
        messagebox.showerror("Erro ao Carregar Clientes", f"Ocorreu um erro ao carregar os clientes: {e}")
    finally:
        if conn:
            conn.close()
    

def criar_aba_clientes(notebook, salvar_cliente_func, excluir_cliente_func, limpar_campos_cliente_func, novo_cliente_func, editar_cliente_func, buscar_cep_func, formatar_cpf_cnpj_func, formatar_telefone_func, exibir_clientes_func):
    """
    Cria e configura a aba de Clientes dentro do notebook principal.

    Esta aba contém formulários para inserir e editar informações de clientes,
    uma Treeview para exibir a lista de clientes e botões para realizar
    ações como novo, editar, excluir, salvar e limpar.

    Args:
        notebook (ttk.Notebook): O widget notebook ao qual esta aba será adicionada.
        salvar_cliente_func (callable): Função a ser chamada ao clicar no botão "Salvar".
        excluir_cliente_func (callable): Função a ser chamada ao clicar no botão "Excluir".
        limpar_campos_cliente_func (callable): Função a ser chamada ao clicar no botão "Limpar".
        novo_cliente_func (callable): Função a ser chamada ao clicar no botão "Novo".
        editar_cliente_func (callable): Função a ser chamada ao clicar no botão "Editar".
        buscar_cep_func (callable): Função a ser chamada para buscar o endereço pelo CEP.
        formatar_cpf_cnpj_func (callable): Função para formatar o campo CPF/CNPJ.
        formatar_telefone_func (callable): Função para formatar o campo Telefone.
        exibir_clientes_func (callable): Função para exibir os clientes no Treeview.
    """
    aba_clientes = ttk.Frame(notebook)

    # --- Configuração de Pesos (Layout Responsivo) ---
    # Define como as linhas e colunas da aba se redimensionam com a janela.
    aba_clientes.columnconfigure(0, weight=1)  # Coluna para rótulos (expande)
    aba_clientes.columnconfigure(1, weight=2)  # Coluna para entradas (expande mais)
    aba_clientes.columnconfigure(2, weight=1)  # Coluna para rótulos (expande)
    aba_clientes.columnconfigure(3, weight=2)  # Coluna para entradas (expande mais)
    aba_clientes.rowconfigure(0, weight=0)     # Linha para info pessoal
    aba_clientes.rowconfigure(1, weight=0)     # Linha para info pessoal
    aba_clientes.rowconfigure(2, weight=0)     # Linha para endereço (CEP e Buscar)
    aba_clientes.rowconfigure(3, weight=0)     # Linha para endereço (Rua e Número)
    aba_clientes.rowconfigure(4, weight=0)     # Linha para endereço (Complemento e Bairro)
    aba_clientes.rowconfigure(5, weight=0)     # Linha para endereço (Cidade e Estado)
    aba_clientes.rowconfigure(6, weight=1)     # Linha para o Treeview (expande verticalmente)
    aba_clientes.rowconfigure(7, weight=0)     # Linha para os botões

    # --- Frame para Informações Pessoais ---
    frame_info_pessoal = ttk.LabelFrame(aba_clientes, text="Informações Pessoais")
    frame_info_pessoal.grid(row=0, column=0, columnspan=4, sticky='ew', padx=10, pady=5)
    frame_info_pessoal.columnconfigure(1, weight=1)
    frame_info_pessoal.columnconfigure(3, weight=1)

    # Rótulo e Entrada para Nome
    lbl_nome = ttk.Label(frame_info_pessoal, text="Nome:")
    entry_nome = ttk.Entry(frame_info_pessoal)
    lbl_erro_nome = ttk.Label(frame_info_pessoal, text="", foreground="red")
    lbl_nome.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entry_nome.grid(row=0, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_nome.grid(row=0, column=4, sticky='w', padx=5)

    # Rótulo e Entrada para CPF/CNPJ
    lbl_cpf_cnpj = ttk.Label(frame_info_pessoal, text="CPF/CNPJ:")
    entry_cpf_cnpj = ttk.Entry(frame_info_pessoal)
    lbl_erro_cpf_cnpj = ttk.Label(frame_info_pessoal, text="", foreground="red")
    lbl_cpf_cnpj.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entry_cpf_cnpj.bind("<KeyRelease>", lambda event: formatar_cpf_cnpj_func(event, entry_cpf_cnpj))
    entry_cpf_cnpj.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_cpf_cnpj.grid(row=1, column=4, sticky='w', padx=5)

    # Rótulo e Entrada para Telefone
    lbl_telefone = ttk.Label(frame_info_pessoal, text="Telefone:")
    entry_telefone = ttk.Entry(frame_info_pessoal)
    lbl_erro_telefone = ttk.Label(frame_info_pessoal, text="", foreground="red")
    lbl_telefone.grid(row=1, column=2, sticky='w', padx=5, pady=5)
    entry_telefone.grid(row=1, column=3, sticky='ew', padx=5, pady=5)
    lbl_erro_telefone.grid(row=1, column=5, sticky='w', padx=5)
    entry_telefone.bind("<KeyRelease>", lambda event: formatar_telefone_func(event, entry_telefone))

    # Rótulo e Entrada para Email
    lbl_email = ttk.Label(frame_info_pessoal, text="Email:")
    entry_email = ttk.Entry(frame_info_pessoal)
    lbl_erro_email = ttk.Label(frame_info_pessoal, text="", foreground="red")
    lbl_email.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    entry_email.grid(row=2, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_email.grid(row=2, column=4, sticky='w', padx=5)

    # --- Frame para Endereço ---
    frame_endereco = ttk.LabelFrame(aba_clientes, text="Endereço")
    frame_endereco.grid(row=2, column=0, columnspan=4, sticky='ew', padx=10, pady=5)
    frame_endereco.columnconfigure(1, weight=1)
    frame_endereco.columnconfigure(3, weight=1)

    # Rótulo, Entrada e Botão para CEP
    lbl_cep = ttk.Label(frame_endereco, text="CEP:")
    entry_cep = ttk.Entry(frame_endereco, width=10)
    lbl_erro_cep = ttk.Label(frame_endereco, text="", foreground="red")
    btn_buscar_cep = ttk.Button(frame_endereco, text="Buscar CEP", command=lambda: buscar_cep_func(
        entry_cep, entry_rua, entry_bairro, entry_cidade, entry_estado, entry_numero
    ))
    lbl_cep.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entry_cep.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    btn_buscar_cep.grid(row=0, column=2, sticky='ew', padx=5, pady=5)
    lbl_erro_cep.grid(row=0, column=3, sticky='w', padx=5)
    # Evento para buscar endereço ao perder o foco do campo CEP
    entry_cep.bind("<FocusOut>", lambda event: buscar_cep_func(
        entry_cep, entry_rua, entry_bairro, entry_cidade, entry_estado, entry_numero
    ))

    # Rótulo e Entrada para Rua
    lbl_rua = ttk.Label(frame_endereco, text="Rua:")
    entry_rua = ttk.Entry(frame_endereco)
    lbl_erro_rua = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_rua.grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entry_rua.grid(row=1, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_rua.grid(row=1, column=4, sticky='w', padx=5)

    lbl_numero = ttk.Label(frame_endereco, text="Número:")
    entry_numero = ttk.Entry(frame_endereco, width=10)
    lbl_erro_numero = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_numero.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    entry_numero.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_numero.grid(row=2, column=4, sticky='w', padx=5)

    lbl_complemento = ttk.Label(frame_endereco, text="Complemento:")
    entry_complemento = ttk.Entry(frame_endereco)
    lbl_erro_complemento = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_complemento.grid(row=2, column=2, sticky='w', padx=5, pady=5)
    entry_complemento.grid(row=2, column=3, sticky='ew', padx=5, pady=5)
    lbl_erro_complemento.grid(row=2, column=5, sticky='w', padx=5)

    # Rótulo e Entrada para Bairro
    lbl_bairro = ttk.Label(frame_endereco, text="Bairro:")
    entry_bairro = ttk.Entry(frame_endereco)
    lbl_erro_bairro = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_bairro.grid(row=3, column=0, sticky='w', padx=5, pady=5)
    entry_bairro.grid(row=3, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
    lbl_erro_bairro.grid(row=3, column=4, sticky='w', padx=5)

    # Rótulo e Entrada para Cidade
    lbl_cidade = ttk.Label(frame_endereco, text="Cidade:")
    entry_cidade = ttk.Entry(frame_endereco)
    lbl_erro_cidade = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_cidade.grid(row=4, column=0, sticky='w', padx=5, pady=5)
    entry_cidade.grid(row=4, column=1, sticky='ew', padx=5, pady=5)
    lbl_erro_cidade.grid(row=4, column=4, sticky='w', padx=5)

    # Rótulo e Entrada para Estado
    lbl_estado = ttk.Label(frame_endereco, text="Estado:")
    entry_estado = ttk.Entry(frame_endereco, width=5)
    lbl_erro_estado = ttk.Label(frame_endereco, text="", foreground="red")
    lbl_estado.grid(row=4, column=2, sticky='w', padx=5, pady=5)
    entry_estado.grid(row=4, column=3, sticky='ew', padx=5, pady=5)
    lbl_erro_estado.grid(row=4, column=5, sticky='w', padx=5)

    # --- Treeview para Listar Clientes ---

    treeview_clientes = ttk.Treeview(aba_clientes, columns=("Nome", "CPF/CNPJ", "Telefone", "Email", "CEP", "Rua", "Número", "Complemento", "Bairro", "Cidade", "Estado"))

    # Configuração dos cabeçalhos das colunas
    treeview_clientes.heading("#0", text="")  # Coluna vazia para o índice
    treeview_clientes.heading("Nome", text="Nome")
    treeview_clientes.heading("CPF/CNPJ", text="CPF/CNPJ")
    treeview_clientes.heading("Telefone", text="Telefone")
    treeview_clientes.heading("Email", text="Email")
    treeview_clientes.heading("CEP", text="CEP")
    treeview_clientes.heading("Rua", text="Rua")
    treeview_clientes.heading("Número", text="Número")
    treeview_clientes.heading("Complemento", text="Complemento")
    treeview_clientes.heading("Bairro", text="Bairro")
    treeview_clientes.heading("Cidade", text="Cidade")
    treeview_clientes.heading("Estado", text="Estado")

    # Configuração da largura das colunas (opcional)
    treeview_clientes.column("#0", width=0, stretch=tk.NO)  # Oculta a coluna do índice
    treeview_clientes.column("Nome", width=150)
    treeview_clientes.column("CPF/CNPJ", width=120)
    treeview_clientes.column("Telefone", width=100)
    treeview_clientes.column("Email", width=200)
    treeview_clientes.column("CEP", width=80)
    treeview_clientes.column("Rua", width=150)
    treeview_clientes.column("Número", width=60)
    treeview_clientes.column("Complemento", width=100)
    treeview_clientes.column("Bairro", width=100)
    treeview_clientes.column("Cidade", width=100)
    treeview_clientes.column("Estado", width=50)

    treeview_clientes.grid(row=6, column=0, columnspan=4, sticky='ewsn', padx=10, pady=5)

    # --- Frame para Botões de Ação ---
    frame_botoes_clientes = ttk.Frame(aba_clientes)
    frame_botoes_clientes.grid(row=7, column=0, columnspan=4, sticky='ew', padx=10, pady=10)

    # Botão "Novo Cliente"
    btn_novo_cliente = ttk.Button(frame_botoes_clientes, text="Novo", command=lambda: novo_cliente_func(
        entry_nome, entry_cpf_cnpj, entry_telefone, entry_email,
        entry_cep, entry_rua, entry_numero, entry_complemento, entry_bairro, entry_cidade, entry_estado,
        lbl_erro_nome, lbl_erro_cpf_cnpj, lbl_erro_telefone, lbl_erro_email,
        lbl_erro_cep, lbl_erro_rua, lbl_erro_numero, lbl_erro_complemento, lbl_erro_bairro, lbl_erro_cidade, lbl_erro_estado
    ))
    btn_novo_cliente.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    # Botão "Editar Cliente"
    btn_editar_cliente = ttk.Button(frame_botoes_clientes, text="Editar", command=lambda: editar_cliente_func(treeview_clientes,
        entry_nome, entry_cpf_cnpj, entry_telefone, entry_email,
        entry_cep, entry_rua, entry_numero, entry_complemento, entry_bairro, entry_cidade, entry_estado,
        lbl_erro_nome, lbl_erro_cpf_cnpj, lbl_erro_telefone, lbl_erro_email,
        lbl_erro_cep, lbl_erro_rua, lbl_erro_numero, lbl_erro_complemento, lbl_erro_bairro, lbl_erro_cidade, lbl_erro_estado
    ))
    btn_editar_cliente.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    # Botão "Excluir Cliente"
    btn_excluir_cliente = ttk.Button(frame_botoes_clientes, text="Excluir", command=lambda: excluir_cliente_func(treeview_clientes))
    btn_excluir_cliente.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    # Botão "Salvar"
    btn_salvar = ttk.Button(frame_botoes_clientes, text="Salvar", command=lambda: salvar_cliente_func(
        entry_nome, entry_cpf_cnpj, entry_telefone, entry_email,
        entry_cep, entry_rua, entry_numero, entry_complemento, entry_bairro, entry_cidade, entry_estado,
        lbl_erro_nome, lbl_erro_cpf_cnpj, lbl_erro_telefone, lbl_erro_email,
        lbl_erro_numero, lbl_erro_complemento, lbl_erro_cep, lbl_erro_rua, lbl_erro_bairro,
        lbl_erro_cidade, lbl_erro_estado, treeview_clientes
    ))
    btn_salvar.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

    # Botão "Limpar"
    btn_limpar = ttk.Button(frame_botoes_clientes, text="Limpar", command=lambda: limpar_campos_cliente_func(
        entry_nome, entry_cpf_cnpj, entry_telefone, entry_email,
        entry_cep, entry_rua, entry_numero, entry_complemento, entry_bairro, entry_cidade, entry_estado,
        lbl_erro_nome, lbl_erro_cpf_cnpj, lbl_erro_telefone, lbl_erro_email,
        lbl_erro_cep, lbl_erro_rua, lbl_erro_numero, lbl_erro_complemento, lbl_erro_bairro, lbl_erro_cidade, lbl_erro_estado
    ))
    btn_limpar.grid(row=0, column=4, padx=10, pady=10, sticky='ew')

    # Configuração de pesos para as colunas do frame de botões
    frame_botoes_clientes.columnconfigure(0, weight=1)  # Para os botões expandirem igualmente
    frame_botoes_clientes.columnconfigure(1, weight=1)
    frame_botoes_clientes.columnconfigure(2, weight=1)
    frame_botoes_clientes.columnconfigure(3, weight=1)
    frame_botoes_clientes.columnconfigure(4, weight=1)

    # Carrega e exibe os clientes no Treeview
    exibir_clientes_func(treeview_clientes)
    # Adiciona a aba de clientes ao notebook
    notebook.add(aba_clientes, text="Clientes")

    return aba_clientes


# Importe a função buscar_endereco_por_cep se ela estiver em outro módulo
# from buscar_endereco_por_cep import buscar_endereco_por_cep

# --- Funções de lógica/manipulação de dados (exemplo - a implementar) ---
lista_de_tecnicos = []

# --- Funções de formatação (para CPF e Telefone) ---
def formatar_cpf(event):
    texto = entry_cpf_tecnico.get()
    texto = ''.join(filter(str.isdigit, texto))  # Mantém apenas os dígitos
    if len(texto) <= 11:
        novo_texto = ''
        for i, char in enumerate(texto):
            novo_texto += char
            if i in [2, 5]:
                novo_texto += '.'
            elif i == 8:
                novo_texto += '-'
        entry_cpf_tecnico.delete(0, tk.END)
        entry_cpf_tecnico.insert(0, novo_texto)

def formatar_telefone(event):
    texto = entry_telefone_tecnico.get()
    texto = ''.join(filter(str.isdigit, texto))
    if len(texto) <= 11:
        novo_texto = ''
        for i, char in enumerate(texto):
            novo_texto += char
            if i == 0 and len(texto) > 1:
                novo_texto = '(' + novo_texto
            elif i == 1 and len(texto) > 1:
                novo_texto += ')'
            elif i == 6:
                novo_texto += '-'
        entry_telefone_tecnico.delete(0, tk.END)
        entry_telefone_tecnico.insert(0, novo_texto)

# --- Funções de lógica/manipulação de dados ---
lista_de_tecnicos = []
indice_editando = None #variavel global para armazenar o indice do tecnico que esta sendo editado

# --- Variáveis globais ---
entry_nome_tecnico = None
entry_cpf_tecnico = None
entry_especialidade_tecnico = None
entry_cep_tecnico = None
entry_rua_tecnico = None
entry_bairro_tecnico = None
entry_cidade_tecnico = None
entry_estado_tecnico = None
entry_telefone_tecnico = None
entry_email_tecnico = None
entry_funcao_tecnico = None
tree_tecnicos = None
indice_editando = None
btn_salvar_tecnico = None  # Declarando o botão globalmente

# --- Funções do Banco de Dados ---
def criar_tabela_tecnicos():
    """Cria a tabela 'tecnicos' no banco de dados, se ela não existir."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                especialidade TEXT NOT NULL,
                cep TEXT NOT NULL,
                rua TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL,
                funcao TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela: {e}")

# --- Funções ---
def salvar_tecnico():
    """Salva os dados do técnico no banco de dados."""
    nome = entry_nome_tecnico.get()
    cpf = entry_cpf_tecnico.get()
    especialidade = entry_especialidade_tecnico.get()
    cep = entry_cep_tecnico.get()
    rua = entry_rua_tecnico.get()
    bairro = entry_bairro_tecnico.get()
    cidade = entry_cidade_tecnico.get()
    estado = entry_estado_tecnico.get()
    telefone = entry_telefone_tecnico.get()
    email = entry_email_tecnico.get()
    funcao = entry_funcao_tecnico.get()

    if not all([nome, cpf, especialidade, cep, rua, bairro, cidade, estado, telefone, email, funcao]):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
        return

    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()

        # Verifica se o CPF já existe
        cursor.execute("SELECT id FROM tecnicos WHERE cpf=?", (cpf,))
        resultado = cursor.fetchone()
        if resultado:
            messagebox.showerror("Erro", "CPF já cadastrado.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO tecnicos (nome, cpf, especialidade, cep, rua, bairro, cidade, estado, telefone, email, funcao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, cpf, especialidade, cep, rua, bairro, cidade, estado, telefone, email, funcao))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Técnico cadastrado com sucesso!")
        atualizar_lista_tecnicos()
        limpar_campos_tecnico()

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar técnico: {e}")

def limpar_campos_tecnico():
    """Limpa os campos do formulário."""
    entry_nome_tecnico.delete(0, tk.END)
    entry_cpf_tecnico.delete(0, tk.END)
    entry_especialidade_tecnico.delete(0, tk.END)
    entry_cep_tecnico.delete(0, tk.END)
    entry_rua_tecnico.delete(0, tk.END)
    entry_bairro_tecnico.delete(0, tk.END)
    entry_cidade_tecnico.delete(0, tk.END)
    entry_estado_tecnico.delete(0, tk.END)
    entry_telefone_tecnico.delete(0, tk.END)
    entry_email_tecnico.delete(0, tk.END)
    entry_funcao_tecnico.delete(0, tk.END)
    btn_salvar_tecnico.config(text="Salvar", command=salvar_tecnico) # Reseta o botão para "Salvar"

def excluir_tecnico():
    """Exclui o técnico selecionado do banco de dados."""
    selecionado = tree_tecnicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_tecnico = tree_tecnicos.item(selecionado[0], 'values')[0]
            cursor.execute("DELETE FROM tecnicos WHERE id=?", (id_tecnico,))
            conn.commit()
            conn.close()
            atualizar_lista_tecnicos()
            messagebox.showinfo("Sucesso", "Técnico excluído com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir técnico: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um técnico para excluir.")

def editar_tecnico():
    """Edita o técnico selecionado no banco de dados."""
    selecionado = tree_tecnicos.selection()
    if selecionado:
        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            id_tecnico = tree_tecnicos.item(selecionado[0], 'values')[0]

            cursor.execute("SELECT * FROM tecnicos WHERE id=?", (id_tecnico,))
            tecnico = cursor.fetchone()
            conn.close()

            if tecnico:
                entry_nome_tecnico.delete(0, tk.END)
                entry_nome_tecnico.insert(0, tecnico[1])
                entry_cpf_tecnico.delete(0, tk.END)
                entry_cpf_tecnico.insert(0, tecnico[2])
                entry_especialidade_tecnico.delete(0, tk.END)
                entry_especialidade_tecnico.insert(0, tecnico[3])
                entry_cep_tecnico.delete(0, tk.END)
                entry_cep_tecnico.insert(0, tecnico[4])
                entry_rua_tecnico.delete(0, tk.END)
                entry_rua_tecnico.insert(0, tecnico[5])
                entry_bairro_tecnico.delete(0, tk.END)
                entry_bairro_tecnico.insert(0, tecnico[6])
                entry_cidade_tecnico.delete(0, tk.END)
                entry_cidade_tecnico.insert(0, tecnico[7])
                entry_estado_tecnico.delete(0, tk.END)
                entry_estado_tecnico.insert(0, tecnico[8])
                entry_telefone_tecnico.delete(0, tk.END)
                entry_telefone_tecnico.insert(0, tecnico[9])
                entry_email_tecnico.delete(0, tk.END)
                entry_email_tecnico.insert(0, tecnico[10])
                entry_funcao_tecnico.delete(0, tk.END)
                entry_funcao_tecnico.insert(0, tecnico[11])

                global indice_editando
                indice_editando = id_tecnico
                btn_salvar_tecnico.config(text="Atualizar", command=atualizar_tecnico) # Modifica o texto do botão para "Atualizar" e muda o comando
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao editar técnico: {e}")
    else:
        messagebox.showerror("Erro", "Selecione um técnico para editar.")

def atualizar_tecnico():
    """Atualiza os dados do técnico no banco de dados."""
    global indice_editando
    if indice_editando:
        nome = entry_nome_tecnico.get()
        cpf = entry_cpf_tecnico.get()
        especialidade = entry_especialidade_tecnico.get()
        cep = entry_cep_tecnico.get()
        rua = entry_rua_tecnico.get()
        bairro = entry_bairro_tecnico.get()
        cidade = entry_cidade_tecnico.get()
        estado = entry_estado_tecnico.get()
        telefone = entry_telefone_tecnico.get()
        email = entry_email_tecnico.get()
        funcao = entry_funcao_tecnico.get()

        if not all([nome, cpf, especialidade, cep, rua, bairro, cidade, estado, telefone, email, funcao]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

        try:
            conn = sqlite3.connect("banco_de_dados.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tecnicos SET 
                    nome=?, cpf=?, especialidade=?, cep=?, rua=?, bairro=?, cidade=?, estado=?, 
                    telefone=?, email=?, funcao=?
                WHERE id=?
            """, (nome, cpf, especialidade, cep, rua, bairro, cidade, estado, telefone, email, funcao, indice_editando))
            conn.commit()
            conn.close()
            atualizar_lista_tecnicos()
            limpar_campos_tecnico()
            btn_salvar_tecnico.config(text="Salvar", command=salvar_tecnico) # Reseta o botão para "Salvar" após atualizar
            indice_editando = None
            messagebox.showinfo("Sucesso", "Técnico atualizado com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar técnico: {e}")
    else:
        messagebox.showerror("Erro", "Nenhum técnico para atualizar.")

def atualizar_lista_tecnicos():
    """Atualiza a Treeview com os dados do banco de dados."""
    try:
        conn = sqlite3.connect("banco_de_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tecnicos")
        tecnicos = cursor.fetchall()
        conn.close()

        for item in tree_tecnicos.get_children():
            tree_tecnicos.delete(item)

        for tecnico in tecnicos:
            endereco_completo = f"{tecnico[5]}, {tecnico[6]}, {tecnico[7]} - {tecnico[8]}"
            tree_tecnicos.insert("", tk.END, values=(tecnico[0], tecnico[1], tecnico[2], tecnico[3], endereco_completo, tecnico[9], tecnico[10], tecnico[11]))
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao atualizar lista de técnicos: {e}")

def buscar_cep_tecnico():
    """Busca o CEP e preenche os campos de endereço."""
    cep = entry_cep_tecnico.get().replace('-', '').strip()
    if not cep or len(cep) != 8 or not cep.isdigit():
        messagebox.showerror("Erro", "CEP inválido.")
        return

    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "erro" in data:
            messagebox.showerror("Erro", "CEP não encontrado.")
        else:
            entry_rua_tecnico.delete(0, tk.END)
            entry_rua_tecnico.insert(0, data.get("logradouro", ""))
            entry_bairro_tecnico.delete(0, tk.END)
            entry_bairro_tecnico.insert(0, data.get("bairro", ""))
            entry_cidade_tecnico.delete(0, tk.END)
            entry_cidade_tecnico.insert(0, data.get("localidade", ""))
            entry_estado_tecnico.delete(0, tk.END)
            entry_estado_tecnico.insert(0, data.get("uf", ""))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao buscar CEP: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Erro", "Resposta inválida do servidor de CEP.")

def formatar_cpf(event):
    """Formata o CPF no formato XXX.XXX.XXX-XX enquanto o usuário digita."""
    texto = entry_cpf_tecnico.get().replace('.', '').replace('-', '')
    novo_texto = ''
    i = 0
    for c in texto:
        if i == 3 or i == 6:
            novo_texto += '.'
        elif i == 9:
            novo_texto += '-'
        novo_texto += c
        i += 1
    entry_cpf_tecnico.delete(0, tk.END)
    entry_cpf_tecnico.insert(0, novo_texto)

def formatar_telefone(entry: ttk.Entry) -> None:
    """Função para formatar o telefone (simulada)."""
    texto = entry.get()
    texto = texto.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    tamanho = len(texto)
    if tamanho == 0:
        return
    elif tamanho == 1:
        texto = "(" + texto
    elif tamanho == 2:
        texto = "(" + texto + ")"
    elif tamanho > 2 and tamanho <= 6:
        texto = "(" + texto[:2] + ") " + texto[2:]
    elif tamanho > 6:
        texto = "(" + texto[:2] + ") " + texto[2:6] + "-" + texto[6:]
    entry.delete(0, tk.END)
    entry.insert(0, texto)

# ...

entry_telefone.bind("<KeyRelease>", lambda event: formatar_telefone(entry_telefone))

# --- Função de criação da aba de Técnicos ---
def criar_aba_tecnicos(notebook):
    """Cria a aba de Técnicos na interface."""
    global entry_nome_tecnico, entry_cpf_tecnico, entry_especialidade_tecnico
    global entry_cep_tecnico, entry_rua_tecnico, entry_bairro_tecnico, entry_cidade_tecnico, entry_estado_tecnico
    global entry_telefone_tecnico, entry_email_tecnico, entry_funcao_tecnico, tree_tecnicos, btn_salvar_tecnico # Adicionado btn_salvar_tecnico

    aba_tecnicos = ttk.Frame(notebook)
    notebook.add(aba_tecnicos, text='Técnicos')

    # --- Frame para o formulário de cadastro de técnicos ---
    frame_cadastro_tecnico = ttk.LabelFrame(aba_tecnicos, text="Cadastro de Técnico", padding=10)
    frame_cadastro_tecnico.pack(padx=10, pady=10, fill='x')

    # Labels e Entries
    lbl_nome_tecnico = ttk.Label(frame_cadastro_tecnico, text="Nome:")
    lbl_nome_tecnico.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nome_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_nome_tecnico.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    lbl_cpf_tecnico = ttk.Label(frame_cadastro_tecnico, text="CPF:")
    lbl_cpf_tecnico.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_cpf_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_cpf_tecnico.bind("<KeyRelease>", formatar_cpf)
    entry_cpf_tecnico.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    lbl_especialidade_tecnico = ttk.Label(frame_cadastro_tecnico, text="Especialidade:")
    lbl_especialidade_tecnico.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_especialidade_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_especialidade_tecnico.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    lbl_cep_tecnico = ttk.Label(frame_cadastro_tecnico, text="CEP:")
    lbl_cep_tecnico.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_cep_tecnico = ttk.Entry(frame_cadastro_tecnico, width=10)
    entry_cep_tecnico.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    btn_buscar_cep = ttk.Button(frame_cadastro_tecnico, text="Buscar", command=buscar_cep_tecnico)
    btn_buscar_cep.grid(row=3, column=2, padx=5, pady=5, sticky='w')

    lbl_rua_tecnico = ttk.Label(frame_cadastro_tecnico, text="Rua:")
    lbl_rua_tecnico.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    entry_rua_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_rua_tecnico.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

    lbl_bairro_tecnico = ttk.Label(frame_cadastro_tecnico, text="Bairro:")
    lbl_bairro_tecnico.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    entry_bairro_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_bairro_tecnico.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    lbl_cidade_tecnico = ttk.Label(frame_cadastro_tecnico, text="Cidade:")
    lbl_cidade_tecnico.grid(row=6, column=0, padx=5, pady=5, sticky='w')
    entry_cidade_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_cidade_tecnico.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

    lbl_estado_tecnico = ttk.Label(frame_cadastro_tecnico, text="Estado (UF):")
    lbl_estado_tecnico.grid(row=7, column=0, padx=5, pady=5, sticky='w')
    entry_estado_tecnico = ttk.Entry(frame_cadastro_tecnico, width=5)
    entry_estado_tecnico.grid(row=7, column=1, padx=5, pady=5, sticky='w')

    lbl_telefone_tecnico = ttk.Label(frame_cadastro_tecnico, text="Telefone:")
    lbl_telefone_tecnico.grid(row=8, column=0, padx=5, pady=5, sticky='w')
    entry_telefone_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_telefone_tecnico.bind("<KeyRelease>", formatar_telefone)
    entry_telefone_tecnico.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

    lbl_email_tecnico = ttk.Label(frame_cadastro_tecnico, text="E-mail:")
    lbl_email_tecnico.grid(row=9, column=0, padx=5, pady=5, sticky='w')
    entry_email_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_email_tecnico.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

    lbl_funcao_tecnico = ttk.Label(frame_cadastro_tecnico, text="Função:")
    lbl_funcao_tecnico.grid(row=10, column=0, padx=5, pady=5, sticky='w')
    entry_funcao_tecnico = ttk.Entry(frame_cadastro_tecnico)
    entry_funcao_tecnico.grid(row=10, column=1, padx=5, pady=5, sticky='ew')

    # --- Frame para os botões de ação ---
    frame_botoes_tecnico = ttk.Frame(aba_tecnicos)
    frame_botoes_tecnico.pack(pady=10, padx=10, fill='x')

    btn_novo_tecnico = ttk.Button(frame_botoes_tecnico, text="Novo", command=limpar_campos_tecnico)
    btn_novo_tecnico.pack(side='left', padx=5)

    btn_salvar_tecnico = ttk.Button(frame_botoes_tecnico, text="Salvar", command=salvar_tecnico) # Cria o botão "Salvar"
    btn_salvar_tecnico.pack(side='left', padx=5)

    btn_editar_tecnico = ttk.Button(frame_botoes_tecnico, text="Editar", command=editar_tecnico)
    btn_editar_tecnico.pack(side='left', padx=5)

    btn_excluir_tecnico = ttk.Button(frame_botoes_tecnico, text="Excluir", command=excluir_tecnico)
    btn_excluir_tecnico.pack(side='left', padx=5)

    # --- Frame para a listagem de técnicos ---
    frame_lista_tecnicos = ttk.LabelFrame(aba_tecnicos, text="Técnicos Cadastrados", padding=10)
    frame_lista_tecnicos.pack(padx=10, pady=10, fill='both', expand=True)

    # Treeview para listar os técnicos
    tree_tecnicos = ttk.Treeview(frame_lista_tecnicos,
                                 columns=("ID", "Nome", "CPF", "Especialidade", "Endereço", "Telefone", "Email", "Função"),
                                 show='headings')
    tree_tecnicos.heading("ID", text="ID")
    tree_tecnicos.heading("Nome", text="Nome")
    tree_tecnicos.heading("CPF", text="CPF")
    tree_tecnicos.heading("Especialidade", text="Especialidade")
    tree_tecnicos.heading("Endereço", text="Endereço")
    tree_tecnicos.heading("Telefone", text="Telefone")
    tree_tecnicos.heading("Email", text="E-mail")
    tree_tecnicos.heading("Função", text="Função")
    tree_tecnicos.pack(fill='both', expand=True)

    # Chamando as funções
    criar_tabela_tecnicos()
    atualizar_lista_tecnicos()

    return aba_tecnicos

def novo_cliente(nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, #já conferido
                cep_entry, rua_entry, numero_entry, complemento_entry,
                bairro_entry, cidade_entry, estado_entry,
                erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                erro_email_label, erro_cep_label, erro_rua_label,
                erro_numero_label, erro_complemento_label, erro_bairro_label,
                erro_cidade_label, erro_estado_label):
    """
    Limpa o conteúdo dos campos de entrada e as mensagens de erro na aba de clientes,
    preparando para a inserção de um novo cliente.

    Args:
        nome_entry (tk.Entry): Widget Entry para o nome do cliente.
        cpf_cnpj_entry (tk.Entry): Widget Entry para o CPF/CNPJ do cliente.
        telefone_entry (tk.Entry): Widget Entry para o telefone do cliente.
        email_entry (tk.Entry): Widget Entry para o email do cliente.
        cep_entry (tk.Entry): Widget Entry para o CEP do cliente.
        rua_entry (tk.Entry): Widget Entry para a rua do cliente.
        numero_entry (tk.Entry): Widget Entry para o número do endereço do cliente.
        complemento_entry (tk.Entry): Widget Entry para o complemento do endereço do cliente.
        bairro_entry (tk.Entry): Widget Entry para o bairro do cliente.
        cidade_entry (tk.Entry): Widget Entry para a cidade do cliente.
        estado_entry (tk.Entry): Widget Entry para o estado do cliente.
        erro_nome_label (tk.Label): Label para exibir erros no nome.
        erro_cpf_cnpj_label (tk.Label): Label para exibir erros no CPF/CNPJ.
        erro_telefone_label (tk.Label): Label para exibir erros no telefone.
        erro_email_label (tk.Label): Label para exibir erros no email.
        erro_cep_label (tk.Label): Label para exibir erros no CEP.
        erro_rua_label (tk.Label): Label para exibir erros na rua.
        erro_numero_label (tk.Label): Label para exibir erros no número.
        erro_complemento_label (tk.Label): Label para exibir erros no complemento.
        erro_bairro_label (tk.Label): Label para exibir erros no bairro.
        erro_cidade_label (tk.Label): Label para exibir erros na cidade.
        erro_estado_label (tk.Label): Label para exibir erros no estado.
    """
    # Limpar o conteúdo dos campos de entrada
    nome_entry.delete(0, tk.END)
    cpf_cnpj_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    cep_entry.delete(0, tk.END)
    rua_entry.delete(0, tk.END)
    numero_entry.delete(0, tk.END)
    complemento_entry.delete(0, tk.END)
    bairro_entry.delete(0, tk.END)
    cidade_entry.delete(0, tk.END)
    estado_entry.delete(0, tk.END)

    # Limpar as mensagens de erro
    erro_nome_label.config(text="")
    erro_cpf_cnpj_label.config(text="")
    erro_telefone_label.config(text="")
    erro_email_label.config(text="")
    erro_cep_label.config(text="")
    erro_rua_label.config(text="")
    erro_numero_label.config(text="")
    erro_complemento_label.config(text="")
    erro_bairro_label.config(text="")
    erro_cidade_label.config(text="")
    erro_estado_label.config(text="")

    # Remover estilos de erro (assumindo que 'remover_estilo_erro' é uma função definida em outro lugar)
    remover_estilo_erro(nome_entry)
    remover_estilo_erro(cpf_cnpj_entry)
    remover_estilo_erro(telefone_entry)
    remover_estilo_erro(email_entry)
    remover_estilo_erro(cep_entry)
    remover_estilo_erro(rua_entry)
    remover_estilo_erro(numero_entry)
    remover_estilo_erro(complemento_entry)
    remover_estilo_erro(bairro_entry)
    remover_estilo_erro(cidade_entry)
    remover_estilo_erro(estado_entry)

def editar_cliente(treeview, nome_entry, cpf_cnpj_entry, telefone_entry, email_entry, # já conferido
                   cep_entry, rua_entry, numero_entry, complemento_entry,
                   bairro_entry, cidade_entry, estado_entry,
                   erro_nome_label, erro_cpf_cnpj_label, erro_telefone_label,
                   erro_email_label, erro_cep_label, erro_rua_label,
                   erro_numero_label, erro_complemento_label, erro_bairro_label,
                   erro_cidade_label, erro_estado_label):
    global modo_edicao_cliente
    global id_cliente_editando
    
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um cliente para editar.")
        return

    item_interno_id = selected_item[0]
    item_info = treeview.item(item_interno_id)
    id_cliente = item_info['text']
    
    id_cliente = item_info['text']
    
    values = item_info['values']
    if values:
        id_cliente_editando = id_cliente
        modo_edicao_cliente = True

        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, values[0])
        cpf_cnpj_entry.delete(0, tk.END)
        cpf_cnpj_entry.insert(0, values[1])
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, values[2])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[3])
        cep_entry.delete(0, tk.END)
        cep_entry.insert(0, values[4])
        rua_entry.delete(0, tk.END)
        rua_entry.insert(0, values[5])
        numero_entry.delete(0, tk.END)
        numero_entry.insert(0, values[6])
        complemento_entry.delete(0, tk.END)
        complemento_entry.insert(0, values[7])
        bairro_entry.delete(0, tk.END)
        bairro_entry.insert(0, values[8])
        cidade_entry.delete(0, tk.END)
        cidade_entry.insert(0, values[9])
        estado_entry.delete(0, tk.END)
        estado_entry.insert(0, values[10])

def criar_janela_principal():
    janela = ThemedTk()  # Usando o ThemedTk para habilitar temas
    janela.title("Ordem de Serviço JVV")
    janela.geometry("800x600")
    janela.minsize(700, 600)

    janela.grid_rowconfigure(0, weight=1) # Permite que a linha do notebook se expanda verticalmente
    janela.grid_rowconfigure(1, weight=0) # A linha do relógio não se expande verticalmente
    janela.grid_columnconfigure(0, weight=1) # Permite que a coluna se expanda horizontalmente

    # Escolha um tema da biblioteca ttkthemes (experimente outros!)
    # janela.set_theme("itft1")  # Tema atualmente ativo

    notebook = ttk.Notebook(janela)
    criar_aba_clientes(notebook, salvar_cliente, excluir_cliente, limpar_campos_cliente, novo_cliente, editar_cliente, buscar_endereco_por_cep, formatar_cpf_cnpj, formatar_telefone, exibir_clientes_func=exibir_clientes) # Correção: Adicionado exibir_clientes_func
    
    # Aba de Técnicos (segunda - NOVA POSIÇÃO)
    criar_aba_tecnicos(notebook)
    
    criar_aba_produtos(notebook, salvar_produto, limpar_campos_produtos, formatar_para_real, formatar_para_porcentagem, calcular_preco_venda)
    
    aba_servicos = criar_aba_servicos(notebook)
    
    aba_os = criar_aba_ordens_servico(notebook, janela)
    notebook.grid(row=0, column=0, sticky='nsew') # Usando grid para o notebook

    # --- Frame para o relógio ---
    frame_relogio = ttk.Frame(janela)
    frame_relogio.grid(row=1, column=0, sticky='ew', padx=10, pady=5) # Usando grid para o frame do relógio

    lbl_relogio = ttk.Label(frame_relogio, font=('calibri', 12, 'bold'), anchor='e')
    lbl_relogio.pack(side='right')

    def atualizar_relogio():
        now = datetime.now()
        data_formatada = now.strftime("%d/%m/%Y")
        hora_formatada = now.strftime("%H:%M:%S")
        lbl_relogio.config(text=f"{data_formatada} - {hora_formatada}")
        janela.after(1000, atualizar_relogio) # Atualiza a cada 1 segundo

    atualizar_relogio()

    janela.mainloop()

if __name__ == "__main__":
    # criar_tabela_produtos()  # Suas chamadas de criação de tabela
    # criar_tabela_clientes()
    # criar_tabela_servicos()

    criar_janela_principal() # A chamada para a função que inicia a interface
