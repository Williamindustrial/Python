import networkx as nx
import matplotlib.pyplot as plt

# Definir el grafo
G = nx.Graph()
G1 = nx.Graph()

# Agregar nodos con coordenadas
G.add_node('0', pos=(40, 50))
G.add_node('$P_{23}$', pos=(16, 45))
G.add_node('$P_{22}$', pos=(42, 65))
G.add_node('$P_{11}$', pos=(52, 75))
G.add_node('$P_{13}$', pos=(62, 69))
G.add_node('$P_{21}$', pos=(60, 66))
#G.add_node('F', pos=(25,85))
#G.add_node('G', pos=(35,69))
#G.add_node('H', pos=(35, 66))


# Agregar arcos
G.add_weighted_edges_from([('0', '$P_{23}$', 107), ('$P_{23}$', '$P_{22}$', 150), ('$P_{22}$', '$P_{11}$', 60),
                           ('$P_{11}$', '$P_{13}$', 51),('$P_{13}$', '$P_{21}$', 17),('$P_{21}$', '0', 111)])

# Definir la posición de los nodos en el grafo
pos = nx.get_node_attributes(G, 'pos')

G1 = nx.Graph()

# Agregar nodos con coordenadas
G1.add_node('0', pos=(40, 50))
G1.add_node('$P_{10}$', pos=(10, 10))
pos1 = nx.get_node_attributes(G1, 'pos')

# Dibujar el grafo
nx.draw(G, pos, with_labels=True, node_color='blue', node_size=500,
        font_size=10, font_weight='bold', arrowsize=10)
nx.draw(G1, pos1, node_color='red',node_size=500)

# Agregar etiquetas de peso a los arcos
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)

# Mostrar el grafo
plt.show()