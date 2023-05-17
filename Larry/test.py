file = open("swerve_angles.txt")
lines = file.readlines()
m1 = lines[0]
print(m1.split(":")[1])
m1 = m1.split(":")[1]
print(str(m1))
file.close()