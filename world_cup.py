# Assignment 3: Real world application of loop control statements

countries = ["Brazil", "Argentina", "France", "Germany", "Spain", "Uganda"]
winner = "Brazil"

count = 0
while True:
    guess = input("Guess the country that will win World Cup 2026 (or 'quit' to stop): ")

    if guess == "quit":
        print("Goodbye!")
        break

    if guess not in countries:
        print("Invalid country, try again.")
        continue

    count = count + 1
    print("Attempt number:", count)

    if guess == winner:
        print(guess, "wins the World Cup 2026!")
        break
    elif guess in ["Spain", "Uganda"]:
        print("Skipping this guess (pass).")
        pass
    else:
        print(guess, "did not win. Try again.")