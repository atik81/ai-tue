import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer() #  recognizer object

engine = pyttsx3.init() # for text-to-speech engine object

import math
from collections import deque
from queue import PriorityQueue
import heapq
from queue import heappush
from queue import heappop
from queue import Queue

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate -60)
    engine.say(text)
    engine.runAndWait()
# i collect distance and journey time from this link https://www.freemaptools.com/how-far-is-it-between.htm.
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
Journey_time = {
    'Manchester': {'Holyhead': 2.40 , 'Liverpool': .45, 'York': 1.37},
    'Holyhead': {'Manchester': 2.40, 'Carlisle': 4.59 },
    'Liverpool': {'Manchester': .45, 'Carlisle': 2.45, 'York': 2.15},
    'York': {'Manchester': 1.33, 'Liverpool':  2.13, 'Newcastle': 2.38, 'Carlisle': 2.35},
    'Carlisle': {'Holyhead': 4.59, 'Liverpool': 2.46, 'York': 2.35, 'Newcastle': 1.18, 'Glasgow': 2.48},
    'Newcastle': {'York': 2.37, 'Carlisle': 3.31, 'Edinburgh': 5.43},
    'Glasgow': {'Carlisle': 2.9, 'Oban': 2.9 , 'Edinburgh':  1.2},
    'Edinburgh': {'Newcastle': 2.18, 'Glasgow': 1.1, 'Oban': 2.42, 'Aberdeen': 2.42, 'Inverness': 2.31},
    'Oban': {'Glasgow': 2.9, 'Edinburgh': 2.44, 'Aberdeen': 3.52},
    'Aberdeen': {'Edinburgh': 2.41, 'Oban': 3.53, 'Inverness': 2.19},
    'Inverness': {'Edinburgh': 3.31, 'Aberdeen': 2.19},
}
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
def speak(text):
    engine.say(text)
    engine.runAndWait()


#(**********************************              def bef               **********************************************)

def bfs(distances,Journey_time,start_city, target_city): 
    q = Queue()     # Initialize a queue for BFS

    visited = set() # a set for visited cities

    q.put((start_city, 0, 0, [start_city]))     # starting city and its distance (0) and path (just the starting city) to the queue


    while not q.empty():     # Loop until the queue is empty

        current_city, current_distance,current_journey_time, current_path = q.get()         # this Dequeue the current city, its distance, and its path


        if current_city == target_city:         # If the current city is the target city, return the distance ,current_journey_time and path

            return current_path, current_distance,current_journey_time

        visited.add(current_city)         # it's Add the current city to the set of visited cities


        for neighbor_city, distance in distances[current_city].items():         # For each neighboring city of the current city
            Journey_time_to_neighbor = Journey_time[current_city][neighbor_city]
            if neighbor_city not in visited:            # If the neighboring city has not been visited yet

                q.put((neighbor_city, current_distance + distance,current_distance + Journey_time_to_neighbor,current_path + [neighbor_city]))

    return None, None, None     # If the target city cannot be reached from the starting city, return None

#(*******************************************              def dfs                          ******** **********************************************)

def dfs(distances, start_city, target_city, path=None, cost=0):
    if path is None:
        path = [start_city]

    if start_city == target_city:    # If the current city is the target city, return the cost ,current_journey_time and path
        return path, cost

    for city in distances[start_city]:
        if city not in path:
            new_cost = cost + distances[start_city][city]
            new_path, new_cost = dfs(distances, city, target_city, path + [city], new_cost)
            if new_path:
                return new_path, new_cost

    return None, None

#(*******************************************              def astar                        ******** **********************************************)

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

#(*******************************************              def dijkstra                        ******************************************************)

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




#(**************************************************Get the start and target ities from the user*****************************)
if __name__ == "__main__":
    while True:
        speak('Please enter your starting city')
        break
if __name__ == "__main__":
    
    while True:
       try:
           speak('Enter your start city please')
           with sr.Microphone() as mic:
            # adjust for ambient noise
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)           # i used this adjust for ambient noise
            audio = recognizer.listen(mic)         # it's listen for speech input
            start_city = recognizer.recognize_google(audio)   # i using Google Speech Recognition for recognize speech 
            start_city = start_city.title()            # capitalize  first letter of city

            print(f"Start city recognized: {start_city}")
            engine.say(f"Start city recognized: {start_city}")
            engine.runAndWait()
            break
       except sr.UnknownValueError:
           print("Could not recognize speech")


    
    while True:
        try:
            speak('Enter your destination city please')
            with sr.Microphone() as mic:
             recognizer.adjust_for_ambient_noise(mic, duration=0.2) # i used this adjust for ambient noise
             audio = recognizer.listen(mic) # it's listen for speech input
             target_city = recognizer.recognize_google(audio)  # i using Google Speech Recognition for recognize speech
             end_city = target_city.title() # capitalize  first letter of city
             print(f"End city recognized: {target_city}")
             engine.say(f"End city recognized: {target_city}")
             engine.runAndWait()
            break
        except sr.UnknownValueError:
           print("Could not recognize speech")



# Validate the input
while start_city not in distances or target_city not in distances:
        speak("Invalid input, please enter valid start and end points.")
        speak('Please enter your starting city')
        start_city = input("Enter start:")
        speak('Please enter your destination')
        target_city = input("Enter end point:")
 
speak("You can prefer to use any of this road , Have a safe journey")

# Find the shortest path using BFS
print("*******************************************     For BFS        ***************************")
 

path, cost, Journey_time= bfs(distances,Journey_time,start_city, target_city)
if path is not None:
    print("Path:", path )
    speak("your can follow this road with breadth first scerch algorithm : " + "->".join(path))
    
    print("Total distance:", cost, 'miles')
    print("total journey time:", Journey_time,"hours" )
    speak("Your total distance is " + str(cost) + " miles.")
    speak("Your total journey time is " + str(Journey_time) + " hours by car")

else:
    print("No path found.")
    speak("soryy i didn't find any road for you")

print("*******************************************     For DFS        ***************************")


path1, cost = dfs(distances, start_city, target_city)
if path is not None:
    speak("")
    print("Path1:", path1 )
    speak("your can follow this road with depth first scerch algorithm: " + "->".join(path1))
    
    print("Total distance:", cost, 'miles')
    speak("Your total distance is " + str(cost) + " miles.")
else:
    print("No path found.")

    
    
print("*******************************************     For Astar        ***************************")
path2, cost = astar(distances,start_city, target_city)

# Print the shortest path
if path2:
    print("Path2:", path2 )
    speak("your can follow this road with Astar algorithm: " + "->".join(path2))
    
    print("Total distance:", cost, 'miles')
    speak("Your total distance is " + str(cost) + " miles.")
else:
    print("No path exists between the start and end cities.")
print("*******************************************     For    dijkstra   ***************************")

path3, cost = dijkstra(distances, start_city, target_city)
if path3 is not None:
    print("Path3:", path3 )
    speak("your can follow this road with Dijkstar algorithm : " + "->".join(path3))
    
    print("Total distance:", cost, 'miles')
    speak("Your total distance is " + str(cost) + " miles.")
else:
    print("No path found.")

speak("thank your for your jouney")


