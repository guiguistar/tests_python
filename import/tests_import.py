import importlib

def f():
    import time

"""
f()
t = time.clock() # Lève une exception de type NameError
"""

def g():
    import time
    t = time.clock() # Fonctionne

g()

import module1
print(module1.a) # 10

import module2
print(module2.a) # 20

from module1 import *
print(a) # 10

from module2 import *
print(a) # 20

import module1
print(dir(module1)) # ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a']
print(dir()) # ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'f', 'g', 'importlib', 'module1', 'module2']
print(module1.__name__) # module1

mod1 = importlib.import_module('module1')
print(dir(mod1)) # ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a']
print(mod1.__name__) # module1

import a.sous_module1 # Fonctionne
print(a.sous_module1.aa) # 100

import b.sous_module2
print(b.sous_module2.aa) # 200

"""
sMod1 = importlib.import_module('sous_module1','a') # ImportError
"""

sMod1 = importlib.import_module('a.sous_module1','a') # Fonctionne

"""
sMod1 = importlib.import_module('..sous_module1','a') # Value Error .. est le dossier parent
"""

"""
sMod1 = importlib.import_module('..sous_module1') # TypeError (le second (package) paramètre est requis)
"""

sMod1 = importlib.import_module('.sous_module1','a') # Fonctionne
print(dir(sMod1)) # ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'aa']
print(sMod1.__loader__) # <_frozen_importlib_external.SourceFileLoader object at 0x7fca040b7780>
