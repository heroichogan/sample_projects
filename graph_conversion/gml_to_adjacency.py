#!/usr/bin/env python
import networkx
import networkx.paths
import re
import random


class DuplicateNodeException( KeyError ):    #<<<<< RIGHT ERROR TO USE?
    def __init__( self, arg ):
        KeyError.__init__(self, arg)
        
        
class CycleException( KeyError ):    #<<<<< USE A DIFFERENT PARENT EXCEPTION!
    def __init__( self, arg ):
        KeyError.__init__(self, arg)        
        

class RandomizingDiGraph( networkx.DiGraph ):
    """Randomization of successors.  Intended to randomize the "don't care" parts of
    topologically sorted node sequence.  SAFE FOR OTHER METHODS?"""
    
    def successors(self, v, with_labels=False):
        """Return sucessor nodes of v."""
        if with_labels:
            try:
                x = self.succ[v].copy()
                random.shuffle(x)
                return x                
            except KeyError:
                raise NetworkXError, "node %s not in graph"%v
        else:
            x = list(self.successors_iter(v))
            random.shuffle(x)
            return x



# Open file, read file into one string, and close file
f = open( 'schedule_daily.gml' )
data = f.read()
f.close() 

# Create graph
g = RandomizingDiGraph()


# Add nodes and node labels
r = re.compile(r'id\t(\d+)\n\t\tlabel\t"(.+)"')
names = {}
for x in r.findall(data):
    #...first check for errors in the graph
    if g.has_node(x[1]):
        raise DuplicateNodeException(x[1])
    
    #...then do the add
    g.add_node(x[1])    
    names[x[0]] = x[1] 


# Add edges
r = re.compile(r'source\t(\d+)\n\t\ttarget\t(\d+)')
for x in r.findall(data):
    #...add the edge
    g.add_edge( names[x[0]], names[x[1]] )
    ts = networkx.paths.topological_sort(g)
    
    #...then check for errors in the graph
    if not ts:
        print '%s -> %s broke it\n' % (names[x[0]], names[x[1]])
        raise CycleException(x[0])
    
    
# Sort topologically
ts = networkx.paths.topological_sort(g)


# Print to stdout
print '<html>'
for x in ts:
    if x.endswith('pm') or x.endswith('am'):
        print '<b>[ ] %s</b><br/>' % x
    else:
        print '[ ] %s<br/>' % x
print '</html>'