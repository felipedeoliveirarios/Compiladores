import constantes

class Token:
  	classe, lexema, tipo = None, None, None

	def __init__(classe, lexema, tipo):
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
	
	def Scanner(entrada):
		if self.estado is None:
			self.estado = "S0"
			self.lexema = ""
			self.token_atual = Token(constantes.lista_de_estados[self.estado][1], self.lexema, None)
		
		erro = True
		
		for transicao in constantes.tabela_de_transição:
			if transicao[0] == estado:
				if entrada in transicao[2]:
					self.estado = transicao[1]
					self.lexema += entrada
					erro = False
					break

		self.token_atual.classe = constantes.lista_de_estados[self.estado][1]
		self.token_atual.lexema = self.lexema

		if erro:
			if constantes.lista_de_estados[self.estado][0]:					#verifica se o estado é final
				if constantes.lista_de_estados[self.estado][1] == "id":		#verifica se a classe do estado é id
					
					self.estado = None										#reseta o estado pra próxima iteração

					if has_key(self.lexema):								#verifica se o token já está na tabela de simbolos
						return tabela_de_simbolos[self.lexema]				#retorna o token se ele já estiver na tabela
					else:												
						tabela_de_simbolos[self.lexema] = self.token_atual	#adiciona na tabela o novo token							
				return self.token_atual										#retorna o token lido
					
			else:															#é ERRO
				pass														#PRA FAZER DEPOIS


def main(arquivo):
	#abrir o arquivo fonte
	#invocar o scanner em loop
	#printar o Token ou exibir o erro
	#exibir tabela_de_simbolos

	with(open(arquivo, r) as fonte):
		token_retornado = None
		scanner = Scanner()

		while(token_retornado is not None and token_retornado.classe is not "EOF"):
			token_retornado = scanner.Scanner(fonte.read(1))

			if(token_retornado.classe is "ERRO"):
				print("ARRUMAR DEPOIS")
			else:
				if token_retornado.classe is not "EOF":
					print("Classe: {}, Lexema: {}, Tipo: {}".format(token_retornado.classe, token_retornado.lexema, token_retornado.tipo))
				