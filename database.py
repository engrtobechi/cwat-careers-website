import sqlite3

# Open connnection to the db
connection = sqlite3.connect('database.db')


# Open the SQL schema file and read
with open('schema.sql') as f:

    # Execute the SQL Statments in the schema file read
    connection.executescript(f.read())

# Create a Cursor object that allows you to process rows in a database
cur = connection.cursor()

# Using the execute function of the Cursor object insert the following jobs into the jobs table
cur.execute("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) VALUES (?, ?, ?, ?, ?, ?)",
            ('Electronics Engineer - Entry Level', 'Enugu, Nigeria', 150000, "NGN", "Designing and testing electronic circuits, components, and systems.", "A bachelor's degree in electrical engineering or a related field.")
            )

connection.commit()
connection.close()