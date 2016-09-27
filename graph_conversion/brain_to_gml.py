#!/usr/bin/env python
import xml.dom.minidom


# Ask for style 
treatAsDirected = int( raw_input('Treat as directed (1/0)? ') )
if not treatAsDirected in (1,0):
    print 'Invalid input.  Will treat graph as directed (which it is anyway).'
    treatAsDirected = 1


# Util function to clean up node data (required by yEd)
def cleanName(n):
    n1 = n.replace('"',"'")
    n1 = n1.replace('&','AND')   #<<<< WHY?
    return n1    


# Create dom object from file
document = xml.dom.minidom.parse( 'leafblaster.xml' )

# Iterate through nodes picking up their id, name, and child (etc.) ids
nameMap, edgeMap = {}, {}
thoughtElements = document.getElementsByTagName('thought')
for x in thoughtElements:
    id = int(x.attributes['id'].nodeValue)
    for y in x.childNodes:
        if y.nodeName == 'name':
            nameMap[id] = cleanName(y.firstChild.nodeValue)
        elif y.nodeName == 'relations':
            childList = []
            for z in y.childNodes:
                # <<< TODO: change link style according to link type
                if z.nodeName in ('child','parent','jump'):
                    childList.append( int(z.attributes['id'].nodeValue) )
            edgeMap[id] = childList



# Util function to remove one backlink (if present)
def removeBacklink(node, edgeMap):
    try:
        destList = edgeMap[node]
        #for x in destList:
        #    pass
    except KeyError:
        pass
    except ValueError:
        pass


# Filter backlinks if desired
if not treatAsDirected:
    nodesList = edgeMap.keys()
    for x in nodesList:
        removeBacklink(x, edgeMap)
    
  

# Format GML graph
s = 'graph\n[\n'
if treatAsDirected == 'y':
    s += '\tdirected\t1\n'
else:
    s += '\tdirected\t0\n'

# ...print nodes <<<< SORTED FOR DEBUG
nodeIdListSorted = nameMap.keys()  
nodeIdListSorted.sort()
for id in nodeIdListSorted:
    s += '\tnode\n'
    s += '\t[\n'
    s += '\t\tid\t%s\n' % id
    s += '\t\tlabel\t"%s"\n' % nameMap[id]
    s += '\t]\n'

# ...print edges <<<< SORTED FOR DEBUG
edgeIdListSorted = edgeMap.keys()
edgeIdListSorted.sort()
for id in edgeIdListSorted:
    targetList = edgeMap[id]
    for target in targetList:
        s += '\tedge\n'
        s += '\t[\n'
        s += '\t\tsource\t%s\n' % id
        s += '\t\ttarget\t%s\n' % target
        s += '\t]\n'

# ...close the graph declaration
s += ']'


# Save GML
f = file('out.gml','w')
f.write(s)
f.close()

# Bye
print 'Done.'