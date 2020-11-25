import os

print (os.environ['HOME'])
print (os.path.expandvars('$HOME/Wallper'))
print (os.path.expanduser('~/Wallper'))