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

# 2. FUNCTION DEFINITIONS AND IMPORTS #################################################

import math # importing math for trig and relevant math functions
import turtle

# 1) Function to convert String Reference Bearing in DMS to azimuth in decimal degrees.

dms="N78d18'59\"W" # needs to except this format only. 11 characters in length (ie. index 0 - 10).

def RefBToAzmDD(bearingStr):

    if bearingStr[0].upper()=="N":
            VertDir = "N"
    elif bearingStr[0].upper()=="S":
            VertDir = "S"

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

# 2) DMStoDD function, for internal angles if specified input format is DMS

dms="78d18'59\"" # needs to except this format only. 9 characters in length (ie index 0 - 8)

def DMStoDD(DMSangle):

    num1=float(DMSangle[0:3]) # extracts degrees
    num2=float(DMSangle[4:6]) # extracts minutes
    num3=float(DMSangle[7:9]) # extracts seconds
    dd=(num1+(num2+(num3/60))/60)

    return dd

# 3) Azimuth Bearing Finder Function, returns azimuth in decimal degrees

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

# 4) Latitude function

def LatCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeLat=math.cos(azmth_rad)*travL
    return changeLat

# 5) Departure function

def DepCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeDep=math.sin(azmth_rad)*travL
    return changeDep

# 6) Function to convert Azimuth in decimal degrees to Bearing in DMS; returns string in DMS format

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


# 7) function to define the angle of miscolsure using the sum of the angles and the sides stated

def AoM(sides,sum_angles):
    AngMisc = (sides - 2) * 180 - sum_angles
    return AngMisc

# 8) function to find the error of closure

def EoC(Total_Lat, Total_Dep):
    ErrClosr = math.sqrt(Total_Lat**2 +Total_Dep**2)
    return ErrClosr

# 9) function to find the Precision Ratio

def PR(EoC,Perimeter):
    PRatio = EoC/Perimeter
    return PRatio

# 3. MAIN FUNCTION ####################################################################

# 3.0 PROGRAM STATEMENTS ----------------------------------------------------

print ("This program provides a proposed solution for Closed Traverse data processing, which serves to automate the calculation\n processes a surveyoror drafter would normally perform after the surveying" )
print ("Insert assumptions and simplifications/Instructions for the user (Disclaimer)")

# 3.1 INPUT LOOP AND PRE-PROCESSING ------------------------------------------------------------

int_angles_list =  []  # create empty list for internal angles
trav_len_list = []   # create empty list for traverse lengths

# Non Looping inputs
degformat = input("Are your internal angles in DMS or decimal degrees format? Please Enter 'DMS' or 'DD': ")
outpt_prec = int(input("How precise do you want your non-angular outputs to be? Enter number of digits after decimal point: "))   
ref_bearing = input("What is your reference bearing from station 1 to 2? Enter format as [N00d00'00\"W]: ")
dir_trav = input("What is the direction of your traverse? Enter 'CC' for counterclockwise or 'C' for clockwise: ")

#initiating screen for turtle to draw survey diagram
wn=turtle.Screen()
wn.bgcolor("white")
height = 5000
width = 5000
turtle.screensize(width, height)
bharat=turtle.Turtle()
bharat.color("black")
bharat.pensize(5)

# Pre-processing inputs for main processing loop
ddref_bearing=RefBToAzmDD(ref_bearing) # Calls conversion function to turn reference bearing string w/ directions into decimal degree azimuth

# variable declarations for running totals / increments
StationCount = 1
perimeter = 0
SumOfAngles = 0

while True: # Input loop for internal angles and traverse lengths, with some pre-processing calculations

    # Ask the user for the Internal Angle of the current station they are evaluating
    if degformat.upper() == "DMS":
        Internal_Angles = input("Please enter the internal angle for observed at station "+str(StationCount)+" in DMS format [000d00'00\"]")
        int_angle=DMStoDD(Internal_Angles) # converts dms internal angle into dd before appending
    else:
        Internal_Angles = input("Please enter the internal angle for observed at station "+str(StationCount)+" in decimal degrees: ")
        int_angle=float(Internal_Angles) # converts to float
    int_angles_list.append(int_angle) # appends internal angles in dd format into list
    SumOfAngles = SumOfAngles + int_angle

    # Ask the user for the Traverse lengths of the current station they are evaluating
    Traverse_Lengths = float(input("Please enter the length for Traverse going from station "+str(StationCount)+" to "+str(StationCount+1)+": "))
    trav_len_list.append(Traverse_Lengths) # appends traverse length into format into list
    perimeter = perimeter + Traverse_Lengths # running total for perimeter

    print()
    end =str(input("Do you want to stop entering values (Y/N)? "))
    print()
    if end.upper() == 'Y' :
        break

    #Right eye with starting point of upper right of face
    if StationCount == 1:
        bharat.left(90-ddref_bearing)
    elif dir_trav == "CC":
        bharat.left(180-int_angle)
    elif dir_trav == "C":
        bharat.left(-1*(180-int_angle))
    bharat.forward(Traverse_Lengths)

    StationCount = StationCount + 1

wn.exitonclick() #exit turtle program

# 3.2 MAIN PROCESSING LOOPS -----------------------------------------------------------

# i. Angle of Misclosure and Balancing -----------------

AoM(StationCount, SumOfAngles)
Bal_angle_list = []

if AoM != 0:
    balance_Val = AoM/StationCount
    for index in range(len(int_angles_list)):
        if AoM > 0:
            Balanced_int_angle = int_angles_list[index] - balance_Val
            Bal_angle_list.append(Balanced_int_angle)
        elif AoM < 0:
            Balanced_int_angle = int_angles_list[index] + balance_Val
            Bal_angle_list.append(Balanced_int_angle)
elif AoM == 0:
    for index in range(len(int_angles_list)):
        Balanced_int_angle = int_angles_list[index]
        Bal_angle_list.append(Balanced_int_angle)

# ii. Bearings and Azimuths, Latitudes, Departures ------------------ 

Brng_list = [ref_bearing] # assigning the string DMS ref bearing from input to index 0
azimuth_list = [ddref_bearing] # assigning the convert ref bearing to index 0
Lat_list = []
Dep_list = []
total_lat = 0
total_dep = 0

for index in range(len(int_angles_list)):
    intAngle = int_angles_list[index]
    if index == 0:
        BrngNext=ddref_bearing
    elif index >= 1:
        BrngNext = azmcalc(dir_trav, BrngB4, intAngle)
        azimuth_list.append(BrngNext)
        Brng_list.append(ddtoDMS(BrngNext))
    
    BrngB4 = BrngNext

    Latitude=LatCalc(BrngNext, trav_len_list[index])
    total_lat = total_lat + Latitude
    Lat_list.append(Latitude)

    Departure = DepCalc(BrngNext, trav_len_list[index])
    total_dep = total_dep + Departure
    Dep_list.append(Departure)

# iii. Error of Closure and Precision Ratio -------------------- 
#    
ErrorOfClosure = EoC(total_lat, total_dep)
PrecisionRatio = PR(ErrorOfClosure, )

# 3.3  OUTPUT LOOP 

degree_sign= u'\N{DEGREE SIGN}' # for output degree symbol

# Display angles, distances, depths from lists in table format
fo = open("CalcDepth.csv", 'w', newline='')
fwriter = csv.writer(fo)
fwriter.writerow(["Traverse","Traverse Lengths", "Original Angles", "Balanced Angles","Bearings", "Azimuths","Latitudes","Departures","Angular Miscolsure","Total Latitude", "Total Departure","Perimeter", "Error Of Closure", "Precision Ratio"]) # Writing header into csv
idcount = 0
for index in range(len(trav_len_list)): # index should be 0, 1, 2, ... to last index in lists
    
    
    # writing out inputs into csv

    idcount = 1

    if index == len(trav_len_list)-1:
        UniqueId = str(idcount)+"-1"
    else:
        UniqueId = str(idcount)+"-"+str(idcount+1)

    idcount = idcount + 1

    TraverseLine = [index] 
    Traverse_out = trav_len_list[index]

    OriginalAngles = int_angles_list[index]
    NewAngles = Bal_angle_list[index]

    Bearings_out = Brng_list[index]
    Azimuths_out = azimuth_list[index]

    Latitudes_out = Lat_list[index] 
    Departures_out = Dep_list[index] 
    

    # AOM_out 
    #total_dep
    #total_lat
    # Perimeter
    # EOC  
    # PR
    
    # writing out calculated values into csv
    DistToGZ = round(input_distances[index],1) # round the input_dist output display to 1 decimal place
    caveDepth = round(calc_depths[index],1)  # round the depth output to 1 decimal place

    fwriter.writerow([idcount, gzx_out,gzy_out,rx_out,ry_out,input_ang_output,DistToGZ,caveDepth]) # Writing to csv         

fo.close()
print("Results successfully exported to csv file")
