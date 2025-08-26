import random

def guess_the_number():
    """
    A simple 'Guess the Number' game.
    The computer picks a number between 1 and 100, and the user tries to guess it.
    """
    secret_number = random.randint(1, 100) # Generate a random number between 1 and 100
    attempts = 0
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")

    while True: # Loop indefinitely until the user guesses correctly
        try:
            guess = int(input("Take a guess: ")) # Get user input and convert to integer
            attempts += 1

            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts!")
                break # Exit the loop if the guess is correct
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except KeyboardInterrupt:
            print("\nExiting game. Thanks for playing!")
            break

# This ensures guess_the_number() is called only when the script is executed directly
if __name__ == "__main__":
    guess_the_number()