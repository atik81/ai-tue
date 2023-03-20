import math
from collections import deque
from queue import PriorityQueue
import heapq
from queue import heappush
from queue import heappop
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
def euclidean_distance(coord1, coord2):
    return math.dist(coord1, coord2)
def astar(distances, start, end):
    # Create a priority queue for A*
    queue = PriorityQueue()
    
    # Set to keep track of visited cities
    visited = set()
    
    # Initialize the start city
    queue.put((0, start, [start]))
    
    while not queue.empty():
        # Dequeue a city and its path
        _, city, path = queue.get()
        
        # Check if the city has been visited before
        if city in visited:
            continue
        
        # Mark the city as visited
        visited.add(city)
        
        # Check if the current city is the end city
        if city == end:
            cost = sum(distances[path[i]][path[i+1]] for i in range(len(path)-1))

            return path, cost
        
        # Enqueue all unvisited cities adjacent to the current city
        for neighbor, cost in distances[city].items():
            if neighbor not in visited:
                # Calculate the heuristic cost to the neighbor city
                heuristic = math.dist(city_coordinates[neighbor], city_coordinates[end])
                total_cost = cost + heuristic
                
                # Add the neighbor city to the priority queue
                queue.put((total_cost, neighbor, path + [neighbor]))
    
    # No path exists between the start and end cities
    return None, None 


start = input("Enter start:")
end = input("Enter end point:")

# Validate the input
while start not in distances or end not in distances:
    print("Invalid input, please enter valid start and end points.")
    start = input("Enter start:")
    end = input("Enter end point:")
path, cost = astar(distances, start, end)

# Print the shortest path
if path:
    print("Path:", path)
    print("Total distance:", cost, 'miles')
else:
    print("No path exists between the start and end cities.")