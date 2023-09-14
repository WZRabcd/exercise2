import sqlite3

# Read the file and copy its content to a list
with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = [line.strip().split(", ") for line in file]

# Connect to the SQLite database
conn = sqlite3.connect("stephen_king_adaptations.db")
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
    movieID INTEGER PRIMARY KEY,
    movieName TEXT,
    movieYear INTEGER,
    imdbRating REAL
)
""")

# Insert the content of the list into the table
for adaptation in stephen_king_adaptations_list:
    cursor.execute("INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)", adaptation)

conn.commit()

# Function to search for a movie by name
def search_movie_by_name(name):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (name,))
    return cursor.fetchone()

# Function to search for movies by year
def search_movies_by_year(year):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year,))
    return cursor.fetchall()

# Function to search for movies by rating
def search_movies_by_rating(rating):
    cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
    return cursor.fetchall()

# Loop for user interaction
while True:
    print("\nSearch Options:")
    print("1. Movie name")
    print("2. Movie year")
    print("3. Movie rating")
    print("4. STOP")

    choice = input("Enter your choice: ")

    if choice == "1":
        movie_name = input("Enter the movie name: ")
        result = search_movie_by_name(movie_name)
        if result:
            print(f"Movie Name: {result[1]}, Movie Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No such movie exists in our database")
    elif choice == "2":
        movie_year = int(input("Enter the movie year: "))
        results = search_movies_by_year(movie_year)
        if results:
            for result in results:
                print(f"Movie Name: {result[1]}, Movie Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No movies were found for that year in our database.")
    elif choice == "3":
        movie_rating = float(input("Enter the movie rating: "))
        results = search_movies_by_rating(movie_rating)
        if results:
            for result in results:
                print(f"Movie Name: {result[1]}, Movie Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No movies at or above that rating were found in the database.")
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()