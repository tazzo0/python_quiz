import requests
import json
import sqlite3


url = "https://imdb-top-100-movies.p.rapidapi.com/"

headers = {
	"x-rapidapi-key": "a3134a3d1dmsh4f25fbc075929aap11ea28jsnb3277241ca39",
	"x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com"
}

res = requests.get(url, headers=headers)
data = res.json()


#  4 methods
status_code = res.status_code
headers = res.headers
text = res.text

print(status_code, headers, text)


# Write JSON to file
with open("movies.json", "w") as file:
    json.dump(data, file, indent=2)


# Get data from JSON
for i in data:
    print(i["title"] + "\n" + i["description"] + "\n")


# Create SQLite database
conn = sqlite3.connect("imdb_movies.sqlite3")
cursor = conn.cursor()

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              rank INTEGER,
              title VARCHAR(255),
              description TEXT
) """
)

insertable_data = []
for i in data:
    insertable_data.append((i["rank"], i["title"], i["description"]))

cursor.executemany(
    "INSERT INTO posts (rank, title, description) VALUES (?, ?, ?)", insertable_data
)
conn.commit()