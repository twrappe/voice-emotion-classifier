sleep = input("How many hours of sleep did you get last night?\n")
stress = input("How stressed are you on a scale of 1 to 20?\n")
substance = input("How much alcohol did you drink on a scale of 1 to 20?\n")
result = (.2 + float(stress)/10*.2 + float(substance)/10*.4 + (abs(float(sleep)-8))*.2)
print(result)