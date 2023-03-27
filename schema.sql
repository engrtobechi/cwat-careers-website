-- The following SQL statement drops or deletes a table called posts if it exists
DROP TABLE IF EXISTS jobs;

-- The following SQL statement creates a new table called posts
CREATE TABLE jobs (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(250) NOT NULL,
    location VARCHAR(250) NOT NULL,
	salary INT,
	currency VARCHAR(10),
	responsibilities VARCHAR(2000),
	requirements VARCHAR(2000)
);