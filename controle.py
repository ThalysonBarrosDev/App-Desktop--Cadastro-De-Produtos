from PyQt5 import uic, QtWidgets, QtGui
import mysql.connector
from reportlab.pdfgen import canvas
from time import sleep

banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Admin@master20',
    database='db_cadastro_produtos'
)

def editar_produtos():
    linha = lista_produtos.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('SELECT * FROM produtos WHERE id='+str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()
    
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))

def excluir_produto():
    linha = lista_produtos.tableWidget.currentRow()
    lista_produtos.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('DELETE FROM produtos WHERE id='+str(valor_id))

    sleep(1)
    produto_excluido.show()

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas('Relatorio_Produtos.pdf')
    pdf.setFont('Times-Bold', 25)
    pdf.drawString(200, 800, 'Produtos Cadastrados:')
    pdf.setFont('Times-Bold', 18)

    pdf.drawString(10, 750, 'ID')
    pdf.drawString(110, 750, 'CÓDIGO')
    pdf.drawString(210, 750, 'PRODUTO')
    pdf.drawString(310, 750, 'PREÇO')
    pdf.drawString(410, 750, 'CATEGORIA')

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 -y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 -y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 -y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 -y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 -y, str(dados_lidos[i][4]))
    
    pdf.save()

def funcao_principal():

    linha1 = front.lineEdit.text()
    linha2 = front.lineEdit_2.text()
    linha3 = front.lineEdit_3.text()

    categoria = ''
    
    if front.radioButton.isChecked():
        print('')
        print('Categoria: Informática')
        categoria = 'Informática'
    elif front.radioButton_2.isChecked():
        print('')
        print('Categoria: Alimentos')
        categoria = 'Alimentos'
    else:
        print('')
        print('Categoria: Eletrônicos')
        categoria = 'Eletrônicos'

    print('Código:',linha1)
    print('Descrição:',linha2)
    print('Preço:',linha3)

    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)'
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

    front.lineEdit.setText('')
    front.lineEdit_2.setText('')
    front.lineEdit_3.setText('')

    sleep(1)
    produto_cadastrado.show()

def pedidos_listados():
    lista_produtos.show()

    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
 
    lista_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_produtos.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            lista_produtos.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])
front = uic.loadUi('src/front.ui')
lista_produtos = uic.loadUi('src/lista_produtos.ui')
tela_editar = uic.loadUi('src/editar_produtos.ui')
produto_excluido = uic.loadUi('src/produto_excluido.ui')
produto_cadastrado = uic.loadUi('src/produto_cadastrado.ui')
front.pushButton.clicked.connect(funcao_principal)
front.pushButton_2.clicked.connect(pedidos_listados)
lista_produtos.pushButton.clicked.connect(gerar_pdf)
lista_produtos.pushButton_2.clicked.connect(excluir_produto)
lista_produtos.pushButton_3.clicked.connect(editar_produtos)

front.setWindowTitle('Cadastro de Produtos')
front.setWindowIcon(QtGui.QIcon('src/estoque.ico'))
lista_produtos.setWindowTitle('Lista de Produtos')
lista_produtos.setWindowIcon(QtGui.QIcon('src/estoque.ico'))
tela_editar.setWindowTitle('Editar Produto')
tela_editar.setWindowIcon(QtGui.QIcon('src/estoque.ico'))
produto_excluido.setWindowTitle('Produto Excluido')
produto_excluido.setWindowIcon(QtGui.QIcon('src/estoque.ico'))
produto_cadastrado.setWindowTitle('Produto Cadastrado')
produto_cadastrado.setWindowIcon(QtGui.QIcon('src/estoque.ico'))

front.show()
app.exec()