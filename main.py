import constantes

class Token:
	classe, lexema, tipo = None, None, None

	def __init__(self, classe, lexema, tipo):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo

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

def has_key(chave):
	return (chave in tabela_de_simbolos.keys())

class Scanner:
	estado = None
	lexema = None
	token_atual = None
	
	def Scanner(self, entrada):
		if entrada == "":
			return Token("EOF", "EOF", None)

		if self.estado is None:
			self.estado = "S0_A"
			self.lexema = ""
			self.token_atual = Token(constantes.lista_de_estados[self.estado][1], self.lexema, None)
		
		sem_caminho = True
		
		for transicao in constantes.tabela_de_transição:
			if transicao[0] == self.estado:					# se a transição checada parte do estado atual
				if entrada in transicao[2]:					# se a entrada faz parte da regra de transição
					self.estado = transicao[1]
					self.lexema += entrada
					sem_caminho = False
					break

		self.token_atual.classe = constantes.lista_de_estados[self.estado][1]
		self.token_atual.lexema = self.lexema

		if sem_caminho:
			if constantes.lista_de_estados[self.estado][0]:					#verifica se o estado é final
				if constantes.lista_de_estados[self.estado][1] == "id":		#verifica se a classe do estado é id

					if has_key(self.lexema):								#verifica se o token já está na tabela de simbolos
						return tabela_de_simbolos[self.lexema]				#retorna o token se ele já estiver na tabela
					else:												
						tabela_de_simbolos[self.lexema] = self.token_atual	#adiciona na tabela o novo token
				
				self.estado = None										#reseta o estado pra próxima iteração
				return self.token_atual										#retorna o token lido
					
			else:															#é ERRO
				self.estado = None
				return Token("ERRO", self.lexema, None)
		else:
			self.estado = None
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
				print("ARRUMAR DEPOIS")
			else:
				if token_retornado.classe != "EOF":
					print("Classe: \"{}\", Lexema: \"{}\", Tipo: \"{}\"".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))

if __name__ == "__main__":
	main("fonte.alg")