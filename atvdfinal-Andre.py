from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import *
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime

app = Tk()
def comandos(*funcs):
   def combinedFunc(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
   return combinedFunc

class Conecta():
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except:
            print('Erro ao se conectar com o banco de dados')

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
class Janela(Frame):

    def __init__(self, master):
        self.font=('times', 13)
        self.master = master
        self.programa = app
        self.programa.resizable(True, True)
        self.home()

        self.db = Conecta('login.db')
        self.db1 = Conecta('manicure.db')

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
            username VARCHAR(10) NOT NULL PRIMARY KEY,
            senha VARCHAR(18) NOT NULL);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
            username VARCHAR(10) NOT NULL PRIMARY KEY,
            senha VARCHAR(18) NOT NULL);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone VARCHAR(20) NOT NULL,
            endereco TEXT NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            dataCadastro date
            );
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone VARCHAR(20) NOT NULL,
            endereco TEXT NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            especialidade TEXT NOT NULL ,
            dataContrato DATE);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            idCliente VARCHAR(11),
            idFuncionario VARCHAR(11),
            tipoServico TEXT, 
            descricao TEXT, 
            valor FLOAT, 
            data DATE);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            cpfCliente VARCHAR(13),
            data DATE,
            hora time);
            """)

        self.db.commit_db()

    def home(self):
        self.programa.title("Login")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=100, padx=10)

        self.nome = Label(self.cont1, width=13, text="Usuario: ", font=self.font)
        self.nome.pack(side=LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side=RIGHT)

        self.senha = Label(self.cont2, width=13, text="Senha: ", font=self.font)
        self.senha.pack(side=LEFT)

        self.senhaEntrada = Entry(self.cont2, show="*")
        self.senhaEntrada.pack(side=RIGHT)

        self.button1 = Button(self.cont3, text="Login Admin", width=13, command=self.realizarLoginUser, font=self.font)
        self.button1.pack(side=RIGHT)

        self.button1 = Button(self.cont3, text="Login Cliente", width=13, command=self.realizarLoginCliente, font=self.font)
        self.button1.pack(side=RIGHT)

        self.lb_cadastro = Label(self.cont4, text='Não é cadastrado?', font=self.font, width=13)
        self.lb_cadastro.pack(side=LEFT)

        self.button2 = Button(self.cont4, text="Cadastrar como Admin", width=20, command=lambda: comandos(self.delete(4), self.cadastroUser()), font=self.font)
        self.button2.pack(side=RIGHT)

        self.button3 = Button(self.cont4, text="Cadastrar como Cliente", width=25,
                              command=lambda: comandos(self.delete(4), self.CadastroCliente()), font=self.font)
        self.button3.pack(side=RIGHT)


    def realizarLoginUser(self):
        while True:
            username = self.nomeEntrada.get()

            self.db.cursor.execute("""
                SELECT * from admins WHERE username = ?;
                """, (username,))

            nickname = self.db.cursor.fetchall()
            if nickname:
                break
            else:
                msg.showwarning(message='Username inexistente. Por favor, tente novamente ou cadastre-se.')
                break

        while True:
            senha = self.senhaEntrada.get()

            self.db.cursor.execute("""
                SELECT senha FROM admins WHERE username = ?;
                """, (username,))

            password = self.db.cursor.fetchall()
            if senha == password[0][0]:
                self.funcFuncionario()
                break
            else:
                msg.showwarning(message='Senha inválida. Por favor, tente novamente.')
                break

    def realizarLoginCliente(self):
        while True:
            global username
            username = self.nomeEntrada.get()

            self.db1.cursor.execute("""
                SELECT * from usuarios WHERE username = ?;
                """, (username,))

            nickname = self.db1.cursor.fetchall()
            if nickname:
                break
            else:
                msg.showwarning(message='Username inexistente. Por favor, tente novamente ou cadastre-se.')
                break

        while True:
            senha = self.senhaEntrada.get()

            self.db1.cursor.execute("""
                SELECT senha FROM usuarios WHERE username = ?;
                """, (username,))

            password = self.db1.cursor.fetchall()
            if senha == password[0][0]:
                global atual
                self.db1.cursor.execute("""
                    select nome FROM clientes c
                    INNER JOIN usuarios u ON c.cpf = u.username and c.cpf = ?
                    """, (username,))
                atual = str(self.db1.cursor.fetchone())
                characters = "'(),"
                for x in range(len(characters)):
                    atual = atual.replace(characters[x], "")
                self.funcCliente()
                break
            else:
                msg.showwarning(message='Senha inválida. Por favor, tente novamente.')
                break

    def funcCliente(self):
        self.delete(4)

        self.programa.title("Página do Cliente")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack(anchor=S, expand=True, pady=5, padx=10)

        self.bemvindo = Label(self.cont1, text=f"Seja Bem Vindo {atual}", width=30, font=self.font)
        self.bemvindo.pack()

        self.button1 = Button(self.cont2, text = "Visualizar Atendimentos", width=20, command=self.visualizarAtendimentos, font=self.font)
        self.button1.pack()

        self.button2 = Button(self.cont3, text="Visualizar Agendamentos", width=20, command=self.visualizarAgendamentos, font=self.font)
        self.button2.pack()

        self.button3 = Button(self.cont4, text="Agendar Visita", width=20, command=self.agendarVisita, font=self.font)
        self.button3.pack()

        self.button4 = Button(self.cont5, text="Sair", width=20, command=lambda: comandos(self.delete(5), self.home()), font=self.font)
        self.button4.pack()

    def visualizarAgendamentos(self):
        self.delete(5)
        self.programa.title("Visualizar Agendamentos")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='CPF Do Cliente')
        self.listaVei.heading("#3", text='Data')
        self.listaVei.heading("#4", text='Hora')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)
        self.db1.cursor.execute("""
                 SELECT * FROM agenda a
                 INNER JOIN clientes c ON a.cpfCliente=c.cpf and c.cpf=?
                 """, (username,))
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1cc("agendac")

    def visualizarAtendimentos(self):
        self.delete(5)
        self.programa.title("Visualizar Atendimentos")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Id Cliente')
        self.listaVei.heading("#3", text='Id Funcionario')
        self.listaVei.heading("#4", text='Tipo de Serviço')
        self.listaVei.heading("#5", text='Descriçao')
        self.listaVei.heading("#6", text='Valor')
        self.listaVei.heading("#7", text='Data')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.column('#7', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)
        self.db1.cursor.execute("""
                SELECT * FROM servicos s
                INNER JOIN clientes c ON s.idCliente=c.id and c.cpf=?
                """, (username,))
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1c()

    def agendarVisita(self):
        self.delete(5)

        self.programa.title("Agendamento")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=5, padx=10)

        self.data = Label(self.cont1, text="Escolha uma Data:", width=20, font=self.font)
        self.data.pack(side=LEFT)

        self.dataEntrada = DateEntry(self.cont1, width=20, background='orange', foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd", locale="pt")
        self.dataEntrada.pack(side=RIGHT, padx=10, pady=10)

        self.horario = Label(self.cont2, text="Horário", width=20, font=self.font)
        self.horario.pack(side=LEFT)

        self.horarioEntrada = Entry(self.cont2, width=20, font=self.font)
        self.horarioEntrada.pack(side=RIGHT)
        self.horarioEntrada.bind("<KeyRelease>", self.formato_hora)

        self.button1 = Button(self.cont3, text="Agendar", width=20, command=self.agendar, font=self.font)
        self.button1.pack()

        self.button2 = Button(self.cont4, text="Voltar", width=13, command=lambda: comandos(self.delete(4), self.funcCliente()), font=self.font)
        self.button2.pack(side=RIGHT)

    def funcFuncionario(self):
        self.delete(4)

        self.programa.title("Página do Funcionario")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=5, padx=10)

        self.button1 = Button(self.cont1, text="Cadastrar Funcionário", width=20, command=self.CadastroFuncionario, font=self.font)
        self.button1.pack()

        self.button2 = Button(self.cont2, text = "Realizar Serviço", width = 20, command=self.realizarServico, font = self.font)
        self.button2.pack()

        self.button3 = Button(self.cont3, text = "Realizar consultas", width = 20, command = self.consultas, font = self.font)
        self.button3.pack()

        self.button4 = Button(self.cont4, text = "Sair", width = 20, command=lambda: comandos(self.delete(4), self.home()), font = self.font)
        self.button4.pack()

    def mostrarAgenda(self):
        self.programa.title("Agenda")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='CPF do Cliente')
        self.listaVei.heading("#3", text='Data')
        self.listaVei.heading("#4", text='Hora')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM agenda;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1('agenda')

    def CadastroCliente(self):
        self.delete(4)

        self.programa.title("Cadastro de Clientes")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.cont8 = Frame(self.master)
        self.cont8.pack()

        self.nome = Label(self.cont1, width = 13, text = "Nome: ", font = self.font)
        self.nome.pack(side = LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side = RIGHT)

        self.telefone = Label(self.cont2, width = 13, text = "Telefone: ", font = self.font)
        self.telefone.pack(side = LEFT)

        self.telefoneEntrada = Entry(self.cont2)
        self.telefoneEntrada.pack(side = RIGHT)

        self.endereco = Label(self.cont3, width = 13, text = "Endereço: ", font = self.font)
        self.endereco.pack(side = LEFT)

        self.enderecoEntrada = Entry(self.cont3)
        self.enderecoEntrada.pack(side = RIGHT)

        self.cpf = Label(self.cont4, width = 13, text = "Cpf: ", font = self.font)
        self.cpf.pack(side = LEFT)

        self.cpfEntrada = Entry(self.cont4)
        self.cpfEntrada.pack(side = RIGHT)
        self.cpfEntrada.bind("<KeyRelease>", self.formato_cpf)

        self.senha = Label(self.cont5, width=13, text="Senha: ", font=self.font)
        self.senha.pack(side=LEFT)

        self.senhaEntrada = Entry(self.cont5, show="*")
        self.senhaEntrada.pack(side=RIGHT)

        self.aviso = Label(self.cont6, width=35, text="Atenção, seu CPF será seu user para o login ", font=self.font)
        self.aviso.pack(side=LEFT)

        self.button = Button(self.cont7, text = "Cadastrar", width = 13, command = self.cadastrarCliente, font = self.font)
        self.button.pack(side = LEFT)

        self.button1 = Button(self.cont8, text = "Voltar", width = 13, command = lambda: comandos(self.delete(8), self.home()), font = self.font)
        self.button1.pack(side = RIGHT)

    def CadastroFuncionario(self):
        self.delete(4)

        self.programa.title("Cadastro de Funcionários")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.cont7 = Frame(self.master)
        self.cont7 .pack()

        self.nome = Label(self.cont1, width=13, text="Nome: ", font=self.font)
        self.nome.pack(side=LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side=RIGHT)

        self.telefone = Label(self.cont2, width=13, text="Telefone: ", font=self.font)
        self.telefone.pack(side=LEFT)

        self.telefoneEntrada = Entry(self.cont2)
        self.telefoneEntrada.pack(side=RIGHT)

        self.endereco = Label(self.cont3, width=13, text="Endereço: ", font=self.font)
        self.endereco.pack(side=LEFT)

        self.enderecoEntrada = Entry(self.cont3)
        self.enderecoEntrada.pack(side=RIGHT)

        self.cpf = Label(self.cont4, width=13, text="Cpf: ", font=self.font)
        self.cpf.pack(side=LEFT)

        self.cpfEntrada = Entry(self.cont4)
        self.cpfEntrada.pack(side=RIGHT)
        self.cpfEntrada.bind("<KeyRelease>", self.formato_cpf)

        self.especialidade = Label(self.cont5, width=13, text="Especialidade: ", font=self.font)
        self.especialidade.pack(side=LEFT)

        self.especialidadeEntrada = Entry(self.cont5)
        self.especialidadeEntrada.pack(side=RIGHT)

        self.dataIni = Label(self.cont6, width=20, text="Data do Contrato: ", font=self.font)
        self.dataIni.pack(side=LEFT)

        self.dataIniEntrada = DateEntry(self.cont6, width=20, background='orange', foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd", locale="pt")
        self.dataIniEntrada.pack(side=RIGHT, padx=10, pady=10)

        self.button = Button(self.cont7, text="Cadastrar", width=13, command=self.cadastrarFuncionario, font=self.font)
        self.button.pack(side=LEFT)

        self.button1 = Button(self.cont7, text="Voltar", width=13,
                              command=lambda: comandos(self.delete(7), self.funcFuncionario()), font=self.font)
        self.button1.pack(side=RIGHT)

    def realizarServico(self):
        self.delete(4)

        self.programa.title("Página de Serviço")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.dataIni = Label(self.cont1, width=20, text="Data: ", font=self.font)
        self.dataIni.pack(side=LEFT)


        self.dataIniEntrada = DateEntry(self.cont1, width=20, background='orange', foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd", locale="pt")
        self.dataIniEntrada.pack(side=RIGHT, padx=10, pady=10)

        self.valor = Label(self.cont2, width=20, text="Valor do serviço: ", font=self.font)
        self.valor.pack(side=LEFT)

        self.valorEntrada = Entry(self.cont2)
        self.valorEntrada.pack(side=RIGHT)

        self.idCliente = Label(self.cont3, width=20, text="Id cliente: ", font=self.font)
        self.idCliente.pack(side=LEFT)

        self.idClienteEntrada = Entry(self.cont3)
        self.idClienteEntrada.pack(side=RIGHT)

        self.idFuncionario = Label(self.cont4, width=20, text="Id Funcionario: ", font=self.font)
        self.idFuncionario.pack(side=LEFT)

        self.idFuncionarioEntrada = Entry(self.cont4)
        self.idFuncionarioEntrada.pack(side=RIGHT)

        self.tipo = Label(self.cont5, width=20, text="Tipo: ", font=self.font)
        self.tipo.pack(side=LEFT)

        self.tipoEntrada = Entry(self.cont5)
        self.tipoEntrada.pack(side=RIGHT)

        self.descricao = Label(self.cont6, width=20, text="Descrição: ", font=self.font)
        self.descricao.pack(side=LEFT)

        self.descricaoEntrada = Entry(self.cont6)
        self.descricaoEntrada.pack(side=RIGHT)

        self.button = Button(self.cont7, text="Cadastrar", width=13, command=self.cadastrarServico, font=self.font)
        self.button.pack(side=LEFT)

        self.button1 = Button(self.cont7, text="Voltar", width=13, command=lambda: comandos(self.delete(7), self.funcFuncionario()), font=self.font)
        self.button1.pack(side=RIGHT)

    def consultas(self):
        self.delete(4)

        self.programa.title("Consultas")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack(anchor=S, expand=True, pady=5, padx=10)

        self.label = Label(self.cont1, width = 15, text = "Realizar consultas", font = self.font)
        self.label.pack(side = "top")

        self.button1 = Button(self.cont2, text = "Clientes", width = 13, command = lambda: comandos(self.delete(6), self.consultarClientes()), font = self.font)
        self.button1.pack()

        self.button2 = Button(self.cont3, text = "Funcionarios", width = 13, command = lambda: comandos(self.delete(6), self.consultarFuncionarios()), font = self.font)
        self.button2.pack()

        self.button3 = Button(self.cont4, text = "Serviços", width = 13, command = lambda: comandos(self.delete(6), self.consultarServicos()), font = self.font)
        self.button3.pack()

        self.button4 = Button(self.cont5, text="Agenda", width=13, command=lambda: comandos(self.delete(6), self.mostrarAgenda()), font=self.font)
        self.button4.pack()

        self.button5 = Button(self.cont6, text = "Voltar", width = 13, command = lambda: comandos(self.delete(6), self.funcFuncionario()), font = self.font)
        self.button5.pack()

    def consultarClientes(self):
        self.programa.title("Consultar Clientes")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5","col6"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Nome')
        self.listaVei.heading("#3", text='Telefone')
        self.listaVei.heading("#4", text='Endereço')
        self.listaVei.heading("#5", text='CPF')
        self.listaVei.heading("#6", text='Data de Cadastro')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM clientes;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("clientes")

    def consultarFuncionarios(self):
        self.programa.title("Consultar Funcionaris")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Nome')
        self.listaVei.heading("#3", text='Telefone')
        self.listaVei.heading("#4", text='Endereço')
        self.listaVei.heading("#5", text='CPF')
        self.listaVei.heading("#6", text='Especialidade')
        self.listaVei.heading("#7", text='Data do Contrato')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.column('#7', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM funcionarios;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("funcionarios")

    def consultarServicos(self):
        self.programa.title("Consultar Serviços")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Id Cliente')
        self.listaVei.heading("#3", text='Id Funcionario')
        self.listaVei.heading("#4", text='Tipo de Serviço')
        self.listaVei.heading("#5", text='Descriçao')
        self.listaVei.heading("#6", text='Valor')
        self.listaVei.heading("#7", text='Data')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.column('#7', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM servicos;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("servicos")

    #VERIFICACOES \\ back-end
    def agendar(self):
        print("chamou")
        horaindisponivel = ['']
        a_data = self.dataEntrada.get()
        a_hora = self.horarioEntrada.get()
        if a_hora and a_data != '':
            self.db1.cursor.execute("""
               SELECT count(id) FROM agenda where data=? and hora=?;
               """, (a_data,a_hora))
            resultado = str(self.db1.cursor.fetchone())
            characters = "'(),[]"
            for x in range(len(characters)):
                resultado = resultado.replace(characters[x], "")
            print(resultado)
            if int(resultado) == 0:
                a_data = datetime.strptime(a_data, '%Y-%m-%d').date()
                print(a_data)
                if a_data.weekday()!= 5 and a_data.weekday()!= 6:
                    if a_hora != horaindisponivel[0]:
                        self.db1.cursor.execute("""
                            insert into agenda (cpfCliente, data, hora) values (?,?,?);
                            """, (username, a_data, a_hora))
                        self.db1.commit_db()
                        msg.showinfo(message='Agendamento Concluido')
                        self.horarioEntrada.delete(0, END)
                    else:
                        msg.showwarning(message='Horario indisponível***')
                else:
                    msg.showwarning(message='Data indisponível')
            else:
                msg.showwarning(message='Horário indisponível')
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')
    def cadastrarCliente(self):
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        p_nome = self.nomeEntrada.get()
        p_endereco = self.enderecoEntrada.get()
        p_cpf = self.cpfEntrada.get()
        p_telefone = self.telefoneEntrada.get()
        p_data = datetime.today().strftime('%Y-%m-%d')
        acumula=0
        if p_nome and p_endereco and p_cpf and p_telefone != '':
            while True:

                data = p_data.split('-')
                if len(data) == 3 and len(data[0]) == 4 and len(data[1]) == 2 and len(data[2]) == 2 and (
                        int(data[0]) >= 2000 and int(data[0]) <= 2021):
                    acumula += 1
                    break
                else:
                    msg.showwarning(message='Data inválida. Por favor, siga o modelo aaaa-mm-dd.')
                    break

            while True:
                if len(p_cpf)==14:
                    cpfsonumero = ""
                    for x in p_cpf:
                        if x in numeros:
                            cpfsonumero = cpfsonumero + x
                    self.db1.cursor.execute("""
                       SELECT * from clientes WHERE cpf = ?;
                       """, (cpfsonumero,))
                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='O cpf inserido já está cadastrado.')
                        break
                    else:
                        acumula+=1
                        break
                else:
                    msg.showwarning(message='CPF inválido.')
                    break

            while True:
                cont_1 = 0
                for x in p_telefone:
                    if x in numeros:
                        cont_1 += 1
                if cont_1 >= 11:
                    self.db1.cursor.execute("""
                       SELECT * from clientes WHERE telefone = ?;
                       """, (p_telefone,))

                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='O telefone inserido já está cadastrado.')
                        break
                    else:
                        acumula += 1
                        break
                else:
                    msg.showwarning(message='O telefone precisa ter pelo menos 11 dígitos numéricos.')
                    break
            while True:
                p_senha = self.senhaEntrada.get()
                check = self.verificarSenha(p_senha)
                if check == True:
                    acumula += 1
                    break
                else:
                    msg.showwarning(
                        message='Por favor, digite uma senha válida (com ao menos 8 caracteres totais, 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial.)')
                    break
            if acumula == 4:
                cpfsonumero = ""
                for x in p_cpf:
                    if x in numeros:
                        cpfsonumero= cpfsonumero+x
                self.db1.cursor.execute("""
                    INSERT INTO clientes(nome,telefone, endereco, cpf, dataCadastro)
                    VALUES (?,?,?,?,?);
                    """, (p_nome, p_telefone, p_endereco, cpfsonumero,p_data))
                self.db1.cursor.execute("""
                    INSERT INTO usuarios (username, senha) VALUES (?,?);
                    """, (cpfsonumero, p_senha))
                self.db1.commit_db()
                msg.showinfo(message='Cadastro realizado com sucesso.')
                self.nomeEntrada.delete(0, END)
                self.enderecoEntrada.delete(0, END)
                self.cpfEntrada.delete(0, END)
                self.telefoneEntrada.delete(0, END)
                self.senhaEntrada.delete(0, END)
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def cadastrarFuncionario(self):
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        p_nome = self.nomeEntrada.get()
        p_endereco = self.enderecoEntrada.get()
        p_cpf = self.cpfEntrada.get()
        p_telefone = self.telefoneEntrada.get()
        p_data = self.dataIniEntrada.get()
        p_especialidade = self.especialidadeEntrada.get()
        acumula = 0
        if p_nome and p_endereco and p_cpf and p_telefone != '':
            while True:

                data = p_data.split('-')
                if len(data) == 3 and len(data[0]) == 4 and len(data[1]) == 2 and len(data[2]) == 2 and (
                        int(data[0]) >= 2000 and int(data[0]) <= 2021):
                    acumula += 1
                    break
                else:
                    msg.showwarning(message='Data inválida. Por favor, siga o modelo aaaa-mm-dd.')
                    break

            while True:
                if len(p_cpf) == 14:
                    self.db1.cursor.execute("""
                         SELECT * from funcionarios WHERE cpf = ?;
                         """, (p_cpf,))
                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='O cpf inserido já está cadastrado.')
                        break
                    else:
                        acumula += 1
                        break
                else:
                    msg.showwarning(message='CPF inválido.')
                    break

            while True:
                cont_1 = 0
                for x in p_telefone:
                    if x in numeros:
                        cont_1 += 1
                if cont_1 >= 11:
                    self.db1.cursor.execute("""
                         SELECT * from funcionarios WHERE telefone = ?;
                         """, (p_telefone,))
                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='O telefone inserido já está cadastrado.')
                        break
                    else:
                        acumula += 1
                        break
                else:
                    msg.showwarning(message='O telefone precisa ter pelo menos 11 dígitos numéricos.')
                    break
            if acumula == 3:
                self.db1.cursor.execute("""
                      INSERT INTO funcionarios(nome,telefone, endereco, cpf,especialidade,dataContrato)
                      VALUES (?,?,?,?,?,?);
                      """, (p_nome, p_telefone, p_endereco, p_cpf, p_especialidade, p_data))
                self.db1.commit_db()
                msg.showinfo(message='Cadastro realizado com sucesso.')
                self.nomeEntrada.delete(0, END)
                self.enderecoEntrada.delete(0, END)
                self.cpfEntrada.delete(0, END)
                self.telefoneEntrada.delete(0, END)
                self.especialidadeEntrada.delete(0, END)
                self.dataIniEntrada.delete(0, END)
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def cadastrarServico(self):
        p_data = self.dataIniEntrada.get()
        p_valor = self.valorEntrada.get()
        p_idCliente = self.idClienteEntrada.get()
        p_idFuncionario = self.idFuncionarioEntrada.get()
        p_tipo = self.tipoEntrada.get()
        p_descricao = self.descricaoEntrada.get()
        if p_data and p_valor and p_idCliente and p_idFuncionario and p_tipo != "":
            cont_acumula = 0
            try:
                int(p_valor), int(p_idCliente), int(p_idFuncionario)
            except:
                msg.showwarning(message='Por favor, digite apenas valores numéricos nos campos.')
            else:
                while True:

                   data = p_data.split('-')
                   if len(data) == 3 and len(data[0]) == 4 and len(data[1]) == 2 and len(data[2]) == 2 and (int(data[0]) >= 2000 and int(data[0]) <= 2021):
                       cont_acumula+=1
                       break
                   else:
                       msg.showwarning(message='Data inválida. Por favor, siga o modelo aaaa-mm-dd.')
                       break

                while True:
                    if int(p_valor) > 0:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='Por favor, digite um valor numérico maior que 0 para o Valor.')
                        break

                while True:
                    self.db1.cursor.execute("""
                    SELECT * from clientes WHERE id = ?;
                    """, (p_idCliente,))

                    rows = self.db1.cursor.fetchall()

                    if rows:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='O cliente informado não está cadastrado no banco de dados.')
                        break

                while True:
                    self.db1.cursor.execute("""
                    SELECT * FROM funcionarios WHERE id = ?;
                    """, (p_idFuncionario,))

                    rows = self.db1.cursor.fetchall()

                    if rows:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='O Funcionario inserido não está cadastrado no banco de dados.')
                        break
                if cont_acumula == 4:
                    self.db1.cursor.execute("""
                        INSERT INTO servicos (idCliente, idFuncionario, tipoServico, descricao, valor, data)
                        VALUES (?,?,?,?,?,?);
                        """, (p_idCliente, p_idFuncionario, p_tipo, p_descricao, str(p_valor), p_data))
                    self.db1.commit_db()
                    msg.showinfo(message='Dados adicionados com sucesso.')
                    self.dataIniEntrada.delete(0, END)
                    self.valorEntrada.delete(0, END)
                    self.idClienteEntrada.delete(0, END)
                    self.idFuncionarioEntrada.delete(0, END)
                    self.tipoEntrada.delete(0, END)
                    self.descricaoEntrada.delete(0, END)

        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def opcoesFrame_1f(self):
        self.bt_voltar = Button(self.frame_1, text="Voltar", width = 13, command=lambda: comandos(self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), self.programa.geometry('550x350'), self.funcFuncionario()), font=self.font)
        self.bt_voltar.pack(anchor=S, expand=True, pady=5, padx=10)

    def opcoesFrame_1c(self):
        self.bt_voltar = Button(self.frame_1, text="Voltar", width = 13, command=lambda: comandos(self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), self.programa.geometry('550x350'), self.funcCliente()), font=self.font)
        self.bt_voltar.pack(anchor=S, expand=True, pady=5, padx=10)

    def opcoesFrame_1cc(self, tabela):
        if tabela == 'agendac':
            tabela_consulta = 'self.visualizarAgendamentos()'

        self.id = Label(self.frame_1, text='Id: ', font=self.font, bg='gray83')
        self.id.place(relx=0.48, rely=0.05)

        self.idEntrada = Entry(self.frame_1)
        self.idEntrada.place(relx=0.46, rely=0.15, relwidth=0.08)

        self.bt_deletar = Button(self.frame_1, text="Deletar", font=self.font, command=lambda: comandos(self.excluir(tabela), self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), exec(tabela_consulta)), width=13)
        self.bt_deletar.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.15)

        self.bt_voltar = Button(self.frame_1, text="Voltar", width=13, command=lambda: comandos(self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), self.programa.geometry('550x350'), self.funcCliente()), font=self.font)
        self.bt_voltar.pack(anchor=S, expand=True, pady=5, padx=10)

    def opcoesFrame_1(self, tabela):
        if tabela == 'clientes':
            tabela_consulta = 'self.consultarClientes()'
        if tabela == 'funcionarios':
            tabela_consulta = 'self.consultarFuncionarios()'
        if tabela == 'servicos':
            tabela_consulta = 'self.consultarServicos()'
        if tabela == 'agenda':
            tabela_consulta = 'self.mostrarAgenda()'

        self.id = Label(self.frame_1, text = 'Id: ', font = self.font, bg='gray83')
        self.id.place(relx=0.48, rely=0.05)

        self.idEntrada = Entry(self.frame_1)
        self.idEntrada.place(relx=0.46, rely=0.15, relwidth=0.08)

        self.bt_deletar = Button(self.frame_1, text="Deletar", font = self.font, command= lambda: comandos(self.excluir(tabela), self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), exec(tabela_consulta)), width = 13)
        self.bt_deletar.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.15)

        self.bt_voltar = Button(self.frame_1, text="Voltar", width = 13, command=lambda: comandos(self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), self.programa.geometry('550x350'), self.consultas()), font=self.font)
        self.bt_voltar.pack(anchor=S, expand=True, pady=5, padx=10)

    def excluir(self, tabela):
        idExcluir = self.idEntrada.get()
        try:
            int(idExcluir)
        except:
            msg.showwarning(message="Digite apenas números.")
        else:
            res = msg.askyesno(title = "Alerta", message = "Tem certeza que deseja excluir?")
            if res == True:
                if tabela == 'clientes':

                    self.db1.cursor.execute("""
                        DELETE FROM clientes
                        WHERE id = (?);
                        """, (idExcluir))

                if tabela == 'funcionarios':

                    self.db1.cursor.execute("""
                        DELETE FROM funcionarios
                        WHERE id = (?);
                        """, (idExcluir))

                if tabela == 'servicos':

                    self.db1.cursor.execute("""
                        DELETE FROM servicos
                        WHERE id = (?);
                        """, (idExcluir,))
                if tabela == 'agenda':
                    self.db1.cursor.execute("""
                        DELETE FROM agenda
                        WHERE id = (?);
                        """, (idExcluir,))
                if tabela == 'agendac':
                    self.db1.cursor.execute("""
                        DELETE FROM agenda
                        WHERE id = (?) and cpfCliente = (?);
                        """, (idExcluir, username))
                self.db1.commit_db()
                msg.showinfo(message="Exclusão realizada com sucesso.")
                self.idEntrada.delete(0,END)

    def frames(self):
        self.frame_1 = Frame(self.programa, bd=4, bg='gray83', highlightbackground='gray45', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.programa, bd=4, bg='gray83', highlightbackground='gray45', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def formato_cpf(self, event=None):
        text = self.cpfEntrada.get().replace(".", "").replace("-", "")[:11]
        new_text = ""
        if event.keysym.lower() == "backspace": return
        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if index in [2, 5]:
                new_text += text[index] + "."
            elif index == 8:
                new_text += text[index] + "-"
            else:
                new_text += text[index]

        self.cpfEntrada.delete(0, "end")
        self.cpfEntrada.insert(0, new_text)

    def formato_hora(self, event=None):
        text = self.horarioEntrada.get().replace(".", "").replace("-", "")[:5]
        new_text = ""
        if event.keysym.lower() == "backspace": return
        for index in range(len(text)):

            if not text[index] in "0123456789": continue
            if index in [1]:
                new_text += text[index] + ":"
            else:
                new_text += text[index]
        self.horarioEntrada.delete(0, "end")
        self.horarioEntrada.insert(0, new_text)

    def cadastroUser(self):
        self.delete(4)
        self.programa.title("Cadastrar Administrador")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=5, padx=10)

        self.nome = Label(self.cont1, width = 15, text = "Nome de Usuario: ", font = self.font)
        self.nome.pack(side = LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side = RIGHT)

        self.senha = Label(self.cont2, width = 15, text = "Senha: ", font = self.font)
        self.senha.pack(side = LEFT)

        self.senhaEntrada = Entry(self.cont2, show = "*")
        self.senhaEntrada.pack(side = RIGHT)

        self.button = Button(self.cont3, text = "Cadastrar", width = 15, command = self.cadastrarUser, font = self.font)
        self.button.pack()

        self.button1 = Button(self.cont4, text = "Voltar", width = 15, command = lambda: comandos(self.delete(4), self.home()), font = self.font)
        self.button1.pack()

    def cadastrarUser(self):
        cont_acumula2 = 0
        while True:
            p_username = self.nomeEntrada.get()
            check = self.verificarUsername(p_username, 'admins')
            if check == True:
                msg.showwarning(message='Nome de usuário já existente. Por favor, escolha outro.')
                break
            else:
                cont_acumula2 += 1
                break

        while True:
            p_senha = self.senhaEntrada.get()
            check = self.verificarSenha(p_senha)
            if check == True:
                cont_acumula2 += 1
                break
            else:
                msg.showwarning(message='Por favor, digite uma senha válida (com ao menos 8 caracteres totais, 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial.)')
                break

        if cont_acumula2 == 2:

            self.db.cursor.execute("""
                INSERT INTO admins(username, senha)
                VALUES (?,?);
                """, (p_username, p_senha))

            self.db.commit_db()
            msg.showinfo(message= 'Cadastro de usuário realizado com sucesso!')
            self.nomeEntrada.delete(0, END)
            self.senhaEntrada.delete(0, END)

    def verificarUsername(self, username, tabela):
        self.db.cursor.execute("""
            SELECT * from """+tabela+""" WHERE username = ?;
        """, (username,))

        rows = self.db.cursor.fetchall()
        if rows:
            return True
        else:
            return False

    def verificarSenha(self, senha):
        cont = 0
        if any(n.isupper() for n in senha):
            cont += 1
        if any(n.islower() for n in senha):
            cont += 1
        if any(n.isdigit() for n in senha):
            cont += 1
        if any(n in ('?#!$%&*()_^~@/') for n in senha):
            cont += 1
        if cont >= 4 and len(senha) >= 8:
            return True

    def delete(self, num):
        for c in range(num):
            exec(f"self.cont{c + 1}.destroy()")


app.geometry('550x350')
Janela(app)
app.mainloop()