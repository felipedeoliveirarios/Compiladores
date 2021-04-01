import constantes
import argparse

# Classe responsável por armazenar os dados de um TOKEN
class TOKEN:
	classe, lexema, tipo = None, None, None

	def __init__(self, classe, lexema, tipo):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo

# TABELA DE SÍMBOLOS, responsável por armazenar os identificadores reconhecidos e palavras reservadas
TABELA_DE_SIMBOLOS = {"inicio": TOKEN("inicio", "inicio", None),
                      "varinicio": TOKEN("varinicio", "varinicio", None),
                      "varfim": TOKEN("varfim", "varfim", None),
                      "escreva": TOKEN("escreva", "escreva", None),
                      "leia": TOKEN("leia", "leia", None),
                      "se": TOKEN("se", "se", None),
                      "entao": TOKEN("entao", "entao", None),
                      "fimse": TOKEN("fimse", "fimse", None),
                      "faca-ate": TOKEN("faca-ate", "faca-ate", None),
                      "fimfaca": TOKEN("fimfaca", "fimfaca", None),
                      "fim": TOKEN("fim", "fim", None),
                      "inteiro": TOKEN("inteiro", "inteiro", None),
                      "lit": TOKEN("lit", "lit", None),
                      "real": TOKEN("real", "real", None)}

# Função que confere se uma chave está na tabela de símbolos.
def HasKey(chave):
	return (chave in TABELA_DE_SIMBOLOS.keys())

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

	# FUNÇÃO SCANNER.
	def SCANNER(self):
		
		if self.buffer == "":
			return TOKEN("EOF", "EOF", None)

		while True:
			proximo_estado = self.estado.busca_transicao(self.buffer[self.indice])

			if self.buffer[self.indice] == "\n":
				self.linha += 1
				self.coluna = 0
			
			else:
				self.coluna += 1


			if proximo_estado is None:
				break
			
			self.estado = constantes.lista_de_estados[proximo_estado]			
			self.indice += 1

			if self.indice == len(self.buffer):
				break

		if self.estado.final:
			lexema = self.buffer[0:self.indice]
			classe = self.estado.classe

			if classe == "id":
				if not HasKey(lexema):
					TABELA_DE_SIMBOLOS[lexema] = TOKEN(classe, lexema, None)
				
				self.buffer = self.buffer[self.indice:]
				self.Reset()

				return TABELA_DE_SIMBOLOS[lexema]

			else:
				self.buffer = self.buffer[self.indice:]
				self.Reset()

				return TOKEN(classe, lexema, None)
		
		# Estado de parada não é final
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

			return TOKEN(classe, self.indice, None)

# FUNÇÃO ERROR
def ERROR(classe, linha, coluna):
	mensagem = ""

	if classe == "ERRO1":
		mensagem = "Caracter não reconhecido pela linguagem."
	
	else:
		mensagem = "Caracter não esperado."
	
	print("{} - {}, linha {} e coluna {}".format(classe, mensagem, linha, coluna))

# FUNÇÃO PRINCIPAL
def PRINCIPAL(arquivo):	
	with open(arquivo) as fonte:
		scanner = Scanner()	# Constrói um objeto do tipo Scanner
		token_retornado = TOKEN("","",None)

		scanner.Alimentar(fonte.read())

		while token_retornado.classe is None or token_retornado.classe != "EOF":

			token_retornado = scanner.SCANNER()

			if token_retornado.classe is not  None and "ERRO" in token_retornado.classe:
				ERROR(token_retornado.classe, scanner.linha, scanner.coluna - 1)
			
			else:
				# Garante que não é comentário, nem EOF, nem espaço vazio.
				if token_retornado.classe is not None and token_retornado.classe != "EOF" and token_retornado.classe != "\s":
					print("Classe: \"{}\", Lexema: \"{}\", Tipo: \"{}\"".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("fonte", help = "Caminho do arquivo de entrada")
	args = parser.parse_args()
	PRINCIPAL(args.fonte)