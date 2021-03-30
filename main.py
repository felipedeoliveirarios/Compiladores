import constantes
from beautifultable import BeautifulTable

import argparse

DEBUG = False

# Classe responsável por armazenar os dados de um token
class Token:
	classe, lexema, tipo = None, None, None

	def __init__(self, classe, lexema, tipo):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo

# Tabela de símbolos, responsável por armazenar os identificadores reconhecidos e palavras reservadas
tabela_de_simbolos = {"inicio": Token("inicio", "inicio", None),
                      "varinicio": Token("varinicio", "varinicio", None),
                      "varfim": Token("varfim", "varfim", None),
                      "escreva": Token("escreva", "escreva", None),
                      "leia": Token("leia", "leia", None),
                      "se": Token("se", "se", None),
                      "entao": Token("entao", "entao", None),
                      "fimse": Token("fimse", "fimse", None),
                      "faca-ate": Token("faca-ate", "faca-ate", None),
                      "fimfaca": Token("fimfaca", "fimfaca", None),
                      "fim": Token("fim", "fim", None),
                      "inteiro": Token("inteiro", "inteiro", None),
                      "lit": Token("lit", "lit", None),
                      "real": Token("real", "real", None)}

# Função que confere se uma chave está na tabela de símbolos.
def HasKey(chave):
	return (chave in tabela_de_simbolos.keys())

# Classe que implementa o scanner.
class Scanner:
	estado = None
	buffer = None
	indice = None
	linha = 0
	coluna = 0

	def __init__(self):
		self.estado = constantes.lista_de_estados["S0_A"]
		self.indice = 0

	def Alimentar(self, entrada):
		self.buffer = entrada
	
	def Reset(self):
		self.estado = constantes.lista_de_estados["S0_A"]
		self.indice = 0
		
		if DEBUG:
			print("RESETAMOS PARA O ESTADO INICIAL. TAMANHO DO BUFFER: {}".format(len(self.buffer)))

	# Função principal do scanner.
	def Scanner(self):
		
		if self.buffer == "":
			return Token("EOF", "EOF", None)

		while True:
			proximo_estado = self.estado.busca_transicao(self.buffer[self.indice])

			if self.buffer[self.indice] == "\n":
				self.linha += 1
				self.coluna = 0
			else:
				self.coluna += 1


			if proximo_estado is None:
				break

			if DEBUG:
				print("INDICE: {}; TAMANHO DO BUFFER: {}".format(self.indice,len(self.buffer)))
			
			self.estado = constantes.lista_de_estados[proximo_estado]			
			self.indice += 1

			if self.indice == len(self.buffer):
				break
		
		if DEBUG:
			print("REMOVENDO DO BUFFER: \"{}\"".format(self.buffer[0:self.indice]))

		if self.estado.final:
			lexema = self.buffer[0:self.indice]
			classe = self.estado.token

			if classe == "id":
				if not HasKey(lexema):
					tabela_de_simbolos[lexema] = Token(classe, lexema, None)
				
				self.buffer = self.buffer[self.indice:]
				self.Reset()

				return tabela_de_simbolos[lexema]
			else:
				self.buffer = self.buffer[self.indice:]
				self.Reset()

				return Token(classe, lexema, None)
		else:
			lexema = self.buffer[0:self.indice]
			
			classe = "ERRO"

			if self.estado == constantes.lista_de_estados["S0_A"]:
				classe = "ERRO1"
			else:
				classe = "ERRO2"
			
			self.indice += 1
			self.buffer = self.buffer[self.indice:]

			self.Reset()

			return Token(classe, self.indice, None)

def Error(classe, linha, coluna):
	mensagem = ""

	if classe == "ERRO1":
		mensagem = "Caracter não reconhecido pela linguagem."
	else:
		mensagem = "Caracter não esperado."
	
	print("{} - {}, linha {} e coluna {}".format(classe, mensagem, linha, coluna))


def main(arquivo):
	#printar o Token ou exibir o erro
	#exibir tabela_de_simbolos
	
	with open(arquivo) as fonte:
		scanner = Scanner()
		token_retornado = Token("","",None)

		scanner.Alimentar(fonte.read())

		while token_retornado.classe != "EOF":

			token_retornado = scanner.Scanner()

			if "ERRO" in token_retornado.classe:
				Error(token_retornado.classe, scanner.linha, scanner.coluna - 1)
			else:
				if token_retornado.classe is not None and token_retornado.classe != "EOF" and token_retornado.classe != "\s":
					print("Classe: \"{}\", Lexema: \"{}\", Tipo: \"{}\"".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))
	
	if DEBUG:
		tabela = BeautifulTable()
		tabela.columns.header = ["Classe", "Lexema", "Tipo"]
		for chave in tabela_de_simbolos.keys():
			token = tabela_de_simbolos[chave]
			tabela.rows.append([token.classe, token.lexema, token.tipo]) 
		print(tabela)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("fonte", help = "Caminho do arquivo de entrada")
	args = parser.parse_args()
	main(args.fonte)