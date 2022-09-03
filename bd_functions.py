import sqlite3
class BancoTeste:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.cursor = self.conn.cursor()

    def inserir(self, aluno, data_n, cpf, serie):
        acao = ("INSERT INTO Aluno (nome_aluno, data_nascimento, cpf, serie) VALUES (?,?,?,?)")
        self.cursor.execute(acao, (aluno, data_n, cpf, serie))
        self.conn.commit()
        print('aluno inserido')

    def inserir_notas(self, serie, semestre, h, m, p, c):
        acao = ("INSERT INTO notas (serie, semestre, historia, matematica, portugues, ciencias) VALUES (?,?,?,?,?,?)")
        self.cursor.execute(acao, (serie, semestre,h,m,p,c))
        self.conn.commit()
        print('aluno inserido')


    def editar(self):
        pass

    def excluir(self):
        pass

    def mostra(self,):
        acao = ("SELECT * FROM aluno")
        self.cursor.execute(acao)
        self.conn.commit()

        for linha in self.cursor.fetchall():
            print(linha)

    def mostrar_2(self):
        acao = "SELECT RA FROM Aluno"
        self.cursor.execute(acao)
        self.conn.commit()

        for lin in self.cursor.fetchall():
            print(lin)

    def fechar(self):
        self.cursor.close()
        self.conn.close()

    def alterar_seq(self):
        self.cursor.execute('UPDATE sqlite_sequence SET seq = 1 WHERE seq = 7')

    def inserir_nota(self):
        self.cursor.execute("INSERT INTO Nota (id_aluno, id_materia, nota1, nota2, nota3, trimestre, ano) VALUES (4, 1, 3, 8, 10, 1, 8)")
        self.conn.commit()

    def mostrar_tabelas(self):
        self.cursor.execute('SELECT Nota.id, Aluno.nome, Nota.nota1, Nota.trimestre FROM Nota INNER JOIN Aluno ON Nota.id_aluno=Aluno.RA')

        for lin in self.cursor.fetchall():
            print(lin)
        self.conn.commit()

    def select_one(self, id_aluno):
        self.cursor.execute('SELECT * FROM Aluno WHERE RA = ?', (id_aluno, ))

        for aluno in self.cursor.fetchone():
            print(aluno)
        self.conn.commit()

if __name__ == '__main__':
    bd = BancoTeste('banco_dados/edu.db')
    bd.select_one(1)
    print("#" * 15)
    bd.mostrar_tabelas()
    bd.fechar()