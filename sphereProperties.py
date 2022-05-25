import math

radius = float(input("Enter the radius: "))

diameter = radius * 2
print("Diameter is %.2f" % diameter)

circumference = 2 * math.pi * radius
print("Circumference is %.2f" % circumference)

sa = 4 * math.pi * math.pi**2
print("Surface area is %.2f" % sa)

volume = (4/3) * math.pi * radius**3
print("Volume is %.2f" % volume)
