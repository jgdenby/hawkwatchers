import random as rd
from Stellar import ktechnets as kt
import numpy as np


def poin2(graph, node1, node2, artist_set, chrono, alb_metrics, sound_metrics):
    if node1 in artist_set:
        todo_metrics = set(alb_metrics + sound_metrics + ["avg_sonics"])
        path_list = [[node1]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = {node1}
        if node1 == node2:
            return path_list[0]

        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = graph[last_node]
            # Search goal node
            if node2 in next_nodes:
                current_path.append(node2)
                return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes and (not next_node in todo_metrics):
                    if chrono:
                        if (
                            graph[next_node]["avg_releaseyear"]
                            <= graph[last_node]["avg_releaseyear"]
                        ):
                            new_path = current_path[:]
                            new_path.append(next_node)
                            path_list.append(new_path)
                            # To avoid backtracking
                            previous_nodes.add(next_node)
                    else:
                        new_path = current_path[:]
                        new_path.append(next_node)
                        path_list.append(new_path)
                        # To avoid backtracking
                        previous_nodes.add(next_node)
            # Continue to next path in list
            path_index += 1
        # No path is found
        return []
    else:
        print("Sorry!" + node1 + " currently not in our radar")


def walk4(
    artnet, alb_metrics, sound_metrics, mweights, matchtype, start=None, max_size=10
):

    artist_set = list(artnet.keys())

    if not start:
        start = artist_set[rd.randint(0, len(artist_set))]

    path = [start]

    while not len(path) > max_size:

        if matchtype not in ["rand", "top"]:
            start = kt.get_best_match(
                artnet, start, matchtype, alb_metrics, sound_metrics, mweights
            )
            path = path + [start]

        else:
            try:
                possible_successors = [
                    a
                    for a in list(artnet[start])
                    if a and a not in alb_metrics + sound_metrics + ["avg_sonics"]
                ]
            except:
                start = artist_set[rd.randint(0, len(artist_set))]
                possible_successors = [
                    a
                    for a in list(artnet[start])
                    if a and a not in alb_metrics + sound_metrics + ["avg_sonics"]
                ]

            if len(possible_successors) > 0:
                if matchtype == "top":
                    start = possible_successors[0]
                else:
                    start = rd.choice(possible_successors)

                if start not in path:
                    path.append(start)
                else:
                    start = rd.choice(possible_successors)
                    path.append(start)
            else:
                break

    return path


def bfk(graph, node, metrics, mweights, dist_thresh, rand, k):  # function for BFS

    path = []  # List for visited nodes.
    queue = []  # Initialize a queue

    path.append(node)
    queue.append(node)

    while queue:  # Creating loop to visit each node
        m = queue.pop(0)
        for nb in graph[m]:
            if nb not in path and "avg_" not in nb:
                if metrics:
                    dt = kt.getNNdist(graph, node, nb, metrics, mweights)
                else:
                    dt = 0.001
                if dt <= dist_thresh or np.isnan(dt):
                    path.append(nb)
                    queue.append(nb)
                else:
                    next
    if rand:
        return rd.choices(path, k=k)
    else:
        return path[0 : k + 1]
