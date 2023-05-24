from MOTLBO import *

NAME_FOLDER = "nsf_uniform_1"
REQUEST = 10

N_POP = 100
GEN = 1000
NUM_REMOVE = 20

motlbo = MOTLBO(N_POP, GEN, NUM_REMOVE, NAME_FOLDER, REQUEST)
motlbo.run()
