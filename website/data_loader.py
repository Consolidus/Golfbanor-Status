import os
import sqlite3

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Load the course data from CSV
sheet_url = "https://www.dropbox.com/s/q52kbxrqopp5sla/Golfbanor%20Status%20-%20Golfbanor%20Status.csv?dl=1"
df = pd.read_csv(sheet_url, engine="python", sep=",", quoting=1, quotechar='"')

"""
# Local SQLITE database
# Connect to database
conn = sqlite3.connect("website/golfcourse_database.db")
c = conn.cursor()
"""

db = create_engine(os.environ.get("DATABASE_FIXED_URL", None))
conn = db.connect()


# Create column names
headers = [
    "course_name",
    "course_region",
    "course_country",
    "course_status",
    "from_date",
    "to_date",
    "undantag",
    "competition",
    "last_update",
    "updated_by",
    "info_source",
    "facebook_url",
    "website_url",
    "booking_system",
    "coordinates",
    "google_maps_url",
]

# Insert country column
df.insert(2, "course_country", "Sverige")

# Update column names
df.columns = headers

# Drop top empty row
df.drop(0, inplace=True)

# Drop date columns
# TODO: FIX PROBLEM WITH SAVING THE DATES TO THE DATABASE
df.drop(["from_date", "to_date", "last_update"], axis=1, inplace=True)

# Drop duplicate courses
df.drop_duplicates("course_name", inplace=True)


# print(df.head())
# print(df.info())
# print(df["course_name"].value_counts())


# Save dataframe to database
df.to_sql("golfcourse", conn, if_exists="append", index=False)
print("Bandata överförd till databas.")
