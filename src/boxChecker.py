"""
- Iterate through the grade column and append each name to a grade list 
- Check if there is a number or 'Home' beside their name
- Perhaps create a list with all the numbers and make sure the length of the number list has all consecutive numbers 
  and matches the number of kids in the actual list
- Check to make sure there are no duplicate numbers or missing numbers
- Append each error message to a list and print them all out at the end to make it easy to know all the errors
- Make the makeBoxList function work for when the delivery type has school in it i.e. when there are no box numbers, we do not worry about box numbers
- If a kid is in the wrong grade, change their grade in the list but not the pandas data frame.
  This way you can create a new pandas data frame out of the final list and dont have to worry about inserting in the grade
"""
# HOURS LOGGED: 14

import pandas as pd
import numpy as np
import copy

DEBUG = False

#Windsor Park 2024.csv

ERROR_LIST = []
def setColour(colour):
    print(colour, end = '')
    return

red = "\033[1;31;40m"
white = "\033[1;37;40m"
green = "\033[1;32;40m"

file1_name = input("Paste the name of the boxlisst you are CHECKING here: ")
file2_name = input("Paste the name of the MASTER box list here here: ")
print('\n')

file1 = pd.read_csv(file1_name) # Box list to be checked
file2 = pd.read_csv(file2_name, sep = ',') # Master box list to check against
file1['Delivery Type'] = file1['Delivery Type'].apply(lambda x: x if pd.isnull(x) or type(x) == str else str(int(x)))

def makeMasterList(masterFile, masterFile_name):
    """
    Creates a list of all students on the master list containing the following:
        - The students name
        - Grade
        - Delivery type
    Also returns a total student count which is GUARANTEED to be correct
    """
    nameList = []
    schoolTypeCount = 0
    homeTypeCount = 0

    index = 0
    for entry in masterFile['Order Status']:
        if entry == "Cancelled":
            masterFile = masterFile.drop(labels = index, axis = 0).reset_index(drop = True)
            index += 1
        else:
            index += 1


    totalStudentCount = homeTypeCount + schoolTypeCount
    if DEBUG:
        print(masterFile)
        print(masterFile['Class'][5])

    index = 0
    for kid in masterFile['Class']:
        currGrade = masterFile['Class'][index]
        nameList.append([masterFile['Student'][index], currGrade, masterFile['Delivery Type'][index]])
        if masterFile['Delivery Type'][index] == 'School':
            schoolTypeCount += 1
        else:
            homeTypeCount += 1
        index += 1

    nameList = sorted(nameList)
    if DEBUG:
        print(nameList)

    return nameList, totalStudentCount

def makeBoxList(file, fileName):
    
    nameList = [] # Creates a list containing tuples of the students name, grade, and delivery type
    boxNumList = [] # Creates a list of the box numbers
    gradeCount = 0
    # The following two counts should add to the total number of student i.e. the length of the nameList
    boxNumCount = 0 # Counter for how many students have numbered boxes
    homeDeliveryCount = 0 # Counter for how many students have Home as their delivery type
    totalStudentCount = 0
    index = 0 # Current row number

    print("----------------------------------------------------------------------")
    print("PRELIMINARY CHECK ON ", fileName, '\n')
    for bool in file.isnull()['Class']: # Iterating through the 'Grade' column to check for NaN values
        if bool == True and index != 0: # If the grade is NaN
            if pd.isnull(file.at[index, 'Student']):
                index += 1
                continue
            elif file.isnull()['Student'][index] != True:
                if type(file['Delivery Type'][index]) == float:
                    nameList.append([file['Student'][index], currGrade, "NULL"])
                    boxNum = "NULL"
                else:
                    nameList.append([file['Student'][index], currGrade, file['Delivery Type'][index]])
                    boxNum = file['Delivery Type'][index]
                if boxNum.isnumeric() == True:
                    boxNumList.append(int(boxNum))
                    boxNumCount += 1
                elif boxNum.isalpha() == True and boxNum.upper() == 'HOME':
                    homeDeliveryCount += 1
                else:
                    setColour(red)
                    print("ERROR: Student", file['Student'][index], "is missing a box number/home tag") # Print an error message is there is no home
                    ERROR_LIST.append(f"{file['Student'][index]} is missing a box number/home tag")
                    setColour(white)
                    totalStudentCount += 1
            index += 1
            continue
        elif index == 0:
            index += 1
            continue
        else: #If the entry is a new grade
            currGrade = file['Class'][index] # Once the grade column is not NaN, change the grade
            if file.isnull()['Student'][index] != True: # If there is not a blank box in the Student Name row
                nameList.append([file['Student'][index], currGrade, file['Delivery Type'][index]])
                boxNum = file['Delivery Type'][index]
                try:
                    if boxNum.isnumeric() == True:
                        boxNumList.append(int(boxNum))
                        boxNumCount += 1
                    elif boxNum.isalpha() == True and boxNum.upper() == 'HOME':
                        homeDeliveryCount += 1
                except AttributeError:
                    setColour(red)
                    print("ERROR: Student <", file['Student'][index], "> is missing a box number/home tag", '\n') # Print an error message if there is no home
                    ERROR_LIST.append(f"{file['Student'][index]} is missing a box number/home tag")
                    setColour(white)
                    totalStudentCount += 1
            #print(currGrade) #DEBUG
            gradeCount += 1
            index += 1
    #print("Number of grades: ", gradeCount, '\n') # DEBUG

    print("Number of students with box numbers: ", boxNumCount)
    missingFlag = False # Flag for if a box number is missing
    boxNumList = sorted(boxNumList)
    for i in range(len(boxNumList)):
        if i+1 in boxNumList:
            continue
        else:
            setColour(red)
            print("ERROR: Box number", i+1, "is missing") # FIXME Test to see if this works when a number is missing
            setColour(white)
            missingFlag = True
    # FIXME The following should not print when being compared to a list with all delivery types as school or home
    if missingFlag == False:
        print("Boxes", sorted(boxNumList)[0], "through", sorted(boxNumList)[len(boxNumList) - 1], "all accounted for", '\n')
    else:
        print('\n')

    print("Number of students with home delivery: ", homeDeliveryCount, '\n')
    totalStudentCount += boxNumCount + homeDeliveryCount
    print("Total student count: ", totalStudentCount, '\n')
    print(len(nameList), "Students on the list")
    print(boxNumCount + homeDeliveryCount, "Students with box numbers or home tags", '\n')

    nameList = sorted(nameList)
    if DEBUG: #DEBUG
        print(nameList)
        print('\n')

    print("FINISHED PRELIMINARY CHECK ON ", fileName, '\n')
    print("----------------------------------------------------------------------", '\n')
    return nameList, boxNumList, boxNumCount, homeDeliveryCount


def compareBoxLists(masterFile, checkFile, masterList_name, checkList_name):

    checkNameList, checkBoxNumList, checkBoxNumCount, checkHomeDeliveryCount = makeBoxList(checkFile, checkList_name)
    masterNameList, totalStudentCount = makeMasterList(masterFile, masterList_name)

    if checkNameList == masterNameList:
        print("LISTS ARE IDENTICAL")
        return
    elif len(checkNameList) == len(masterNameList):
        print("BOTH LISTS HAVE THE SAME NUMBER OF STUDENTS BUT ARE NOT IDENTICAL. SEARCHING FOR MISTAKES...", '\n')
        checkSpelledNameList = nameCheck(checkNameList, masterNameList)
        boxCheck(checkSpelledNameList, masterNameList)
        #gradeCheck(masterFile, checkSpelledFile, masterNameList, checkNameList) # May want to pass checkFile returned by the spellCheck function instead
    else:
        setColour(red)
        print("ERROR: THERE ARE KID(S) MISSING FROM THE BOX LIST")
        setColour(white)
        # FIXME FIND THE MISSING KID OR THE FOLLOWING FUNCTIONS DO NOT WORK // EDIT THE SPELLCHECK FUNCTION TO ADD A MISSING KID
        greaterBox = masterList_name if len(masterNameList) > len(checkNameList) else checkList_name
        lesserBox = masterList_name if len(masterNameList) < len(checkNameList) else checkList_name
        print(greaterBox, "has more kids on it than", lesserBox, '\n')
        checkSpelledNameList = nameCheck(checkNameList, masterNameList)
        boxCheck(checkSpelledNameList, masterNameList) # FIXME: CHANGE THIS BACK
        #gradeCheck(masterFile, checkSpelledFile, masterNameList, checkNameList)
    return


def gradeCheck(masterFile, checkFile, masterNameList, checkNameList): # Function assumes both lists are the same length, as that is the condition for calling

    print("----------------------------------------------------------------------")
    print("CHECKING FOR INCONSISTENCIES IN GRADES")

    gradeCountDict = {} # Dictionary that keeps track of how many kids are in each grade for the box list
    gradeCountDict_master = {} # Dictionary that keeps track of how many kids are in each grade for the master list


    i = 0
    for entry in masterFile['Class']:
        if pd.isnull(masterFile.at[i, 'Class']) == True:
            i += 1
            continue
        else:
            gradeCountDict[entry] = 0
            gradeCountDict_master[entry] = 0
            i += 1
    if DEBUG == True: # DEBUG
        print(gradeCountDict, '\n')
        print(masterNameList)
        print(checkNameList) 
    index = 0
    for kid in masterNameList:
        if checkNameList[index][0] == masterNameList[index][0]:
            if checkNameList[index][1] == masterNameList[index][1]:
                gradeCountDict[checkNameList[index][1]] += 1
                gradeCountDict_master[kid[1]] += 1
                index += 1
                continue
            else:
                setColour(red)
                print("ERROR: GRADE INCONSISTENCY")
                setColour(white)
                print("On the master list <", masterNameList[index][0], "> has the grade: ", masterNameList[index][1])
                print("On the box list <", checkNameList[index][0], "> has the grade: ", checkNameList[index][1], '\n')
                print("Would you like to chnage <", masterNameList[index][0], "> to ", masterNameList[index][1], " ? [y/n]")
                changeGrade = input()
                if changeGrade == 'y':
                    checkNameList[index][1] = masterNameList[index][1]
                else:
                    continue
                gradeCountDict[checkNameList[index][1]] += 1
                gradeCountDict_master[kid[1]] += 1
                index += 1
    if DEBUG: #DEBUG
        print(gradeCountDict)
        print(gradeCountDict_master)

        
    for key in gradeCountDict_master:
        print("Students in", key, "on the box list: ", gradeCountDict[key])
        print("Students in", key, "on the master list: ", gradeCountDict_master[key])
        if gradeCountDict_master[key] == gradeCountDict[key]:
            setColour(green)
            print(key, "has", gradeCountDict_master[key], "kids on both lists")
            setColour(white)
        elif gradeCountDict_master[key] > gradeCountDict[key]: # If the master list has more kids in a given grade than the box list
            setColour(red)
            print("ERROR: Grade count inconsistency")
            print("The MASTER list has", gradeCountDict_master[key] - gradeCountDict[key], "more kid(s) in", key, "than the BOX list")
            setColour(white)
        elif gradeCountDict_master[key] < gradeCountDict[key]: # If the box list has more kids in a grade than the master list
            setColour(red)
            print("ERROR: Grade count inconsistency")
            print("The BOX list has", gradeCountDict[key] - gradeCountDict_master[key], "more kid(s) in", key, "than the MASTER list")
            setColour(white)
        print('\n')


    return



def spellCheck(masterNameList, checkNameList, masterFile, checkFile):
    # FUNCTION MAY BE FINISHED

    print("----------------------------------------------------------------------")
    print("CHECKING FOR SPELLING ERRORS AND MISSING KIDS")

    masterStudentList = {} # List to keep track of only the students name
    checkStudentList = {}


    for i in range(len(masterFile['Student'])):
        if pd.isnull(masterFile.at[i, 'Student']):
            continue
        else:
            masterStudentList[masterFile['Student'][i]] = i 
    if DEBUG == True: #DEBUG
        print(masterStudentList)

    for i in range(len(checkFile['Student'])):
        if pd.isnull(checkFile.at[i, 'Student']):
            continue
        else:
            checkStudentList[checkFile['Student'][i]] = i
    if DEBUG == True: #DEBUG
        print(checkStudentList) #The dictionary with the student from the box list

        print(checkFile)
    for index in range(len(checkNameList)):
        if checkNameList[index][0] == masterNameList[index][0]:
            index += 1
            continue
        else:
            setColour(red)
            print("ERROR: INCORRECT NAME")
            setColour(white)
            print("Name on master list: ", masterNameList[index][0])
            print("Name on box list: ", checkNameList[index][0])
            print("Would you like to correct the name to <", masterNameList[index][0], "> from the master list? [y/n]")
            fixName = input()
            print('\n')

            if fixName == 'y':
                checkFile.loc[checkStudentList[checkNameList[index][0]], 'Student'] = masterNameList[index][0]
                checkNameList[index][0] = masterNameList[index][0] # Correct the spelling in the list

            elif fixName == 'n':
                # IF THEY SELECT NO FOR FIXING TBE SPELLING THEN IT IS LIKELEY A MISSING KID AND WE SHOULD ADD THE NAME TO THE BOX LIST
                """
                nameInList = False
                for name in masterStudentList:
                    if checkNameList[index][0] == name:
                        nameInList = True
                        break
                    else:
                        nameInList = False
                        continue
                """
                    # IF THE KID NEEDS TO BE ADDED
                if True:
                    print("< ", masterNameList[index][0], "> is on the master list")
                    print("Would you like to add <", masterNameList[index][0], "> to the box list in", masterNameList[index][1], "[y/n]?")
                    addName = input()

                    if addName == 'y':

                        if DEBUG == True:
                            print(masterNameList[index][0])

                        nameIndex = masterFile[masterFile['Student'] == masterNameList[index][0]].index[0]
                        line = pd.DataFrame({'School': np.nan, 'Grade': np.nan, 'Student': masterNameList[index][0], 'Delivery Type': 'School'}, index = [nameIndex])
                        checkFile = pd.concat([checkFile.iloc[:nameIndex], line, checkFile.iloc[nameIndex:]]).reset_index(drop = True)
                        checkNameList.append([masterNameList[index][0], masterNameList[index][1]])
                        checkNameList = sorted(checkNameList)
                        print(checkNameList)
                        print('\n')
                        print(masterNameList)
                        index = 0
                        spellCheck(masterNameList, checkNameList, masterFile, checkFile)
                        addName == ''
                    else:
                        print("< ", checkNameList[index][0], "> is not on the master list")
                        print("Would you like to remove <", checkNameList[index][0], "> from the box list? [y/n]")
                        removeName = input()
                        if removeName == 'y':
                            checkFile = checkFile.drop(labels = index, axis = 0).reset_index(drop = True)
                            checkNameList.remove(checkNameList[index][0])
                            checkNameList = sorted(checkNameList)
                            index = 0
                            spellCheck(masterNameList, checkNameList, masterFile, checkFile)
                        addName = ''
                
                if DEBUG == True:
                    print(checkFile)
                    print(checkNameList)
                    print(masterNameList)
    spellCheck(masterNameList, checkNameList, masterFile, checkFile)
    if DEBUG == True: #DEBUG
        print(checkFile)
    return checkFile, checkNameList # Return the cheeckFile so that you can compare it with correct spelling to the master file


def boxCheck(checkNameList, masterNameList): #FIXME these parameters are wrong, this should only take the number of students from the master list but not a list with the box numbers, as there will be none
    """
    - CHECK FOR MISSING BOX NUMBERS
    - CHECK FOR DUPLICATE BOX NUMBERS
    - CHECK TO MAKE SURE THE TOTAL HOME COUNT AND NUMBER COUNT ADD UP TO THE TOTAL STUDENTS
    - CHECK TO MAKE SURE THAT THE TOTAL NUMBER OF BOX NUMBERS ADDS TO THE TOTAL NUMBER OF STUDENT WITH THE "SCHOOL" DELIVERY TYPE IN THE MASTER LIST
    - CHECK TO MAKE SURE THAT THE NUMBER OF STUDENTS ON BOTH LISTS WITH THE HOME TAG IS CORRECT
    - FOR EVERY SHARED DUPLICATE BOX NUMBER, POP THE LAST NUMBER FROM POTENTIAL NUMS. THIS WILL MAKE IT SO THAT THE LAST FEW NUMBERS ARENT ALWAYS MISSING
    """

    boxNumList = []
    boxHomeCount = 0
    boxSchoolCount = 0
    deliveryErrorList = []
    masterSchoolCount = 0
    masterHomeCount = 0
    boxNameList = [] # List of NAMES ONLY from the box list
    totalNameList = [] # List of NAMES ONLY from the master list

    for kid in checkNameList:
        boxNameList.append(kid[0])
        if kid[2].isnumeric() == True:
            boxNumList.append(int(kid[2]))
            boxSchoolCount += 1
        elif kid[2] == 'Home':
            print(kid) #DEBUG
            boxHomeCount += 1
        else:
            message = '<', kid[0], '> in ', kid[1], ' is missing a box number/home tag'
            deliveryErrorList.append(message)
    boxNumList = sorted(boxNumList)
    #for num in boxNumList:
        #print(num) #DEBUG
    for student in masterNameList:
        totalNameList.append(student[0])
        if student[2] == 'School':
            masterSchoolCount += 1
        elif student[2] == 'Home':
            masterHomeCount += 1
    print("THERE ARE THIS MANY KIDS IN TOTAL:", len(totalNameList)) #DEBUG
    print("THERE ARE THIS MANY KIDS ON THE BOX LIST:", len(boxNameList)) #DEBUG
    correctCount = 0
    missingNumList = []
    checkedNums = []
    duplicateNums = []
    for i in range(len(boxNumList)): # FIX THIS ALGORITHM
        #print(boxNumList[i]) #DEBUG
        if i + 1 in checkedNums:
            duplicateNums.append(i + 1)
            boxNumList.remove(i + 1)
            continue
        elif i + 1 == int(boxNumList[i]):
            checkedNums.append(i + 1)
            correctCount += 1
            continue
        else:
            missingNumList.append(i + 1)
            boxNumList.append(i+1)
            boxNumList = sorted(boxNumList)

    print("\nThere are ", boxSchoolCount, 'kids with box numbers on the BOX list')
    print("There are ", masterSchoolCount, ' kids with the school delivery type on the MASTER list\n')
    if boxSchoolCount == correctCount:
        setColour(green)
        print('Boxes 1 through ', boxNumList[-1], ' are all accounted for')
        setColour(white)
    else:
        setColour(red)
        for i in range(len(missingNumList)):
            print('Box number ', missingNumList[i], ' is missing')
    for num in duplicateNums:
        print("The box number ", num, " appears twice")
    setColour(white)

    print("\nThere are ", boxHomeCount, " kids with Home tags on the BOX list")
    print("There are ", masterHomeCount, " kids with the Home delivery type on the MASTER list\n")

    setColour(red)
    for i in range(len(deliveryErrorList)):
        print(deliveryErrorList[i])
    setColour(white)

    return None


def nameCheck(checkNameList, masterNameList):
    
    missingList = []
    notOnBoxList = []
    accountedForList = []
    correctCount = 0
    totalCount = 0

    for i in range(len(masterNameList)):
        totalCount += 1
    
    for iBox in range(len(checkNameList)):
        boxKid = checkNameList[iBox]
        missingFlag = True
        for iMaster in range(len(masterNameList)):
            masterKid = masterNameList[iMaster]
            if boxKid[0] == masterKid[0]:
                accountedForList.append(masterKid[0])
                setColour(green)
                print(boxKid[0], '\t', 'MATCHES', '\t', masterKid[0])
                setColour(white)
                correctCount += 1
                missingFlag = False
                break
        if missingFlag == True:
            missingList.append(boxKid)

    for kid in missingList:
        checkNameList.remove(kid)

    for kid in masterNameList:
        missingFlag = True
        for student in accountedForList:
            if kid[0] == student:
                missingFlag = False
                break
        if missingFlag == True:
            notOnBoxList.append(kid)

    setColour(red)
    for kid in missingList:
        print(kid, " has no match")
    print('\n')
    for student in notOnBoxList:
        print(student, " has no match")
    setColour(white)
    print("Number of correct stduents:", correctCount)
    print("Total number of students", totalCount)

    for name in missingList:
        for student in notOnBoxList:
            print("Does the name <", name[0], "> on the BOX list match with the name <", student[0], "> on the MASTER list? [y/n]")
            choice = input()
            """
            while choice != 'y' or choice != 'n':
                print("Invalid input, please enter y or n")
                choice = input()
            """
            if choice == 'n':
                continue
            elif choice == 'y':
                print('Would you like to fix the spelling of the name on the BOX list to <', student[0], '> from the MASTER list? [y/n]')
                fixSpell = input()
                print('\n')
                """
                while fixSpell != 'y' or fixSpell != 'n':
                    print("Invalid input, please enter y or n")
                    fixSpell = input()
                """
                if fixSpell == 'y':
                    notOnBoxList.remove(student)
                    name[0] = student[0]
                    break
        
     
    for kid in notOnBoxList:
        print("<", kid[0], "> was missing from the box list, would you like to add ", kid[0], " to the box list in ", kid[1], "? [y/n]")
        addToBox = input()
        if addToBox == 'y':
            if kid[2] == 'School':
                checkNameList.append(kid)
            else:
                student = copy.deepcopy(kid)
                student[2] = "NULL"
                checkNameList.append(student)
        else:
            continue

    for kid in missingList:
        checkNameList.append(kid)

    checkNameList = sorted(checkNameList)
            

    return checkNameList

#Windsor Park 2024.csv

compareBoxLists(file2, file1, file2_name, file1_name)

