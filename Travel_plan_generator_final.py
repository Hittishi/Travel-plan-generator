from unionfind import unionfind
import heapq


class GlobalVar:
    mst_graph = {

    }
    minimum_spanning_tree = []
    a_star_graph = {
        # Graph which stores g distances and f distances
        'A': {'B': [2, 2], 'C': [3, 2]},
        'B': {'D': [3, 5], 'E': [1, 1]},
        'C': {'F': [2, 0]},
        'D': {},
        'E': {'F': [1, 0]},
        'F': {}
    }
    airport_list = {
        'AXB': 'A',
        'TEX': 'B',
        'WDC': 'C',
        'DEL': 'D',
        'EWR': 'E',
        'FRA': 'F'
    }


def make_graph():
    # tuple = (cost, n1, n2)
    return {
        'A': [(3, 'D', 'A'), (3, 'C', 'A'), (2, 'B', 'A')],
        'B': [(2, 'A', 'B'), (4, 'C', 'B'), (3, 'E', 'B')],
        'C': [(3, 'A', 'C'), (5, 'D', 'C'), (1, 'E', 'C'), (4, 'B', 'C')],
        'D': [(3, 'A', 'D'), (5, 'C', 'D'), (7, 'F', 'D')],
        'E': [(8, 'F', 'E'), (1, 'C', 'E'), (3, 'B', 'E')],
        'F': [(9, 'G', 'F'), (8, 'E', 'F'), (7, 'D', 'F')],
        'G': [(9, 'F', 'G')],
    }


def load_edges(graph):
    num_nodes = 0
    edges = []

    for key, value in graph.items():
        # initialising the Minimum spanning tree dictionary
        GlobalVar.mst_graph[key] = []
        num_nodes += 1
        edges.extend(value)

    return num_nodes, sorted(edges)


def conv_char(c):
    return ord(c) - 65


def a_star_graph_builder():
    # Write an algo for generating g and h values for each node for a given graph
    return None


def a_star(graph, node1, node2):
    f_distance = {node: float('inf') for node in graph}
    f_distance[node1] = 0
    g_distance = {node: float('inf') for node in graph}
    g_distance[node1] = 0
    came_from = {node: None for node in graph}
    came_from[node1] = node1
    queue = [(0, node1)]
    while queue:
        current_f_distance, current_node = heapq.heappop(queue)
        if current_node == node2:
            print('found the end_node')
            # printing path
            path = [node1]
            min_f_distance = f_distance[node2]
            for key, value in came_from.items():
                if f_distance[key] == min_f_distance:
                    path.append(key)
            print('path', end=" ")
            print(path)
            return f_distance, came_from
        for next_node, weights in graph[current_node].items():
            temp_g_distance = g_distance[current_node] + weights[0]
            if temp_g_distance < g_distance[next_node]:
                g_distance[next_node] = temp_g_distance
                heuristic = weights[1]
                f_distance[next_node] = temp_g_distance + heuristic
                came_from[next_node] = current_node
                heapq.heappush(queue, (f_distance[next_node], next_node))
    return f_distance, came_from


def kruskal(graph):
    cost = 0
    minimum_spanning_tree = []
    no_of_nodes, edges = load_edges(graph)
    finder = unionfind(no_of_nodes)
    for edge in edges:
        cost, n1, n2 = edge[0], edge[1], edge[2]
        if not finder.issame(conv_char(n1), conv_char(n2)):
            cost += cost
            finder.unite(conv_char(n1), conv_char(n2))
            minimum_spanning_tree.append((n1, n2, cost))
            temp_list = GlobalVar.mst_graph[n1]
            temp_list.append(n2)
            GlobalVar.mst_graph[n1] = temp_list
            temp_list = GlobalVar.mst_graph[n2]
            temp_list.append(n1)
            GlobalVar.mst_graph[n2] = temp_list
            GlobalVar.minimum_spanning_tree = minimum_spanning_tree
    return minimum_spanning_tree, cost


def prims(graph, start='A'):
    unvisited = list(graph.keys())
    # initialising the Minimum spanning tree dictionary
    for key in unvisited:
        GlobalVar.mst_graph[key] = []
    visited = []
    total_cost = 0
    minimum_spanning_tree = []

    unvisited.remove(start)
    visited.append(start)

    heap = graph[start]
    heapq.heapify(heap)

    while unvisited:
        (cost, n2, n1) = heapq.heappop(heap)
        new_node = None

        if n1 in unvisited and n2 in visited:
            new_node = n1
            minimum_spanning_tree.append((n2, n1, cost))
            # code
            temporary_list = GlobalVar.mst_graph[n1]
            temporary_list.append(n2)
            GlobalVar.mst_graph[n1] = temporary_list
            temporary_list = GlobalVar.mst_graph[n2]
            temporary_list.append(n1)
            GlobalVar.mst_graph[n2] = temporary_list
        elif n1 in visited and n2 in unvisited:
            new_node = n2
            minimum_spanning_tree.append((n1, n2, cost))
            # code
            temporary_list = GlobalVar.mst_graph[n1]
            temporary_list.append(n2)
            GlobalVar.mst_graph[n1] = temporary_list
            temporary_list = GlobalVar.mst_graph[n2]
            temporary_list.append(n1)
            GlobalVar.mst_graph[n2] = temporary_list
        if new_node is not None:
            unvisited.remove(new_node)
            visited.append(new_node)
            total_cost += cost
            for node in graph[new_node]:
                heapq.heappush(heap, node)
    GlobalVar.minimum_spanning_tree = minimum_spanning_tree
    return minimum_spanning_tree, total_cost


def bfs_shortest_path(graph, node1, node2):
    current_path = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return current_path[0]

    while path_index < len(current_path):
        current_path = current_path[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if next_node not in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                current_path.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


def path_weight_finder(path):
    path_weight = 0
    length = len(path)
    for i in range(0, length - 1):
        node1 = path[i]
        node2 = path[i + 1]
        for a_set in GlobalVar.minimum_spanning_tree:
            if a_set[0] == node1 and a_set[1] == node2:
                weight = a_set[2]
                path_weight = path_weight + weight
    print(path_weight)


def main():
    actual_path = []
    print("Welcome to Travel Plan generator")
    print("Please select source Airport from the following list")
    for airport in GlobalVar.airport_list:
        print(airport)
    source = input("Please select Source Airport")
    for airport in GlobalVar.airport_list:
        if airport != source:
            print(airport)
    destination = input("Please select Destination Airport")
    source_index = GlobalVar.airport_list[source]
    destination_index = GlobalVar.airport_list[destination]
    graph = make_graph()
    algo = input("Select algorithm : 1)Prims 2)Krushkal 3)A*")
    if algo == "Prims":
        minimum_spanning_tree, total_cost = prims(graph, 'A')
        print(f'Minimum spanning tree: {minimum_spanning_tree}')
        shortest_path = bfs_shortest_path(GlobalVar.mst_graph, source_index, destination_index)
        print(shortest_path)
    elif algo == "Krushkal":
        minimum_spanning_tree, total_cost = kruskal(graph)
        print(f'Minimum spanning tree: {minimum_spanning_tree}')
        shortest_path = bfs_shortest_path(GlobalVar.mst_graph, source_index, destination_index)
        print(shortest_path)
    elif algo == "A*":
        path = a_star(GlobalVar.a_star_graph,'A' , 'E')
        #printbfs_shortest_path(GlobalVar.mst_graph, 'E', 'A'))
        #print(source_index,destination_index)
        print(path)

    #minimum_spanning_tree, total_cost = kruskal(graph)
    #minimum_spanning_tree, total_cost = prims(graph, 'A')
    #print(f'Minimum spanning tree: {minimum_spanning_tree}')

    # print(f'Total cost: {total_cost}')
    # print(GlobalVar.mst_graph)
    #shortest_path = bfs_shortest_path(GlobalVar.mst_graph, source_index, destination_index)
    #print(bfs_shortest_path(GlobalVar.mst_graph, 'A', 'E'))
    #print(shortest_path)
    # print('Total weight of path = ', end=" ")
    # path_weight_finder(shortest_path)
    """
    path= a_star(GlobalVar.a_star_graph, source_index, destination_index)
    for each_index in path:

        for airport, id in GlobalVar.airport_list.items() :
            if id==each_index :
                actual_path.append(airport)
    print(actual_path)
    """



main()
