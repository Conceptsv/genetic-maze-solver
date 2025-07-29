
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt

class MazeGraph:
    def __init__(self, size):
        self.size = size
        self.graph = nx.grid_2d_graph(size, size)
        self._randomize_weights()
        self.start = (0, 0)
        self.goal = (size - 1, size - 1)
    def _randomize_weights(self):
        for u, v in self.graph.edges():
            self.graph[u][v]['weight'] = random.randint(1, 20)
    def find_path(self):
        return nx.shortest_path(self.graph, self.start, self.goal, weight='weight')
    def visualize(self, path=None):
        pos = {(x, y): (y, -x) for x, y in self.graph.nodes()}
        weights = [self.graph[u][v]['weight'] for u, v in self.graph.edges()]
        nx.draw(self.graph, pos, with_labels=False, node_size=30, edge_color=weights, edge_cmap=plt.cm.plasma)
        if path:
            edges_in_path = list(zip(path, path[1:]))
            nx.draw_networkx_edges(self.graph, pos, edgelist=edges_in_path, edge_color='red', width=2)
        plt.show()

def mutate_path(path, size):
    mutated = list(path)
    idx = random.randint(1, len(path) - 2)
    new_node = (random.randint(0, size - 1), random.randint(0, size - 1))
    if new_node not in mutated:
        mutated[idx] = new_node
    return mutated

def evaluate_path(graph, path):
    score = 0
    for i in range(len(path) - 1):
        if graph.has_edge(path[i], path[i + 1]):
            score += graph[path[i]][path[i + 1]]['weight']
        else:
            score += 100
    return score

def genetic_solver(size, generations=200, population_size=50):
    maze = MazeGraph(size)
    initial_path = maze.find_path()
    population = [initial_path for _ in range(population_size)]
    best_path = initial_path
    for _ in range(generations):
        new_population = []
        for p in population:
            new_population.append(mutate_path(p, size))
        population += new_population
        population = sorted(population, key=lambda p: evaluate_path(maze.graph, p))[:population_size]
        if evaluate_path(maze.graph, population[0]) < evaluate_path(maze.graph, best_path):
            best_path = population[0]
    maze.visualize(best_path)
    return best_path

if __name__ == "__main__":
    best = genetic_solver(12)
    print(best)
