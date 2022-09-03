import sqlite3
import sys
from datetime import datetime, date
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence
from TelaGUI import *


class App(QMainWindow, QTableWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        super().setupUi(self)

        timer = QTimer(self)
        timer.timeout.connect(self.relojo)
        timer.start(1000)

        self.some = False
        self.dt_key = QShortcut(QKeySequence('esc'), self)
        self.dt_key.activated.connect(self.menu_esconde)

        ######################### BOTOES MENU LATERAL ###########################
        self.pushButton_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))  # HOME
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))  # TABELA
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))  # CAD ALUN
        self.pushButton_11.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))  # CAD PROF
        self.pushButton_13.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.pushButton_12.clicked.connect(self.fechar_app)  # SAIR
        # self.pushButton_13.clicked.connect(lambda: self.stackedWidget.setCurrentIndex())  # CAD NOTAS

        ######################### BOTOES DA PESQUISA ###########################
        self.pushButton.clicked.connect(self.btn_ser)
        self.pushButton_14.clicked.connect(lambda: self.atualizar_banco(self.tabela_geral))  # atualiza o banco
        self.pushButton_4.clicked.connect(self.btn3_cad)  # cad
        self.pushButton_5.clicked.connect(self.btn4_alt)
        self.pushButton_6.clicked.connect(self.btn6_dlt)

        ######################### BOTOES PARA CADASTRAR PROFESSOR #######################
        self.pushButton_9.clicked.connect(self.cadastrar_prof)

        ######################### BOTOES PARA CADASTRAR ALUNO ###########################
        self.pushButton_7.clicked.connect(self.cadastrar_aluno)
        self.pushButton_15.clicked.connect(self.btn15_cad)
        self.pushButton_16.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        ######################### BUTTON FOR ALTERAR ###########################
        self.pushButton_21.clicked.connect(self.btn21_alt)
        self.pushButton_20.clicked.connect(self.btn20_alt)
        self.pushButton_22.clicked.connect(self.alterar_cadastro)

        ######################### BOTOES MATERIA ###########################
        self.pushButton_29.clicked.connect(self.cad_mat)
        self.pushButton_31.clicked.connect(lambda :self.stackedWidget.setCurrentIndex(1))
        self.pushButton_30.clicked.connect(self.alt_mat)

        ######################### BOTOES DELETAR ###########################
        self.pushButton_17.clicked.connect(self.deleta_registro)
        self.pushButton_19.clicked.connect(lambda: self.atualizar_banco(self.tabela_deletar))
        self.pushButton_18.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

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

    def menu_esconde(self):
        if self.some:
            self.menu_bar.show()
            self.some = False
        else:
            self.menu_bar.hide()
            self.some = True

    def relojo(self):
        now = QTime.currentTime()
        label_hora = now.toString('hh:mm:ss')
        self.label_7.setText(label_hora)

        data_atual = date.today()
        h = '{}/{}/{}'.format(data_atual.day, data_atual.month,
                              data_atual.year)
        self.label_8.setText(str(h))

        ######################### FUNCOES DOS BTNS ###########################

    def btn_ser(self):
        self.procura = self.textEdit.toPlainText()
        self.pro_dif = self.comboBox_3.currentText()
        self.usu = self.comboBox.currentText()

        if self.procura == '':
            QtWidgets.QMessageBox.about(self.p2, 'AVISO', 'NENHUM VALOR FOI INSERIDO NA BARRA DE PESQUISA')
            return

        if self.pro_dif == 'ID':
            try:
                self.bd = sqlite3.connect('banco_dados/edu.db')
            except Exception as error:
                print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
            else:
                self.cursor = self.bd.cursor()
                acao = 'SELECT * FROM Aluno WHERE RA= ?'
                self.cursor.execute(acao, (self.procura,))
                self.bd.commit()

                self.atualiza_pessoa(self.tabela_geral)

    def btn3_cad(self):
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
            self.atualizar_banco(self.tabela_alterar)

        elif self.comboBox.currentText() == 'Professor':
            self.label_6.setText('ALTERAR PROFESSOR')
            self.stack = self.stackedWidget.setCurrentIndex(4)
            self.atualizar_banco(self.tabela_alterar)

        elif self.comboBox.currentText() == 'Materias':
            self.stack = self.stackedWidget.setCurrentIndex(8)
            self.atualizar_banco(self.tabela_materia)
            self.lineEdit_15.show()
            self.lineEdit_24.hide()
            self.lineEdit_25.hide()
            self.pushButton_29.hide()
            self.pushButton_30.show()
            self.pushButton_32.hide()
            self.pushButton_33.hide()

    def btn6_dlt(self):
        self.stack = self.stackedWidget.setCurrentIndex(5)
        self.atualizar_banco(self.tabela_deletar)

    def btn15_cad(self):
        self.atualizar_banco(self.tabela_geral)
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

    def btn21_alt(self):
        if self.lineEdit_14.text() == "":
            QtWidgets.QMessageBox.about(self.p_2_alt, 'AVISO', 'INSIRA UM ID')
            return

        id_alterar = self.lineEdit_14.text()
        self.bd = sqlite3.connect('banco_dados/edu.db')
        self.cursor = self.bd.cursor()

        if self.comboBox.currentText() == 'Alunos':
            self.cursor.execute("SELECT RA FROM Aluno")
            self.dados_3 = self.cursor.fetchall()
            lista_vazia = []
            for i in self.dados_3:
                lista_vazia.append(i)
            if id_alterar not in str(lista_vazia):
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

                self.cursor.execute("SELECT * FROM Aluno WHERE RA = ?", (id_alterar,))
                self.dados_3 = self.cursor.fetchall()

                for i in self.dados_3:
                    self.lineEdit_9.setText(f'{i[1]}')
                    self.lineEdit_11.setText(f'{i[2]}')
                    self.lineEdit_13.setText(f'{i[4]}')
                    # self.lineEdit_12.setText(f'{i[4]}')
                    conver_data = datetime.strptime(i[5], '%d/%m/%Y').date()
                    self.dateEdit_3.setDate(conver_data)
                    self.lineEdit_10.setText(f'{i[3]}')
            except Exception as error:
                print(f'Error: {error}')

        if self.comboBox.currentText() == 'Professor':
            self.cursor.execute("SELECT id FROM Professor")
            self.dados_3 = self.cursor.fetchall()
            lista_vazia = []
            for i in self.dados_3:
                lista_vazia.append(i)
            if id_alterar not in str(lista_vazia):
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

                self.cursor.execute("SELECT * FROM Professor WHERE id = ?", (id_alterar,))
                self.dados_3 = self.cursor.fetchall()

                for i in self.dados_3:
                    self.lineEdit_9.setText(f'{i[1]}')
                    self.lineEdit_10.setText(f'{i[2]}')
                    self.lineEdit_13.setText(f'{i[3]}')
                    conver_data = datetime.strptime(i[5], '%d/%m/%Y').date()
                    self.dateEdit_3.setDate(conver_data)
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

    def fechar_app(self):
        sys.exit()

    ######################### BANCO DE DADOS ###########################

    ######## CADASTRAR ALUNO #########
    def cadastrar_aluno(self):
        numeros = '1234567890'
        caracter_s = '!@#$%¨&*()_-+=[]{}'
        lista_nome_vazia = []
        # CONFERINDO NOME E SOBRENOME
        try:
            self.nome = self.lineEdit.text().strip() + ' ' + self.lineEdit_2.text().strip()
            self.resp = self.lineEdit_5.text().strip()
            self.cel = self.lineEdit_3.text().strip()
            self.data = self.dateEdit.text()
            self.cpf = self.lineEdit_4.text()

            if self.nome == '' or self.resp == '' or self.cpf == '':
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'Existe campos vazios')
                return

            # VERIFICANDO NOME
            for a in self.nome:
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

            # VEREFICAR O CPF
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
                return

        except:
            print('error')

        # enviando os dados
        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            self.cursor = self.bd.cursor()
            acao = 'INSERT INTO Aluno (nome, nome_resp, cpf, celular, data_nasc) VALUES (?,?,?,?,?)'
            self.cursor.execute(acao, (self.nome.upper(), self.resp.upper(), self.cpf, self.cel, self.data))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'CADASTRADO COM SUCESSO')

            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')

    ######## CADASTRAR PROFESSOR #########
    def cadastrar_prof(self):
        numeros = '1234567890'
        caracter_s = '!@#$%¨&*()_-+=[]{}'
        lista_nome_vazia = []

        self.nome = self.lineEdit_6.text().strip()
        self.cel = self.lineEdit_7.text().strip()
        self.data = self.dateEdit_2.text()

        if self.nome == '' or self.cel == '':
            QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'Existe campos vazios')
            return

        # VERIFICANDO NOME DO PROFESSOR
        for a in self.nome:
            lista_nome_vazia.append(a)
        for a in lista_nome_vazia:
            if a in numeros:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                return
            elif a in caracter_s:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', f'VALOR INCORRETO EM NOME: {a}')
                return

            # VERIFICA CEL
            '''if int(self.cel) != int:
                QtWidgets.QMessageBox.about(self.p_2_cad, 'AVISO', 'NUMERO INVALIDO')
                return'''
        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            self.cursor = self.bd.cursor()
            acao = 'INSERT INTO Professor (nome, celular, data_nasc) VALUES (?,?,?)'
            self.cursor.execute(acao, (self.nome, self.cel, self.data))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'PROFESSOR CADASTRADO')

            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')

    ######## CADASTRAR MAT #########
    def cad_mat(self):
        numeros = "1234567890"
        self.nome_mat = self.lineEdit_24.text()
        self.nome_prof = self.lineEdit_25.text()

        if self.nome_mat == '':
            QMessageBox.about(self.p5_mat, "AVISO", "INSIRA UM NOME")
            return
        if self.nome_prof not in numeros:
            QMessageBox.about(self.p5_mat, "AVISO", "APENAS NUMEROS NO ID PROFESSOR")
            return

        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            self.cursor = self.bd.cursor()
            acao = 'INSERT INTO Materia (nome, prof_materia) VALUES (?,?)'
            self.cursor.execute(acao, (self.nome_mat.upper(), self.nome_prof))
            self.bd.commit()
            QtWidgets.QMessageBox.about(self.p_2_cad, 'CADASTRADO', 'CADASTRADO COM SUCESSO')

    def alt_mat(self):
        pass

    ######## ALTERAR BANCO #########
    def alterar_cadastro(self):
        self.nome = self.lineEdit_9.text()
        self.resp = self.lineEdit_11.text()
        self.cel = self.lineEdit_13.text()
        self.data = self.dateEdit_3.text()
        self.cpf = self.lineEdit_10.text()

        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            if self.comboBox.currentText() == 'Alunos':
                self.cursor = self.bd.cursor()
                acao = 'UPDATE Aluno SET nome = ?, nome_resp = ?, cpf = ?, celular = ?, data_nasc = ? WHERE RA = ?'
                self.cursor.execute(acao, (
                    self.nome.upper(), self.resp.upper(), self.cpf, self.cel, self.data, self.lineEdit_14.text()))
                self.bd.commit()
                QtWidgets.QMessageBox.about(self.p_2_cad, 'ALTERADO', 'ALTERADO COM SUCESSO')

            if self.comboBox.currentText() == 'Professor':
                self.lineEdit_11.hide()

                self.cursor = self.bd.cursor()
                acao = 'UPDATE Professor SET nome = ?, cpf = ?, celular = ?, data_nasc = ? WHERE id = ?'
                self.cursor.execute(acao, (
                    self.nome.upper(), self.cpf, self.cel, self.data, self.lineEdit_14.text()))
                self.bd.commit()
                QtWidgets.QMessageBox.about(self.p_2_cad, 'ALTERADO', 'ALTERADO COM SUCESSO')

            self.lineEdit_9.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_14.setText('')

            self.atualizar_banco(self.tabela_alterar)

    ######## ATUALIZAR BANCO #########
    def atualizar_banco(self, tabela):
        self.nome_tabela = tabela

        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            ######## ALUNOS #########
            if self.comboBox.currentText() == 'Alunos':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT * FROM aluno')
                self.dados = self.cursor.fetchall()

                # Duas listas para definir nomes na coluna e nas linhas
                nomes = ['ID', 'NOME', 'RESPONSAVEL', 'CPF', 'CELULAR', 'DATA DE NASC.']
                lista_vazia = []
                for x in range(0, len(self.dados)):
                    lista_vazia.append(' ')

                # Alteração nas colunas
                self.nome_tabela.setRowCount(len(self.dados))
                self.nome_tabela.setColumnCount(6)
                self.nome_tabela.setColumnWidth(0, 15)
                self.nome_tabela.setColumnWidth(1, 200)
                self.nome_tabela.setColumnWidth(2, 150)
                self.nome_tabela.setColumnWidth(3, 100)
                self.nome_tabela.setColumnWidth(4, 100)
                self.nome_tabela.setVerticalHeaderLabels(lista_vazia)
                self.nome_tabela.setHorizontalHeaderLabels(nomes)

                # Adicinamos Items na coluna
                for l in range(0, len(self.dados)):
                    for c in range(0, 6):
                        self.nome_tabela.setItem(l, c, QTableWidgetItem(str(self.dados[l][c])))

            ######## PROFESSORES #########
            elif self.comboBox.currentText() == 'Professor':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT * FROM Professor')
                self.dados = self.cursor.fetchall()

                nomes = ['ID', 'NOME', 'CPF', 'CELULAR', 'DATA NASC']
                lista_vazia = []
                for x in range(0, len(self.dados)):
                    lista_vazia.append(' ')

                self.nome_tabela.setRowCount(len(self.dados))
                self.nome_tabela.setColumnCount(5)
                self.nome_tabela.setColumnWidth(0, 15)
                self.nome_tabela.setColumnWidth(1, 200)
                self.nome_tabela.setColumnWidth(3, 115)
                self.nome_tabela.setVerticalHeaderLabels(lista_vazia)
                self.nome_tabela.setHorizontalHeaderLabels(nomes)

                for l in range(0, len(self.dados)):
                    for c in range(0, 4):
                        self.nome_tabela.setItem(l, c, QTableWidgetItem(str(self.dados[l][c])))

            ######## MATERIAS #########
            if self.comboBox.currentText() == 'Materias':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT * FROM Materia')
                self.dados = self.cursor.fetchall()

                # Duas listas para definir nomes na coluna e nas linhas
                nomes = ['ID', 'NOME', 'PROFESSOR']
                lista_vazia = []
                for x in range(0, len(self.dados)):
                    lista_vazia.append(' ')

                # Alteração nas colunas
                self.nome_tabela.setRowCount(len(self.dados))
                self.nome_tabela.setColumnWidth(1, 200)
                self.nome_tabela.setColumnCount(3)
                self.nome_tabela.setVerticalHeaderLabels(lista_vazia)
                self.nome_tabela.setHorizontalHeaderLabels(nomes)

                # Adicinamos Items na coluna
                for l in range(0, len(self.dados)):
                    for c in range(0, 3):
                        self.nome_tabela.setItem(l, c, QTableWidgetItem(str(self.dados[l][c])))

    def atualiza_pessoa(self, tabela):
        self.nome_tabela = tabela

        self.seletor = self.textEdit.toPlainText()
        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            ######## SELECIONA UM ALUNO #########
            if self.comboBox.currentText() == 'Alunos' and self.comboBox_3 != '':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor = self.bd.cursor()
                if self.comboBox_3.currentText() == "ID":
                    try:
                        self.seletor_num = int(self.seletor)
                    except:
                        QMessageBox.about(self.p2, "Aviso", "DIGITE APENAS NUMEROS")
                        self.textEdit.setText('')
                        return
                    else:
                        self.cursor.execute('SELECT * FROM Aluno WHERE RA=?', (int(self.seletor),))

                if self.comboBox_3.currentText() == "NOME":
                    self.cursor.execute('SELECT * FROM Aluno WHERE nome=?', (self.seletor.upper(),))
                self.dados = self.cursor.fetchall()
                print('ola')
                try:
                    if self.dados[0][0]:
                        print(self.dados[0][0])
                        print(self.dados[0][1])

                except:
                    QMessageBox.about(self.p2, "AVISO", "ID NÃO ENCONTRADO")
                    self.textEdit.setText('')
                    return

                # Duas listas para definir nomes na coluna e nas linhas
                nomes = ['ID', 'NOME', 'RESPONSAVEL', 'CPF', 'CELULAR', 'DATA DE NASC.']
                lista_vazia = []

                # Alteração nas colunas
                self.nome_tabela.setRowCount(len(self.dados))
                self.nome_tabela.setColumnCount(6)
                self.nome_tabela.setColumnWidth(0, 15)
                self.nome_tabela.setColumnWidth(1, 150)
                self.nome_tabela.setColumnWidth(3, 50)
                self.nome_tabela.setVerticalHeaderLabels(lista_vazia)
                self.nome_tabela.setHorizontalHeaderLabels(nomes)

                for l in range(0, len(self.dados)):
                    for c in range(6):
                        self.nome_tabela.setItem(l, c, QTableWidgetItem(str(self.dados[l][c])))
                self.textEdit.setText('')

            ######## SELECIONA UM PROFESSORE #########
            elif self.comboBox.currentText() == 'Professor':
                # chamamos o banco de dados e pedimos um SELECT
                self.cursor = self.bd.cursor()
                if self.comboBox_3.currentText() == "ID":
                    try:
                        self.seletor_num = int(self.seletor)
                    except:
                        QMessageBox.about(self.p2, "Aviso", "DIGITE APENAS NUMEROS")
                        self.textEdit.setText('')
                        return
                    else:
                        self.cursor.execute('SELECT * FROM Professor WHERE id=?', (int(self.seletor),))

                if self.comboBox_3.currentText() == "NOME":
                    self.cursor.execute('SELECT * FROM Professor WHERE nome=?', (self.seletor.upper(),))
                self.dados = self.cursor.fetchall()

                try:
                    if self.dados[0][0]:
                        print(self.dados[0][0])
                        print(self.dados[0][1])

                except:
                    QMessageBox.about(self.p2, "AVISO", "ID NÃO ENCONTRADO")
                    self.textEdit.setText('')
                    return
                nomes = ['ID', 'NOME', 'CPF', 'DATA NASC']
                lista_vazia = []
                for x in range(0, len(self.dados)):
                    lista_vazia.append(' ')

                self.nome_tabela.setRowCount(len(self.dados))
                self.nome_tabela.setColumnCount(4)
                self.nome_tabela.setColumnWidth(0, 15)
                self.nome_tabela.setColumnWidth(1, 200)
                self.nome_tabela.setColumnWidth(3, 115)
                self.nome_tabela.setVerticalHeaderLabels(lista_vazia)
                self.nome_tabela.setHorizontalHeaderLabels(nomes)

                for l in range(0, len(self.dados)):
                    for c in range(0, 4):
                        self.nome_tabela.setItem(l, c, QTableWidgetItem(str(self.dados[l][c])))

    ######## DELETAR CADASTROS #########
    def deleta_registro(self):
        ids = []
        try:
            self.bd = sqlite3.connect('banco_dados/edu.db')
        except Exception as error:
            print(f'OCORREU UM ERRO NO BANCO DE DADOS: {error}')
        else:
            if self.comboBox.currentText() == 'Aluno':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT RA FROM Aluno')
                self.dados_2 = self.cursor.fetchall()
                for x in self.dados_2:
                    ids.append(x)
                if ids == []:
                    try:
                        self.cursor_2 = self.bd.cursor()
                        self.cursor_2.execute("SELECT seq FROM sqlite_sequence WHERE name = 'Aluno'")
                        self.cursor_3 = self.bd.cursor()
                        self.cursor_3.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Aluno' ")
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
                    acao = 'DELETE FROM Aluno WHERE RA=?'
                    self.cursor.execute(acao, (self.id_delete,))
                    self.bd.commit()
                    self.cursor.close()
                    self.atualizar_banco(self.tabela_deletar)
                    self.lineEdit_8.setText('')

            if self.comboBox.currentText() == 'Professor':
                self.cursor = self.bd.cursor()
                self.cursor.execute('SELECT id FROM Professor')
                self.dados_2 = self.cursor.fetchall()
                for x in self.dados_2:
                    ids.append(x)
                if ids == []:
                    # SE TODOS OS DADOS FOREM APAGADOS, SEQ RETORNA PARA 0
                    try:
                        self.cursor_2 = self.bd.cursor()
                        self.cursor_2.execute("SELECT seq FROM sqlite_sequence WHERE name = 'Professor'")
                        self.cursor_3 = self.bd.cursor()
                        self.cursor_3.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'Professor' ")
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
                    acao = 'DELETE FROM Professor WHERE id=?'
                    self.cursor.execute(acao, (self.id_delete,))
                    self.bd.commit()
                    self.cursor.close()
                    self.atualizar_banco(self.tabela_deletar)
                    self.lineEdit_8.setText('')


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = App()
    app.show()
    qt.exec_()
