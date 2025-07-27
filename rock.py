import random
import sqlite3
from datetime import datetime

# Connect to SQLite database (or create one)
conn = sqlite3.connect("rps_game.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS game_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_choice TEXT,
    computer_choice TEXT,
    result TEXT,
    timestamp TEXT
)
""")
conn.commit()

# Stats counters
user_wins = 0
computer_wins = 0
draws = 0
total_games = 0

print('Winning rules of the game ROCK PAPER SCISSORS are:\n'
      + "Rock vs Paper -> Paper wins \n"
      + "Rock vs Scissors -> Rock wins \n"
      + "Paper vs Scissors -> Scissors wins \n")

choices = {1: 'Rock', 2: 'Paper', 3: 'Scissors'}

while True:
    print("\nEnter your choice \n 1 - Rock \n 2 - Paper \n 3 - Scissors")
    try:
        choice = int(input("Your choice: "))
        if choice not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid input! Please enter 1, 2, or 3.")
        continue

    user_choice = choices[choice]
    print("User choice is:", user_choice)

    comp_choice_num = random.randint(1, 3)
    computer_choice = choices[comp_choice_num]
    print("Computer choice is:", computer_choice)

    print(user_choice, "vs", computer_choice)

    # Determine result
    if user_choice == computer_choice:
        result = "Draw"
        draws += 1
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "User Wins"
        user_wins += 1
    else:
        result = "Computer Wins"
        computer_wins += 1

    total_games += 1
    print(f"<== {result}! ==>")

    # Save result in DB
    cursor.execute("""
        INSERT INTO game_results (player_choice, computer_choice, result, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_choice, computer_choice, result, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    # Play again?
    ans = input("Do you want to play again? (Y/N): ").lower()
    if ans == 'n':
        break

# Print summary
print("\n==== Game Summary ====")
print(f"Total games played: {total_games}")
print(f"User wins: {user_wins}")
print(f"Computer wins: {computer_wins}")
print(f"Draws: {draws}")

# Optionally: Show game history
show_history = input("Do you want to see the game history from the database? (Y/N): ").lower()
if show_history == 'y':
    print("\n--- Game History ---")
    for row in cursor.execute("SELECT * FROM game_results ORDER BY id DESC"):
        print(f"[{row[4]}] You: {row[1]} | Computer: {row[2]} => {row[3]}")

# Close DB connection
conn.close()
print("Thanks for playing!")
