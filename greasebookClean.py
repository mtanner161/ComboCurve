# Cleaning custom daily allocation reports from Greasebook
# Developed by Michael Tanner

# import required packages
import os
import json
import pandas as pd
import numpy as np
import re
import smtplib

# get raw CSV download from working direcotry
rawProduction = pd.read_excel(
    r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Clients\King Operating\Finance - Reservoir\Daily Production Data\1.11.2022greasebook.xlsx"
)

# setting the headers
rawProduction = rawProduction.iloc[1:, :]
rawProduction.columns = rawProduction.iloc[0]
rawProduction = rawProduction[1:]

# opening a file pointer and setting to write mode
fp = open(r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kellyAssets.csv", "w")

# set the header values
headerString = (
    "Date," + "Lease," + "Field," + "Well Name," + "Oil," + "Gas," + "Water\n"
)

# write the header
fp.write(headerString)

# clean the "Lease" colmun so it spilts into Lease, Field and Well Name
for i in range(0, len(rawProduction)):
    row = rawProduction.iloc[i]
    leaseName = row["Lease"]
    if row["Date"] == "Totals":
        break
    splitString = re.split("-|–", leaseName)
    if len(splitString) == 3:
        outputString = (
            row["Date"]
            + ","
            + splitString[0]
            + ","
            + splitString[1]
            + ","
            + splitString[2]
            + ","
            + row["Oil"]
            + ","
            + row["Gas"]
            + ","
            + row["Water produced"]
            + "\n"
        )
    else:
        outputString = (
            row["Date"]
            + ","
            + splitString[0]
            + ","
            + splitString[1]
            + ","
            + "No Well Name"
            + ","
            + row["Oil"]
            + ","
            + row["Gas"]
            + ","
            + row["Water produced"]
            + "\n"
        )
    # replace with Pretty Area Names
    outputString = outputString.replace("Peak", "East Texas")
    outputString = outputString.replace("CWS", "South Texas")
    outputString = outputString.replace("Otex", "Gulf Coast")

    # write the string
    fp.write(outputString)

fp.close()

cleanKellyAsset = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kellyAssets.csv"
)

todayDate = "1/11/2022"
oilSum = 0
gasSum = 0

for i in range(0, len(cleanKellyAsset)):
    if cleanKellyAsset.iloc[i, 0] == todayDate:
        gasSum = gasSum + float(cleanKellyAsset.iloc[i, 5])
        oilSum = oilSum + float(cleanKellyAsset.iloc[i, 4])
    else:
        continue


print(oilSum)
print(gasSum)

dashboardLink = "https://app.powerbi.com/view?r=eyJrIjoiM2U5OTYxOWYtOTEyMS00M2YxLWE0NTktMDFjZjcwNzlmMjg3IiwidCI6IjA1MTM5NTUzLWVlOTAtNDdhZi1iNmY3LTU0ZDk2OTc4ZTQ5ZSJ9&pageName=ReportSectionb8f3ed9f3c4313759775"


from mailer import Mailer

mail = Mailer(email="operations.king@gmail.com", password="Bigshow1637%")

mail.send(
    receiver="mtanner@kingoperating.com, kduncan@kingoperating.com, pgerome@kingoperating.com",
    subject="Daily Production Report: 1/11/2021 - ETX, STX and Gulf Coast",
    message="Today's oil production: "
    + str(oilSum)
    + " bbl. \n\n"
    + "Daily gas production: "
    + str(gasSum)
    + " mcf. \n\nView the Dashboard here: "
    + dashboardLink,
)


print("done")
