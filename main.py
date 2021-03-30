import constantes
from beautifultable import BeautifulTable

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

			self.buffer = self.buffer[self.indice:]

			self.Reset()

			return Token(classe, (self.indice, lexema), None)

def main(arquivo):
	#printar o Token ou exibir o erro
	#exibir tabela_de_simbolos
	
	with open(arquivo) as fonte:
		scanner = Scanner()
		token_retornado = Token("","",None)

		scanner.Alimentar(fonte.read())

		while token_retornado.classe != "EOF":

			token_retornado = scanner.Scanner()

			if(token_retornado.classe == "ERRO"):
				print("Classe: \"{}\", Lexema: \"{}\", Tipo: \"{}\"".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))
			else:
				if token_retornado.classe != "EOF":
					print("Classe: \"{}\", Lexema: \"{}\", Tipo: \"{}\"".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))
	
	tabela = BeautifulTable()
	tabela.columns.header = ["Classe", "Lexema", "Tipo"]
	for chave in tabela_de_simbolos.keys():
		token = tabela_de_simbolos[chave]
		tabela.rows.append([token.classe, token.lexema, token.tipo]) 
	print(tabela)

if __name__ == "__main__":
	main("fonte.alg")