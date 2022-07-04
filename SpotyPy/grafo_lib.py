import random
from Grafo import Grafo
from collections import deque

AMORTIGUACION = 0.85
PRP_VOLVER_A_ORIGEN = 30
N_ITER_PR = 5
N_ITER_PR_PERSONALIZADO = 20

def bfs_camino_minimo(grafo, origen):
	'''Recorre un grafo no pesado y devuelve el camino minimo para todos los vértices, partiendo del 
	origen, en la forma de un diccionario de padres.'''
	visitados = set()
	padre = {}
	padre[origen] = None
	visitados.add(origen)
	q = deque()
	q.append(origen)
	while q:
		v = q.popleft()
		for w in grafo.adyacentes(v):
			if w not in visitados:
				padre[w] = v
				visitados.add(w)
				q.append(w)
	return padre

def crear_camino(padre, origen, destino):
	'''A partir del diccionario de padres, crea un camino (si es posible) en forma de lista, desde 
	el origen al destino'''
	if destino not in padre:
		return None
	actual = destino
	camino = []
	while actual is not None:
		camino.append(actual)
		actual = padre[actual]
	return camino[::-1]

def bfs_obtener_cant_en_rango(grafo, origen, rango):
	'''Recibe un grafo, un vértice origen, y un numero N (rango). Devuelve la cantidad de vértices
	a N distancia del vértice en cuestión.'''
	visitados = set()
	en_rango = 0
	orden = {}
	orden[origen] = 0
	visitados.add(origen)
	q = deque()
	q.append(origen)
	while q:
		v = q.popleft()
		if v in orden:
			if orden[v] == rango:
				break
		for w in grafo.adyacentes(v):
			if w not in visitados:
				orden[w] = orden[v] + 1
				if orden[w] == rango:
					en_rango += 1
				visitados.add(w)
				q.append(w)
	return en_rango


def obtener_pagerank_personalizado(grafo, origen, pagerank):
	'''A partir de un diccionario de pagerank personalizado (que puede tener valores de una previa 
	iteracion de pagerank, o no) actualiza el pagerank de todos los vertices del grafo, en forma 
	de vertice:pagerank en el diccionario.'''
	n = N_ITER_PR_PERSONALIZADO * grafo.cantidad_vertices()
	vertice = origen
	valor = 1
	for i in range(n):
		valor = valor / len(grafo.adyacentes(vertice))
		vertice = random.choice(grafo.adyacentes(vertice))
		pagerank[vertice] = pagerank.get(vertice, 0) + valor
		if random.randint(0, 100) <= PRP_VOLVER_A_ORIGEN:
			vertice = origen
			valor = 1
	return pagerank


def obtener_pagerank(grafo):
	'''Recibe un grafo, y devuelve un diccionario en el cuál las claves son los vértices del grafo,
	y los valores son el pagerank de cada vértice.'''
	pagerank = {}
	for i in range(N_ITER_PR):
		for v in grafo:
			suma = 0
			for w in grafo.adyacentes(v):
				pagerank[w] = pagerank.get(w, 0)
				suma += pagerank[w] / len(grafo.adyacentes(w))
			pagerank[v] = (1 - AMORTIGUACION) / grafo.cantidad_vertices() + suma * AMORTIGUACION
	return pagerank


def clustering(grafo, v):
	"""Devuelve el coeficiente de clustering del elemento elegido para un grafo no dirigido"""
	adyacentes = list(grafo.adyacentes(v))
	grado_salida = len(adyacentes)
	if grado_salida < 2:
		return 0.000
	conexiones_adyacentes = 0
	for i in range(len(adyacentes) - 1):
		u = adyacentes[i]
		for j in range(i + 1, len(adyacentes)):
			w = adyacentes[j]
			if u != w and grafo.son_adyacentes(u, w):
				conexiones_adyacentes += 1
	return (2 * conexiones_adyacentes) / (grado_salida * (grado_salida - 1))