bill    = float(input("Enter total bill amount: "))
people  = int(input("Enter number of people: "))

print("\nTip: [1] 10%  [2] 15%  [3] 20%  [4] Custom")
while True:
    choice = input("Choice (1-4): ")
    if choice == "1":
        tip = 10
        break
    elif choice == "2":
        tip = 15
        break
    elif choice == "3":
        tip = 20
        break
    elif choice == "4":
        tip = float(input("Enter custom tip %: "))
        break
    else:
        print("Enter 1, 2, 3, or 4.")

tip_amount = bill * (tip / 100)

total = bill + tip_amount

per_person = total / people

print("\n")
print(" BILL RECEIPT ")
print("\n")
print(f"Original bill: {bill:,}")
print(f"Tip ({tip}%): {tip_amount:,}")
print(f"Total bill: {total:,}")
print("\n")
print(f"People: {people}")
print(f"Each person pays: {per_person:,}")