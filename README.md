# log4om_potaupdate
Update the POTA award database for log4om using data from the POTA website's CSV export file

# Limitations
* Only adds parks, doesn't remove or update
* Makes a educated guess on the database file location
* Doesn't do extensive DXCC code checks
* Doesn't deal with the Active flag

# Requirements
Install python3.x from the Microsoft store, or from python.org

# Usage
Back up your Activations.SQLite file first, then run "python log4om_potaupdate.py"
