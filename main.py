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

lista_de_estados = ["S0", #incial
					"S1", #digitos (\D)
					"S2", #separador de casa decimal (.,)
					"S3", #digitos decimais (\D)
					"S4", #exponencial
					"S5", #sinal de expoente (+-)
					"S6", #valor do expoente
					"S7", #abre aspas
					"S8", #texto
					"S9", #fecha aspas
					"S10", #
					"S11", #
					"S12", #
					"S13", #
					"S14", #
					"S15", #
					"S16", #
					"S17", #
					"S18", #
					"S19", #
					"S20"]

classe_de_lexemas = ["Num", "Literal", "id", "Comentário", "EOF", "OPR", "RCB", "OPM", "AB_P", "FC_P", "PT_V", "ERRO", "Vir", "\s"]


#(incial, destino, entrada)
tabela_de_transição = [
					   #Num
					   ["S0", "S1", "1234567890"],
					   ["S1", "S1", "1234567890"],
					   ["S1", "S2", "."],
					   ["S1", "S4", "Ee"],
					   ["S2", "S3", "1234567890"],
					   ["S3", "S3", "1234567890"],
					   ["S3", "S4", "Ee"],
					   ["S4", "S5", "-+"],
					   ["S4", "S6", "1234567890"],
					   ["S5", "S6", "1234567890"],
					   ["S6", "S6", "1234567890"],
					   #Literal
					   ["S0", "S7", "\""],
					   ["S7", "S7", ANY],
					   ["S7", "S8", "\""],
					   #id
					   ["S0", "S9", LETRAS],
					   ["S9", "S9", LETRAS + NUMEROS + "_"],
					   #Comentário
					   ["S0", "S10", "{"],
					   ["S10", "S10", ANY],
					   ["S10", "S11", "}"],
					   #EOF
					   ["S0", "S12", EOF],
					   #OPR
					   ["S0", "S13_A", ">"],
					   ["S0", "S13_B", "<"],
					   ["S0", "S13_C", "="],
					   ["S13_A", "S13_C", "="],
					   ["S13_B", "S13_C", "="],
					   #RCB
					   ["S13_B", "S14", "-"],
					   #OPM
					   ["S0", "S15", "+-*/"],
					   #AB_P
					   ["S0", "S16", "("],
					   #FC_P
					   ["S0", "S17", ")"],
					   #PT_V
					   ["S0", "S18", ";"],
					   #Vir
					   ["S0", "S19", ","]]

def Scanner():
	pass




