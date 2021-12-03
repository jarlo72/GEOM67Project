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
import csv

# 1) Function to convert String Reference Bearing in DMS to azimuth in decimal degrees.

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

def DMStoDD(DMSangle):

    num3=(float(DMSangle[-3:-1])) # extracts seconds
    num2=(float(DMSangle[-6:-4])) # extracts minutes
    num1=(float(DMSangle[:-7])) # extracts degree
    dd=(num1+(num2+(num3/60))/60)

    return dd

# 3) Azimuth Bearing Finder Function, returns azimuth in decimal degrees

def azmcalc(CalcDir, BearingBefore, intAngle):

    # Different formula to find angle depending on user specified direction of travel
    if CalcDir == "CC":
            BearingNext = BearingBefore - (180 - intAngle)
    elif CalcDir == "C":
            BearingNext = BearingBefore + (180 - intAngle)

    if BearingNext > 360:
            BearingNext = BearingNext - 360
    elif BearingNext < 0:
            BearingNext = BearingNext + 360

    return BearingNext

# 4) Function to convert Azimuth in decimal degrees to Bearing in DMS; returns string in DMS format

def ddtoDMS(dd):

    if dd >= 0 and dd < 90:
        min,sec_ = divmod(dd*3600,60)
        deg,min = divmod(min, 60)
        sec = int(round(sec_,0))
        bearing = "N"+str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""+"E"

    elif dd >= 90 and dd < 180:
        min,sec_ = divmod((180-dd)*3600,60)
        deg,min = divmod(min, 60)
        sec = int(round(sec_,0))
        bearing = "S"+str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""+"E"

    elif dd >= 180 and dd < 270:
        min,sec_ = divmod((dd-180)*3600,60)
        deg,min = divmod(min, 60)
        sec = int(round(sec_,0))
        bearing = "S"+str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""+"W"

    elif dd >= 270 and dd < 360:
        min,sec_ = divmod((360-dd)*3600,60)
        deg,min = divmod(min, 60)
        sec = int(round(sec_,0))
        bearing = "N"+str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""+"W"

    return bearing

# 5) Converts DD to DMS for any angle which doesn't require directions, such as internal angles and angle of misclosure

def ddtoDMS2(dd):
    min,sec_ = divmod(dd*3600,60)
    deg,min = divmod(min, 60)
    sec = int(round(sec_,0))
    bearing = str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""
    return bearing

# 6) Latitude function

def LatCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeLat=math.cos(azmth_rad)*travL
    return changeLat

# 7) Departure function

def DepCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeDep=math.sin(azmth_rad)*travL
    return changeDep

# 8) function to define the angle of miscolsure using the sum of the angles and the sides stated

def AoM(sides,sum_angles):
    AngMisc = (sides - 2) * 180 - sum_angles
    return AngMisc

# 9) function to find the error of closure

def EoC(Total_Lat, Total_Dep):
    ErrClosr = math.sqrt(Total_Lat**2 +Total_Dep**2)
    return ErrClosr

# 10) function to find the Precision Ratio

def PR(EoC,Perimeter):
    num,denom = (EoC/Perimeter).as_integer_ratio()
    num2,denom2=(num/num,denom/num)
    Pratio=(str(int(num2))+"/"+str(int(denom2)))
    return Pratio

# 3. MAIN FUNCTION ####################################################################

# 3.0 PROGRAM STATEMENTS ---------------------------------------------------------------------------------

print ("This program provides a proposed solution for Closed Traverse data processing, which serves to automate the calculation\n processes a surveyoror drafter would normally perform after the surveying" )
print ("Insert assumptions and simplifications/Instructions for the user (Disclaimer)")
print()

# 3.1 INPUT LOOP AND PRE-PROCESSING ------------------------------------------------------------

int_angles_list =  []  # create empty list for internal angles
trav_len_list = []   # create empty list for traverse lengths

# Non Looping inputs. User enters these only once
degformat = input("Are your internal angles in DMS or decimal degrees format? Please Enter 'DMS' or 'DD': ")
unit_pref = input("Specify the units for your traverse lengths. Please enter 'ft' or 'm': ")
outpt_prec = int(input("How precise do you want your non-angular outputs to be? Enter number of digits after decimal point: "))   
ref_bearing = input("What is your reference bearing from station 1 to 2? Enter format as [N00d00'00\"W]: ")
dir_trav = input("What is the direction of your traverse? Enter 'CC' for counterclockwise or 'C' for clockwise: ")
print()
ddref_bearing=RefBToAzmDD(ref_bearing) # Calls conversion function to turn reference bearing string w/ directions into decimal degree azimuth

#initiating screen for turtle to draw survey diagram
wn=turtle.Screen()
wn.bgcolor("white")
height = 5000
width = 5000
turtle.screensize(width, height)
bharat=turtle.Turtle()
bharat.color("black")
bharat.pensize(5)

# variable declarations for running totals / increments to be used in the following input loop
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

    #Turtle named Bharat will draw traverse lines for each iteration of the loop
    if StationCount == 1:
        bharat.left(90-ddref_bearing)
    elif dir_trav == "CC":
        bharat.left(180-int_angle)
    elif dir_trav == "C":
        bharat.left(-1*(180-int_angle))
    bharat.forward(Traverse_Lengths)

    print()
    end =str(input("Do you want to stop entering values (Y/N)? "))
    print()
    if end.upper() == 'Y' :
        break

    StationCount = StationCount + 1

# 3.2 MAIN PROCESSING LOOPS --------------------------------------------------------------------------

# i. Angle of Misclosure and Balancing --------------------------------------------------------------

AngleOfMisc = AoM(StationCount, SumOfAngles)
Bal_angle_list = []

if AngleOfMisc != 0:
    balance_Val = (AngleOfMisc/StationCount)
    for index in range(len(int_angles_list)):
        if AngleOfMisc > 0:
            Balanced_int_angle = int_angles_list[index] - balance_Val
            Bal_angle_list.append(Balanced_int_angle)
        elif AngleOfMisc < 0:
            Balanced_int_angle = int_angles_list[index] + balance_Val
            Bal_angle_list.append(Balanced_int_angle)
elif AngleOfMisc== 0:
    for index in range(len(int_angles_list)):
        Balanced_int_angle = int_angles_list[index]
        Bal_angle_list.append(Balanced_int_angle)

# ii. Bearings and Azimuths, Latitudes, Departures ------------------------------------------------ 

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

# iii. Error of Closure and Precision Ratio -------------------------------------------------- 
#    
ErrorOfClosure = EoC(total_lat, total_dep)
PrecisionRatio = PR(ErrorOfClosure, perimeter)

# 3.3  OUTPUT LOOP 

# Display angles, distances, depths from lists in table format
fo = open("Closed_Traverse_Survey.csv", 'w', newline='')
fwriter = csv.writer(fo)
fwriter.writerow(["Traverse","Traverse Lengths ("+unit_pref+")", "Original Angles", "Balanced Angles","Bearings", "Azimuths","Latitude ("+unit_pref+")","Departure ("+unit_pref+")","Angular Miscolsure","Total Latitude Change ("+unit_pref+")", "Total Departure Change ("+unit_pref+")","Perimeter ("+unit_pref+")", "Error Of Closure", "Precision Ratio"]) # Writing header into csv
idcount = 1

for index in range(len(trav_len_list)): # index should be 0, 1, 2, ... to last index in lists
    
    # writing out inputs into csv

    if index == len(trav_len_list)-1:
        TraverseLine = str(idcount)+" to 1"
    else:
        TraverseLine = str(idcount)+" to "+str(idcount+1)

    idcount = idcount + 1

    Traverse_out = trav_len_list[index]

    OriginalAngles = ddtoDMS2(int_angles_list[index])
    NewAngles = ddtoDMS2(Bal_angle_list[index])

    Bearings_out = Brng_list[index]
    Azimuths_out = ddtoDMS2(azimuth_list[index])

    Latitudes_out = round(Lat_list[index],outpt_prec)
    Departures_out = round(Dep_list[index],outpt_prec)

    if index == 0:
        AOM_out = ddtoDMS2(AngleOfMisc)
        total_dep = round(total_dep,outpt_prec)
        total_lat = round(total_lat,outpt_prec)
        Perimeter = round(perimeter,outpt_prec)
        ErroC = round(ErrorOfClosure,outpt_prec) 
        PR_out = (PrecisionRatio) # Not necessary, but included for neatness and consistency
        fwriter.writerow([TraverseLine, Traverse_out, OriginalAngles, NewAngles, Bearings_out, Azimuths_out, Latitudes_out, Departures_out, AOM_out, total_lat, total_dep, Perimeter,ErroC, PR_out]) 
    else:
        fwriter.writerow([TraverseLine, Traverse_out, OriginalAngles, NewAngles, Bearings_out, Azimuths_out, Latitudes_out, Departures_out])       

fo.close()
print("Results successfully exported to csv file. Click on Turtle Window to close program")

wn.exitonclick() #exit turtle program
