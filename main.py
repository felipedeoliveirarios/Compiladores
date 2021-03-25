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

		# Reconhece a string vazia como EOF.
		if entrada == "":
			return Token("EOF", "EOF", None)

		# Detecta strings formadas por apenas espaços
		if entrada.isspace():
			# Reinicia a máquina de estados
			self.estado = None
			if DEBUG: print("[LOG] Espaço encontrado. Retornando token anterior.")
			# Retorna o último token inalterado.
			return self.token_atual

		# Caso tenha sido reiniciada, volta ao estado original.
		if self.estado is None:
			self.estado = "S0_A"
			self.lexema = ""
			self.token_atual = Token(constantes.lista_de_estados[self.estado][1], self.lexema, None)
		
		# Indica se foi possível encontrar uma transição para o estado atual e entrada dada.
		sem_caminho = True
		
		# Percorre a tabela de transição.
		for transicao in constantes.tabela_de_transição:

			# Caso a transição sendo checada parta do estado atual
			if transicao[0] == self.estado:

				# Caso a entrada seja válida para a regra de transição
				if entrada in transicao[2]:
					
					if DEBUG: print("[LOG] Transicionando de {} para {} (entrada \"{}\" se encaixa na regra <{}>)".format(self.estado, transicao[1], entrada, transicao[2]))

					# Altera o estado.
					self.estado = transicao[1]

					# Adiciona o caractere de entrada ao lexema.
					self.lexema += entrada

					# Gira a flag de caminho.
					sem_caminho = False

					# Atualiza o token atual com a classe e o lexema.
					self.token_atual.classe = constantes.lista_de_estados[self.estado][1]
					self.token_atual.lexema = self.lexema

					# Encerra o loop.
					break

		# Caso a entrada não leve a nenhum outro estado
		if sem_caminho:
			if DEBUG: print("[LOG] Não foi encontrada uma transição para a entrada.")
			# Verifica se o estado atual é final.
			if constantes.lista_de_estados[self.estado][0]:
				if DEBUG: print("[LOG] O estado atual é final.")

				# Verifica se a classe do estado atual é ID.
				if constantes.lista_de_estados[self.estado][1] == "id":
					if DEBUG: print("[LOG] O estado atual é id.")
					# Verifica se o token relacionado ao identificador já está na tabela de símbolos
					if has_key(self.lexema):
						# Atualiza o token atual com uma cópia da tabela de símbolos
						if DEBUG: print("[LOG] Atualizando token na tabela de símbolos.")
						self.token_atual = tabela_de_simbolos[self.lexema]
						self.estado = None
						# Retorna o token copiado da tabela de símbolos
						return self.token_atual

					# Caso o token não esteja na tabela de símbolos...
					else:
						if DEBUG: print("[LOG] Inserindo token na tabela de símbolos.")
						# Adiciona o novo token à tabela.
						tabela_de_simbolos[self.lexema] = self.token_atual
				
				if DEBUG: print("[LOG] Reiniciando a Máquina de estados.")
				# Reinicia a máquina de estados, preparando para a próxima iteração.
				self.estado = None

				# Executa a máquina de estados do zero para a entrada atual.
				if DEBUG: print("[LOG] Reexecutando para \"{}\".".format(entrada))
				self.Scanner(entrada)

				# Retorna o token gerado na reexecução.
				return self.token_atual

			# Caso o estado atual não seja final (ERRO)...
			if DEBUG: print("[LOG] O estado atual não é final.")	
			else:
				# Reinicia a máquina de estados, preparando para a próxima iteração.
				self.estado = None
				# Retorna um token de erro.
				return Token("ERRO", self.lexema, None)
		
		# Caso tenha sido possível encontrar uma regra de transição para a entrada...
		else:
			# Retorna o token atualizado.
			return self.token_atual


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