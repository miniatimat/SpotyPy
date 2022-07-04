import random

class Grafo:

	def __init__(self, es_dirigido = False, vertices = []):
		self.vertices = {}
		self.cantidad_e = 0
		self.es_dirigido = es_dirigido
		for v in vertices:
			self.vertices[v] = {}
		self.iter_n = 0

	def __str__(self):
		cadena = ''
		for v, ady in self.vertices.items():
			ady_aux = list(ady)
			cadena += f'{v}: {ady_aux}\n'
		return cadena

	def __repr__(self):
		cadena = ''
		for v, ady in self.vertices.items():
			cadena += f'{v}: {list(ady)}\n'
		return cadena

	def __iter__(self):
		self.iter_n = 0
		return iter(self.vertices)

	def __next__(self):
		try:
			aux = list(self.vertices.keys())[self.iter_n]
		except IndexError:
			raise StopIteration
		self.iter_n += 1
		return aux

	def vertice(self, v):
		'''Añade un vértice al grafo. No hace nada si el vertice ya existía.'''
		self.vertices[v] = self.vertices.get(v, {})

	def borrar(self, v):
		'''Borra un vértice de un grafo, incluyendo todas las aristas que conectaban a ese vértice. 
		Lanza KeyError si no existe el vértice'''
		if v not in self.vertices:
			raise KeyError(f"{v} no se encuentra en el grafo")
		self.vertices.pop(v)
		for w, ady in self.vertices.items():
			while v in ady:
				ady.pop(v)

	def arista(self, v, w, peso = 1):
		'''Crea una arista entre dos vértices del grafo, con peso opcional. Lanza KeyError si alguno
		 de los vértices no existe. Si la arista ya existía, únicamente reemplaza el peso.'''
		if v not in self.vertices:
			raise KeyError(f'No existe el vértice {v}')
			return
		if w not in self.vertices:
			raise KeyError(f'No existe el vértice {w}')
			return
		self.vertices[v][w] = peso
		if not self.es_dirigido:
			self.vertices[w][v] = peso
		self.cantidad_e += 1

	def borrar_arista(self, v, w):
		'''Borra una arista entre dos vértices. Lanza KeyError si alguno de los vértices no existe, 
		o ValueError si no son adyacentes.'''
		if v not in self.vertices:
			raise KeyError(f'No existe el vértice {v}')
		if w not in self.vertices:
			raise KeyError(f'No existe el vértice {w}')
		if v not in self.vertices[w]:
			raise ValueError(f"{v} no es adyacente de {w}")
		self.vertices[v].pop(w)
		if not self.es_dirigido:
			self.vertices[w].pop(v)
		self.cantidad_e -= 1

	def adyacentes(self, v):
		'''Devuelve una lista de adyacentes al vértice.'''
		if v not in self.vertices:
			raise KeyError(f'No existe el vértice {v}')
		return list(self.vertices[v])

	def son_adyacentes(self, v, w):
		'''Devuelve True si son adyacentes, False en caso contrario. Lanza KeyError si alguno de los
		vértices no existe.'''
		if v not in self.vertices:
			raise KeyError(f'No existe el vértice {v}')
		if w not in self.vertices:
			raise KeyError(f'No existe el vértice {w}')
		return w in self.vertices[v]

	def pertenece(self, v):
		'''Devuelve True si existe el vértice en el grafo.'''
		return v in self.vertices

	def aleatorio(self):
		'''Devuelve un vértice aleatorio del grafo. Lanza IndexError si el grafo está vacío.'''
		if (self.esta_vacio()):
			raise IndexError(f"El grafo está vacío")
		return random.choice(list(self.vertices))

	def peso(self, v, w):
		'''Devuelve el peso de una arista entre los dos vértices. Lanza KeyError si alguno de los 
		vértices no existe, o ValueError si no son adyacentes.'''
		if v not in self.vertices:
			raise KeyError(f'No existe el vértice {v}')
		if w not in self.vertices:
			raise KeyError(f'No existe el vértice {w}')
		if w not in self.vertices[v]:
			raise ValueError(f"{w} no es adyacente de {v}")
		return self.vertices[v][w]

	def obtener_vertices(self):
		'''Devuelve una lista de todos los vértices del grafo.'''
		return list(self.vertices)

	def esta_vacio(self):
		'''Devuelve True si el grafo no tiene vértices, false en caso contrario.'''
		return len(self.vertices) == 0

	def cantidad_vertices(self):
		'''Devuelve la cantidad de vértices en el grafo.'''
		return len(self.vertices)

	def cantidad_aristas(self):
		'''Devuelve la cantidad de aristas en el grafo.'''
		return self.cantidad_e
