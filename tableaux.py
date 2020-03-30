#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(A):
    if A.right == None:
        return A.label
    elif A.label == "-":
        return "-" + Inorder(A.right)
    elif A.label in ["Y", "O", ">", "="]:
        return "(" + Inorder(A.left) + A.label + Inorder(A.right) + ")"

def string2tree(A):
    conectivos = ["O", "Y", ">", "="]
    pila = []
    for c in A:
        if c in letrasProposicionales:
            pila.append(Tree(c, None, None))
        elif c == "-":
            formulaaux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(formulaaux)
        elif c in conectivos:
            formulaaux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(formulaaux)
    return pila[-1]

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"


def es_literal(f):
	A = Inorder(f)
    if len(A) <= 2:
        return True
    else:
        return False

def no_literales(l):
	for i in l:
        if es_literal(i):
            return True
        else:
            return False

def par_complementario(l):
    letrasProposicionales = [chr(x) for x in range(97, 123)]
	for i in letrasProposicionales:
        A = Tree(i, None, None)
        No_A = Tree("-", None, i)

        if A and No_A in l:
            return True
        else:
            return False

def alfa_beta(f):
    if f.label == "-":
        if f.right.label == "-":
            return "1alfa"
        elif f.right.label == "O":
            return "3alfa"
        elif f.right.label == ">":
            return "4alfa"
        elif f.right.label == "Y":
            return "1beta"
    elif f.label == "Y":
        return "2alfa"
    elif f.label == "O":
        return "2beta"
    elif f.label == ">":
        return "3beta"
    else:
        return "hoja"

def clasifica_y_extiende(f):
	global listaHojas

	clasificacion = alfa_beta(f)

	if clasificacion == "hoja":
		listaHojas.remove([f])
		listaHojas.append(f)

	elif clasificacion == "1alfa":
		hoja = [f.right.right]
		listaHojas.remove([f])
		listaHojas.append(hoja)

	elif clasificacion == "2alfa":
	  	hoja_l = f.left
	  	hoja_r = f.right
	  	listaHojas.remove([f])
	  	listaHojas.append([hoja_l,hoja_r])

	elif clasificacion == "3alfa":
	  	hoja_l = Tree('-', None, f.right.left)
	  	hoja_r = Tree('-', None, f.right.right)
	  	listaHojas.remove([f])
	  	listaHojas.append([hijo_izq,hijo_der])

	elif clasificacion == "4alfa":
	  	hoja_l = f.right.left
	  	hoja_r = Tree('-', None, f.right.right)
	  	listaHojas.remove([f])
	  	listaHojas.append([hijo_izq,hijo_der])

	elif clasificacion == "1beta":
	  	hoja_l = Tree('-', None, f.right.left)
	  	hoja_r = Tree('-', None, f.right.right)
	  	listaHojas.remove([f])
	  	listaHojas.append([hoja_l], [hoja_r])

	elif clasificacion == "2beta":
	  	hoja_l = f.left
	  	hoja_r = f.right
	  	listaHojas.remove([f])
	  	listaHojas.append([hoja_l], [hoja_r])

	elif clasificacion == "3beta":
	  	hoja_l = Tree('-', None, f.left)
	  	hoja_r = f.right
	  	listaHojas.remove([f])
	  	listaHojas.append([hoja_l], [hoja_r])

def Tableaux(f):
	global listaHojas
	global listaInterpsVerdaderas

	A = StringtoTree(f)
	listaHojas = [[A]]
	clasifica_y_extiende(A)
	while len(listaHojas)>0:
		for i in listaHojas:
			if not no_literales(i):
				if par_complementario(i):
					listaHojas.remove(i)
				else:
					listaInterpsVerdaderas.append(i)
					listaHojas.remove(i)
			else:
				clasifica_y_extiende(no_literales(i))

	return listaInterpsVerdaderas
