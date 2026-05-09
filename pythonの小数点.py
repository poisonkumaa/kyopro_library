from decimal import Decimal

print(0.1 + 0.2 == 0.3)  #False
print(Decimal(0.1) + Decimal(0.2) == Decimal(0.3))  #False
print(1 / 10 + 2 / 10 == 3 / 10) # False
print(Decimal(1) / Decimal(10) + Decimal(2) / Decimal(10) == Decimal(3) / Decimal(10))  #True