NUMEROS = "1234567890"
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
EOF = ""
ESPACO_VAZIO = """ 	
"""
COMENTARIO = NUMEROS + LETRAS + ESPACO_VAZIO + "!\"#\\$%&'()*+,-./:;<=>?@[]^/_`/|~"
STRING = NUMEROS + LETRAS + ESPACO_VAZIO + "!#$%&'()*+,-./\\:;<=>?@[]^/_`/{|}~"

TOKENS_DE_SINCRONIZAÇÃO = [
    'P', 'V', 'A', 'ES', 'CMD', 'CP', 'R', 'CP_R', 'LD', 'COND', 'CAB', 'EXP_R'
]

'''
--------------------------------------------------------------------------------------------------------
Parte do Analisador Léxico
--------------------------------------------------------------------------------------------------------
'''
class Estado:
    regras_de_transicao = None
    classe = None
    final = None
    mensagem_de_erro = ""

    def __init__(self,
                 regras_de_transicao,
                 classe,
                 final,
                 mensagem_de_erro=""):
        self.regras_de_transicao = regras_de_transicao
        self.final = final
        self.classe = classe
        self.mensagem_de_erro = mensagem_de_erro

    def busca_transicao(self, entrada):

        chave = None

        for item in self.regras_de_transicao.items():
            if entrada in item[1]:
                chave = item[0]
                break

        return chave


# Link do DFA: https://graphonline.ru/en/?graph=hUPLMoFNyQmgbhPm
# lista_de_estados[x] = Estado(regras_de_transicao, classe do token que reconhece, final ou não)
lista_de_estados = {}
lista_de_estados["S0_A"] = Estado(
    {
        "S0_B": ESPACO_VAZIO,
        "S1": NUMEROS,
        "S7": "\"",
        "S9": LETRAS,
        "S10": "{",
        "S12": EOF,
        "S13_A": ">",
        "S13_B": "<",
        "S13_C": "=",
        "S15": "+-*/",
        "S16": "(",
        "S17": ")",
        "S18": ";",
        "S19": ","
    }, None, False, "Caractere não esperado")

lista_de_estados["S0_B"] = Estado({
    "S0_B": ESPACO_VAZIO,
}, "\s", True)

lista_de_estados["S1"] = Estado({
    "S1": NUMEROS,
    "S2": ".",
    "S4": "Ee"
}, "Num", True)

lista_de_estados["S2"] = Estado({"S3": NUMEROS}, None, False,
                                "Era esperado um dígito")

lista_de_estados["S3"] = Estado({"S3": NUMEROS, "S4": "Ee"}, "Num", True)

lista_de_estados["S4"] = Estado({
    "S5": "-+",
    "S6": NUMEROS
}, None, False, "Era esperado um dígito ou sinal")

lista_de_estados["S5"] = Estado({"S6": NUMEROS}, None, False,
                                "Era esperado um dígito")

lista_de_estados["S6"] = Estado({"S6": NUMEROS}, "Num", True)

lista_de_estados["S7"] = Estado({
    "S7": STRING,
    "S8": "\""
}, None, False, "Caractere não reconhecido")

lista_de_estados["S8"] = Estado({}, "Literal", True)

lista_de_estados["S9"] = Estado({"S9": LETRAS + NUMEROS + "_"}, "id", True)

lista_de_estados["S10"] = Estado({
    "S10": COMENTARIO,
    "S11": "}"
}, None, False, "Caractere não reconhecido")

lista_de_estados["S11"] = Estado({}, None, True)

lista_de_estados["S12"] = Estado({}, "EOF", True)

lista_de_estados["S13_A"] = Estado({"S13_C": "="}, "OPR", True)

lista_de_estados["S13_B"] = Estado({"S13_C": "=", "S14": "-"}, "OPR", True)

lista_de_estados["S13_C"] = Estado({}, "OPR", True)

lista_de_estados["S14"] = Estado({}, "RCB", True)

lista_de_estados["S15"] = Estado({}, "OPM", True)

lista_de_estados["S16"] = Estado({}, "AB_P", True)

lista_de_estados["S17"] = Estado({}, "FC_P", True)

lista_de_estados["S18"] = Estado({}, "PT_V", True)

lista_de_estados["S19"] = Estado({}, "Vir", True)
'''
--------------------------------------------------------------------------------------------------------
Parte do Analisador Sintático
--------------------------------------------------------------------------------------------------------
'''
regras_de_producao = [
    ["P'", "P"],  # 1
    ["P", "inicio V A"],  # 2
    ["V", "varincio LV"],  # 3
    ["LV", "D LV"],  # 4
    ["LV", "varfim PT_V"],  # 5
    ["D", "TIPO L PT_V"],  # 6
    ["L", "id , L"],  # 7
    ["L", "id"],  # 8
    ["TIPO", "inteiro"],  # 9	
    ["TIPO", "real"],  # 10
    ["TIPO", "lit"],  # 11
    ["A", "ES A"],  # 12
    ["ES", "leia id PT_V"],  # 13
    ["ES", "escreva ARG PT_V"],  # 14
    ["ARG", "Literal"],  # 15
    ["ARG", "Num"],  # 16
    ["ARG", "id"],  # 17
    ["A", "CMD A"],  # 18
    ["CMD", "id RCB LD PT_V"],  # 19
    ["LD", "OPRD OPM OPRD"],  # 20
    ["LD", "OPRD"],  # 21
    ["OPRD", "id"],  # 22
    ["OPRD", "Num"],  # 23
    ["A", "COND A"],  # 24
    ["COND", "CAB CP"],  # 25
    ["CAB", "se AB_P EXP_R FC_P então"],  # 26
    ["EXP_R", "OPRD OPR OPRD"],  # 27
    ["CP", "ES CP"],  # 28
    ["CP", "CMD CP"],  # 29
    ["CP", "COND CP"],  # 30
    ["CP", "fimse"],  # 31
    ["A", "R A"],  # 32
    ["R", "facaAte AB_P EXP_R FC_P CP_R"],  # 33
    ["CP_R", "ES CP_R"],  # 34
    ["CP_R", "CMD CP_R"],  # 35
    ["CP_R", "COND CP_R"],  # 36
    ["CP_R", "fimFaca"],  # 37
    ["A", "fim"]  # 38
]

tabela_lr_goTo = {}
tabela_lr_goTo[0] = {'P': 1}

tabela_lr_goTo[2] = {'V': 3}

tabela_lr_goTo[3] = {'A': 5, 'ES': 6, 'CMD': 7, 'COND': 8, 'CAB': 14, 'R': 9}

tabela_lr_goTo[4] = {'LV': 17, 'D': 18, 'TIPO': 20}

tabela_lr_goTo[6] = {'A': 24, 'ES': 6, 'CMD': 7, 'COND': 8, 'CAB': 14, 'R': 9}

tabela_lr_goTo[7] = {'A': 25, 'ES': 6, 'CMD': 7, 'COND': 8, 'CAB': 14, 'R': 9}

tabela_lr_goTo[8] = {'A': 26, 'ES': 6, 'CMD': 7, 'COND': 8, 'CAB': 14, 'R': 9}

tabela_lr_goTo[9] = {'A': 27, 'ES': 6, 'CMD': 7, 'COND': 8, 'CAB': 14, 'R': 9}

tabela_lr_goTo[12] = {'ARG': 29}

tabela_lr_goTo[14] = {'ES': 35, 'CMD': 36, 'COND': 37, 'CAB': 14, 'CP': 34}

tabela_lr_goTo[18] = {'LV': 41, 'D': 18, 'TIPO': 20}

tabela_lr_goTo[20] = {'L': 43}

tabela_lr_goTo[33] = {'LD': 47, 'OPRD': 48}

tabela_lr_goTo[35] = {'ES': 35, 'CMD': 36, 'COND': 37, 'CAB': 14, 'CP': 51}

tabela_lr_goTo[36] = {'ES': 35, 'CMD': 36, 'COND': 37, 'CAB': 14, 'CP': 52}

tabela_lr_goTo[37] = {'ES': 35, 'CMD': 36, 'COND': 37, 'CAB': 14, 'CP': 53}

tabela_lr_goTo[39] = {'OPRD': 55, 'EXP_R': 54}

tabela_lr_goTo[40] = {'OPRD': 55, 'EXP_R': 56}

tabela_lr_goTo[58] = {'L': 64}

tabela_lr_goTo[60] = {'OPRD': 65}

tabela_lr_goTo[61] = {'ES': 67, 'CMD': 68, 'COND': 69, 'CAB': 14, 'CP_R': 66}

tabela_lr_goTo[62] = {'OPRD': 71}

tabela_lr_goTo[67] = {'ES': 67, 'CMD': 68, 'COND': 69, 'CAB': 14, 'CP_R': 73}

tabela_lr_goTo[68] = {'ES': 67, 'CMD': 68, 'COND': 69, 'CAB': 14, 'CP_R': 74}

tabela_lr_goTo[69] = {'ES': 67, 'CMD': 68, 'COND': 69, 'CAB': 14, 'CP_R': 75}

tabela_lr_action = [
    # Estado 0
    {
        'inicio': 's2'
    },

    # Estado 1
    {
        'EOF': 'acc'
    },

    # Estado 2
    {
        'varinicio': 's4',
    },

    # Estado 3
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'facaAte': 's15',
        'fim': 's10'
    },

    # Estado 4
    {
        'varfim': 's19',
        'inteiro': 's21',
        'real': 's22',
        'lit': 's23'
    },

    # Estado 5
    {
        'EOF': 'r1'
    },

    # Estado 6
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'facaAte': 's15',
        'fim': 's10'
    },

    # Estado 7
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'facaAte': 's15',
        'fim': 's10'
    },

    # Estado 8
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'facaAte': 's15',
        'fim': 's10'
    },

    # Estado 9
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'facaAte': 's15',
        'fim': 's10'
    },

    # Estado 10
    {
        'EOF': 'r37'
    },

    # Estado 11
    {
        'id': 's28'
    },

    # Estado 12
    {
        'id': 's32',
        'Literal': 's30',
        'Num': 's31'
    },

    # Estado 13
    {
        'RCB': 's33'
    },

    # Estado 14
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimse': 's38'
    },

    # Estado 15
    {
        'AB_P': 's39'
    },

    # Estado 16
    {
        'AB_P': 's40'
    },

    # Estado 17
    {
        'id': 'r2',
        'leia': 'r2',
        'escreva': 'r2',
        'se': 'r2',
        'facaAte': 'r2',
        'fim': 'r2'
    },

    # Estado 18
    {
        'varfim': 's19',
        'inteiro': 's21',
        'real': 's22',
        'lit': 's23'
    },

    # Estado 19
    {
        'PT_V': 's42'
    },

    # Estado 20
    {
        'id': 's44'
    },

    # Estado 21
    {
        'id': 'r8'
    },

    # Estado 22
    {
        'id': 'r9'
    },

    # Estado 23
    {
        'id': 'r10'
    },

    # Estado 24
    {
        'EOF': 'r11'
    },

    # Estado 25
    {
        'EOF': 'r17'
    },

    # Estado 26
    {
        'EOF': 'r23'
    },

    # Estado 27
    {
        'EOF': 'r31'
    },

    # Estado 28
    {
        'PT_V': 's45'
    },

    # Estado 29
    {
        'PT_V': 's46'
    },

    # Estado 30
    {
        'PT_V': 'r14'
    },

    # Estado 31
    {
        'PT_V': 'r15'
    },

    # Estado 32
    {
        'PT_V': 'r16'
    },

    # Estado 33
    {
        'id': 's49',
        'Num': 's50'
    },

    # Estado 34
    {
        'id': 'r24',
        'leia': 'r24',
        'escreva': 'r24',
        'se': 'r24',
        'fimse': 'r24',
        'facaAte': 'r24',
        'fimFaca': 'r24',
        'fim': 'r24'
    },

    # Estado 35
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimse': 's38',
    },

    # Estado 36
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'AB_P': 's16',
        'fimse': 's38',
    },

    # Estado 37
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'AB_P': 's16',
        'fimse': 's38',
    },

    #Estado 38
    {
        'id': 'r30',
        'leia': 'r30',
        'escreva': 'r30',
        'se': 'r30',
        'fimse': 'r30',
        'facaAte': 'r30',
        'fimFaca': 'r30',
        'fim': 'r30'
    },

    #Estado 39
    {
        'id': 's49',
        'Num': 's50'
    },

    #Estado 40
    {
        'id': 's49',
        'Num': 's50'
    },

    #Estado 41
    {
        'id': 'r3',
        'leia': 'r3',
        'escreva': 'r3',
        'se': 'r3',
        'fimse': 'r3',
        'facaAte': 'r3',
        'fim': 'r3'
    },

    #Estado 42
    {
        'id': 'r4',
        'leia': 'r4',
        'escreva': 'r4',
        'se': 'r4',
        'fimse': 'r4',
        'facaAte': 'r4',
        'fim': 'r4'
    },

    #Estado 43
    {
        'PT_V': 's57'
    },

    #Estado 44
    {
        'PT_V': 'r7',
        ',': 's58'
    },

    #Estado 45
    {
        'id': 'r12',
        'leia': 'r12',
        'escreva': 'r12',
        'se': 'r12',
        'fimse': 'r12',
        'facaAte': 'r12',
        'fimFaca': 'r12',
        'fim': 'r12'
    },

    #Estado 46
    {
        'id': 'r13',
        'leia': 'r13',
        'escreva': 'r13',
        'se': 'r13',
        'fimse': 'r13',
        'facaAte': 'r13',
        'fimFaca': 'r13',
        'fim': 'r13'
    },

    #Estado 47
    {
        'PT_V': 's59'
    },

    #Estado 48
    {
        'PT_V': 'r20',
        'OPM': 's60'
    },

    #Estado 49
    {
        'PT_V': 'r21',
        'OPM': 'r21',
        'FC_P': 'r21',
        'OPR': 'r21'
    },

    #Estado 50
    {
        'PT_V': 'r22',
        'OPM': 'r22',
        'FC_P': 'r22',
        'OPR': 'r22'
    },

    #Estado 51
    {
        'id': 'r27',
        'leia': 'r27',
        'escreva': 'r27',
        'se': 'r27',
        'fimse': 'r27',
        'facaAte': 'r27',
        'fimFaca': 'r27',
        'fim': 'r27'
    },

    #Estado 52
    {
        'id': 'r28',
        'leia': 'r28',
        'escreva': 'r28',
        'se': 'r28',
        'fimse': 'r28',
        'facaAte': 'r28',
        'fimFaca': 'r28',
        'fim': 'r28'
    },

    #Estado 53
    {
        'id': 'r29',
        'leia': 'r29',
        'escreva': 'r29',
        'se': 'r29',
        'fimse': 'r29',
        'facaAte': 'r29',
        'fimFaca': 'r29',
        'fim': 'r29'
    },

    #Estado 54
    {
        'FC_P': 's61'
    },

    #Estado 55
    {
        'OPR': 's62'
    },

    #Estado 56
    {
        'FC_P': 's63'
    },

    #Estado 57
    {
        'varfim': 'r5',
        'inteiro': 'r5',
        'real': 'r5',
        'lit': 'r5'
    },

    #Estado 58
    {
        'id': 's44'
    },

    #Estado 59
    {
        'id': 'r18',
        'leia': 'r18',
        'escreva': 'r18',
        'se': 'r18',
        'fimse': 'r18',
        'facaAte': 'r18',
        'fimFaca': 'r18',
        'fim': 'r18'
    },

    #Estado 60
    {
        'id': 's49',
        'Num': 's50'
    },

    #Estado 61
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimFaca': 's70'
    },

    #Estado 62
    {
        'id': 's49',
        'Num': 's50'
    },

    #Estado 63
    {
        'entao': 's72'
    },

    #Estado 64
    {
        'PT_V': 'r6'
    },

    #Estado 65
    {
        'PT_V': 'r19'
    },

    #Estado 66
    {
        'id': 'r32',
        'leia': 'r32',
        'escreva': 'r32',
        'se': 'r32',
        'facaAte': 'r32',
        'fim': 'r32'
    },

    #Estado 67
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimFaca': 's70'
    },

    #Estado 68
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimFaca': 's70'
    },

    #Estado 69
    {
        'id': 's13',
        'leia': 's11',
        'escreva': 's12',
        'se': 's16',
        'fimFaca': 's70'
    },

    #Estado 70
    {
        'id': 'r36',
        'leia': 'r36',
        'escreva': 'r36',
        'se': 'r36',
        'facaAte': 'r36',
        'fim': 'r36'
    },

    #Estado 71
    {
        'FC_P': 'r26'
    },

    #Estado 72
    {
        'id': 'r25',
        'leia': 'r25',
        'escreva': 'r25',
        'se': 'r25',
        'fimse': 'r25'
    },

    #Estado 73
    {
        'id': 'r33',
        'leia': 'r33',
        'escreva': 'r33',
        'se': 'r33',
        'facaAte': 'r33',
        'fim': 'r33'
    },

    #Estado 74
    {
        'id': 'r34',
        'leia': 'r34',
        'escreva': 'r34',
        'se': 'r34',
        'facaAte': 'r34',
        'fim': 'r34'
    },

    # Estado 75
    {
        'id': 'r35',
        'leia': 'r35',
        'escreva': 'r35',
        'se': 'r35',
        'facaAte': 'r35',
        'fim': 'r35'
    }
]

'''
--------------------------------------------------------------------------------------------------------
Parte do Analisador Semântico
--------------------------------------------------------------------------------------------------------
'''
tipo_texto = {
	"inteiro" 	: "int",
	"real" 		: "float",
	"lit" 		: "char[]"
}

cabecalho_programa = """#include<stdio.h>
#include<stdbool.h>

typedef int inteiro;
typedef float real;
typedef char lit[128];

int main(){
"""
rodape_programa = """
return 0;
}
"""