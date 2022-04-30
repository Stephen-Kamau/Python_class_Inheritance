from emp import FullTimeEmployee , Department , PartTimeEmployee , Company
from emp import LeaveApplicationException , Leave , VaccinationLeave , Manager

manager_1 = Manager(106 ,"Tom" , False , 4)
manager_2 = Manager(201 ,"Neil" , False ,4 )
dpt1 = Department("IT Helpdesk"  , manager_1, True)
dpt2 = Department("Marketing" ,manager_2 , False)


# add employees to _departments
dpt1.addEmployee(FullTimeEmployee(101 ,"Jeff" , False , 4))
dpt1.addEmployee(FullTimeEmployee(102 ,"Jim" , True , 4))
dpt1.addEmployee(FullTimeEmployee(104 ,"Jack" , True , 2))
dpt1.addEmployee(FullTimeEmployee(105 ,"Jane" , False , 1))
dpt2.addEmployee(FullTimeEmployee(205 ,"Charles" , False , 4))
dpt2.addEmployee(FullTimeEmployee(203 ,"Elliot" , False , 3))
# add part time employee
dpt1.addEmployee(PartTimeEmployee(103 ,"Joe" , False , 20))
dpt2.addEmployee(PartTimeEmployee(204 ,"Darren" , True , 32))
dpt2.addEmployee(PartTimeEmployee(202 ,"fred" , True , 10))




# company.__str__()


# test leave class



leave1 = Leave(dpt1.searchEmployee(101) , "30/6/2021" , "5/7/2021")
leave2 = Leave(dpt1.searchEmployee(101) , "15/7/2021" , "19/7/2021")
leave3 = Leave(dpt1.searchEmployee(103) , "29/6/2021" , "6/7/2021")
leave4 = VaccinationLeave(dpt1.searchEmployee(104) , "30/6/2021" , "30/6/2021")
leave5 = Leave(dpt1.searchEmployee(105) , "30/6/2021" , "5/7/2021")
leave5 = Leave(dpt1.searchEmployee(105) , "7/7/2021" , "22/7/2021")
leave7 = VaccinationLeave(dpt1.searchEmployee(106) , "30/6/2021" , "30/6/2021")
leave8 = VaccinationLeave(dpt1.searchEmployee(106) , "30/7/2021" , "30/7/2021")
leave9 = Leave(dpt2.searchEmployee(201) , "30/6/2021" , "5/7/2021")
leave10 = VaccinationLeave(dpt2.searchEmployee(201) , "6/7/2021" , "6/7/2021")
leave11 = Leave(dpt2.searchEmployee(205) , "30/6/2021" , "5/7/2021")
leave12 = VaccinationLeave(dpt2.searchEmployee(205) , "30/7/2021" , "30/7/2021")
leave13 = Leave(dpt2.searchEmployee(204) , "30/6/2021" , "5/7/2021")
leave14 = Leave(dpt2.searchEmployee(204) , "7/5/2021" , "15/7/2021")
leave15 = Leave(dpt2.searchEmployee(203) , "30/6/2021" , "5/7/2021")
leave16 = Leave(dpt2.searchEmployee(203) , "9/7/2021" , "13/7/2021")
leave17 = Leave(dpt2.searchEmployee(202) , "5/7/2021" , "8/7/2021")
leave18 = Leave(dpt2.searchEmployee(202) , "13/7/2021" , "13/7/2021")



company = Company("SUSS" , "EDU1002334")
company.addDepartment(dpt1)
company.addDepartment(dpt2)
# update _SAFE_MANAGEMENT_PERCENTAGE to 40
company.setSafeManagementPercentage(40)


company.addLeave(leave1)
company.addLeave(leave2)
company.addLeave(leave3);
company.addLeave(leave4);
company.addLeave(leave5);
company.addLeave(leave7);
company.addLeave(leave8);
company.addLeave(leave9);
company.addLeave(leave10);
company.addLeave(leave11);
company.addLeave(leave12);
company.addLeave(leave13);
company.addLeave(leave14);
company.addLeave(leave15);
company.addLeave(leave16);
company.addLeave(leave17);
company.addLeave(leave18);
