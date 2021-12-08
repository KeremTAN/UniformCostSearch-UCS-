# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from collections import defaultdict
from queue import PriorityQueue

import pandas as pd


class CityNotFoundError(Exception):
    def __init__(self, city) -> object:
        print("%s does not exist" % city)


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    cities = pd.read_csv(path, encoding='utf-8')

    startCities = list((map(lambda city: city.replace('İ', 'I').replace('ı', 'i').upper(), cities["city1"])))
    destinationCities = list((map(lambda city: city.replace('İ', 'I').replace('ı', 'i').upper(), cities["city2"])))
    distances = list(cities["distance"])

    unStartCities = startCities + destinationCities
    unDestinationCities = destinationCities + startCities
    distances += distances
    unDirectedGraph = zip(unStartCities, unDestinationCities, distances)
    global distance
    distance = {}

    graphOfCities = defaultdict(list)
    for (x, y, z) in unDirectedGraph:
        graphOfCities[x].append(y)
        distance[(x, y)] = z

    chooseCities(path, graphOfCities)


# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    visited = set()
    path = list()
    queue = PriorityQueue()
    queue.put((0, start))

    while queue:
        cost, node = queue.get()
        # if node in path:
        #    path.remove(-1)
        # else:
        #    path.append(node)

        if node not in visited:
            visited.add(node)
            if node == end:
                # routeDisp = path[0]
                # for i in range(1, len(path)):
                #    routeDisp += " -> " + path[i]
                print(f"The minimum distance between {start} and {end} is {cost} km.")
                # print(f"The route to be followed between {start} and {end} \n{routeDisp}")
                return

            for neighbor in graph[node]:
                if neighbor not in visited:
                    total_cost = cost + distance[node, neighbor]
                    queue.put((total_cost, neighbor))
                    print(f"NODE: {node} NEIGHBOR: {neighbor} DISTANCE {distance[node, neighbor]}")


def chooseCities(path, graphOfCities):
    cities = pd.read_csv(path, encoding='utf-8')
    allCities = set(cities["city1"])
    allCities.update(cities["city2"])
    allCities = set(map(lambda city: city.replace('İ', 'I').replace('ı', 'i').upper(), allCities))
    print("ALL START CITIES %s" % allCities)
    while True:
        startCity = input("Please, enter your start city : ").replace('İ', 'I').replace('ı', 'i').upper()
        if allCities.__contains__(startCity):
            break
        else:
            CityNotFoundError(startCity)
    allCities.remove(startCity)
    print("ALL DESTINATION CITIES %s" % allCities)
    while True:
        destinationCity = input("Please, enter your destination city : ").replace('İ', 'I').replace('ı', 'i').upper()
        if allCities.__contains__(destinationCity):
            break
        else:
            CityNotFoundError(destinationCity)
    uniform_cost_search(graphOfCities, startCity, destinationCity)


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    print("WARNING! There is NOT case sensitive for ı, i, I and İ characters in our system.")
    try:
        build_graph("cities.csv")
    except FileNotFoundError:
        print("File path could not find!")
    except Exception:
        print("Unexpected error has been existed")
