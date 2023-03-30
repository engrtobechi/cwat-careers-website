-- The following SQL statement drops or deletes a table called jobs if it exists
DROP TABLE IF EXISTS jobs;

-- The following SQL statements creates two new tables called jobs and applications
CREATE TABLE "jobs" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(250) NOT NULL,
	"location"	VARCHAR(250) NOT NULL,
	"salary"	INT,
	"currency"	VARCHAR(10),
	"responsibilities"	VARCHAR(2000),
	"requirements"	VARCHAR(2000),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "applications" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"job_id" INTEGER NOT NULL,
	"first_name" TEXT NOT NULL,
	"last_name" TEXT NOT NULL,
	"email" TEXT NOT NULL,
	"linkedin_url" TEXT,
	"education" TEXT,
	"work_experience" TEXT,
	"resume_url" TEXT NOT NULL,
	"status" TEXT NOT NULL DEFAULT 'Pending',
	"date_created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(job_id) REFERENCES jobs(id)
);

CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY,
    "username" TEXT UNIQUE,
    "password" TEXT,
    "email" TEXT UNIQUE,
    "joined_at" INTEGER
);