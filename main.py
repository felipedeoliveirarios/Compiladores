import constantes

class Token:
  	classe, lexema, tipo = None, None, None

	def __init__(classe, lexema, tipo):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo

tabela_de_simbolos = [Token("inicio", "inicio", None),
                      Token("varinicio", "varinicio", None),
                      Token("varfim", "varfim", None),
                      Token("escreva", "escreva", None),
                      Token("leia", "leia", None),
                      Token("se", "se", None),
                      Token("entao", "entao", None),
                      Token("fimse", "fimse", None),
                      Token("faca-ate", "faca-ate", None),
                      Token("fimfaca", "fimfaca", None),
                      Token("fim", "fim", None),
                      Token("inteiro", "inteiro", None),
                      Token("lit", "lit", None),
                      Token("real", "real", None)]


class Scanner:
	estado = None
	lexema = None
	
	def Scanner(entrada):
		if estado is None:
			estado = "S0"
			lexema = ""
		erro = True
		for transicao in constantes.tabela_de_transição:
			if transicao[0] == estado:
				if entrada in transicao[2]:
					estado = transicao[1]
					lexema += entrada
					erro = False
					break
		
		if erro:
			
		
		

	