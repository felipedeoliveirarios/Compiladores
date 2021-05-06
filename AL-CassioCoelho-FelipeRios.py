import constantes
import argparse

DEBUG = False

# Classe responsável por armazenar os dados de um TOKEN
class TOKEN:
	classe, lexema, tipo = None, None, None

	def __init__(self, classe, lexema, tipo):
		self.classe = classe
		self.lexema = lexema
		self.tipo = tipo

# TABELA DE SÍMBOLOS, responsável por armazenar os identificadores reconhecidos e palavras reservadas
TABELA_DE_SIMBOLOS = {"inicio": TOKEN("inicio", "inicio", None),
                      "varinicio": TOKEN("varinicio", "varinicio", None),
                      "varfim": TOKEN("varfim", "varfim", None),
                      "escreva": TOKEN("escreva", "escreva", None),
                      "leia": TOKEN("leia", "leia", None),
                      "se": TOKEN("se", "se", None),
                      "entao": TOKEN("entao", "entao", None),
                      "fimse": TOKEN("fimse", "fimse", None),
                      "faca-ate": TOKEN("faca-ate", "faca-ate", None),
                      "fimfaca": TOKEN("fimfaca", "fimfaca", None),
                      "fim": TOKEN("fim", "fim", None),
                      "inteiro": TOKEN("inteiro", "inteiro", None),
                      "lit": TOKEN("lit", "lit", None),
                      "real": TOKEN("real", "real", None)}

# Função que confere se uma chave está na tabela de símbolos.
def HasKey(chave):
	return (chave in TABELA_DE_SIMBOLOS.keys())

#-------------------------------------------------------------------------------------------
# Scanner
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

			if classe == "id":
				if not HasKey(lexema):
					TABELA_DE_SIMBOLOS[lexema] = TOKEN(classe, lexema, None)
				

				self.Consumir()
				self.Reset()

				return TABELA_DE_SIMBOLOS[lexema]

			else:
				self.Consumir()
				self.Reset()

				return TOKEN(classe, lexema, None)
		
		# Estado de parada não é final
		else:
			lexema = self.buffer[0:self.indice]
			
			classe = "ERRO"
			
			self.indice += 1
			
			self.Consumir()
			self.Reset()

			return TOKEN(classe, self.indice, None)

# FUNÇÃO ERROR
def ERROR(estado, linha, coluna):
	mensagem = estado.mensagem_de_erro
	chave_estado = ""

	for key in constantes.lista_de_estados.keys():
		if constantes.lista_de_estados[key] == estado:
			chave_estado = key
			break

	identificador = "ERRO#" + chave_estado[1:]

	print("{} - {}, linha {} e coluna {}".format(identificador, mensagem, linha, coluna))

#-------------------------------------------------------------------------------------------
# Parser
#-------------------------------------------------------------------------------------------
# Classe que implementa o parser
class Parser:
	pilhaEstados = []
	pilhaTokens = []
	lexico = None
	entrada = None

	def __init__(self, scanner):
		self.pilhaEstados.append(0)
		self.lexico = scanner
		self.proximoToken()

	def PARSER(self):

		# Faz a checagem de erro do analisador léxico
		if self.entrada.classe is not None and "ERRO" in self.entrada.classe:
			ERROR(self.lexico.estado, self.lexico.linha, self.lexico.coluna)
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

						# Desempilha a quantidade correta de tokens e estados
						for i in range(quantidade):
							self.pilhaEstados.pop()
							self.pilhaTokens.pop()

						# Atualiza a variável do topo da pilha
						topoEstado = self.pilhaEstados[-1]

						# Empilha o lado esquerdo da regra
						self.pilhaTokens.append(ladoEsquerdo)

						# Faz o goto para o estado no topo, usando o lado esquerdo como self.entrada
						self.pilhaEstados.append(constantes.tabela_lr_goTo[topoEstado][ladoEsquerdo])

						# Exibe a regra de produção
						print(ladoEsquerdo + " -> " + ladoDireito)

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
					
					print("ERRO SINTÁTICO - Token {} inesperado na linha {}, coluna {}. Se esperava {}.".format(self.entrada.lexema, self.lexico.linha, self.lexico.coluna, esperado))

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

		# Executa o parser em loop
		while parser.PARSER():
			pass
			

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("fonte", help = "Caminho do arquivo de entrada")
	args = parser.parse_args()
	PRINCIPAL(args.fonte)