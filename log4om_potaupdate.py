# A script to update the the POTA park list in the Log4OM2 sqlite database.  At
# the moment, it will only add new entires.  Removing old, and updating
# existing hasn't been implemented yet.

import csv, sqlite3, requests, os
from io import StringIO

def read_csv_from_web():
    # Download and parse the all_parks.csv file from the pota website, returns a list.
    try:
        # Get the updated POTA CSV file
        r = requests.get('https://pota.us/all_parks.csv')
    except:
        print("Failed to fetch all_park.csv from POTA website")

    # Setup StringIO object (csv module expects a file, not a string)
    f = StringIO(r.text)

    # Build the CSV reader
    csvreader = csv.reader(f)

    # Read the data into a list
    data = list(csvreader)

    # Return the data to the calling function
    return data


def read_csv_from_file():
    # Read and return the contents of the pota CSV file
    # This is useful in debugging, so you don't have to re-download the file
    # over and over during testing.
    
    # Open the file
    with open(r'C:\Users\ianbo\Downloads\pota\all_parks.csv', 'r') as csvfile:
        # Load the contents of the file into 'data' variable
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    # Return the contents of data to the calling function
    return data

def update_db(potadata):
    # Update the log4om database from the potadata table
    # At the moment, I only add missing data

    # Guess the database location path
    dbpath = os.environ.get('APPDATA') + '\\Log4OM2\\Activations.SQLite'
    # Open the database file
    try:
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
    except:
        print("Unable to open database.")
    
    add_count = 0
    existing_count = 0

    # Build the query variable
    insertcmd = """insert into AwardReferences(AwardCode, ReferenceCode, ValidFrom, ValidTo, ReferenceDescription, AllowedDXCC, Valid)
        values('POTA', ?, '19000101', '99981231', ?, ?, 1);"""

    # Loop through our list of updates, check for an existing reference
    for park in potadata:
        # Grab this park's data from the databse if it exists
        cursor.execute("select * from AwardReferences where AwardCode = 'POTA' and ReferenceCode = '%s';" % park[0])
        result = cursor.fetchall()
        
        if len(result) == 0:
            # Park doesn't seem to be in the DB
            print("Park %s is missing from the database, adding" % park[0])
            add_count = add_count + 1
            # Add missing data
            # Build the data variable
            insertdata = (park[0], park[1], "#" + park[3] + "#")

            cursor.execute(insertcmd, insertdata)
            conn.commit()
        else:
            print("Park %s already in the database" % park[0])
            existing_count = existing_count + 1
    
    # Summary
    print("%s parks added, %s parks already existed." % (add_count, existing_count))


if __name__ == "__main__":
    # Call the function to read the CSV data
    # potadata = read_csv_from_file()
    potadata = read_csv_from_web()

    # Check the first line to see if the data looks valid
    if potadata.pop(0) == ['reference', 'name', 'active', 'entityId', 'locationDesc']:
        # Data looks good, update the data
        update_db(potadata)
    else:
        # CSV data doesn't match expected results, return an error
        raise ValueError
    
