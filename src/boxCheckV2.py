"""
- Implement feature for catching duplicate kids.
  Currently duplicate kids show up as 'MISSING BOX NUMBER/HOME TAG'
- IF THE NUMBER OF POTENITAL MATCHES FOR A MISSPELLED NAME IS 0, RUN THROUGH ALL UNMATCHED NAMES UNTIL FOUND
- Program should iterate through list until finding the 'School' key so that you dont have to delete first two lines
- Check if the school count/box number count for the BOX LIST does NOT increase with duplicate numbers (test on sister annata box list since everything else is perfect except for 1 duplicate #)
- After checking names against similar names, go through all unmatched names just incase
"""


import pandas as pd
import numpy as np
import difflib as diff

# GLOBAL VARIABLES
DEBUG = False
ERROR_MESSAGE_LIST = []
STARTING_BOX_NUM = 1
# GLOBAL VARIABLES

def setColour(colour):
    print(colour, end = '')
    return

red = "\033[1;31;40m"
white = "\033[1;37;40m"
green = "\033[1;32;40m"
yellow = "\033[1;33;40m"

class Student:
    name: str
    grade: str
    deliveryType: str
    matchStatus: bool

    def __init__(self, name, grade, deliveryType):
        """
        name: string. Students name
        grade: string. Students grade
        deliveryType: string. Students delivery type OR box number if school type
        matchStatus: Bool (susceptable to change). True is the student has a match on the master list, False otherwise
        """
        self.name = name
        self.grade = grade
        self.deliveryType = deliveryType
        self.matchStatus = False
        pass
    
    def __str__(self):
        return f'Name: <{self.name}>    Grade: <{self.grade}>    Delivery Type: <{self.deliveryType}>'
    
    def __lt__(self, other):
        if self.name < other.name:
            return self
        else:
            return other
    
    def __eq__(self, other):
        if self.name == other.name and self.grade == other.grade:
            return True
        else:
            return False

    pass

class MasterStudent(Student):

    deliveryStatus: str

    def __init__(self, name, grade, deliveryType, deliveryStatus):
        self.name = name
        self.grade = grade
        self.deliveryType = deliveryType
        self.matchStatus = False
        self.deliveryStatus = deliveryStatus
        pass

def fixSpelling(student: Student, masterStudentName: str):
    student.name = masterStudentName
    return

def match(student: Student, masterStudent: MasterStudent):
    student.matchStatus = True
    masterStudent.matchStatus = True
    return

def makeMasterList(masterList: pd.DataFrame):

    masterStudentList = []
    grades = set()

    for i, row in masterList.iterrows():
        masterStudentList.append(MasterStudent(row['Student'], row['Class'], row['Delivery Type'], row['Order Status']))
        grades.add(row['Class'])

    return masterStudentList, grades

def makeBoxList(boxList: pd.DataFrame):
    """
    This function takes in a pandas data frame and turns it into a list of "Student" objejects that can be used throughout the program.
    """

    boxStudentList = []
    grades = set()

    for i, row in boxList.iterrows():
        if type(row['Class']) != float:
            currGrade = row['Class']
            grades.add(currGrade)
        if type(row['Student']) == float:
            continue
        if type(row['Delivery Type']) == float:
            boxStudentList.append(Student(row['Student'], currGrade, 'NONE'))
        else:
            boxStudentList.append(Student(row['Student'], currGrade, row['Delivery Type']))

    return boxStudentList, grades

def nameCheck(boxStudentList, masterStudentList):
    """
    This function will compare the names of all the kids to check if the same name appears on both box lists. It also checks to makes sure
    the student has the same grade in both lists. If there is a name that matches on both lists but does not have the same grade, a "partial match"
    message will be displayed. If a name on the box list or a name on the master list has no match, this is printed in red
    as an error message. For names on the BOX LIST that do not have a match, we will check for similar names on the MASTER LIST and tell the user
    these similar names are "potential matches." The user will then be prompted to change the wrong name.
    """

    checkedStudents = [] #Students on the box list whos name AND grade matches a student on the master list
    wrongGradeStudents = [] #Students on the box list whos name matches a student on the master list BUT the grade is not the same
    unmatchedBoxStudents = [] #Students on the box list that dont have a matching name on the master list
    unmatchedMasterStudents = [] #Students on the master list who do not have match on the box list BEFORE spellchecking
    notOnBoxList = [] #Students on the master list who do not have match on the box list AFTER spellchecking

    for kid in boxStudentList:
        for student in masterStudentList:
            if (kid.name).lower() == (student.name).lower() and kid.grade == student.grade:
                match(kid, student) #Set the match status of the tow kids to True
                checkedStudents.append((kid, student))
            elif kid.name == student.name and kid.grade != student.grade:
                match(kid, student) #FIXME: may want to change this to match when they are confirmed
                wrongGradeStudents.append((kid, student))
            else:
                continue
    
    setColour(green)
    for kid, student in checkedStudents:
        print("MATCH: ", f"<{kid.name}>", "\tMATCHES\t", f"<{student.name}>")
    setColour(white)
    print('\n')

    setColour(yellow)
    for kid, student in wrongGradeStudents:
        #May want to make this function give you the option to fix the grade
        print("PARTIAL MATCH: ", f"<{kid.name}> has the grade <{kid.grade}> on the BOX LIST and <{student.grade}> on the MASTER LIST")
    setColour(white)
    print('\n')

    setColour(red)
    print("BOX LIST STUDENTS WITH NO MATCH")
    for kid in boxStudentList:
        if kid.matchStatus == False:
            unmatchedBoxStudents.append(kid) #Appends the whole object to the list
            print(f"NO MATCH: <{kid.name}> in {kid.grade} on the BOX list has no match")
    print('\nMASTER LIST STUDENTS WITH NO MATCH')
    for student in masterStudentList:
        if student.matchStatus == False:
            unmatchedMasterStudents.append(student)
            print(f"NO MATCH: <{student.name}> in {student.grade} on the MASTER LIST has no match")
    setColour(white)
    print('\n')

    unmatchedMasterNames = []
    for student in unmatchedMasterStudents:
        unmatchedMasterNames.append(student.name)

    for kid in unmatchedBoxStudents:
        potentialMatches = diff.get_close_matches(kid.name, unmatchedMasterNames)
        for student in unmatchedMasterStudents:
            if student.name in potentialMatches:
                name = student.name
            else:
                continue
            print(f"POTENTIAL MATCH: Does <{kid.name}> on the BOX LIST match with the name <{name}> on the MASTER LIST [y/n]?")
            choice = input()
            if choice == 'y':
                print(f"Would you like to fix the spelling of <{kid.name}> to <{name}> from the MASTER LIST (recommended) [y/n]?")
                fixName = input()
                if fixName == 'y':
                    fixSpelling(kid, name)
                    match(kid, student)
                    break
                elif fixName == 'n':
                    continue
            elif choice == 'n':
                continue

    if (kid.matchStatus != True for kid in unmatchedBoxStudents):
        setColour(red)
        print("\nThe following students from the BOX LIST have not been matched:\n")
        setColour(white)
        missingFlag = False
        for kid in unmatchedBoxStudents:
            if kid.matchStatus == False:
                missingFlag = True
                print(kid)
        if missingFlag == False:
            setColour(green)
            print("ALL STUDENTS ON THE BOX LIST HAVE BEEN MATCHED\n")
        else:
            setColour(red)
            print("THESE STUDENTS ARE LIKELY ON THE WRONG BOX LIST. PLEASE CHECK AND FIX MANUALLY.\n")
        setColour(white)

    if len(unmatchedMasterStudents) != 0:
        setColour(red)
        print("The following students from the MASTER LIST have not been matched:\n")
        setColour(white)
        missingFlag = False
        for kid in unmatchedMasterStudents:
            if kid.matchStatus == False:
                missingFlag = True
                print(kid)
        if missingFlag == False:
            setColour(green)
            print("ALL STUDENTS ON THE MASTER LIST HAVE BEEN MATCHED\n")
        else:
            setColour(red)
            print("\nTHESE STUDENTS ARE LIKELY MISSING FROM THE BOX LIST. PLEASE CHECK AND FIX MANUALLY.\n")
        setColour(white)

    return boxStudentList, masterStudentList

def boxCheck(boxStudentList, masterStudentList, startingBoxNum):
    """
    NOTE: startingBoxNum should ALWAYS BE 1 FOR NOW. First round box list mistakes should be fixed and therefore should not affect the program 
    when used for second round. May be able to improve on the feature later.
    The following is a list of everything this function does:
    - Make sure every box number is accounted for
    - Check missing box nuumbers
    - Check duplicate box numbers
    - Check school and home counts and make sure they are equal
    - Check to make sure the school count on the master list matches the kids with box numbers
    - If there are two kids that ashare a box number check for if they are siblings, then ignore the duplicate
    - Make this take a parameter that is the last box number that was left off after first round delivery. If pre-first round then start at 1
    - Iterate through the box numbers list and check them against the potential box numbers STARTING FROM THE STARTING NUM
      This way we know if a number is wrong if it is less than the starting num
    """

    masterSchoolCount = 0 #All kids on the master list with delivery type 'School'. Also the potential number of box numbers
    masterHomeCount = 0 #All Kids on the master list with delivery type 'Home
    boxSchoolCount = 0
    boxHomeCount = 0
    missingTagList = [] #List of students who are missing abox number or Home tag
    boxNumList = [] #List of the box numbers
    checkedNumList = [] #List of box numbers that were checked
    missingNumList = []
    dupNumList = set() # Set so as to not have duplicate duplicates
    dupNumsOK = []

    for kid in masterStudentList:
        if kid.deliveryType == 'School':
            masterSchoolCount += 1
        elif kid.deliveryType == 'Home':
            masterHomeCount += 1

    for kid in boxStudentList:
        if (kid.deliveryType).isnumeric() == True:
            boxSchoolCount += 1
            boxNumList.append(int(kid.deliveryType))
        elif kid.deliveryType == 'School':
            #boxSchoolCount += 1 # FIXME: DO WE WANT THIS????? EDIT: Potenitial make a new quantity of kids with shcool type but no number
            missingTagList.append(kid)
        elif (kid.deliveryType).upper() == 'HOME':
            boxHomeCount += 1
        elif kid.deliveryType == 'Pickup':
            continue
        else:
            setColour(red)
            print(f"ERROR: <{kid.name}> has an invalid delivery type. The delivery type <{kid.deliveryType}> does not exist. Please enter the number beside the type that this should be.")
            setColour(white)
            print("1. School")
            print("2. Home")
            print("3. Pickup")
            print("4. Unsure")
            choices = ['1', '2', '3', '4']
            choice = input()
            while choice not in choices:
                choice = input("Please enter the number 1, 2, 3 or 4: ")
            if choice == '1':
                kid.deliveryType = 'School'
            elif choice == '2':
                kid.deliveryType = 'Home'
            elif choice == '3':
                kid.deliveryType = 'Pickup'
            elif choice == '4':
                kid.deliveryType = 'Unsure'
                missingTagList.append(kid)

    # Iterate through ALL box numbers but only print the box numbers accounted for starting at the starting number entered by the user.

    potentialBoxNums = [] #All potential box numbers that SHOULD be on the box list based on the kids with 'School' delivery type
    for i in range(1, boxSchoolCount + 1):
        potentialBoxNums.append(i)

    # FIXME: THIS BLOCK NEEDS TO BE FXED TO PROPERLY ADD DUPLICATE BOX NUMS
    for num in sorted(boxNumList):
        if num in potentialBoxNums and num not in checkedNumList:
            checkedNumList.append(int(num))
            potentialBoxNums.remove(int(num))
        elif num in checkedNumList:
            dupNumList.add(int(num))
            potentialBoxNums.pop(-1)
        elif potentialBoxNums[0] > num:
            missingNumList.append(potentialBoxNums)
            potentialBoxNums.pop(0)
            potentialBoxNums.append(potentialBoxNums[-1] + 1)

    for num in potentialBoxNums:
        missingNumList.append(num)


    print("\nThere are ", masterSchoolCount, " students on the MASTER LIST with the 'School' delivery type")
    print("There are ", boxSchoolCount, " students on the BOX LIST with box numbers\n")
    #print(dupNumList) #DEBUG
    #print(sorted(boxNumList)) #DEBUG
    for num in dupNumList:
        print("The number ", num, " appears multiple times on the box list. Would you like to ignore this duplicate (enter y if the box number is shared by siblings) [y/n]?")
        ignore = input()
        if ignore == 'y':
            dupNumsOK.append(num)
        elif ignore == 'n':
            continue

    print('\n')
    for num in missingNumList:
        setColour(red)
        print("BOX NUMBER MISSING FROM BOX LIST: ", num)
        setColour(white)

    dupNumFlag = False
    for num in dupNumList:
        if num in dupNumsOK:
            continue
        else:
            dupNumFlag = True
            setColour(red)
            print("\nDUPLICATE BOX NUMBER FOUND: ", num)
            setColour(white)
    print('\n')
    
    if len(missingNumList) == 0:
        setColour(green)
        print("BOX NUMBERS ", startingBoxNum, " TO ", sorted(boxNumList)[-1], " ARE ALL ACCOUNTED FOR\n")

    if dupNumFlag == False or len(dupNumList) == 0:
        setColour(green)
        print("THERE ARE NO UNWANTED DUPLICATE BOX NUMBERS\n")
        setColour(white)
    
    for kid in missingTagList:
        print("\033[1;31;40mMISSING BOX NUMBER/HOME TAG: \033[1;37;40m", kid)
    print('\n')
    setColour(white)

    return

def gradeCheck(boxStudentList: list, masterStudentList: list, boxGrades: set, masterGrades: set):
    """
    Iterates through each grade found on the box list and the master list to make sure they all match. If there is a grade on the BOX LIST that
    does not match a grade on the MASTER LIST, then the user will be prompted to change it to one of the grades on the MASTER LIST.
    """
    masterGrades = sorted(list(masterGrades))
    for grade in sorted(boxGrades):
        if grade in masterGrades:
            masterGrades.remove(grade)
        else:
            print("The grade <", grade, "> is not on the MASTER list. Enter the number beside the grade you would like to replace it with.")
            for i in range(len(masterGrades)):
                print(f"{i+1}. {masterGrades[i]}")
            choice = int(input())
            newGrade = masterGrades[choice - 1]
            for kid in boxStudentList:
                if kid.grade == grade:
                    kid.grade = newGrade

    return

def compareLists(boxFile, masterFile):

    boxStudentList, boxGrades = makeBoxList(boxFile)
    masterStudentList, masterGrades = makeMasterList(masterFile)
    gradeCheck(boxStudentList, masterStudentList, boxGrades, masterGrades)
    boxStudentList, masterStudentList = nameCheck(boxStudentList, masterStudentList)
    boxCheck(boxStudentList, masterStudentList, STARTING_BOX_NUM)

    return


if __name__ == "__main__":

    boxFile_name = input("Paste the name of the BOX list you are CHECKING here: ")
    masterFile_name = input("Paste the name of the MASTER list here here: ")
    STARTING_BOX_NUM = input("Enter the box number that the program should start checking at (enter 1 if first round delivery): ")
    print('\n')

    boxFile = pd.read_csv(boxFile_name) # Box list to be checked
    masterFile = pd.read_csv(masterFile_name, sep = ',') # Master box list to check against
    boxFile['Delivery Type'] = boxFile['Delivery Type'].apply(lambda x: x if pd.isnull(x) or type(x) == str else str(int(x)))

    for i, row in masterFile.iterrows():
        if row['Order Status'] == "Cancelled":
            masterFile = masterFile.drop(labels = i, axis = 0).reset_index(drop = True)

    compareLists(boxFile, masterFile)

    pass