
from abc import ABC,abstractmethod

class  Employee(ABC):
    def __init__(self , _employeeId , _name , _WorkFromHome):
        self._employeeId = _employeeId
        self._name = _name
        self._WorkFromHome = _WorkFromHome
        self._leaveBalance = 0
    def get_name(self):
        return self._name
    def get_employeeId(self):
        return self._employeeId
    def WorkFromHome(self):
        return self._WorkFromHome
    @abstractmethod
    def getLeaveEntitlement(self):
        return self._leaveBalance
    def adjustLeave(self , adjustment):
        self._leaveBalance= adjustment
    def __str__(self):
        if self.WorkFromHome():
            wfh ="YES"
        else:
            wfh = "NO"
        print(f"ID: {self.get_employeeId()}  Name : {self.get_name()}  Leave Balance: {self._leaveBalance} WFH: {wfh}")


class PartTimeEmployee(Employee):
    _LEAVE_ENTITLEMENT ={4:22 ,3:20 , 2:18 , 1:16}
    def __init__(self ,employeeId ,name , workFromHome , hoursPerWeek):
        super().__init__(employeeId,name,workFromHome)
        self._hoursPerWeek = hoursPerWeek

    def getLeaveEntitlement(self):  #to do
        for hours,leave in PartTimeEmployee._LEAVE_ENTITLEMENT.items():
            if self._hoursPerWeek<=hours:
                return leave
        return 16

    def __str__(self):
        self.adjustLeave(self.getLeaveEntitlement())

        if self.WorkFromHome():
            wfh ="YES"
        else:
            wfh = "NO"
        print(f"ID: {self.get_employeeId()}  Name : {self.get_name()}  Leave Balance: {self._leaveBalance} WFH: {wfh}  Hours/Week: {self._hoursPerWeek}")


class FullTimeEmployee(Employee):
    _LEAVE_ENTITLEMENT = {4:22 ,3:20 , 2:18 , 1:16}
    def __init__(self ,employeeId ,name , workFromHome , grade):
        Employee.__init__(self, employeeId,name,workFromHome)
        self._grade = grade
    def getLeaveEntitlement(self):  #to do
        for grade,leave in FullTimeEmployee._LEAVE_ENTITLEMENT.items():
            if self._grade==grade:
                return leave
        return 16
    def __str__(self):
        self.adjustLeave(self.getLeaveEntitlement())
        if self.WorkFromHome():
            wfh ="YES"
        else:
            wfh = "NO"
        print(f"ID: {self.get_employeeId()}  Name : {self.get_name()}  Leave Balance: {self.getLeaveEntitlement()} WFH: {wfh}  Grade: {self._grade}")

class Manager(FullTimeEmployee):
    _LEAVE_ENTITLEMENT = 25
    def __init__(self,employeeid,name,workFromHome,grade):
        super().__init__(employeeid,name,workFromHome,grade)

    def getLeaveEntitlement(self):
        return Manager._LEAVE_ENTITLEMENT


class Department:
    """docstring for ."""
    def __init__(self , _name:str , _manager:Employee ,_essentialServices:bool):
        self._name = _name
        self._manager = _manager
        self._essentialServices = _essentialServices
        self._employees = []
    def get_name(self):
        return self._name

    def get_essentialServices(self):
        return self._essentialServices

    def searchEmployee(self , employeeId):
        for emp_object in self._employees:
            if emp_object._employeeId == employeeId:
                return emp_object
        if self._manager._employeeId == employeeId:
            return self._manager
        return None

    def addEmployee(self , newEmployee):
        new_employeeId = newEmployee._employeeId
        for emp in self._employees:
            if emp._employeeId == new_employeeId:
                return False
        if self._manager._employeeId == new_employeeId:
            return False
        self._employees.append(newEmployee)
        return True
    def safeManagementCheck(self,percentage):
        Count = 0
        for employee in self._employees:
            if employee._WorkFromHome == True:
                Count+=1
        if self._manager._WorkFromHome == True:
            Count+=1
        rate = ( Count / (len(self._employees) + 1)) * 100
        if self._essentialServices == True:
            return str('No. of Employees working from home:{} ({:.1f}%) - exempted.\n\n'.format(Count,rate))
        elif rate>=percentage:
            return str('No. of Employees working from home:{} ({:.1f}%) - passed requirement.\n\n'.format(Count,rate))
        else:
            return str('No. of Employees working from home:{} ({:.1f}%) - failed requirements\n\n'.format(Count,rate))


    def __str__(self):
        print(f"Department:  {self._name}   Essential Services : {self._essentialServices}")
        print("Manager " , end =" ")
        self._manager.__str__()
        for emp in self._employees:
            emp.__str__()




class Company:
    _SAFE_MANAGEMENT_PERCENTAGE =50.0
    def __init__(self , _name ,_uniqueEntityNumber ):
        self._NEXT_ID =  202100001
        self._leaveApplications = {}
        self._uniqueEntityNumber = _uniqueEntityNumber
        self._name = _name
        self._departments =[]
    def getSafeManagementPercentage(self):
        return Company._SAFE_MANAGEMENT_PERCENTAGE

    def setSafeManagementPercentage(self , newPercentage):
        Company._SAFE_MANAGEMENT_PERCENTAGE = newPercentage
    def searchDepartment(self , name):
        for dpt in self._departments:
            if dpt._name == name:
                return dpt
        return None

    def addDepartment(self , Department):
        for dpt in self._departments:
            if dpt._name == Department._name:
                return False
        self._departments.append(Department)
        return True

    def getLeave(self , employeeId):
        return self._leaveApplications.get(employeeId , [])

    def addLeave(self , leave):
        try:
            employeeId = leave.get_applicant()._employeeId
            startDate = leave.get_fromDate()
            endDate = leave.get_toDate()
            objs = self._leaveApplications.get(employeeId , None)
            if objs:
                leave_vals =objs
            else:
                leave_vals =[]
            if self.overlappingLeave(employeeId , startDate , endDate):
                raise LeaveApplicationException("Dates Must not Overlap")
            else:
                leave._leaveRequestId = self._NEXT_ID
                leave_vals.append(leave)
                self._NEXT_ID+=1
                self._leaveApplications[employeeId] = leave_vals
                leave.get_applicant()._leaveBalance = leave.get_applicant().getLeaveEntitlement() - leave.get_duration()
                #set WORK from home to True if is in today

                return leave
        except Exception as e:
            print(f"Exception  {e}")

    def cancelLeave(self , employeeId , leaveRequestId):
        emp_leaves = self._leaveApplications.get(employeeId , [])
        try:
            if len(emp_leaves)==0:
                raise LeaveApplicationException(f"Employee with {employeeId} not found")
            else:
                for emp_obj in emp_leaves:
                    if emp_obj.get_leaveRequestId() == leaveRequestId:
                        if emp_obj.get_status() == "Approved":
                            emp_obj.set_status("Cancelled")
                            emp_obj.get_applicant().adjustLeave(emp_obj.get_duration())
                            return
            raise LeaveApplicationException(f"Leave with the ID  {leaveRequestId} Not Found")
        except Exception as e:
            print(f"Exception  {e}")

    def overlappingLeave(self , employeeId ,fromDate , toDate):
        emp_leaves = self._leaveApplications.get(employeeId , [])
        for emp in emp_leaves:
            if (toDate <= emp.get_toDate() or emp.get_fromDate() >= toDate):
                return True
        return False

    def getVaccinationLeaveCount(self , employeeId , year):
        count = 0
        emp_leaves = self._leaveApplications.get(employeeId , [])
        if len(emp_leaves)==0:
            return 0
        else:
            for emp in emp_leaves:
                 emp_date = emp.get_fromDate()
                 if emp_date.year == year and emp.get_status()=="Approved":
                     count +=1
            return count

    def __str__(self):
        '''
        function returns a string containting the
        Department information
        '''
        print(f"Company: {self._name}   UEN:  {self._uniqueEntityNumber}\n")
        for dpt in self._departments:
            dpt.__str__()
            print(dpt.safeManagementCheck(self.getSafeManagementPercentage()))
            print("")

# QUESTION 3
from datetime import datetime
from datetime import date
# my_string = '2019/10/31'


class LeaveApplicationException(Exception):
    pass

class Leave:
    _NEXT_ID =  202100001
    def __init__(self , applicant , fromDate , toDate):
        #split date into month day and year
        day1 , month1 , year1 = fromDate.split("/")
        day2 , month2 , year2 = toDate.split("/")
        self._applicant = applicant
        self._leaveRequestId = Leave._NEXT_ID+1
        self._duration =0
        self._fromDate = date(int(year1) , int(month1) , int(day1))
        self._toDate = date(int(year2) , int(month2) , int(day2))
        self._status ="Cancelled"
        try:
            if self._fromDate == self._toDate:
                raise LeaveApplicationException("Date are the same\n")
            elif self._toDate < self._fromDate:
                raise LeaveApplicationException("ToDate must  be greater than from date\n")
            elif self._fromDate.weekday()>=5:
                raise LeaveApplicationException("Dates must not be weekend\n")
            else:
                self._status = "Approved"
                self._duration =abs(self._toDate - self._fromDate).days
        except Exception as e:
            print(f"Exception {e}")

    def set_status(self , newStatus):
        self._status = newStatus
    def get_status(self):
        return self._status
    def get_fromDate(self):
        return self._fromDate
    def get_toDate(self):
        return self._toDate
    def get_duration(self):
        return self._duration
    def get_applicant(self):
        return self._applicant
    def get_leaveRequestId(self):
        return self._leaveRequestId
    def __str__(self):
        res =f"""
        Leave Request ID: {self.get_leaveRequestId()}
        ID: {self._applicant._employeeId}   Name: {self.get_applicant()._name}
        From: {self.get_fromDate()}  to {self.get_toDate()}
        Duration: {self.get_duration() } days
        Status: {self.get_status()}"""
        print(res)
# ID{self._applicant()}\n
class VaccinationLeave(Leave):
    def __init__(self , applicant , fromDate , toDate):
        #super().__init__(applicant , fromDate , toDate)
        day1 , month1 , year1 = fromDate.split("/")
        day2 , month2 , year2 = toDate.split("/")
        self._applicant = applicant
        self._duration = 0
        self._leaveRequestId = Leave._NEXT_ID+1
        self._fromDate = date(int(year1) , int(month1) , int(day1))
        self._toDate = date(int(year2) , int(month2) , int(day2))
        self._status ="Cancelled"
        try:
            if self._fromDate != self._toDate:
                raise LeaveApplicationException("Dates must be same\n")
            elif self._fromDate < date(2020 , 12 , 30):
                raise LeaveApplicationException("Dates must be from 30/12/2020\n")
            elif self._fromDate.weekday()>=5:
                raise LeaveApplicationException("Dates must not be in weekend\n")
            else:
                self._duration = 0
                self.set_status("Approved")
        except Exception as e:
            print(f"Exception : {e}")

    def __str__(self):
        res =f"""
        Leave Request ID: {self.get_leaveRequestId()}
        ID: {self._applicant._employeeId}   Name: {self.get_applicant()._name}
        From: {self.get_fromDate()}  to {self.get_toDate()}
        Duration: {self.get_duration() } day (vaccination)
        Status: {self.get_status()}"""
        print(res)
