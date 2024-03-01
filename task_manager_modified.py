# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
#==========Function section==========
# Function 1: reg_user is called when the user selects 'r' to register a user.
        
def reg_user(menu_choice):

    if menu_choice == 'r':

        #Add a new user to the user.txt file
        # - Request input of a new username
        new_username = input("New Username: ")

        #check whether user name exist
        ex_user_name=list(username_password.keys())
        #ask user to enter new name if name is already exist
        while new_username in ex_user_name:
            print ("User name is already exist, please choose a different name")
            new_username = input("New Username: ")
        #if name is not exist continue to request password
        if new_username not in ex_user_name:
            # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                username_password[new_username] = new_password
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                return("New user added")
            # - Otherwise you present a relevant message.
            else:
                print("Passwords do no match")
#Function 2: add_task is called when a user selects 'a' to add a new task. 
def add_task (menu_choice):
    if menu_choice == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            task_title = input("Title of Task: ")
            task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        # Then get the current date.
        curr_date = datetime.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        return("Task successfully added.")
    #Function 3: view_all is called when a user selects 'va' to view all tasks listed in tasks.txt.
def view_all(menu_choice):
    if menu_choice == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
        return("End of task")   
#Function 4: view_mine is called when a user selects 'vm' to view all tasks assigned to them.
def view_mine(menu_choice, username):
    if menu_choice == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
        '''
        #display task with a corresponding number
        #create a value start with 1 to mark the task number
        i=1
        #create an empty dict to store task assigned to the curr_user
        list_of_task={}
        #an empty list to store key and value of dict above
        temp_list=[]
        for t in task_list:
            try:
                if t['username'] == curr_user:
                    list_of_task['Task number']=i
                    list_of_task['Task']=t['title']
                    list_of_task['Assigned']=t['username']
                    list_of_task['Date Assigned']= t['assigned_date'].strftime(DATETIME_STRING_FORMAT)
                    list_of_task['Due Date']= t['due_date'].strftime(DATETIME_STRING_FORMAT)
                    list_of_task['Task Description']=t['description']
                    list_of_task['completed']=t['completed']
                    i+=1
                    for k,v in list_of_task.items():
                        temp=[k,v]
                        temp_list.append(temp)
                    for k,v in list_of_task.items():
                        print('{}:{}'.format(k,v),end="\n")
            except:
                if t['username']!= curr_user:
                    pass
        #if there is no task print no assigned task
        if len(temp_list)==0:
            print("No assigned task")
            pass
        #if there is task display them
        elif len(temp_list)!=0:   
        #display list of task for user to choose or -1 to return to main menu   
            user_choice=int(input("Please select \n a task by enter the task number \n or enter -1 to return to the main menu"))
        #return if user choose -1
            if user_choice==-1:
                pass
        #if user_choice is out of the task list range then print relevant message
            elif user_choice >(len(temp_list)/7): 
                print("You dont have that task. Please choose the correct task number")
            elif user_choice!=-1 and len(temp_list)==0:
                print("You dont have any task")
        #if user choose a number within the range of all the
        #task assigned to curr_user which store under temp_list
        #the list will be displayed is 7 pices of information of the task based on the task number
        #chosen by user. For example, if user choose number 1, disp_list
        #will contain 7 pieces of info from (0-> 7) =(1-1)*7 -> 1*7 or 
        #(user_choice-1)*7->user_choice*7
            elif user_choice!=-1 and user_choice <= (len(temp_list)/7): 
                disp_list=temp_list[((user_choice-1)*7):((user_choice)*7)]
                print("You have chosen task: \n")
                for s in disp_list:
                    print(*s)
                #request input from user to see what user want to do with the task 1 to mark as
                #completed or 2 to edit it
                next_choice=int(input("\n Please choose 1 to mark task as complete or 2 to edit task: "))
                    #if user want to mark it, loop through all task list
                    #if username is same with curr_user, task title is same with the task 
                    #title display above within disp_list. If it is completed print user 
                    #can not change its status, if it not change the value of complete of such
                    #task into true.
                    #once done open tasks.txt to overwrite data to update what has been changed by user
                if next_choice==1:
                    for j in range(len(task_list)):
                        try:
                            if task_list[j]['username']==curr_user and task_list[j]['title']==disp_list[1][1]and task_list[j]['completed']==True:
                                print("The chosen task has been completed and can not change its status")
                            elif task_list[j]['username']==curr_user and task_list[j]['title']==disp_list[1][1]and task_list[j]['completed']==False:
                                task_list[j]['completed']=True
                                with open("tasks.txt", "w") as task_file:
                                    ls_ed=[]
                                    for t in task_list:
                                        str_attrs_ed = [t['username'],
                                                        t['title'],
                                                        t['description'],
                                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                                        "Yes" if t['completed'] else "No"
                                                        ]
                                        ls_ed.append(";".join(str_attrs_ed))
                                    task_file.write("\n".join(ls_ed))
                                    return("Task successfully edited.")
                        except IndexError:
                            pass
                    #if user choose to edit task, print task can not be edited if the task is already completed
                    #it has been completed allow user to edit name and due date
                    #after get the input from user open the file to overwrite new data into txt file
                elif next_choice==2:
                    #add the choice for user to choose to edit user name or the due date
                    edit_choice=input("Please type in 'N' to assign a new name, or 'D' to assign new date:")
                    #in case user want to edit name check if the task has been completed or not
                    #if it is completed show message of not allowing user to edit it
                    #if it has not been completed allow user to input new user name and edit it in the main task file
                    if edit_choice=='N':
                        for a in range(len(task_list)):
                            try:
                                if task_list[a]['username']==curr_user and task_list[a]['title']==disp_list[1][1]and task_list[a]['completed']==True:
                                    return("The chosen task has been completed and can not be edited")
                                elif task_list[a]['username']==curr_user and task_list[a]['title']==disp_list[1][1]and task_list[a]['completed']==False:
                                    user_ed = input("Edit Username to:\t")
                                    if user_ed != "":
                                        task_list[a]['username'] = user_ed
                                    with open("tasks.txt", "w") as task_file:
                                        ls_ed2=[]
                                        for t in task_list:
                                            str_attrs_ed2 = [
                                                    t['username'],
                                                    t['title'],
                                                    t['description'],
                                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                                    "Yes" if t['completed'] else "No"
                                                    ]
                                            ls_ed2.append(";".join(str_attrs_ed2))
                                        task_file.write("\n".join(ls_ed2))
                            except IndexError:
                                pass
                        return("Task successfully edited.")
                    #in case user want to edit due date check if the task has been completed or not
                    #if it is completed show message of not allowing user to edit it
                    #if it has not been completed allow user to input new due date and edit it in the main task file
                    elif edit_choice=="D":
                        for a in range(len(task_list)):
                            try:
                                if task_list[a]['username']==curr_user and task_list[a]['title']==disp_list[1][1]and task_list[a]['completed']==True:
                                    print("The chosen task has been completed and can not be edited")
                                elif task_list[a]['username']==curr_user and task_list[a]['title']==disp_list[1][1]and task_list[a]['completed']==False:
                                    due_date_ed = input("Edit Due Date to:\t")
                                    due_date_ed_f=datetime.strptime(due_date_ed, DATETIME_STRING_FORMAT)
                                    if due_date_ed != "":
                                        task_list[a]['due_date'] = due_date_ed_f
                                    with open("tasks.txt", "w") as task_file:
                                        ls_ed2=[]
                                        for t in task_list:
                                            str_attrs_ed2 = [
                                                    t['username'],
                                                    t['title'],
                                                    t['description'],
                                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                                    "Yes" if t['completed'] else "No"
                                                    ]
                                            ls_ed2.append(";".join(str_attrs_ed2))
                                        task_file.write("\n".join(ls_ed2))
                            except IndexError:
                                pass
                        return("Task successfully edited.")
                    else:
                        return("Invalid input")
                else:
                    return("Invalid input")
        else:
            return("Invalid input")
#Function 5: Generating text files 'task_overview.txt' and 'user_overview.txt'.
def generate_reports():
# If the user inputs 'gr' reports are generated with statistics
    if menu=="gr":
        # Open the files and set them to write. If the files don't exist they
        # will be created automatically.
        #calculate total task, completed task, incompleted task
        #overdue task, percentage incomplete and overdue
        if curr_user=="admin":
            with open("task_ov.txt","w+") as task_ov:
                total_tasks = len(task_list)
                num_completed = 0
                num_incomplete = 0
                num_inc_overdue = 0
                per_incomplete = 0
                per_overdue = 0
                for x in range(len(task_list)):
                    if task_list[x]['completed']==True:
                        num_completed +=1
                    elif task_list[x]['completed']==False:
                        num_incomplete+=1
                        if task_list[x]['due_date']>datetime.today():
                            num_inc_overdue +=1
                #to avoid there is no task (divide 0 error)
                if total_tasks == 0:
                    per_incomplete = 0
                    per_overdue = 0
                else:
                    per_incomplete = round(100*num_incomplete/total_tasks)
                    per_overdue = round(100*num_inc_overdue/total_tasks)
                task_ov.write("Task overview \n")
                task_ov.write(f"Total Tasks:\t\t{total_tasks}\nCompleted Tasks:\t{num_completed}\nIncomplete Tasks:\t{num_incomplete}\nOverdue Tasks:\t\t{num_inc_overdue}\nPortion Incomplete:\t{per_incomplete}%\nPortion Overdue:\t{per_overdue}%")
            #generate report for user, with task of such user
            #number of incompleted task, over due and percentage of that users' tasks
            with open("user_ov.txt","w+") as user_ov:
                users=[(k,v) for k,v in username_password.items()]
                num_users = len(users)
                total_tasks = len(task_list)
                user_ov.write(f"Total Users:\t\t{num_users}\n")
                user_ov.write(f"Total Tasks:\t\t{total_tasks}")
                #loop through each user in the list
                for x in range(num_users):
                    num_tasks = 0
                    num_completed = 0
                    num_incomplete = 0
                    num_inc_overdue = 0
                    per_incomplete = 0
                    per_overdue = 0
                    per_completed = 0
                    por_tasks = 0
                    user_ov.write("\n----------------------------------------------------\n")
                    user_ov.write(f"User:\t\t\t\t\t{users[x][0]}\n")

                    #loop through task list to see which one is assigned to which user
                    for y in range(total_tasks):
                        if task_list[y]['username']==users[x][0]:
                            num_tasks+=1
                            if task_list[y]['completed']==True:
                                num_completed+=1
                            elif task_list[y]['completed']==False:
                                num_incomplete+=1
                                if task_list[y]['due_date']>datetime.today():
                                    num_inc_overdue+=1
                    if num_tasks == 0:
                        per_incomplete = 0
                        per_overdue = 0
                        per_completed = 0
                    else:
                        per_incomplete = round(100*num_incomplete/num_tasks)
                        per_overdue = round(100*num_inc_overdue/num_tasks)
                        per_completed = round(100*num_completed/num_tasks)

                    if total_tasks == 0:
                        por_tasks = 0
                    else:
                        por_tasks = round(100*num_tasks/total_tasks)
                    user_ov.write(f"User Tasks:\t\t\t\t{num_tasks}\nPortion Total Tasks:\t\t{por_tasks}%\nPortion Completed:\t\t{per_completed}%\nPortion Incomplete:\t\t{per_incomplete}%\nPortion Overdue:\t\t{per_overdue}%")
                    user_ov.write("\n----------------------------------------------------\n")
        else:
            return("\nYou are not authorised to use this.\n")
#Function 6: to display report for admin users
def data_statistic():
    if menu=='ds'and curr_user=="admin":
        #generate the task_ov and user_ov file in case the gr function hasnt been called yet
        #The code for this part is identical to the code in gr function
        with open("task_ov.txt","w+") as task_ov:
                total_tasks = len(task_list)
                num_completed = 0
                num_incomplete = 0
                num_inc_overdue = 0
                per_incomplete = 0
                per_overdue = 0
                for x in range(len(task_list)):
                    if task_list[x]['completed']==True:
                        num_completed +=1
                    elif task_list[x]['completed']==False:
                        num_incomplete+=1
                        if task_list[x]['due_date']>datetime.today():
                            num_inc_overdue +=1
                #to avoid there is no task (divide 0 error)
                if total_tasks == 0:
                    per_incomplete = 0
                    per_overdue = 0
                else:
                    per_incomplete = round(100*num_incomplete/total_tasks)
                    per_overdue = round(100*num_inc_overdue/total_tasks)
                task_ov.write("Task overview \n")
                task_ov.write(f"Total Tasks:\t\t{total_tasks}\nCompleted Tasks:\t{num_completed}\nIncomplete Tasks:\t{num_incomplete}\nOverdue Tasks:\t\t{num_inc_overdue}\nPortion Incomplete:\t{per_incomplete}%\nPortion Overdue:\t{per_overdue}%")
            #generate report for user, with task of such user
            #number of incompleted task, over due and percentage of that users' tasks
        with open("user_ov.txt","w+") as user_ov:
            users=[(k,v) for k,v in username_password.items()]
            num_users = len(users)
            total_tasks = len(task_list)
            user_ov.write(f"Total Users:\t\t{num_users}\n")
            user_ov.write(f"Total Tasks:\t\t{total_tasks}")
            #loop through each user in the list
            for x in range(num_users):
                num_tasks = 0
                num_completed = 0
                num_incomplete = 0
                num_inc_overdue = 0
                per_incomplete = 0
                per_overdue = 0
                per_completed = 0
                por_tasks = 0
                user_ov.write("\n----------------------------------------------------\n")
                user_ov.write(f"User:\t\t\t\t\t{users[x][0]}\n")

                #loop through task list to see which one is assigned to which user
                for y in range(total_tasks):
                    if task_list[y]['username']==users[x][0]:
                        num_tasks+=1
                        if task_list[y]['completed']==True:
                            num_completed+=1
                        elif task_list[y]['completed']==False:
                            num_incomplete+=1
                            if task_list[y]['due_date']>datetime.today():
                                num_inc_overdue+=1
                if num_tasks == 0:
                    per_incomplete = 0
                    per_overdue = 0
                    per_completed = 0
                else:
                    per_incomplete = round(100*num_incomplete/num_tasks)
                    per_overdue = round(100*num_inc_overdue/num_tasks)
                    per_completed = round(100*num_completed/num_tasks)

                if total_tasks == 0:
                    por_tasks = 0
                else:
                    por_tasks = round(100*num_tasks/total_tasks)
                user_ov.write(f"User Tasks:\t\t\t\t{num_tasks}\nPortion Total Tasks:\t\t{por_tasks}%\nPortion Completed:\t\t{per_completed}%\nPortion Incomplete:\t\t{per_incomplete}%\nPortion Overdue:\t\t{per_overdue}%")
                user_ov.write("\n----------------------------------------------------\n")
        #Print out each line in the task_ov and user_ov file to display
        #on the screen the reports 
        print("Here is the overview of users \n")
        with open("user_ov.txt","r") as user_ov:
            for line in user_ov:
                print(line)
        print("\nHere is the overview of task \n")
        with open("task_ov.txt","r") as task_ov:
            for line in task_ov:
                print(line)
    #==========Display the menu================
    #Indefinite loop created to display the menu once the user is logged in.
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports                
    ds - Display statistics
    e - Exit
    : ''').lower() 
    
    if menu == "r":  # Choosing 'r' from the menu causes the reg_user function to be called.

        print(reg_user(menu))

    elif menu == "a":

        print(add_task(menu))

    elif menu == "va":  # Choosing 'va' from the menu causes the view_all function to be called.

        print(view_all(menu))

    elif menu == "vm":  # Choosing 'vm' from the menu causes the view_mine function to be called.

        print(view_mine(menu, username))

    elif menu == "gr":  # Choosing 'gr' from the menu causes text files user_overview and task_overview to be generated.

        print(generate_reports())  # Calling function to generate report files.
        
    elif menu == 'ds':

        print(data_statistic())  # Calling function generate files in case they do no exist yet.
    
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("You have made a wrong choice, Please Try again")



    







        



                
                