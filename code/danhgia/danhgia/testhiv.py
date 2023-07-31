import pygmo as pg


pop = [[0, 0, 0]]
check = round(pg.hypervolume(pop).compute([1,1,1]) ,4 )

print(check)