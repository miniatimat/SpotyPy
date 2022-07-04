#!/usr/bin/python3
import csv
import sys
from grafo_lib import bfs_obtener_cant_en_rango, crear_camino, obtener_pagerank, obtener_pagerank_personalizado, clustering, bfs_camino_minimo
from Grafo import Grafo
import itertools


USER_ID = 'USER_ID'
TRACK_NAME = 'TRACK_NAME'
ARTIST = 'ARTIST'
PLAYLIST_NAME = 'PLAYLIST_NAME'

# Comandos
CMD_CAMINO_MAS_CORTO = 'camino'
CMD_MAS_IMPORTANTES = 'mas_importantes'
CMD_RECOMENDACION = 'recomendacion'
CMD_CICLO = 'ciclo'
CMD_RANGO = 'rango'
CMD_CLUSTERING = 'clustering'


def tsv_crear_estructura(ruta_tsv):
	'''Recibe una ruta a un archivo tsv, y devuelve una lista de diccionarios, siendo cada diccionario una fila del 
	archivo, y teniendo como clave a las'''
	with open(ruta_tsv, encoding='utf-8' ) as archivo:
		reader = csv.DictReader(archivo, delimiter='\t', quoting=csv.QUOTE_NONE)
		elementos = []
		for fila in reader:
			elementos.append(fila)
		return elementos

def crear_grafos(elementos):
	'''A partir de los elementos de un archivo TSV ya procesado, crea dos grafos: un grafo bipartito X con las canciones
	y los usuarios de una base de datos de spotify, y otro grafo Y de todas las canciones de la base de datos, con 
	aristas dependiendo de si comparten una playlist. Además, crea dos conjuntos de canciones y usuarios, y un 
	diccionario de playlists, con cada cancion dentro de un conjunto como valor, y el nombre de la playlist como 
	clave.'''
	x = Grafo()
	y = Grafo()
	playlists = {}
	usuarios = set()
	canciones = set()
	for elem in elementos:
		cancion = elem[TRACK_NAME] + ' - ' + elem[ARTIST]
		usuario = elem[USER_ID]
		playlist = elem[PLAYLIST_NAME]
		playlists[playlist] = playlists.get(playlist, set())
		playlists[playlist].add(cancion)
		x.vertice(usuario)
		x.vertice(cancion)
		y.vertice(cancion)
		x.arista(usuario, cancion, playlist)
		usuarios.add(usuario)
		canciones.add(cancion)
	return x, y, playlists, usuarios, canciones


def crear_grafo_canciones(y, playlists):
	"""Crea el grafo Y, a partir de las canciones que estan en una misma playlist.
	Al estar todas las canciones ya en la playlist, no hace falta comparar. Orden N*log(N), siendo N el numero de 
	entradas."""
	#playlists{ metal:[ bad apple - monica, mama - mix], }
	for playlist in playlists.values():
		playlist = list(playlist)
		for i in range(len(playlist) - 1):
			v = playlist[i]
			for j in range(i + 1, len(playlist)):
				w = playlist[j]
				y.arista(v, w)


def camino_mas_corto(x, origen, destino):
	'''A partir de un grafo, un conjunto de canciones y otro de usuarios, un origen y un destino, esta función crea
	un camino mínimo entre amb'''
	padre = bfs_camino_minimo(x, origen)
	camino = crear_camino(padre, origen, destino)
	if not camino:
		return None
	anterior = camino.pop(0)
	resultado = ''
	while len(camino) > 0:
		usuario = camino.pop(0)
		siguiente = camino.pop(0)
		resultado += f'{anterior} --> aparece en playlist --> '
		playlist = x.peso(anterior, usuario)
		resultado += f'{playlist} --> de --> {usuario} --> tiene una playlist --> '
		playlist = x.peso(usuario, siguiente)
		resultado += f'{playlist} --> donde aparece --> '
		anterior = siguiente
	resultado += anterior
	return resultado


def recomendacion(grafo_x, pide_canciones, n, sugerencias, usuarios, canciones):
	'''Crea una lista con N recomendaciones a partir de una serie de sugerencias (canciones), usando el 
	algoritmo de pagerank personalizado sobre el grafo X.'''
	pagerank = {}
	for origen in sugerencias:
		obtener_pagerank_personalizado(grafo_x, origen, pagerank)
	aux = sorted(pagerank, key=pagerank.get, reverse=True)
	if pide_canciones:
		return [c for c in aux if c in canciones and c not in sugerencias][:n]
	else:
		return [u for u in aux if u in usuarios][:n]


def _ciclo_canciones(grafo_y, visitados, cantidad, cancion, inicio, ciclo):
	if cantidad == 0:
		if cancion in grafo_y.adyacentes(inicio):
			ciclo.insert(0, cancion)
			return True
		return False
	visitados.add(cancion)
	for proxima_cancion in grafo_y.adyacentes(cancion):
		if proxima_cancion not in visitados and _ciclo_canciones(grafo_y, visitados, cantidad-1, proxima_cancion, inicio, ciclo):
			ciclo.insert(0, cancion)
			return True
	visitados.remove(cancion)
	return False


def ciclo_canciones(grafo_y, playlists, cantidad, cancion):
	""" Genera un ciclo con otras N canciones, partiendo y terminando en la cancion seleccionada. """
	visitados = set()
	ciclo = []
	_ciclo_canciones(grafo_y, visitados, cantidad - 1, cancion, cancion, ciclo)
	ciclo.append(cancion)
	return ciclo


def procesar_comando(comando, parametros, x, y, usuarios, canciones, playlists, pagerank):
	if comando == CMD_CAMINO_MAS_CORTO:
		aux = parametros.split(' >>>> ')
		if len(aux) != 2:
			print(f'<{CMD_CAMINO_MAS_CORTO}> debe recibir dos parametros.')
			return
		origen, destino = aux
		if origen not in canciones or destino not in canciones:
			print('Tanto el origen como el destino deben ser canciones')
			return
		elif origen == destino:
			print('Las canciones deben ser distintas.')
			return
		resultado = camino_mas_corto(x, origen, destino)
		if not resultado:
			print('No se encontro recorrido')
			return
		print(resultado)

	elif comando == CMD_MAS_IMPORTANTES:
		if len(pagerank) == 0:
			pagerank_aux = obtener_pagerank(x)
			pagerank_lista = sorted(pagerank_aux, key=pagerank_aux.get, reverse = True)
			for x in pagerank_lista:
				if x in canciones:
					pagerank.append(x)
		n = parametros
		if not n.isdigit():
			print('El parámetro debe ser un número.')
			return
		n = int(n)
		print('; '.join(pagerank[:n]))

	elif comando == CMD_RECOMENDACION:
		aux = parametros.split(" ", 2)
		if len(aux) != 3:
			print("Parametros incorrectos")
			return
		cancion_o_usuario, cantidad, basado_en = aux[0], aux[1], aux[2]
		sugerencias = basado_en.split(' >>>> ')
		pide_canciones = True
		
		for cancion in sugerencias:
			if cancion not in canciones:
				print(f'<{cancion}> no es una canción')
				return
		if not cantidad.isdigit():
			print('La cantidad debe ser un número')
			return
		cantidad = int(cantidad)
		if cancion_o_usuario == 'usuarios':
			pide_canciones = False
		elif cancion_o_usuario != 'canciones':
			print('Solo se pueden devolver usuarios o canciones')
			return
		recomendaciones = recomendacion(x, pide_canciones, cantidad, sugerencias, usuarios, canciones)
		print("; ".join(recomendaciones))

	elif comando == CMD_CICLO: 
		aux = parametros.split(' ', 1)
		if len(aux) != 2:
			print(f'<{CMD_CICLO}> debe recibir dos parametros.')
			return
		n, cancion = aux[0], aux[1]
		if cancion not in canciones:
			print(f'<{cancion}> no es una canción')
			return
		if not n.isdigit():
			print('El segundo parámetro debe ser un número positivo.')
			return
		n = int(n)
		if y.cantidad_aristas() == 0:
			crear_grafo_canciones(y, playlists)
		ciclo = ciclo_canciones(y, playlists, n, cancion)
		if len(ciclo) != (n + 1):
			print('No se encontro recorrido')
			return
		else:
			print(" --> ".join(ciclo))

	elif comando == CMD_RANGO:
		aux = parametros.split(' ', 1)
		if len(aux) != 2:
			print(f'<{CMD_RANGO}> debe recibir dos parametros.')
			return
		rango = aux[0]
		cancion = aux[1]
		if not rango.isdigit():
			print('El primer parámetro debe ser un número positivo.')
			return
		rango = int(rango)
		if cancion not in canciones:
			print('El segundo parámetro debe ser una canción.')
			return
		if y.cantidad_aristas() == 0:
			crear_grafo_canciones(y, playlists)
		print(bfs_obtener_cant_en_rango(y, cancion, rango))

	elif comando == CMD_CLUSTERING:
		cancion = parametros
		coeficiente = 0
		if y.cantidad_aristas() == 0:
			crear_grafo_canciones(y, playlists)
		if cancion == '':
			suma = 0
			for v in y.obtener_vertices():
				suma += clustering(y, v)
			coeficiente = suma / y.cantidad_vertices()
		else:
			if cancion not in canciones:
				print(f'<{cancion}> no es una canción')
				return
			coeficiente = clustering(y, cancion)
		print((str.format('{0:.3f}',coeficiente)))

	else:
		print(f'<{comando}> no es un comando válido.')


def main():
	if len(sys.argv) != 2:
		print('No se recibió la cantidad correcta de parámetros.')
		return
	ruta = sys.argv[1]
	try:
		elementos = tsv_crear_estructura(ruta)
	except FileNotFoundError:
		print('El archivo no existe.')
		return
	x, y, playlists, usuarios, canciones = crear_grafos(elementos)
	pagerank = []
	while True:
		try:
			print("Enter you command")
			linea = input()
			aux = linea.rstrip('\n').split(' ', 1)
			if len(aux) == 1:
				aux.append('')
			comando, parametros = aux[0], aux[1]
			procesar_comando(comando, parametros, x, y, usuarios, canciones, playlists, pagerank)
		except EOFError:
			break

main()
