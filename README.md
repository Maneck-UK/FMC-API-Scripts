# FMC-API-Scripts
Cisco Firepower Manager API Python Scripts

This repository contains scripts written in python that interact with the Cisco Firepower Manager (FMC) API to do stuff.
I have recieved help from both collegues and the Cisco community which assisted me in gaining the the knowledge required to write these scripts.
Thanks to you all.
In the same spirit as shown in all the help I have received; I am making the scripts available for anyone to use.
I have used these scripts on a production environment, firstly on FMC 6.4.x and then of 6.5.x. So they work as I intended, this may not always be ideal.
Please test them before they are used on another FMC environment, especially if it is a production environment.

Use of these scripts is entirely at your own risk.

post-csv-hosts-070620.py
creates network host objects for use in FMC policies via API POST operation
set up to call csv filneame during script input py post-csv-hosts-070620.py <hosts2post>.csv
find sample csv file post2hosts.csv

get-hosts-for-csv-070620.py
collects all network host objects in FMC via API GET operation
option 1 places the data in a text file, the GET collects the Object ID which is required to delete an object. 

delete-hosts-from-csv-070620.py
after removing hosts you do not want to delete from the GEThosts file and changing the file to a CSV file.
the delete hosts script will delete all the host objects in the csv from FMC via API DELETE operation
