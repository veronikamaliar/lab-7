BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "expense_categories" (
	"category_id"	INTEGER NOT NULL,
	"category_name"	VARCHAR,
	PRIMARY KEY("category_id")
);
CREATE TABLE IF NOT EXISTS "expenses" (
	"expense_id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"category_id"	INTEGER,
	"amount"	FLOAT,
	"date_incurred"	DATE,
	PRIMARY KEY("expense_id"),
	FOREIGN KEY("category_id") REFERENCES "expense_categories"("category_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);
CREATE TABLE IF NOT EXISTS "income_sources" (
	"income_source_id"	INTEGER NOT NULL,
	"source_name"	VARCHAR,
	"description"	VARCHAR,
	PRIMARY KEY("income_source_id")
);
CREATE TABLE IF NOT EXISTS "incomes" (
	"income_id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"income_source_id"	INTEGER,
	"amount"	FLOAT,
	"date_received"	DATE,
	PRIMARY KEY("income_id"),
	FOREIGN KEY("income_source_id") REFERENCES "income_sources"("income_source_id"),
	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER NOT NULL,
	"first_name"	VARCHAR,
	"last_name"	VARCHAR,
	"email"	VARCHAR,
	"password"	VARCHAR,
	PRIMARY KEY("user_id")
);
INSERT INTO "expense_categories" VALUES (1,'Food');
INSERT INTO "expense_categories" VALUES (2,'Transport');
INSERT INTO "expenses" VALUES (1,1,1,200.0,'2024-12-01');
INSERT INTO "expenses" VALUES (2,2,2,50.0,'2024-12-01');
INSERT INTO "expenses" VALUES (3,1,NULL,100.0,'2024-12-01');
INSERT INTO "income_sources" VALUES (1,'Salary','Monthly salary from employer');
INSERT INTO "income_sources" VALUES (2,'Freelance','Freelance work income');
INSERT INTO "income_sources" VALUES (3,'Investment','Income from investments');
INSERT INTO "incomes" VALUES (1,1,1,1500.0,'2024-12-01');
INSERT INTO "incomes" VALUES (2,2,2,1200.0,'2024-12-01');
INSERT INTO "incomes" VALUES (3,1,3,800.0,'2024-12-01');
INSERT INTO "users" VALUES (1,'John','Smith','johnnn@gmail.com','123J45');
INSERT INTO "users" VALUES (2,'Ann','Mari','ann.mari@gmail.com','6A789');
COMMIT;
