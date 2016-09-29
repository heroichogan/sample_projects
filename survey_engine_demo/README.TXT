Real survey instruments have a lot of branch and data handling logic that is EXTREMELY tedious to develop through a GUI (in fact, it's unavailable in many tools). So I wanted to see what it would take to write a survey engine in Python. I think this is the right approach, since Python is so readable and so strong in string and data structures. 

In the example, I provide a base class that does all the networking boilerplate and delegate the individual survey logic and scoring to each survey instrument subclass. This division of labor makes writing complex surveys easy for anyone who is willing to learn basic Python syntax, which is well within the capabilities of the survey specialists I have known.

This proof-of-concept is for a single user and does not separate out the data. 

Tools used: CherryPy, Python
