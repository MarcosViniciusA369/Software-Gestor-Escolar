import sqlite3
import sys
from datetime import datetime, date
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence
from TelaGUI import *
import bd_create
import os
from threading import *
from time import sleep

class App(QMainWindow, QTableWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        super().setupUi(self)

        self.frame_31.hide()

        '''try:
            if os.path.exists("banco_dados/Pyedu_bd.db"):
                print('yes')
            else:
                self.frame_31.show()
                self.label_15.setText('BANCO NÃO ENCONTRADO, CRIADO UM NOVO....')
        except:
            print("error")
        finally:'''

        self.bd = sqlite3.connect('banco_dados/Pyedu_bd.db')
        self.cursor = self.bd.cursor()
        bd_create.create_all()


        timer = QTimer(self)
        timer.timeout.connect(self.clock)
        timer.start(1000)

        self.show_bar = True
        self.dt_key = QShortcut(QKeySequence('esc'), self)
        self.dt_key.activated.connect(self.menubar_show)

        ######################### BOTOES MENU LATERAL ###########################
        self.pushButton_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))  # HOME
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))  # TABELA
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))  # CAD ALUN
        self.pushButton_11.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))  # CAD PROF
        self.pushButton_13.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.pushButton_12.clicked.connect(self.close_app)  # SAIR
        # self.pushButton_13.clicked.connect(lambda: self.stackedWidget.setCurrentIndex())  # CAD NOTAS

        ######################### BOTOES DA PESQUISA ###########################
        self.pushButton.clicked.connect(self.btn_one_person)
        self.pushButton_14.clicked.connect(lambda: self.update_database(self.tabela_geral))  # atualiza o banco
        self.pushButton_4.clicked.connect(self.btn3_reg)  # cad
        self.pushButton_5.clicked.connect(self.btn4_alt)
        self.pushButton_6.clicked.connect(self.btn6_dlt)

        ######################### BOTOES PARA CADASTRAR PROFESSOR #######################
        self.pushButton_9.clicked.connect(self.register_teacher)

        ######################### BOTOES PARA CADASTRAR ALUNO ###########################
        self.pushButton_7.clicked.connect(self.register_student)
        self.pushButton_15.clicked.connect(self.btn15_reg)
        self.pushButton_16.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        ######################### BUTTON FOR ALTERAR ###########################
        self.pushButton_21.clicked.connect(self.btn21_alt)
        self.pushButton_20.clicked.connect(self.btn20_alt)
        self.pushButton_22.clicked.connect(self.alter_register)

        ######################### BOTOES MATERIA ###########################
        self.pushButton_29.clicked.connect(self.reg_sub)
        self.pushButton_31.clicked.connect(lambda :self.stackedWidget.setCurrentIndex(1))
        self.pushButton_30.clicked.connect(self.alt_sub)

        ######################### BOTOES DELETAR ###########################
        self.pushButton_17.clicked.connect(self.delete_registry)
        self.pushButton_19.clicked.connect(lambda: self.update_database(self.tabela_deletar))
        self.pushButton_18.clicked.connect(self.btn18_dlt)

        ######################### COMBOX ###########################
        self.comboBox.addItems(['Alunos', 'Professor', 'Materias'])
        self.comboBox_3.addItems(['-', 'ID', 'NOME'])

        # ANO LETIVO
        for i in range(1, 10):
            self.comboBox_2.addItems([f'{str(i)}º ANO'])

        ######################### BTN E LINE ESCONDIDOS ###########################
        # alt
        self.pushButton_8.hide()
        self.pushButton_10.hide()
        self.lineEdit_9.hide()
        self.lineEdit_10.hide()
        self.lineEdit_11.hide()
        self.lineEdit_13.hide()
        self.dateEdit_3.hide()
        self.pushButton_22.hide()

        # notas
        self.lineEdit_16.hide()
        self.lineEdit_17.hide()
        self.lineEdit_18.hide()
        self.lineEdit_19.hide()
        self.lineEdit_21.hide()
        self.lineEdit_22.hide()

        self.label_10.hide()
        self.label_11.hide()

    def menubar_show(self):
        if self.show_bar:
            self.menu_bar.show()
            self.show_bar = False
        else:
            self.menu_bar.hide()
            self.show_bar = True

    def clock(self):
        now = QTime.currentTime()
        label_time = now.toString('hh:mm:ss')
        self.label_7.setText(label_time)

        data_atual = date.today()
        h = '{}/{}/{}'.format(data_atual.day, data_atual.month,
                              data_atual.year)
        self.label_8.setText(str(h))

    def thr(self):
        t1 = Thread(target=self.pop_up)

    def pop_up(self):
        self.frame_31.show()
        self.label_15.setText('BANCO NÃO ENCONTRADO, CRIADO UM NOVO....')
        sleep(1)

    ######################### FUNCOES DOS BTNS ###########################

    def btn_one_person(self):
        self.search_text = self.textEdit.toPlainText()
        self.combox_select = self.comboBox_3.currentText()
        self.usu = self.comboBox.currentText()

        if self.search_text == '':
            QtWidgets.QMessageBox.about(self.p2, 'AVISO', 'NENHUM VALOR FOI INSERIDO NA BARRA DE PESQUISA')
            return

        if self.combox_select == 'ID':
            try:
                self.cursor = self.bd.cursor()
                act = 'SELECT * FROM student WHERE RA= ?'
                self.cursor.execute(act, (self.search_text,))
                self.bd.commit()
                self.update_person(self.tabela_geral)

            except Exception as error:
                print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

    def btn3_reg(self):
        if self.comboBox.currentText() == 'Alunos':
            self.stack = self.stackedWidget.setCurrentIndex(3)
            self.pushButton_8.hide()
            self.pushButton_7.show()

        elif self.comboBox.currentText() == 'Professor':
            self.stack = self.stackedWidget.setCurrentIndex(2)
            self.pushButton_10.hide()
            self.pushButton_9.show()

        elif self.comboBox.currentText() == 'Materias':
            self.pushButton_32.hide()
            self.pushButton_33.hide()

            self.stack = self.stackedWidget.setCurrentIndex(8)
            self.lineEdit_15.hide()
            self.lineEdit_24.show()
            self.lineEdit_25.show()
            self.pushButton_30.hide()
            self.pushButton_29.show()

    def btn4_alt(self):
        if self.comboBox.currentText() == 'Alunos':
            self.label_6.setText('ALTERAR ALUNO')
            self.stack = self.stackedWidget.setCurrentIndex(4)
            self.update_database(self.tabela_alterar)

        elif self.comboBox.currentText() == 'Professor':
            self.label_6.setText('ALTERAR PROFESSOR')
            self.stack = self.stackedWidget.setCurrentIndex(4)
            self.update_database(self.tabela_alterar)

        elif self.comboBox.currentText() == 'Materias':
            self.stack = self.stackedWidget.setCurrentIndex(8)
            self.update_database(self.tabela_materia)
            self.lineEdit_15.show()
            self.lineEdit_24.hide()
            self.lineEdit_25.hide()
            self.pushButton_29.hide()
            self.pushButton_30.show()
            self.pushButton_32.hide()
            self.pushButton_33.hide()

    def btn6_dlt(self):
        self.stack = self.stackedWidget.setCurrentIndex(5)
        self.update_database(self.tabela_deletar)

    def btn15_reg(self):
        self.update_database(self.tabela_geral)
        self.stackedWidget.setCurrentIndex(1)

    def btn18_dlt(self):
        self.update_database(self.tabela_geral)
        self.stackedWidget.setCurrentIndex(1)

    def btn20_alt(self):
        self.lineEdit_14.setText('')
        self.stackedWidget.setCurrentIndex(1)
        self.pushButton_22.hide()
        self.pushButton_21.show()
        self.lineEdit_14.show()
        self.lineEdit_9.hide()
        self.lineEdit_10.hide()
        self.lineEdit_11.hide()
        self.lineEdit_13.hide()
        self.dateEdit_3.hide()
        self.update_database(self.tabela_geral)

    def btn21_alt(self):
        if self.lineEdit_14.text() == "":
            QtWidgets.QMessageBox.about(self.p_2_alt, 'AVISO', 'INSIRA UM ID')
            return

        id_alter = self.lineEdit_14.text()

        if self.comboBox.currentText() == 'Alunos':
            self.cursor.execute("SELECT RA FROM student")
            self.data_3 = self.cursor.fetchall()
            empty_list = []
            for i in self.data_3:
                empty_list.append(i)
            if id_alter not in str(empty_list):
                QtWidgets.QMessageBox.about(self.p_2_alt, 'AVISO', 'ID NÃO ENCONTRADO')
                return
            try:
                self.lineEdit_9.show()
                self.lineEdit_10.show()
                self.lineEdit_11.show()
                self.lineEdit_13.show()
                self.lineEdit_14.hide()
                self.dateEdit_3.show()
                self.pushButton_22.show()
                self.pushButton_21.hide()

                self.cursor.execute("SELECT * FROM student WHERE RA = ?", (id_alter,))
                self.data_3 = self.cursor.fetchall()

                for i in self.data_3:
                    self.lineEdit_9.setText(f'{i[1]}')
                    self.lineEdit_11.setText(f'{i[2]}')
                    self.lineEdit_13.setText(f'{i[4]}')
                    # self.lineEdit_12.setText(f'{i[4]}')
                    conver_date = datetime.strptime(i[5], '%d/%m/%Y').date()
                    self.dateEdit_3.setDate(conver_date)
                    self.lineEdit_10.setText(f'{i[3]}')
            except Exception as error:
                print(f'Error: {error}')

        if self.comboBox.currentText() == 'Professor':
            self.cursor.execute("SELECT id FROM teacher")
            self.data_3 = self.cursor.fetchall()
            empty_list = []
            for i in self.data_3:
                empty_list.append(i)
            if id_alter not in str(empty_list):
                QtWidgets.QMessageBox.about(self.p_2_alt, 'AVISO', 'ID NÃO ENCONTRADO')
                return
            try:
                self.lineEdit_9.show()
                self.lineEdit_10.show()
                self.lineEdit_11.hide()
                self.lineEdit_13.show()
                self.lineEdit_14.hide()
                self.dateEdit_3.show()
                self.pushButton_22.show()
                self.pushButton_21.hide()

                self.cursor.execute("SELECT * FROM teacher WHERE id = ?", (id_alter,))
                self.data_3 = self.cursor.fetchall()

                for i in self.data_3:
                    self.lineEdit_9.setText(f'{i[1]}')
                    self.lineEdit_10.setText(f'{i[2]}')
                    self.lineEdit_13.setText(f'{i[3]}')
                    conver_date = datetime.strptime(i[5], '%d/%m/%Y').date()
                    self.dateEdit_3.setDate(conver_date)
            except Exception as error:
                print(f'Error: {error}')

    def btn21_alt_now(self):
        self.lineEdit_9.hide()
        self.lineEdit_10.hide()
        self.lineEdit_11.hide()
        self.lineEdit_13.hide()
        self.lineEdit_14.show()
        self.dateEdit_3.hide()
        self.pushButton_22.hide()
        self.pushButton_21.show()

    def close_app(self):
        sys.exit()

    ######################### BANCO DE DADOS ###########################

    ######## CADASTRAR ALUNO #########
    def register_student(self):
        numeros = '1234567890'
        caracter_s = '!@#$%¨&*()_-+=[]{}'
        lista_nome_vazia = []
        # CONFERINDO NOME E SOBRENOME
        try:
            self.name = self.lineEdit.text().strip() + ' ' + self.lineEdit_2.text().strip()
            self.resp = self.lineEdit_5.text().strip()
            self.phone = self.lineEdit_3.text().strip()
            self.date = self.dateEdit.text()
            self.cpf = self.lineEdit_4.text()
            self.year = self.comboBox_2.currentText()

            if self.name == '' or self.resp == '' or self.cpf == '':
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'Existe campos vazios')
                return

            # VERIFICANDO NOME
            for a in self.name:
                lista_nome_vazia.append(a)
            for a in lista_nome_vazia:
                if a in numeros:
                    QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                    return
                elif a in caracter_s:
                    QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                    return

            # VERIFICANDO NOME DO RESPONSAVEL
            for a in self.resp:
                lista_nome_vazia.append(a)
            for a in lista_nome_vazia:
                if a in numeros:
                    print(f'{a} é numero')
                    return
                elif a in caracter_s:
                    print(f'{a} é caracter special')
                    return

            '''# VEREFICAR O CPF
            cpf = str(self.cpf)
            if len(cpf) < 11:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'cpf inserido incorretamente')
                return
            if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
                return
            calc = lambda t: int(t[1]) * (t[0] + 2)
            d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
            d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11
            ok = str(d1) == cpf[-2] and str(d2) == cpf[-1]

            if ok == False:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'cpf invalido')
                return'''

        except:
            print('error')

        # enviando os dados
        try:
            self.cursor = self.bd.cursor()
            acao = 'INSERT INTO student (name, name_resp, cpf, phone_number, birth_date, year) VALUES (?,?,?,?,?,?)'
            self.cursor.execute(acao, (self.name.upper(), self.resp.upper(), self.cpf, self.phone, self.date, self.year[0]))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'CADASTRADO COM SUCESSO')

        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

        else:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')

    ######## CADASTRAR PROFESSOR #########
    def register_teacher(self):
        num = '1234567890'
        caracter = '!@#$%¨&*()_-+=[]{}'
        empty_list = []

        self.name = self.lineEdit_6.text().strip()
        self.cpf = self.lineEdit_7.text()
        self.phone = self.lineEdit_26.text().strip()
        self.date = self.dateEdit_2.text()
        print(self.date)


        if self.name == '' or self.phone == '':
            QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'Existe campos vazios')
            return

        # VERIFICANDO NOME DO PROFESSOR
        for a in self.name:
            empty_list.append(a)
        for a in empty_list:
            if a in num:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                return
            elif a in caracter:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                return

            # VERIFICA CEL
            '''if int(self.cel) != int:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'NUMERO INVALIDO')
                return'''
        try:
            self.cursor = self.bd.cursor()
            act = 'INSERT INTO teacher (name, cpf, phone_number, birth_date) VALUES (?,?,?,?)'
            self.cursor.execute(act, (self.name, self.cpf, self.phone, self.date))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'PROFESSOR CADASTRADO')

            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

    ######## CADASTRAR MAT #########
    def reg_sub(self):
        num = "1234567890"
        self.name_sub = self.lineEdit_24.text()
        self.name_teac = self.lineEdit_25.text()

        if self.name_sub == '':
            QMessageBox.about(self.p5_mat, "AVISO", "INSIRA UM NOME")
            return
        if self.name_teac not in num:
            QMessageBox.about(self.p5_mat, "AVISO", "APENAS NUMEROS NO ID PROFESSOR")
            return

        try:
            self.cursor = self.bd.cursor()
            act = 'INSERT INTO subjects (name, id_teacher) VALUES (?,?)'
            self.cursor.execute(act, (self.name_sub.upper(), self.name_teac))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'CADASTRADO COM SUCESSO')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

    def alt_sub(self):
        pass

    ######## ALTERAR BANCO #########
    def alter_register(self):
        self.name = self.lineEdit_9.text()
        self.resp = self.lineEdit_11.text()
        self.phone = self.lineEdit_13.text()
        self.date = self.dateEdit_3.text()
        self.cpf = self.lineEdit_10.text()

        try:
            if self.comboBox.currentText() == 'Alunos':
                self.cursor = self.bd.cursor()
                act = 'UPDATE student SET name = ?, name_resp = ?, cpf = ?, phone_number = ?, birth_date = ? WHERE RA = ?'
                self.cursor.execute(act, (
                    self.name.upper(), self.resp.upper(), self.cpf, self.phone, self.date, self.lineEdit_14.text()))
                self.bd.commit()
                QtWidgets.QMessageBox.about(self.p_2_cad, 'ALTERADO', 'ALTERADO COM SUCESSO')

            if self.comboBox.currentText() == 'Professor':
                self.lineEdit_11.hide()

                self.cursor = self.bd.cursor()
                act = 'UPDATE teacher SET name = ?, cpf = ?, phone_number = ?, birth_date = ? WHERE id = ?'
                self.cursor.execute(act, (
                    self.name.upper(), self.cpf, self.phone, self.date, self.lineEdit_14.text()))
                self.bd.commit()
                QtWidgets.QMessageBox.about(self.p_2_cad, 'ALTERADO', 'ALTERADO COM SUCESSO')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            self.lineEdit_9.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_14.setText('')

            self.update_database(self.tabela_alterar)

    ######## ATUALIZAR BANCO #########
    def update_database(self, table):
        self.name_table = table

        try:
            ######## ALUNOS #########
            if self.comboBox.currentText() == 'Alunos':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT * FROM student')
                self.data = self.cursor.fetchall()

                # Duas listas para definir nomes na coluna e nas linhas
                name_colum = ['ID', 'NOME', 'RESPONSAVEL', 'CPF', 'CELULAR', 'DATA DE NASC.', 'ANO LETIVO']
                empty_list = []
                for x in range(0, len(self.data)):
                    empty_list.append(' ')

                # Alteração nas colunas
                self.name_table.setRowCount(len(self.data))
                self.name_table.setColumnCount(7)
                self.name_table.setColumnWidth(0, 15)
                self.name_table.setColumnWidth(1, 170)
                self.name_table.setColumnWidth(2, 150)
                self.name_table.setColumnWidth(3, 100)
                self.name_table.setColumnWidth(4, 80)
                self.name_table.setVerticalHeaderLabels(empty_list)
                self.name_table.setHorizontalHeaderLabels(name_colum)

                # Adicinamos Items na coluna
                for l in range(0, len(self.data)):
                    for c in range(0, 7):
                        self.name_table.setItem(l, c, QTableWidgetItem(str(self.data[l][c])))

            ######## PROFESSORES #########
            elif self.comboBox.currentText() == 'Professor':
                self.cursor.execute('SELECT * FROM teacher')
                self.data = self.cursor.fetchall()

                name_colum = ['ID', 'NOME', 'CPF', 'CELULAR', 'DATA NASC']
                empty_list = []
                for x in range(0, len(self.data)):
                    empty_list.append(' ')

                self.name_table.setRowCount(len(self.data))
                self.name_table.setColumnCount(5)
                self.name_table.setColumnWidth(0, 15)
                self.name_table.setColumnWidth(1, 200)
                self.name_table.setColumnWidth(3, 115)
                self.name_table.setVerticalHeaderLabels(empty_list)
                self.name_table.setHorizontalHeaderLabels(name_colum)

                for l in range(0, len(self.data)):
                    for c in range(0, 4):
                        self.name_table.setItem(l, c, QTableWidgetItem(str(self.data[l][c])))

            ######## MATERIAS #########
            if self.comboBox.currentText() == 'Materias':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor.execute('SELECT * FROM subjects')
                self.data = self.cursor.fetchall()

                # Duas listas para definir nomes na coluna e nas linhas
                name_colum = ['ID', 'NOME', 'PROFESSOR']
                empty_list = []
                for x in range(0, len(self.data)):
                    empty_list.append(' ')

                # Alteração nas colunas
                self.name_table.setRowCount(len(self.data))
                self.name_table.setColumnWidth(1, 200)
                self.name_table.setColumnCount(3)
                self.name_table.setVerticalHeaderLabels(empty_list)
                self.name_table.setHorizontalHeaderLabels(name_colum)

                # Adicinamos Items na coluna
                for l in range(0, len(self.data)):
                    for c in range(0, 3):
                        self.name_table.setItem(l, c, QTableWidgetItem(str(self.data[l][c])))

        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

    def update_person(self, table):
        self.name_table = table
        self.selector = self.textEdit.toPlainText()

        try:
            ######## SELECIONA UM ALUNO #########
            if self.comboBox.currentText() == 'Alunos' and self.comboBox_3 != '':
                # chamamos o banco de dados e pedimos um SELECT
                if self.comboBox_3.currentText() == "ID":
                    try:
                        self.seletor_num = int(self.selector)
                    except:
                        QMessageBox.about(self.p2, "Aviso", "DIGITE APENAS NUMEROS")
                        self.textEdit.setText('')
                        return
                    else:
                        self.cursor.execute('SELECT * FROM student WHERE RA=?', (int(self.selector),))

                if self.comboBox_3.currentText() == "NOME":
                    self.cursor.execute('SELECT * FROM student WHERE name=?', (self.selector.upper(),))
                self.data = self.cursor.fetchall()
                print('ola')
                try:
                    if self.data[0][0]:
                        print(self.data[0][0])
                        print(self.data[0][1])

                except:
                    QMessageBox.about(self.p2, "AVISO", "ID NÃO ENCONTRADO")
                    self.textEdit.setText('')
                    return

                # Duas listas para definir nomes na coluna e nas linhas
                nomes = ['ID', 'NOME', 'RESPONSAVEL', 'CPF', 'CELULAR', 'DATA DE NASC.']
                lista_vazia = []

                # Alteração nas colunas
                self.name_table.setRowCount(len(self.data))
                self.name_table.setColumnCount(6)
                self.name_table.setColumnWidth(0, 15)
                self.name_table.setColumnWidth(1, 150)
                self.name_table.setColumnWidth(3, 50)
                self.name_table.setVerticalHeaderLabels(lista_vazia)
                self.name_table.setHorizontalHeaderLabels(nomes)

                for l in range(0, len(self.data)):
                    for c in range(6):
                        self.name_table.setItem(l, c, QTableWidgetItem(str(self.data[l][c])))
                self.textEdit.setText('')

            ######## SELECIONA UM PROFESSORE #########
            elif self.comboBox.currentText() == 'Professor':
                # chamamos o banco de dados e pedimos um SELECT
                if self.comboBox_3.currentText() == "ID":
                    try:
                        self.seletor_num = int(self.selector)
                    except:
                        QMessageBox.about(self.p2, "Aviso", "DIGITE APENAS NUMEROS")
                        self.textEdit.setText('')
                        return
                    else:
                        self.cursor.execute('SELECT * FROM teacher WHERE id=?', (int(self.selector),))

                if self.comboBox_3.currentText() == "NOME":
                    self.cursor.execute('SELECT * FROM teacher WHERE name=?', (self.selector.upper(),))
                self.data = self.cursor.fetchall()

                try:
                    if self.data[0][0]:
                        print(self.data[0][0])
                        print(self.data[0][1])

                except:
                    QMessageBox.about(self.p2, "AVISO", "ID NÃO ENCONTRADO")
                    self.textEdit.setText('')
                    return
                nomes = ['ID', 'NOME', 'CPF', 'DATA NASC']
                lista_vazia = []
                for x in range(0, len(self.data)):
                    lista_vazia.append(' ')

                self.name_table.setRowCount(len(self.data))
                self.name_table.setColumnCount(4)
                self.name_table.setColumnWidth(0, 15)
                self.name_table.setColumnWidth(1, 200)
                self.name_table.setColumnWidth(3, 115)
                self.name_table.setVerticalHeaderLabels(lista_vazia)
                self.name_table.setHorizontalHeaderLabels(nomes)

                for l in range(0, len(self.data)):
                    for c in range(0, 4):
                        self.name_table.setItem(l, c, QTableWidgetItem(str(self.data[l][c])))

        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

    ######## DELETAR CADASTROS #########
    def delete_registry(self):
        ids = []
        try:
            if self.comboBox.currentText() == 'Alunos':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT RA FROM student')
                self.dados = self.cursor.fetchall()
                for x in self.dados:
                    ids.append(x)

                if ids == []:
                    try:
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'student'")
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'student' ")
                        self.bd.commit()
                    except Exception as error_2:
                        print(f"Error: {error_2}")
                try:
                    self.id_delete = self.lineEdit_8.text()
                    """SE ID FOR IGUAL A 0, RETORNA"""
                    if self.id_delete == '':
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'INFORME O ID')
                        return
                    if self.id_delete not in str(ids):
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'ID NÃO ENCONTRADO')
                        return
                    else:
                        QtWidgets.QMessageBox.about(self.p_2_del, 'DELETADO', 'DELETADO COM SUCCESO')
                except:
                    print('error')
                else:
                    self.cursor = self.bd.cursor()
                    acao = 'DELETE FROM student WHERE RA=?'
                    self.cursor.execute(acao, (self.id_delete,))
                    self.bd.commit()
                    self.cursor.close()
                    self.update_database(self.tabela_deletar)
                    self.lineEdit_8.setText('')

            if self.comboBox.currentText() == 'Professor':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT id FROM teacher')
                self.dados = self.cursor.fetchall()
                for x in self.dados:
                    ids.append(x)
                if ids == []:
                    # SE TODOS OS DADOS FOREM APAGADOS, SEQ RETORNA PARA 0
                    try:
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'teacher'")
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'teacher' ")
                        self.bd.commit()
                    except Exception as error_2:
                        print(f"Error: {error_2}")
                try:
                    self.id_delete = self.lineEdit_8.text()

                    """SE ID FOR IGUAL A 0, RETORNA"""
                    if self.id_delete == '':
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'INFORME O ID')
                        return
                    if self.id_delete not in str(ids):
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'ID NÃO ENCONTRADO')
                        return
                    else:
                        QtWidgets.QMessageBox.about(self.p_2_del, 'DELETADO', 'DELETADO COM SUCCESO')
                except:
                    print('error')
                else:
                    acao = 'DELETE FROM teacher WHERE id=?'
                    self.cursor.execute(acao, (self.id_delete,))
                    self.bd.commit()
                    self.update_database(self.tabela_deletar)
                    self.lineEdit_8.setText('')

            if self.comboBox.currentText() == 'Materias':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT id FROM subjects')
                self.dados = self.cursor.fetchall()
                for x in self.dados:
                    ids.append(x)
                if ids == []:
                    try:
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'subjects'")
                        self.cursor = self.bd.cursor()
                        self.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'subjects' ")
                        self.bd.commit()
                    except Exception as error_2:
                        print(f"Error: {error_2}")
                try:
                    self.id_delete = self.lineEdit_8.text()
                    """SE ID FOR IGUAL A 0, RETORNA"""
                    if self.id_delete == '':
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'INFORME O ID')
                        return
                    if self.id_delete not in str(ids):
                        QtWidgets.QMessageBox.about(self.p_2_del, 'AVISO', 'ID NÃO ENCONTRADO')
                        return
                    else:
                        QtWidgets.QMessageBox.about(self.p_2_del, 'DELETADO', 'DELETADO COM SUCCESO')
                except:
                    print('error')
                else:
                    self.cursor = self.bd.cursor()
                    acao = 'DELETE FROM subjects WHERE id=?'
                    self.cursor.execute(acao, (self.id_delete,))
                    self.bd.commit()
                    self.update_database(self.tabela_deletar)
                    self.lineEdit_8.setText('')


        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.show()
    qt.exec_()
