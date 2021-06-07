import constantes
import argparse
import pdb

DEBUG = False

# Classe responsável por armazenar os dados de um TOKEN
class TOKEN:
	classe, lexema, tipo = None, None, None

	def __init__(self, classe, lexema, tipo, linha_e_coluna=None):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo
		self.linha_e_coluna = linha_e_coluna
	
	def __repr__(self):
		return '<CLASSE: {}; LEXEMA: "{}"; TIPO: {}>'.format(self.classe, self.lexema, self.tipo)

# TABELA DE SÍMBOLOS, responsável por armazenar os identificadores reconhecidos e palavras reservadas
TABELA_DE_SIMBOLOS = {"inicio": TOKEN("inicio", "inicio", None),
					  "varinicio": TOKEN("varinicio", "varinicio", None),
					  "varfim": TOKEN("varfim", "varfim", None),
					  "escreva": TOKEN("escreva", "escreva", None),
					  "leia": TOKEN("leia", "leia", None),
					  "se": TOKEN("se", "se", None),
					  "entao": TOKEN("entao", "entao", None),
					  "fimse": TOKEN("fimse", "fimse", None),
					  "facaAte": TOKEN("facaAte", "facaAte", None),
					  "fimFaca": TOKEN("fimFaca", "fimFaca", None),
					  "fim": TOKEN("fim", "fim", None),
					  "inteiro": TOKEN("inteiro", "inteiro", "inteiro"),
					  "lit": TOKEN("lit", "lit", "lit"),
					  "real": TOKEN("real", "real", "real")}

# Função que confere se uma chave está na tabela de símbolos.
def HasKey(chave):
	return (chave in TABELA_DE_SIMBOLOS.keys())

#-------------------------------------------------------------------------------------------
# Scanner (LÉXICO)
#-------------------------------------------------------------------------------------------

# Classe que implementa o scanner.
class Scanner:
	estado = None
	buffer = None
	indice = None
	linha = 1
	coluna = 0

	def __init__(self):
		self.estado = constantes.lista_de_estados["S0_A"]
		self.indice = 0

	def Alimentar(self, entrada):
		self.buffer = entrada
	
	def Reset(self):
		self.estado = constantes.lista_de_estados["S0_A"]
		self.indice = 0
	
	def Consumir(self):
		for char in self.buffer[:self.indice]:
			if char == "\n":
				self.linha += 1
				self.coluna = 0
				
			else:
				self.coluna += 1

		self.buffer = self.buffer[self.indice:]

	# FUNÇÃO SCANNER.
	def SCANNER(self):
		
		if self.buffer == "":
			return TOKEN("EOF", "EOF", None)

		while True:
			proximo_estado = self.estado.busca_transicao(self.buffer[self.indice])

			if proximo_estado is None:
				break
			
			self.estado = constantes.lista_de_estados[proximo_estado]			
			self.indice += 1

			if self.indice == len(self.buffer):
				break

		if self.estado.final:
			lexema = self.buffer[0:self.indice]
			classe = self.estado.classe
			tipo = None

			if classe == "Literal":
				tipo = "lit"
			
			elif classe == "Num":
				if self.estado == constantes.lista_de_estados['S1']:
					tipo = "inteiro"
				else:
					tipo = "real"

			if classe == "id":
				if not HasKey(lexema):
					TABELA_DE_SIMBOLOS[lexema] = TOKEN(classe, lexema, None, [self.linha, self.coluna])
				

				self.Consumir()
				self.Reset()

				return TABELA_DE_SIMBOLOS[lexema]

			else:
				self.Consumir()
				self.Reset()

				return TOKEN(classe, lexema, tipo, [self.linha, self.coluna])
		
		# Estado de parada não é final
		else:
			lexema = self.buffer[0:self.indice]
			
			classe = "ERRO"
			
			self.indice += 1
			
			self.Consumir()
			self.Reset()

			return TOKEN(classe, self.indice, None, [self.linha, self.coluna])

# FUNÇÃO ERROR
def ERROR(estado, linha, coluna):
	mensagem = estado.mensagem_de_erro
	chave_estado = ""

	for key in constantes.lista_de_estados.keys():
		if constantes.lista_de_estados[key] == estado:
			chave_estado = key
			break

	identificador = "ERRO_LX#" + chave_estado[1:]

	print("{} - {}, linha {} e coluna {}".format(identificador, mensagem, linha, coluna))

#-------------------------------------------------------------------------------------------
# Parser (SINTÁTICO)
#-------------------------------------------------------------------------------------------
# Classe que implementa o parser
class Parser:
	pilhaEstados = []
	pilhaTokens = []
	pilhaSemanticaTokens = []
	lexico = None
	semantico = None
	entrada = None
	erro = False

	def __init__(self, scanner):
		self.pilhaEstados.append(0)
		self.lexico = scanner
		self.proximoToken()
		self.erro = False

	def PARSER(self):

		# Faz a checagem de erro do analisador léxico
		if (self.entrada.classe is not None) and ("ERRO" in self.entrada.classe):
			ERROR(self.lexico.estado, self.lexico.linha, self.lexico.coluna)
			self.erro = True
			return True

		else:
			# Garante que não é comentário, nem EOF, nem espaço vazio.
			if self.entrada.classe is not None and self.entrada.classe != "\s":

				# AQUI COMEÇA A BRUXARIA DO ANALISADOR SINTÁTICO

				# Encontra o topo da pilha de estados
				topoEstado = self.pilhaEstados[-1]

				# Testa se existe uma ação válida
				if self.entrada.classe in constantes.tabela_lr_action[topoEstado].keys():
					# Obtém a ação para a self.entrada atual à partir do estado atual
					action = constantes.tabela_lr_action[topoEstado][self.entrada.classe]

					# Se a ação for um shift
					if action[0] == 's':
						posição = int(action[1:])
						self.pilhaTokens.append(self.entrada.classe)
						self.pilhaSemanticaTokens.append(self.entrada)
						self.pilhaEstados.append(posição)

						# Chama o analisador léxico e obtém um token
						self.proximoToken()

						return True

					# Se a ação for um reduce
					elif action[0] == 'r':

						# Separa a posição da regra de produção do valor da tabela
						posição = int(action[1:])

						# Obtém os dois lados da regra de produção do reduce
						ladoEsquerdo = constantes.regras_de_producao[posição][0]
						ladoDireito = constantes.regras_de_producao[posição][1]

						# Conta a quantidade de símbolos do lado direito
						quantidade = ladoDireito.count(" ") + 1

						# Cria um buffer para armazenar os Tokens removidos da pilha
						buffer = []

						# Desempilha a quantidade correta de tokens e estados
						for i in range(quantidade):
							self.pilhaEstados.pop()
							self.pilhaTokens.pop()
							token_completo = self.pilhaSemanticaTokens.pop()

							# Se o token deve ser repassado para o semântico...
							if token_completo is not None and token_completo.classe in ["id", "inteiro", "real", "lit", "Num", "Literal", "OPM", "OPR"]:
								# Remove os tokens da pilha e coloca no buffer
								buffer.append(token_completo)

						# Atualiza a variável do topo da pilha
						topoEstado = self.pilhaEstados[-1]

						# Empilha o lado esquerdo da regra
						self.pilhaTokens.append(ladoEsquerdo)
						self.pilhaSemanticaTokens.append(None)

						# Faz o goto para o estado no topo, usando o lado esquerdo como self.entrada
						self.pilhaEstados.append(constantes.tabela_lr_goTo[topoEstado][ladoEsquerdo])

						# Exibe a regra de produção
						print(ladoEsquerdo + " -> " + ladoDireito)
						# AQUI É FEITA A INVOCAÇÃO DO SEMÂNTICO
						self.semantico.Analisar(posição + 1, buffer)
						
						if self.semantico.erro:
							self.erro = True

						# Mantém o while rodando
						return True

					# Se a acção foi um accept
					elif action == 'acc':
						# Para o while
						return False

				# ERRRRROOOOU
				else:
					# Obtém os terminais esperados para o estado atual.
					esperado = constantes.tabela_lr_action[topoEstado].keys()
					
					print("ERRO_ST - Token {} inesperado na linha {}, coluna {}. Se esperava {}.".format(self.entrada.lexema, self.lexico.linha, self.lexico.coluna, esperado))

					# Exclui símbolos da pilha até encontrar um símbolo de recuperação					
					while True:
						if self.pilhaTokens[-1] in constantes.TOKENS_DE_SINCRONIZAÇÃO:
							break;
						
						self.pilhaTokens.pop()
						self.pilhaEstados.pop()
					
					# Exclui o símbolo de recuperação
					self.pilhaTokens.pop()
					self.pilhaEstados.pop()

					# Segue o passeio
					self.proximoToken()

					return True
			
			# O TOKEN RETORNADO É IGNORADO
			else:
				self.proximoToken()
				return True
	
	def proximoToken(self):
		self.entrada = self.lexico.SCANNER()

#-------------------------------------------------------------------------------------------
# Analisador Semântico
#-------------------------------------------------------------------------------------------

class Semantico:
	vardef = ""
	corpo = ""
	variaveis_temporarias = 0
	pilha_semantica = []
	erro = False

	def __init__(self):
		self.cabecalho = ""
		self.vardef = ""
		self.corpo = ""
		self.variaveis_temporarias = 0
		self.pilha_semantica = []
		self.erro = False

	def Analisar(self, posição, buffer):
		if posição == 5:
			self.Regra5(buffer)

		elif posição == 6:
			self.Regra6(buffer)

		elif posição == 7:
			self.Regra7(buffer)

		elif posição == 8:
			self.Regra8(buffer)

		elif posição == 9:
			self.Regra9(buffer)

		elif posição == 10:
			self.Regra10(buffer)

		elif posição == 11:
			self.Regra11(buffer)

		elif posição == 13:
			self.Regra13(buffer)

		elif posição == 14:
			self.Regra14(buffer)

		elif posição == 15:
			self.Regra15(buffer)

		elif posição == 16:
			self.Regra16(buffer)

		elif posição == 17:
			self.Regra17(buffer)

		elif posição == 19:
			self.Regra19(buffer)

		elif posição == 20:
			self.Regra20(buffer)

		elif posição == 21:
			self.Regra21(buffer)

		elif posição == 22:
			self.Regra22(buffer)

		elif posição == 23:
			self.Regra23(buffer)

		elif posição == 25:
			self.Regra25(buffer)

		elif posição == 26:
			self.Regra26(buffer)

		elif posição == 27:
			self.Regra27(buffer)

		elif posição == 33:
			self.Regra33(buffer)

		elif posição == 34:
			self.Regra34(buffer)

		elif posição == 35:
			self.Regra35(buffer)

		elif posição == 36:
			self.Regra36(buffer)

		elif posição == 37:
			self.Regra37(buffer)
	
	###################################################################
	#	Regras Semânticas
	###################################################################
	
	def Regra5(self, buffer): # LV → varfim;
		self.vardef += "\n"*3

	def Regra6(self, buffer): # D → TIPO L;
		# Procura o tipo na pilha
		i = -1
		while(self.pilha_semantica and self.pilha_semantica[i].classe == 'id'):
			i -= 1
		tipo = self.pilha_semantica.pop(i).tipo
		# Para cada token inserido anteriormente na pilha...
		while(self.pilha_semantica and self.pilha_semantica[-1].classe == 'id'):
			token = self.pilha_semantica.pop()
			TABELA_DE_SIMBOLOS[token.lexema].tipo = tipo
			self.vardef += "{} {};\n".format(tipo, token.lexema)

	def Regra7(self, buffer): # L → id, L
		if confereDeclaracao(buffer[0]):
			# Variável já foi declarada.
			print("ERRO_SM#8 - Variável já declarada (linha {}, coluna{})".format(buffer[0].linha_e_coluna))
			self.erro = True
		self.pilha_semantica.append(buffer[0])

	def Regra8(self, buffer): # L → id
		if confereDeclaracao(buffer[0]):
			# Variável já foi declarada.
			print("ERRO_SM#8 - Variável já declarada (linha {}, coluna{})".format(buffer[0].linha_e_coluna))
			self.erro = True

		self.pilha_semantica.append(buffer[0])

	def Regra9(self, buffer): # TIPO → int
		self.pilha_semantica.append(buffer[0])

	def Regra10(self, buffer): # TIPO → real
		self.pilha_semantica.append(buffer[0])

	def Regra11(self, buffer): # TIPO → lit
		self.pilha_semantica.append(buffer[0])

	def Regra13(self, buffer): # ES → leia id
		if confereDeclaracao(buffer[0]):
			if buffer[0].tipo == "lit":
				self.corpo += 'scanf("%s", &{});\n'.format(buffer[0].lexema);
			elif buffer[0].tipo == "inteiro":
				self.corpo += 'scanf("%d", &{});\n'.format(buffer[0].lexema);
			elif buffer[0].tipo == "real":
				self.corpo += 'scanf("%f", &{});\n'.format(buffer[0].lexema);
		else:
			# Variável ainda não foi declarada.
			print("ERRO_SM#13 - Variável não declarada ({})".format(buffer[0].linha_e_coluna))
			self.erro = True

	def Regra14(self, buffer): # ES → escreva ARG
		ARG = self.pilha_semantica.pop()
		if ARG.tipo == "lit":
			self.corpo += 'printf("%s", {});\n'.format(ARG.lexema);
		elif ARG.tipo == "inteiro":
			self.corpo += 'printf("%d", {});\n'.format(ARG.lexema);
		elif ARG.tipo == "real":
			self.corpo += 'printf("%f", {});\n'.format(ARG.lexema);

	def Regra15(self, buffer): # ARG → literal
		self.pilha_semantica.append(buffer[0])

	def Regra16(self, buffer): # ARG → num
		self.pilha_semantica.append(buffer[0])

	def Regra17(self, buffer): # ARG → id
		if not confereDeclaracao(buffer[0]):
			# Variável ainda não foi declarada.
			print("ERRO_SM#17 - Variável não declarada (linha {}, coluna{})".format(buffer[0].linha_e_coluna[0], buffer[0].linha_e_coluna[1]))
			self.erro = True
		
		self.pilha_semantica.append(buffer[0])
	
	#def Regra18(self, buffer): # A → CMD A  

	def Regra19(self, buffer): # CMD → id rcb LD
		CMD = TOKEN("CMD", "", None)
		if confereDeclaracao(buffer[0]):
			ld = self.pilha_semantica.pop()
			CMD.lexema += "{} = {};\n".format(buffer[0].lexema, ld.lexema)

			if (self.pilha_semantica and self.pilha_semantica[-1].classe == "T_DEF"):
				T_DEF = self.pilha_semantica.pop()
				self.corpo += T_DEF.lexema
			self.corpo += CMD.lexema
		
			#self.pilha_semantica.append(CMD)
			#self.pilha_semantica.append(T_DEF)

	def Regra20(self, buffer): # LD → OPRD opm OPRD
		operando1 = self.pilha_semantica.pop()
		operando2 = self.pilha_semantica.pop()

		if operando1.tipo != 'lit' and operando2.tipo != 'lit':
			
			if operando1.tipo != 'real' or operando2.tipo != 'real':
				temp = TOKEN("id", "T{}".format(self.variaveis_temporarias), "float")
			else:
				temp = TOKEN("id", "T{}".format(self.variaveis_temporarias), "int")

			T_DEF = TOKEN("T_DEF", "", None)
			T_DEF.lexema += "{} {} = {} {} {};\n".format(temp.tipo, temp.lexema, operando1.lexema, buffer[0].lexema, operando2.lexema)
			self.variaveis_temporarias += 1

			self.pilha_semantica.append(T_DEF)				
			self.pilha_semantica.append(temp)

		else:
			print("ERRO_SM#20 - Operandos com tipos incompatíveis (linha {}, coluna{})".format(buffer[0].linha_e_coluna[0], buffer[0].linha_e_coluna[1]))
			self.erro = True

	def Regra21(self, buffer): #LD → OPRD
		pass

	def Regra22(self, buffer): #OPRD → id
		if confereDeclaracao(buffer[0]):
			self.pilha_semantica.append(buffer[0])
		else:
			# Variável ainda não foi declarada.
			print("ERRO_SM#22 - Variável não declarada (linha {}, coluna{})".format(buffer[0].linha_e_coluna[0], buffer[0].linha_e_coluna[1]))
			self.erro = True

	def Regra23(self, buffer): #OPRD → num
		self.pilha_semantica.append(buffer[0])

	def Regra25(self, buffer): #COND → CAB CP
		self.corpo += '}\n'

	def Regra26(self, buffer): #CAB → se (EXPR_R) entao
		EXPR_R = ""
		
		while(self.pilha_semantica and self.pilha_semantica[-1].classe == 'EXPR_R'):
			token = self.pilha_semantica.pop()
			EXPR_R += " {}".format(token.lexema)
		self.corpo += self.pilha_semantica.pop().lexema
		self.corpo += 'if({})'.format(EXPR_R) + "{\n";

	def Regra27(self, buffer): #EXP_R → OPRD opr OPRD
		operando1 = self.pilha_semantica.pop()
		operando2 = self.pilha_semantica.pop()

		if operando1.tipo == operando2.tipo:
			temp = TOKEN("EXPR_R", "T{}".format(self.variaveis_temporarias), "bool")
			
			T_DEF = TOKEN("T_DEF", "", None)
			T_DEF.lexema += "bool {} = {} {} {};\n".format(temp.lexema, operando1.lexema, buffer[0].lexema, operando2.lexema)
			self.variaveis_temporarias += 1

			self.pilha_semantica.append(T_DEF)
			self.pilha_semantica.append(temp)
		else:
			print("ERRO_SM#27 - Operandos com tipos incompatíveis (linha {}, coluna{})".format(buffer[0].linha_e_coluna[0], buffer[0].linha_e_coluna[1]))
			self.erro = True

	def Regra33(self, buffer): # R → facaAte (EXPR_R) CPR_R
		CPR_R = ""
		while(self.pilha_semantica and self.pilha_semantica[-1].classe != 'EXPR_R'):
			CPR_R += self.pilha_semantica.pop().lexema
		EXPR_R = self.pilha_semantica.pop()
		T_DEF = self.pilha_semantica.pop()
		self.corpo += T_DEF.lexema;
		self.corpo += "while ({})".format(EXPR_R.lexema) + "{\n" + "{}".format(CPR_R) + "}\n"

	def Regra34(self, buffer): # CP_R → ES CP_R
		#ES = self.pilha_semantica.pop()
		#CP_R = TOKEN("CP_R", ES.lexema, None)
		#self.pilha_semantica.append(CP_R)
		pass

	def Regra35(self, buffer): # CP_R → CMD CP_R
		#CMD = self.pilha_semantica.pop()
		#CP_R = TOKEN("CP_R", CMD.lexema, None)
		#self.pilha_semantica.append(CP_R)
		pass

	def Regra36(self, buffer): # CP_R → COND CP_R
		#COND = self.pilha_semantica.pop()
		#CP_R = TOKEN("CP_R", COND.lexema, None)
		#self.pilha_semantica.append(CP_R)
		pass

	def Regra37(self, buffer): # CP_R → fimFaca
		pass

# Confere se uma variável foi declarada
def confereDeclaracao(token):
	if HasKey(token.lexema) and TABELA_DE_SIMBOLOS[token.lexema].tipo:
		return True
	else:
		return False

#-------------------------------------------------------------------------------------------
# PRINCIPAL
#-------------------------------------------------------------------------------------------

# FUNÇÃO PRINCIPAL
def PRINCIPAL(arquivo):	
	with open(arquivo) as fonte:

		# Constrói um objeto do tipo Scanner
		scanner = Scanner()

		# Insere a entrada no scanner
		scanner.Alimentar(fonte.read())

		# Constrói um objeto do tipo Parser
		parser = Parser(scanner)
		semantico = Semantico()
		parser.semantico = semantico

		# Executa o parser em loop
		while parser.PARSER():
			pass
		
		if not parser.erro:
			with open("PROGRAMA.C", "w") as final:
				final.write(constantes.cabecalho_programa)
				final.write(parser.semantico.vardef)
				final.write(parser.semantico.corpo)
				final.write(constantes.rodape_programa)

			

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("fonte", help = "Caminho do arquivo de entrada")
	args = parser.parse_args()
	PRINCIPAL(args.fonte)