# python 3.5 sostituisce input(stringa) con eval(input(stringa))
latoA = input("inserisci latoA ")
print(type(eval(latoA)))
latoA = int(eval(latoA))
latoB = int(eval(input('inserisci latoB ')))
print(type(latoB))
area = latoA * latoB
print(area)
