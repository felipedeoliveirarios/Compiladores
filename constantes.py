NUMEROS = "1234567890"
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuwxyz"
COMENTARIO = NUMEROS + LETRAS + "!\"#\\$%&'()*+,-./:;<=>?@[]^/_`/|~"
STRING = NUMEROS + LETRAS + "!#$%&'()*+,-./\\:;<=>?@[]^/_`/{|}~"
EOF = ""
ESPACO_VAZIO = """ 	
"""


#estado, final?, classe
lista_de_estados = {"S0_A" 	: [False, None],
					"S0_B"	: [True, None],
					"S1" 	: [True, "Num"],
					"S2" 	: [False, None],
					"S3" 	: [True, "Num"],
					"S4" 	: [False, None],
					"S5" 	: [False, None ],
					"S6" 	: [True, "Num"],
					"S7" 	: [False, None],
					"S8" 	: [True, "Literal"],
					"S9" 	: [True, "id"],
					"S10" 	: [False, None],
					"S11" 	: [True, None],
					"S12" 	: [True, "EOF"],
					"S13_A" : [True, "OPR"],
					"S13_B" : [True, "OPR"],
					"S13_C" : [True , "OPR"],
					"S14" 	: [True, "RCB"],
					"S15" 	: [True, "OPM"],
					"S16" 	: [True, "AB_P"],
					"S17" 	: [True, "FC_P"],
					"S18" 	: [True, "PT_V"],
					"S19" 	: [True, "Vir"],
					"S20" 	: [True, "ERRO"]}

#(incial, destino, entrada)
tabela_de_transição = [
					   ["S0_A", "S0_B", ESPACO_VAZIO],
					   ["S0_B", "S0_B", ESPACO_VAZIO],
					   #Num
					   ["S0_A", "S1", NUMEROS],
					   ["S1", "S1", NUMEROS],
					   ["S1", "S2", "."],
					   ["S1", "S4", "Ee"],
					   ["S2", "S3", NUMEROS],
					   ["S3", "S3", NUMEROS],
					   ["S3", "S4", "Ee"],
					   ["S4", "S5", "-+"],
					   ["S4", "S6", NUMEROS],
					   ["S5", "S6", NUMEROS],
					   ["S6", "S6", NUMEROS],
					   #Literal
					   ["S0_A", "S7", "\""],
					   ["S7", "S7", STRING],
					   ["S7", "S8", "\""],
					   #id
					   ["S0_A", "S9", LETRAS],
					   ["S9", "S9", LETRAS + NUMEROS + "_"],
					   #Comentário
					   ["S0_A", "S10", "{"],
					   ["S10", "S10", COMENTARIO],
					   ["S10", "S11", "}"],
					   #EOF
					   ["S0_A", "S12", EOF],
					   #OPR
					   ["S0_A", "S13_A", ">"],
					   ["S0_A", "S13_B", "<"],
					   ["S0_A", "S13_C", "="],
					   ["S13_A", "S13_C", "="],
					   ["S13_B", "S13_C", "="],
					   #RCB
					   ["S13_B", "S14", "-"],
					   #OPM
					   ["S0_A", "S15", "+-*/"],
					   #AB_P
					   ["S0_A", "S16", "("],
					   #FC_P
					   ["S0_A", "S17", ")"],
					   #PT_V
					   ["S0_A", "S18", ";"],
					   #Vir
					   ["S0_A", "S19", ","]]
