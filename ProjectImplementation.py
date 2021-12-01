# 1. PROGRAM METADATA ###################################

# Horizontal Closed Traverse Survey Calculator
# Created by: Justin Brassard, Bharat Bharat, Jon Marlo Delicano 
# For: Project Implementation
# Date: December 7, 2021
# Program function: 
# Assumes:
# Inputs entered with keyboard
# Outputs displayed on screen

# Structure of implementation follows the algorithm

# 2. FUNCTION DEFINITIONS AND IMPORTS ##################################

import math

# Function to convert String Reference Bearing in DMS to azimuth in decimal degrees.

dms="N78d18'59\"W" # needs to except this format only. 11 characters in length (ie. index 0 - 10).

def RefBToAzmDD(bearingStr):

    if bearingStr[0].upper()=="N":
            VertDir = "N"
    elif bearingStr[0].upper()=="S":
            VertDir = "N"

    if bearingStr[-1].upper()=="W":
            HorDir = "W"
    elif bearingStr[-1].upper()=="E":
            HorDir = "E"

    # Extracts the DMS values from bearing string
    num1=float(bearingStr[1:3]) # extracts degrees
    num2=float(bearingStr[4:6]) # extracts minutes
    num3=float(bearingStr[7:9]) # extracts seconds
    # print(num1, num2, num3)

    # Selection structure to allocate quadrant azimuth is in.
    if (VertDir == "N") and (HorDir == "W"):
            AZMdd=360-(num1+(num2+(num3/60))/60)
    elif (VertDir == "N") and (HorDir == "E"):
            AZMdd=(num1+(num2+(num3/60))/60)
    elif (VertDir == "S") and (HorDir == "W"):
            AZMdd=180+(num1+(num2+(num3/60))/60)
    elif (VertDir == "S") and (HorDir == "E"):
            AZMdd=180-(num1+(num2+(num3/60))/60)

    return AZMdd

# DMStoDD function, for internal angles if specified input format is DMS

dms="78d18'59\"" # needs to except this format only. 9 characters in length (ie index 0 - 8)

def DMStoDD(DMSangle):

    num1=float(DMSangle[0:2]) # extracts degrees
    num2=float(DMSangle[3:5]) # extracts minutes
    num3=float(DMSangle[6:8]) # extracts seconds
    dd=(num1+(num2+(num3/60))/60)

    return dd

print(DMStoDD(dms))

# Azimuth Finder function, returns azimuth in decimal degrees

def azmcalc(CalcDir, BearingBefore, intAngle):

    if CalcDir == "CC":
            BearingNext = BearingBefore - (180 - intAngle)

    elif CalcDir == "C":
            BearingNext = BearingBefore + (180 - intAngle)

    if BearingNext > 360:
            BearingNext = BearingNext - 360
    elif BearingNext < 0:
            BearingNext = BearingNext + 360

    return BearingNext

# Latitude function

def LatCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeLat=math.cos(azmth_rad)*travL
    return changeLat

# Departure function

def LatCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeDep=math.sin(azmth_rad)*travL
    return changeDep

# Function to convert Azimuth in decimal degrees to Bearing in DMS; returns string in DMS format

def ddtoDMS(dd):

    if dd >= 0 and dd < 90:
        min,sec_ = divmod(dd*3600,60)
        deg,min = divmod(min, 60)
        sec = round(sec_,0)
        bearing = "N"+str(int(deg))+"d"+str(int(min))+"'"+str(int(sec))+"\""+"E"

    elif dd >= 90 and dd < 180:
        min,sec_ = divmod((180-dd)*3600,60)
        deg,min = divmod(min, 60)
        sec = round(sec_,0)
        bearing = "S"+str(int(deg))+"d"+str(int(min))+"'"+str(int(sec))+"\""+"E"

    elif dd >= 180 and dd < 270:
        min,sec_ = divmod((dd-180)*3600,60)
        deg,min = divmod(min, 60)
        sec = round(sec_,0)
        bearing = "S"+str(int(deg))+"d"+str(int(min))+"'"+str(int(sec))+"\""+"W"

    elif dd >= 270 and dd < 360:
        min,sec_ = divmod((360-dd)*3600,60)
        deg,min = divmod(min, 60)
        sec = round(sec_,0)
        bearing = "N"+str(int(deg))+"d"+str(int(min))+"'"+str(int(sec))+"\""+"W"

    return bearing

# 3. MAIN FUNCTION ##################################

# 3.0 PROGRAM STATEMENTS

# 3.1 INPUT LOOP 

# 3.2 MAIN PROCESSING

# i. Angle of Misclosure and Balancing -----------------

# ii. Bearings and Azimuths ------------------ 

# iii. Latitudes and Longitudes -----------------------

# iv. Draw traverse with Turtle graphics ------------------

# v. Error of Closure and Precision Ratio --------------------

# 3.3  OUTPUT LOOP 