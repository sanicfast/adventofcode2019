import logging
from sys import argv
import heapq
import time
if argv[2] == 'debug':
    logging.basicConfig(level=logging.DEBUG)
else: 
    logging.basicConfig(level=logging.INFO)

# run this with the following command:
# python day6.py ./data/day6.txt info

def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().splitlines()
    return list(map(lambda x: x.split(')'),rawdata))

class CelestialBody:
    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = [] if children is None else children
        self.orbit_count = 0
        self.dist=-2 #starting at -2 because the initial orbit jump and last orbit jump are not counted
    def __lt__(self,other): # need this for the heapq comparison to work nicely
        return self.dist < other.dist
    def __eq__(self,other):
        return self.dist == other.dist

start = time.time()

orbit_list = get_data(argv[1])
celestial_bodies = {}   
for orbit in orbit_list:
    logging.debug(orbit)
    parent_name,child_name = orbit
    new_parent = parent_name not in celestial_bodies.keys()
    new_child = child_name not in celestial_bodies.keys()
    if new_parent: #parent does not exist. create it.
        parent = CelestialBody(parent_name)
        celestial_bodies[parent_name]=parent
    else: #parent already exists. load it.
        parent = celestial_bodies[parent_name]
    if new_child: #child does not exist. create it.
        child = CelestialBody(child_name,parent)
        celestial_bodies[child_name]=child
    else: #child already exists. load it.
        child = celestial_bodies[child_name]
        if child.parent != None:
            raise ValueError(f"Child already has a parent. {child.name} {child.parent.name} {parent.name}")
        child.parent = parent
    parent.children.append(child)
    
mystack = [v for v in celestial_bodies.values() if type(v.parent)==type(None)]

part1=0
iterations=0
while mystack:
    body = mystack.pop()
    logging.debug(f"iterations: {iterations}, part1: {part1}, mystack: {len(mystack)}")
    logging.debug(f'body:{body.name}, children{[c.name for c in body.children]}')
    mystack.extend(body.children)
    if type(body.parent) != type(None):
        body.orbit_count = body.parent.orbit_count + 1
        part1+=body.orbit_count
    iterations+=1
logging.info(f'part1: {part1}')

# doing dijkstra's algorithm. setting up our heap and list of visited spots.
mystack2 = [v for k,v in celestial_bodies.items() if k=='YOU']
heapq.heapify(mystack2)
visited =set()

while mystack2:
    current_body = heapq.heappop(mystack2) 
    if current_body.name == 'SAN': #check to see if we've found our destination
        logging.info(f'part2: {current_body.dist}')
        break
    if current_body.name in visited: #check to see if we've already visited this node
        continue
    visited.add(current_body.name) #if not, add it to our visited list
    if type(current_body.parent) != type(None):
        current_body.parent.dist = current_body.dist + 1
        heapq.heappush(mystack2,current_body.parent)
    for child in current_body.children:
        child.dist = current_body.dist + 1
        heapq.heappush(mystack2,child)

logging.info(f'Time: {round(time.time()-start,5)} seconds.')

# INFO:root:part1: 158090
# INFO:root:part2: 241
# Time: 0.02428 seconds.