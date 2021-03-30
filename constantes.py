NUMEROS = "1234567890"
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
COMENTARIO = NUMEROS + LETRAS + "!\"#\\$%&'()*+,-./:;<=>?@[]^/_`/|~"
STRING = NUMEROS + LETRAS + "!#$%&'()*+,-./\\:;<=>?@[]^/_`/{|}~"
EOF = ""
ESPACO_VAZIO = """ 	
"""

class Estado:
	token = None
	regras_de_transicao = None
	final = None

	def __init__(self, regras_de_transicao, token, final):
		self.regras_de_transicao = regras_de_transicao
		self.final = final
		self.token = token

	def busca_transicao(self, entrada):
		
		chave = None

		for item in self.regras_de_transicao.items():
			if entrada in item[1]:
				chave = item[0]
				break
		
		return chave


lista_de_estados = {}
lista_de_estados["S0_A"] = Estado(
								{
									"S0_B" 	: ESPACO_VAZIO,
								 	"S1" 	: NUMEROS,
									"S7" 	: "\"",
									"S9"	: LETRAS,
									"S10"	: "{",
									"S12"	: EOF,
									"S13_A"	: ">",
									"S13_B"	: "<",
					   				"S13_C"	: "=",
									"S15"	: "+-*/",
									"S16"	: "(",
									"S17"	: ")",
					   				"S18"	: ";",
					   				"S19"	: ","
								},
								None,
								False
								)

lista_de_estados["S0_B"] = Estado(
								{
									"S0_B" : ESPACO_VAZIO,
								},
								"\s",
								True)

lista_de_estados["S1"] = Estado(
								{
								"S1"	: NUMEROS,
					   			"S2"	: ".",
					   			"S4"	: "Ee"
								},
								"Num",
								True)

lista_de_estados["S2"] = Estado(
								{
								"S3" 	: NUMEROS
								},
								None,
								False)

lista_de_estados["S3"] = Estado(
								{
								"S3"	: NUMEROS,
					   			"S4"	: "Ee"
								},
								"Num",
								True)

lista_de_estados["S4"] = Estado(
								{
								"S5"	: "-+",
					   			"S6"	: NUMEROS
								},
								None,
								False)

lista_de_estados["S5"] = Estado(
								{
								"S6"	: NUMEROS
								},
								None,
								False)

lista_de_estados["S6"] = Estado(
								{
								"S6"	: NUMEROS
								},
								"Num",
								True)

lista_de_estados["S7"] = Estado(
								{
								"S7"	: STRING,
					   			"S8"	: "\""
								},
								None,
								False)

lista_de_estados["S8"] = Estado(
								{},
								"Literal",
								True)

lista_de_estados["S9"] = Estado(
								{
								"S9"	: LETRAS + NUMEROS + "_"
								},
								"id",
								True)

lista_de_estados["S10"] = Estado(
								{
								"S10"	: COMENTARIO,
					   			"S11"	: "}"
								},
								None,
								False)

lista_de_estados["S11"] = Estado(
								{

								},
								None,
								True)

lista_de_estados["S12"] = Estado(
								{

								},
								"EOF",
								True)

lista_de_estados["S13_A"] = Estado(
								{
								"S13_C"	: "="
								},
								"OPR",
								True)

lista_de_estados["S13_B"] = Estado(
								{
								"S13_C"	: "=",
					   			"S14"	: "-"
								},
								"OPR",
								True)

lista_de_estados["S13_C"] = Estado(
								{},
								"OPR",
								True)

lista_de_estados["S14"] = Estado(
								{},
								"RCB",
								True)

lista_de_estados["S15"] = Estado(
								{},
								"OPM",
								True)

lista_de_estados["S16"] = Estado(
								{},
								"AB_P",
								True)

lista_de_estados["S17"] = Estado(
								{},
								"FC_P",
								True)

lista_de_estados["S18"] = Estado(
								{},
								"PT_V",
								True)

lista_de_estados["S19"] = Estado(
								{},
								"Vir",
								True)

lista_de_estados["S20"] = Estado(
								{},
								"ERRO",
								True)

