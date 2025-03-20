import logging
from sys import argv
logging.basicConfig(level=logging.INFO)

# logging.info("Starting day6.py")
# AAA)BBB, which means "BBB is in orbit around AAA".

def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().splitlines()
    return list(map(lambda x: x.split(')'),rawdata))
orbit_list = get_data("./data/day6.txt")

class CelestialBody:
    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = [] if children is None else children
        self.orbit_count = 0

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
    
mystack = [v for k,v in celestial_bodies.items() if v.parent==None]

part1=0
iterations=0
while mystack:
    body = mystack.pop()
    logging.debug(f"iterations: {iterations}, part1: {part1}, mystack: {len(mystack)}")
    logging.debug(f'body:{body.name}, children{[c.name for c in body.children]}')
    mystack.extend(body.children)
    if body.parent != None:
        body.orbit_count = body.parent.orbit_count + 1
        part1+=body.orbit_count
    iterations+=1
logging.info(f'part1: {part1}')
