import math
from collections import deque
from queue import PriorityQueue
import heapq
from queue import heappush
from queue import heappop
from queue import Queue



city_coordinates = {
    'Manchester': [53.5, -2.3],
    'Liverpool': [53.4, -2.99],
    'York': [54, -1.1],
    'Carlisle': [54.9, -2.9],
    'Newcastle': [55, -1.6],
    'Glasgow': [55.9, -4.3],
    'Edinburgh': [56, -3.2],
    'Oban': [56.4, -5.5],
    'Aberdeen': [57.2, -2.1],
    'Holyhead': [53.3, -4.6],
    'Inverness': [57.5, -4.2],
}
distances = {
    'Manchester': {'Holyhead': 119.8, 'Liverpool': 34, 'York': 57.5 },
    'Holyhead': {'Manchester': 120.5, 'Carlisle': 223 },
    'Liverpool': {'Manchester': 34.3, 'Carlisle': 123.7, 'York': 101.2},
    'York': {'Manchester': 72.5, 'Liverpool': 102.2 , 'Newcastle': 119.1, 'Carlisle': 116.7},
    'Carlisle': {'Holyhead': 223.3, 'Liverpool': 123.9, 'York': 116.7, 'Newcastle': 157.3, 'Glasgow': 96},
    'Newcastle': {'York': 117.2, 'Carlisle': 157.7, 'Edinburgh': 256.1},
    'Glasgow': {'Carlisle': 96.2, 'Oban': 97 , 'Edinburgh': 47 },
    'Edinburgh': {'Newcastle': 249.5, 'Glasgow': 46, 'Oban': 121.8, 'Aberdeen': 120.8, 'Inverness': 157.4},
    'Oban': {'Glasgow': 96.5, 'Edinburgh': 122.6, 'Aberdeen': 173.8 },
    'Aberdeen': {'Edinburgh': 120.7, 'Oban': 174, 'Inverness': 104.3},
    'Inverness': {'Edinburgh': 157.6, 'Aberdeen': 104.3},
}


def bfs(distances,start_city, target_city):
    # Initialize a queue for BFS and a set for visited cities
    q = Queue()
    visited = set()

    # Enqueue the starting city and its distance (0) and path (just the starting city) to the queue
    q.put((start_city, 0, [start_city]))

    # Loop until the queue is empty
    while not q.empty():
        # Dequeue the current city, its distance, and its path
        current_city, current_distance, current_path = q.get()

        # If the current city is the target city, return the distance and path
        if current_city == target_city:
            return current_path, current_distance,

        # Add the current city to the set of visited cities
        visited.add(current_city)

        # For each neighboring city of the current city
        for neighbor_city, distance in distances[current_city].items():
            # If the neighboring city has not been visited yet
            if neighbor_city not in visited:
                # Enqueue the neighboring city and its distance and path to the queue
                q.put((neighbor_city, current_distance + distance, current_path + [neighbor_city]))

    # If the target city cannot be reached from the starting city, return None
    return None, None

def dfs(distances, start_city, target_city, path=None, cost=0):
    if path is None:
        path = [start_city]

    if start_city == target_city:
        return path, cost

    for city in distances[start_city]:
        if city not in path:
            new_cost = cost + distances[start_city][city]
            new_path, new_cost = dfs(distances, city, target_city, path + [city], new_cost)
            if new_path:
                return new_path, new_cost

    return None, None


def astar(distances, start_city, target_city):
    # Create a priority queue for A*
    queue = PriorityQueue()
    
    # Set to keep track of visited cities
    visited = set()
    
    # Initialize the start city
    queue.put((0, start_city, [start_city]))
    
    while not queue.empty():
        # Dequeue a city and its path
        _, city, path = queue.get()
        
        # Check if the city has been visited before
        if city in visited:
            continue
        
        # Mark the city as visited
        visited.add(city)
        
        # Check if the current city is the end city
        if city == target_city:
            cost = sum(distances[path[i]][path[i+1]] for i in range(len(path)-1))

            return path, cost
        
        # Enqueue all unvisited cities adjacent to the current city
        for neighbor, cost in distances[city].items():
            if neighbor not in visited:
                # Calculate the heuristic cost to the neighbor city
                heuristic = math.dist(city_coordinates[neighbor], city_coordinates[target_city])
                total_cost = cost + heuristic
                
                # Add the neighbor city to the priority queue
                queue.put((total_cost, neighbor, path + [neighbor]))
    
    # No path exists between the start and end cities
    return None, None 


def dijkstra(distances, start_city, target_city):
    queue = [(0, start_city, [])]
    visited = set()

    while queue:
        (cost, current, path) = heapq.heappop(queue)

        if current in visited:
            continue

        path = path + [current]

        if current == target_city:
            return (path, cost)

        visited.add(current)

        for neighbor in distances[current]:
            if neighbor not in visited:
                total_cost = cost + distances[current][neighbor]
                heapq.heappush(queue, (total_cost, neighbor, path))

    return None, None




# Get the start and end cities from the user
start_city = input("Enter start:")
target_city= input("Enter end point:")

# Validate the input
while start_city not in distances or target_city not in distances:
    print("Invalid input, please enter valid start and end points.")
    start_city= input("Enter start:")
    target_city= input("Enter end point:")

# Find the shortest path using BFS
print("*******************************************     For BFS        ***************************")
 


path, cost = bfs(distances,start_city, target_city)
if path is not None:
    print("Path:", path )
    print("Total distance:", cost, 'miles')
else:
    print("No path found.")

print("*******************************************     For DFS        ***************************")
    
path, cost = dfs(distances, start_city, target_city)
if path is not None:
    print("Path:", path)
    print("Total distance:", cost, "miles")
else:
    print("No path found.")

    
    
print("*******************************************     For Astar        ***************************")
path, cost = astar(distances,start_city, target_city)

# Print the shortest path
if path:
    print("Path:", path)
    print("Total distance:", cost, 'miles')
else:
    print("No path exists between the start and end cities.")
print("*******************************************     For    dijkstra   ***************************")
path, cost = dijkstra(distances, start_city, target_city)
if path is not None:
    print("Path:", path)
    print("Total distance:", cost, 'miles')
else:
    print("No path found.")



