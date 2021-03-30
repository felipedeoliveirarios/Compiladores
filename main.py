import constantes
from beautifultable import BeautifulTable

DEBUG = True

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

		# Reinicia a máquina de estados se o estado atual for definido como None.
		if self.estado is None:
			self.Reset()
		
		# Reconhece a string vazia como EOF.
		if entrada == "":
			if DEBUG: print("[LOG] EOF encontrado.")
			self.estado = None
			return Token("EOF", "EOF", None)

		# Testa se existe uma transição do estado atual que aceite a entrada.
		proximo_estado = self.estado.busca_transicao(entrada)

		# Salva o token atual para possível uso em erros.
		backup_token = self.token_atual

		# Caso não hajam transições do estado atual da máquina que aceitem a entrada dada...
		if proximo_estado is None:
			if DEBUG: print("[LOG] Sem transições partindo do estado atual com a entrada \"{}\".".format(self.estado))

			# Caso o estado atual seja final, encerra o token atual e reinicia a execução à partir do estado inicial para o símbolo lido.
			if self.estado.final:

				if self.token_atual.classe == "id":
					if DEBUG: print("[LOG] O token atual é um identificador.")
					# Confere se o identificador já está na tabela de símbolos
					if has_key(self.lexema):
						if DEBUG: print("[LOG] Token já presente na tabela de símbolos.")
						# Atualiza o token atual com uma cópia da tabela de símbolos
						self.token_atual = tabela_de_simbolos[self.lexema]
					else:
						if DEBUG: print("[LOG] Adicionando novo símbolo na tabela (\"{}\").".format(self.lexema))
						tabela_de_simbolos[self.lexema] = self.token_atual
				
				
				# Reinicia o scanner
				self.Reset()
				# Tenta encontrar uma nova transição para a entrada à partir do estado inicial.
				proximo_estado = self.estado.busca_transicao(entrada)

		# Caso tenha sido possível efetuar uma transição da máquina de estados...
		if proximo_estado is not None:
			if DEBUG: print("[LOG] Efetuando transição para {}.".format(proximo_estado))
			self.estado = constantes.lista_de_estados[proximo_estado]
			# Adiciona a entrada ao lexema do token em análise
			self.lexema += entrada
			# Atualiza lexema e estado do token em análise
			self.token_atual.classe = self.estado.token
			self.token_atual.lexema = self.lexema

		# Caso não tenha sido possível efetuar uma transição da máquina de estados...
		else:
			if DEBUG: print("[LOG] Sem transições disponíveis.")
			# Confere se o estado atual é final
			if self.estado.final:
				if DEBUG: print("[LOG] O estado atual é final.")
				# Confere se o token atual é um identificador
				if self.token_atual.classe == "id":
					if DEBUG: print("[LOG] O token atual é um identificador.")
					# Confere se o identificador já está na tabela de símbolos
					if has_key(self.lexema):
						if DEBUG: print("[LOG] Token já presente na tabela de símbolos.")
						# Atualiza o token atual com uma cópia da tabela de símbolos
						self.token_atual = tabela_de_simbolos[self.lexema]
					else:
						if DEBUG: print("[LOG] Adicionando novo símbolo na tabela (\"{}\").".format(self.lexema))
						tabela_de_simbolos[self.lexema] = self.token_atual
					#força o reset na próxima chamada
					self.estado = None
			else:
				self.token_atual = backup_token
				self.token_atual.lexema += self.lexema
				self.token_atual.classe = "ERRO"
		
		return self.token_atual
	
	def Reset(self):
		if DEBUG: print("[LOG] Reiniciando Scanner.")
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