import src.stanleyControl as sc

test = sc.stanleyController(1.0)
test.trajectory([0,0],[1,1])
print(test.closestPointError([0,1]))