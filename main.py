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
def has_key(chave):
	return (chave in tabela_de_simbolos.keys())


				


# Classe que implementa o scanner.
class Scanner:
	estado = None
	lexema = None
	token_atual = None
	
	# Função principal do scanner.
	def Scanner(self, entrada):

		if DEBUG: print("[LOG] Scanner chamado para a entrada \"{}\".".format(entrada))

		if self.estado is None:
			self.Reset()

		# Reconhece a string vazia como EOF.
		if entrada == "":
			return Token("EOF", "EOF", None)			
		
		# Indica se foi possível encontrar uma transição para o estado atual e entrada dada.
		sem_caminho = True

		proximo_estado = self.estado.busca_transicao(entrada)
		backup_token = self.token_atual

		if proximo_estado is None:
			self.Reset()
			proximo_estado = self.estado.busca_transicao(entrada)

		if proximo_estado is not None:
			self.estado = constantes.lista_de_estados[proximo_estado]
			self.lexema += entrada
			self.token_atual.classe = self.estado.token
			self.token_atual.lexema = self.lexema

		if proximo_estado is None:
			if self.estado.final:
				if self.token_atual.classe == "id":
					if has_key(self.lexema):
						# Atualiza o token atual com uma cópia da tabela de símbolos
						self.token_atual = tabela_de_simbolos[self.lexema]
					else:
						tabela_de_simbolos[self.lexema] = self.token_atual
					#força o reset na próxima chamada
					self.estado = None
			else:
				self.token_atual = backup_token
				self.token_atual.classe = "ERRO"
		
		return self.token_atual
	
	def Reset(self):
		self.estado = constantes.lista_de_estados["S0_A"]
		self.lexema = ""
		self.token_atual = Token("SO_A", self.lexema, None)


def main(arquivo):
	#printar o Token ou exibir o erro
	#exibir tabela_de_simbolos
	
	with open(arquivo) as fonte:
		token_retornado = Token("", "", None)
		scanner = Scanner()

		while token_retornado is not None and token_retornado.classe != "EOF":
			token_retornado = scanner.Scanner(fonte.read(1))

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