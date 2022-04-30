from emp import FullTimeEmployee , Department , PartTimeEmployee , Company
from emp import LeaveApplicationException , Leave , VaccinationLeave , Manager
from objects import company , dpt1 , dpt2

from datetime import datetime
def verifyDate(date_string):
    format = "%d/%m/%Y"
    try:
        res = bool(datetime.strptime(date_string, format))
        return True
    except ValueError:
        res = False



def getMenu():
    menu =f"""
    Menu
    ======
    1. Apply Leave
    2. Cancel Leave
    3. Display Employee Leave Profile
    4. Daily Movement Update
    5. Update Safe Management Measure Percentage
    6. Display Departments' SMM status
    0. Exit"""
    print(menu)
    option = input("Enter option:  ")

    return option

from datetime import date
option = getMenu()
while True:
    if option == "1":
        ID =input("Enter employee ID: ")
        dept = input("Enter employee's department:  ")
        if not (dpt1.searchEmployee(int(ID)) or dpt2.searchEmployee(int(ID))):
            print("No such employee, please retry ")
            option = getMenu()
        elif not (dept == dpt1.get_name() or dept == dpt2.get_name()):
            print("No such department, please retry ")
            option = getMenu()
        else:
            from_date = input("Enter from-date in dd/mm/yyyy: ")
            to_date = input("Enter to-date in dd/mm/yyyy: ")
            #verify date
            while not verifyDate(from_date):
                print(f"{from_date} is not in the format dd/mm/yyyy")
                from_date = input("Enter from-date in dd/mm/yyyy: ")
            while not verifyDate(to_date):
                print(f"{to_date} is not in the format dd/mm/yyyy")
                to_date = input("Enter to-date in dd/mm/yyyy: ")

            dpt_obj = dpt1 if  dpt1.searchEmployee(int(ID)) else dpt2
            vac_leave = input("Vaccination leave? (Y/N):")
            while (vac_leave not in ["Y" , "N" , "y" , 'n']):
                print("Select the right option")
                vac_leave = input("Vaccination leave? (Y/N):")

            if vac_leave.upper() == "N":
                 leave_obj = Leave(dpt_obj.searchEmployee(int(ID)) , f"{from_date}" , f"{to_date}")
            else:
                leave_obj = VaccinationLeave(dpt_obj.searchEmployee(int(ID)) , f"{from_date}" , f"{to_date}")

            try:
                day1 , month1 , year1 = from_date.split("/")
                day2 , month2 , year2 = to_date.split("/")
                from_date = date(int(year1) , int(month1) , int(day1))
                to_date = date(int(year2) , int(month2) , int(day2))
                if  company.overlappingLeave(int(ID) ,from_date , to_date):
                    raise LeaveApplicationException("Leave request should not overlap with approved leaves")
                elif from_date.weekday()>=5:
                    raise LeaveApplicationException("Leave request should not have from-date on weekend")
                else:
                    company.addLeave(leave_obj)
                    print("Leave Request added!!")
                    leave_obj.__str__()
            except Exception as e:
                print(e)


        option = getMenu()
    elif option == "2":
        ID =input("Enter employee ID: ")
        req_id = input("Enter leave request ID to cancel: ")
        if not (dpt1.searchEmployee(int(ID)) or dpt1.searchEmployee(int(ID))):
            print("No such employee, please retry ")
            option = getMenu()
        company.cancelLeave(int(ID) , int(req_id))
        print()
        option = getMenu()
    elif option == "3":
        ID =input("Enter employee ID: ")
        dept = input("Enter employee's department:  ")
        if not (dpt1.searchEmployee(int(ID)) or dpt1.searchEmployee(int(ID))):
            print("No such employee, please retry ")
            option = getMenu()
        elif not (dept == dpt1.get_name() or dept == dpt2.get_name()):
            print("No such department, please retry ")
            option = getMenu()
        else:
            dpt_obj = dpt1 if  dpt1.searchEmployee(int(ID)) else dpt2
            dpt_emp = dpt_obj.searchEmployee(int(ID))
            all_leaves = company.getLeave(int(ID))
            dpt_emp.__str__()
            for each_leave in all_leaves:
                each_leave.__str__()
                print("")
        option = getMenu()
    elif option == "4":
        ID =input("Enter employee ID: ")
        dept = input("Enter employee's department:  ")
        if not (dpt1.searchEmployee(int(ID)) or dpt1.searchEmployee(int(ID))):
            print("No such employee, please retry ")
            option = getMenu()
        elif not (dept == dpt1.get_name() or dept == dpt2.get_name()):
            print("No such department, please retry ")
            option = getMenu()
        else:
            dpt_obj = dpt1 if  dpt1.searchEmployee(int(ID)) else dpt2
            dpt_emp = dpt_obj.searchEmployee(int(ID))

            print(f"Current work from home status is {dpt_emp._WorkFromHome}")
            vac_leave = input("Change the status? (Y/N): ")
            while (vac_leave not in ["Y" , "N" , "y" , 'n']):
                print("Select the right option")
                vac_leave = input("Change the status? (Y/N): ")
            if vac_leave.upper() == "Y":
                dpt_emp._WorkFromHome = False if dpt_emp._WorkFromHome else True
            else:
                pass

        option = getMenu()
    elif option == "5":
        print(f"Current Safe Management Measure % is {company.getSafeManagementPercentage()}")
        new_safe = input("Enter new Safe Management Measure %:  ")

        try:
            new_safe = int(new_safe)
        except Exception as e:
            new_safe = input("Re-Enter new Safe Management Measure %:  ")
        while (new_safe >100 or new_safe <0):
            print("Sorry, please re-enter within range (0, 100)")
            new_safe = input("Enter new Safe Management Measure %:  ")
            new_safe = int(new_safe)
        company.setSafeManagementPercentage(new_safe)
        print(f"Safe Management Measure % updated to {new_safe}")

        option = getMenu()
    elif option =="6":
        print(f"Company: {company._name}   UEN:  {company._uniqueEntityNumber}\n")
        for dpt in company._departments:
            dpt.__str__()
            dpt.safeManagementCheck(40)
            print("")
        exit(1)
    elif option == "0":
        print("Exiting....")
        exit(1)
    else:
        option =getMenu()
