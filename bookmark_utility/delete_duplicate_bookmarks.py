#!/usr/bin/env python
import re


# Open file, read file into one string, and close file
f = open( r'C:\Documents and Settings\Matt\Application Data\Opera\Opera\profile\opera6.adr' ) 
data = f.read()
f.close() 


# Find urls in bookmarks file
r = re.compile( r'#URL.*?URL=.+?://(.+?)\n', re.DOTALL )
names, duplicates = {}, []
for x in r.findall(data):
    if names.has_key(x):
        duplicates.append(x)
    names[x] = 1 



# Create new bookmarks file...
f = open( 'opera6_new.adr', 'w' )

# Write bookmark data
summary = {}
r = re.compile( r'#URL.*?NAME=(.*?)\n.*?URL=.+?://(.+?)\n', re.DOTALL ) 
pos = 0
m = r.search( data, pos )
while m:
    # Get the matches
    name, url = m.groups()
    
    # Scan
    if name.startswith( '==>' ):
        name = name[3:]
    
    # Write part before name, then write name; also build summary datta
    f.write( data[pos:m.start(1)] ) 
    if url in duplicates:
        # Indicate duplicate found
        f.write( '==>' )
        
        # Build summary data
        if summary.has_key(url):
            summary[url].append( name )
        else:
            summary[url] = [name] 

    f.write( name ) 
    
    # Write part between name and url, then write url
    f.write( data[m.end(1):m.start(2)] )
    f.write( url ) 
    
    # Write last part of match (past last group)
    f.write( data[m.end(2):m.end()] ) 
    
    # Look for next match
    pos = m.end()    
    m = r.search( data, pos )
    
# Write last part of file (past last match)
f.write( data[pos:len(data)] )

# Close the file
f.close()


# Write summary data
msg = '%s bookmarks (%s duplicates)' % (len(names), len(duplicates))
print msg
print '-' * len(msg)
print

# Write cross reference
urls = summary.keys()
urls.sort()
for x in urls:
    print '==>%s' % x
    for y in summary[x]:
        print '   %s' % y 
    print 
    


