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


# A function to define the angle of miscolsure using the sum of the angles and the sides stated

def AOM(sides,sum_angles):
        AOM = (sides - 2) * 180 - sum_angles
        return AOM


# A function to find the error of closure

def EC (Total_Lat, Total_Dep):
        EC = math.sqrt(Total_Lat**2 +Total_Dep**2)
        return EC


# A function to find the Percision Ratio

def PR (EC,Perimeter):
        PR = EC/Perimeter
        return PR



# 3. MAIN FUNCTION ##################################

# 3.0 PROGRAM STATEMENTS

print ("This program provides a proposed solution for Closed Traverse data processing, which serves to automate the calculation\n processes a surveyoror drafter would normally perform after the surveying" )
print ("Insert assumptions and simplifications/Instructions for the user (Disclaimer)")

# 3.1 INPUT LOOP 

    Angles_IN =  []       	           # create empty list for receiver angles
    Distances_IN = []                      # create empty list for distance to GZ

    # Obtain angle and distance for multiple locations from the user
    
Count = 1

    while True:
        angle_degrees = float(input("\tEnter the angle of the reciever in degrees: "))
        Angles_IN.append(angle_degrees)
    # Ask the user for the Internal Angle of the current station they are evaluating
        Internal_Angles = float(input("Please enter the internal angle for the current station: "))
    # Ask the user for the Traverse lengths of the current station they are evaluating
        Traverse_Lengths = float(input("Please enter the Traverse length for the current station: "))


        Distance_GZ_CALC =round(CalculateDistance(GZ_X,GZ_Y,R_X,R_Y),1)
        Distances_IN.append(Distance_GZ_CALC)

        print()
        end =str(input("Do you want to stop enetering values (Y/N)? "))
        print()
        if end.upper() == 'Y' :
            break

        Count = Count +1

# 3.2 MAIN PROCESSING

# i. Angle of Misclosure and Balancing -----------------


# Function to Calculate the angle of misclosure

Total_Actual = 

Total_Theor = 


# ii. Bearings and Azimuths ------------------ 

# iii. Latitudes and Longitudes -----------------------

# Change in latitude
# Change in departure

# iv. Draw traverse with Turtle graphics ------------------

# v. Error of Closure and Precision Ratio --------------------

# perimiter

# 3.3  OUTPUT LOOP 

    degree_sign= u'\N{DEGREE SIGN}' # for output degree symbol

    # Display angles, distances, depths from lists in table format
    fo = open("CalcDepth.csv", 'w', newline='')
    fwriter = csv.writer(fo)
    fwriter.writerow(["ID","GZ_X", "GZ_Y", "R_X", "R_Y","Angle_degrees", "DistanceToGZ_m", "CaveDepth_m"]) # Writing header into csv
    idcount = 0
    for index in range(len(calc_depths)): # index should be 0, 1, 2, ... to last index in lists
        
        idcount = idcount + 1 # unique identifier
        # writing out inputs into csv
        gzx_out = gzx_input[index] 
        gzy_out = gzy_input[index]
        rx_out = rx_input[index]
        ry_out = ry_input[index]
        input_ang_output = input_angles[index] 
        
        # writing out calculated values into csv
        DistToGZ = round(input_distances[index],1) # round the input_dist output display to 1 decimal place
        caveDepth = round(calc_depths[index],1)  # round the depth output to 1 decimal place

        fwriter.writerow([idcount, gzx_out,gzy_out,rx_out,ry_out,input_ang_output,DistToGZ,caveDepth]) # Writing to csv         

    fo.close()
    print("Results successfully exported to csv file")