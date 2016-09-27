Real survey instruments have a lot of branch and data handling logic that is EXTREMELY tedious to develop through a GUI (in fact, it's unavailable in many tools). So I wanted to see what it would take to write a survey engine in Python. I think this is the right approach: you use a subclass to implement banch logic and scoring. (This proof-of-concept is for a single user and does not separate out the data). 

Tools used: CherryPy, Python
