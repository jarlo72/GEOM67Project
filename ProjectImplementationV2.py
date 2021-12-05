# 1. PROGRAM METADATA ##############################################################################################################################################################

# Horizontal Closed Traverse Survey Calculator
# Created by: Justin Brassard, Bharat Bharat, Jon Marlo Delicano 
# For: Project Implementation
# Date: December 7, 2021
# Program function: 
# Assumes:
# Inputs entered with keyboard
# Outputs displayed on screen and exported to csv

# 2. FUNCTION DEFINITIONS AND RELEVENT LIBRARY IMPORTS ##############################################################################################################################

import math # importing math for trig and relevant math functions
import turtle # importing turtles for drawing a sketch of survey
import csv # importing csv to read inputs and write outputs

# 1) Function to convert Reference Bearing in string-directional-DMS format to an azimuth in decimal degrees for calculation processes-----------------------------
def RefBToAzmDD(bearingStr): 

    # checks bearing's vertical direction and assigns the string designation
    if bearingStr[0].upper()=="N":
            VertDir = "N"
    elif bearingStr[0].upper()=="S":
            VertDir = "S"

    # checks bearing's horizontal direction and assigns the string designation
    if bearingStr[-1].upper()=="W":
            HorDir = "W"
    elif bearingStr[-1].upper()=="E":
            HorDir = "E"

    # Extracts the DMS values from bearing string, reading from the left
    num1=float(bearingStr[1:3]) # extracts degrees
    num2=float(bearingStr[4:6]) # extracts minutes
    num3=float(bearingStr[7:9]) # extracts seconds

    # Selection structure to allocate which quadrant the bearing is in to assign appropriate azimuth calculation
    if (VertDir == "N") and (HorDir == "W"):
            AZMdd=360-(num1+(num2+(num3/60))/60)
    elif (VertDir == "N") and (HorDir == "E"):
            AZMdd=(num1+(num2+(num3/60))/60)
    elif (VertDir == "S") and (HorDir == "W"):
            AZMdd=180+(num1+(num2+(num3/60))/60)
    elif (VertDir == "S") and (HorDir == "E"):
            AZMdd=180-(num1+(num2+(num3/60))/60)

    return AZMdd # returns an azimuth as decimal degrees float

# 2) DMS to decimal degrees conversion function, for any angles if specified input format is DMS ------------------------------------------------------------------------
def DMStoDD(DMSangle):

    # Extracts the DMS values from bearing string, reading from the right to account for flexibility in # of digit entered the degrees portion of angle
    num3=(float(DMSangle[-3:-1])) # extracts seconds
    num2=(float(DMSangle[-6:-4])) # extracts minutes
    num1=(float(DMSangle[:-7])) # extracts degree
    dd=(num1+(num2+(num3/60))/60) # calculating decimal degrees from DMS portions.

    return dd # returns the internal angle as decimal decimal degree float

# 3) Azimuth Bearing Finder Function, returns azimuth in decimal degrees ----------------------------------------------------------------------------------------------------
def azmcalc(CalcDir, BearingBefore, intAngle): 

    # Different formula to find angle depending on user specified direction of travel
    if CalcDir.upper() == "CC": # for a counter clockwise traverse 
            BearingNext = BearingBefore - (180 - intAngle)
    elif CalcDir.upper() == "C": # for a counter clockwise traverse 
            BearingNext = BearingBefore + (180 - intAngle)

    # Assigns angle between 0 - 360 degrees if dd azimuth bearing surpasses this limit
    if BearingNext > 360:
            BearingNext = BearingNext - 360
    elif BearingNext < 0:
            BearingNext = BearingNext + 360

    return BearingNext # returns the azimuth bearing for the next traverse, in decimal degrees

# 4) Function to convert Azimuth in decimal degrees to Bearing in DMS; returns string in DMS format --------------------------------------------------------------------------
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

# 5) Converts DD to DMS for any angle which doesn't require directions, such as internal angles and angle of misclosure------------------------------------------------------------
def ddtoDMS2(dd):
    min,sec_ = divmod(dd*3600,60)
    deg,min = divmod(min, 60)
    sec = int(round(sec_,0))
    bearing = str(int(deg))+"d"+"{:02d}".format(int(min))+"'"+"{:02d}".format(sec)+"\""
    return bearing

# 6) Latitude function--------------------------------------------------------------------------------------------------------------------------------------------------------------
def LatCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeLat=math.cos(azmth_rad)*travL
    return changeLat

# 7) Departure function--------------------------------------------------------------------------------------------------------------------------------------------------------------
def DepCalc(azmth, travL):
    azmth_rad = math.radians(azmth)
    changeDep=math.sin(azmth_rad)*travL
    return changeDep

# 8) function to define the angle of miscolsure using the sum of the angles and the sides stated --------------------------------------------------------------------------------
def AoM(sides,sum_angles):
    AngMisc = (sides - 2) * 180 - sum_angles
    return AngMisc

# 9) function to find the error of closure --------------------------------------------------------------------------------------------------------------------------------------------
def EoC(Total_Lat, Total_Dep):
    ErrClosr = math.sqrt(Total_Lat**2 +Total_Dep**2)
    return ErrClosr

# 10) function to find the Precision Ratio --------------------------------------------------------------------------------------------------------------------------------------------
def PR(EoC,Perimeter):
    num,denom = (EoC/Perimeter).as_integer_ratio()
    num2,denom2=(num/num,denom/num)
    Pratio=(str(int(num2))+"/"+str(int(denom2)))
    return Pratio

# Try: # try starts here

# 3. MAIN FUNCTION STARTS HERE ############################################################################################################################################################

# 3.0 PROGRAM STATEMENTS ----------------------------------------------------------------------------------------------------------------------------

print ("This program provides a proposed solution for Closed Traverse data processing, which serves to automate the calculation\nprocesses a surveyor")
print ("would normally perform after the surveying" )
print ("Insert assumptions and simplifications/Instructions for the user (Disclaimer)")
print()

# 3.1 USER INPUT AND VARIOUS PRE-PROCESSING -------------------------------------------------------------------------------------------------------

#i. One time inputs and processing ---------------------------------------------------------------------------------------------------------------

# Non Looping inputs. User enters these only once.
degformat = input("Are your internal angles in DMS or decimal degrees format? Please Enter 'DMS' or 'DD': ")
print()
unit_pref = input("Specify the units for your traverse lengths. Please enter 'ft' or 'm': ")
print()
outpt_prec = int(input("How precise do you want your non-angular outputs to be? Enter number of digits after decimal point: "))   
print()
ref_bearing = input("What is your reference Bearing or Azimuth from station 1 to 2?\nEnter format as [N00d00'00\"W] for Bearing or [000d00'00\"] for Azimuth: ")
print()
dir_trav = input("What is the direction of your traverse? Enter 'CC' for counterclockwise or 'C' for clockwise: ")
print()

if ref_bearing.find("N") == -1 and ref_bearing.find("S") == -1:
    ddref_bearing=DMStoDD(ref_bearing) # Calls conversion function to turn reference azimuth string into decimal degree azimuth
else:        
    ddref_bearing=RefBToAzmDD(ref_bearing) # Calls conversion function to turn reference bearing string w/ directions into decimal degree azimuth

#initiating screen for turtle to draw survey diagram
wn=turtle.Screen()
wn.bgcolor("white")
height = 5000 # screen size height is 5000 to be conservative
width = 5000 # screen size width is 5000 to be conservative
turtle.screensize(width, height)
bharat=turtle.Turtle()
bharat.color("black")
bharat.pensize(2)

# ii. Input Loop ---------------------------------------------------------------------------------------------------------------------------------------

# list declaration for appending successive user inputs and variable declarations for running totals / increments to be used in the following input loop
int_angles_list =  []  # create empty list for internal angles
trav_len_list = []   # create empty list for traverse lengths
rowcount = 0 # for reading csv
perimeter = 0 # for perimeter running total
SumOfAngles = 0 # Running total for actual angles, to be used for Angle of Misclosure

# Obtain internal angles and traverse lengths from an external csv in the same directory
fo = open("survey_inputs.csv") # opens a csv that must be called this name
freader = list(csv.reader(fo))

for row in freader: # Input loop for internal angles and traverse lengths, with some pre-processing calculations
    if rowcount > 0: # To skip the header title

        # Ask the user for the Internal Angle of the current station they are evaluating
        Internal_Angles = (freader[rowcount][0]) # Reading value at current row and first column, which should be internal angles

        if degformat.upper() == "DMS": # If degree format is specified as DMS for degree minutes seconds, then we need to convert it to decimal degrees float
            int_angle=DMStoDD(Internal_Angles) # calls function to convert DMS internal angle into dd before appending
        else:
            int_angle=float(Internal_Angles) # already in decimal degrees, only converts to float
        int_angles_list.append(int_angle) # appends internal angles in dd format into list
        SumOfAngles = SumOfAngles + int_angle # running total

        # Ask the user for the Traverse lengths of the current station they are evaluating
        Traverse_Lengths = float(freader[rowcount][1])
        trav_len_list.append(Traverse_Lengths) # appends traverse length into format into list
        perimeter = perimeter + Traverse_Lengths # running total for perimeter

        #Turtle named Bharat will draw traverse lines for each iteration of the loop. Algorithm depends on direction of travel
        if rowcount == 1: 
            bharat.left(90-ddref_bearing) # sets direction of first traverse using input ref bearing
        elif dir_trav.upper() == "CC":
            bharat.left(180-int_angle)
        elif dir_trav.upper() == "C":
            bharat.left(-1*(180-int_angle))
        bharat.forward(Traverse_Lengths)
        print("Drawing traverse line from station", rowcount, "...")

    rowcount=rowcount+1 # increments row count before looping again

# 3.2 MAIN PROCESSING LOOPS ----------------------------------------------------------------------------------------------------------------------------------------

# i. Angle of Misclosure and Balancing -----------------------------------------------------------------------------------------------------------------------------

AngleOfMisc = AoM(len(trav_len_list), SumOfAngles) # Calls function to calculate angle of misclosure
Bal_angle_list = [] # Creates empty list for the new or balanced internal angles to be appended in the loop below
balance_Val = (AngleOfMisc/len(int_angles_list)) # Balancing value determined by dividing angle of misclosure by number of internal angles

for index in range(len(int_angles_list)):
    if AngleOfMisc > 0: # If angle of misclosure is positive, we must subtract the balancing value from each internal angle to balance and append it into the new balanced angle list
        Balanced_int_angle = int_angles_list[index] - balance_Val
    elif AngleOfMisc < 0: # If angle of misclosure is negative, we must add the balancing value from each internal angle to balance, and append it into the new balanced angle list
        Balanced_int_angle = int_angles_list[index] + balance_Val
    elif AngleOfMisc== 0: # if angle of misclosure is 0, no need to balance angles but is re-appended to new list for convenience in subsequent processes
            Balanced_int_angle = int_angles_list[index]

    Bal_angle_list.append(Balanced_int_angle) # appends balanced or original internal into a new list

# ii. Bearings and Azimuths, Latitudes, Departures ------------------------------------------------------------------------------------------------------------------- 

Brng_list = []
azimuth_list = [ddref_bearing] # assigning the converted ref bearing to index 0
Lat_list = [] # creating empty list which latitudes will be appended to
Dep_list = [] # creating empty list which departures will be appended to
total_lat = 0 # starting running total count for total / change in latitude
total_dep = 0 # starting running total count for total / change in departure

for index in range(len(int_angles_list)):
    intAngle = int_angles_list[index]
    if index == 0:
        Brng_list.append(ddtoDMS(ddref_bearing))
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

# Writing all the outputs into a CSV
fo = open("Closed_Traverse_Survey.csv", 'w', newline='') # Opens an output csv file. Removes the added space between lines
fwriter = csv.writer(fo)
fwriter.writerow(["Traverse(Current-To-Next Station)","Traverse Lengths ("+unit_pref+")", "Original Internal Angles at Current", "Balanced Internal Angles at Current",
    "Bearings", "Azimuths","Latitude ("+unit_pref+")","Departure ("+unit_pref+")","Angle of Misclosure","Total Latitude Change ("+unit_pref+")", "Total Departure Change ("+unit_pref+")",
    "Perimeter ("+unit_pref+")", "Error Of Closure ("+unit_pref+")", "Precision Ratio"]) # Writing the output headers into csv with a unique ID

# Starting Output Loop
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
print()
print("Results successfully exported to csv file. Click on Turtle Window to close program")

wn.exitonclick() #exit turtle program

# Except statements