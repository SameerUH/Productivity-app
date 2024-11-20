#Student Name: Sameer Ul Haq
#Student ID: w23002216

#Imports
from flask import *

#Making the app:
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#User class which is used to update and access values.
class User():
    def __init__(self, username, password, email, notifications, tasks):
        self.username = username
        self.password = password
        self.email = email
        self.notifications = notifications
        self.tasks = int(tasks)

    def update(self, username, password, email, notifications, tasks):
        self.username = username
        self.password = password
        self.email = email
        self.notifications = notifications
        self.tasks = tasks


#The default user object to be used
current_user = User("username", "password", "email", "notifications", 0)

#Start screen:
@app.route("/")
def start_screen():
    '''

    :return: Start screen
    '''
    # Displays the start screen with the corresponding html file.
    return render_template("start_screen.html")

#Login page:
@app.route("/login_page", methods = ["POST", "GET"])

def login_page():
    '''
    :variables: username and password which is what the user has inputted.
    :return: Either the main home page if what the user has inputted is correct or reloads the login page with an error.
    '''
    error = None
    if request.method == "POST":
        #Stores the user input form the html login page:
        username = request.form['username']
        password = request.form['password']
        #Does a loop to go through the whole users file to check if what the user has inputted is correct.
        user_accounts = open("users.txt", "r")
        for line in user_accounts:
            file_username = line.strip().split(',')[0]
            file_password = line.strip().split(',')[1]
            if username == file_username and password == file_password:
                email = line.strip().split(',')[2]
                notifications = line.strip().split(',')[3]
                tasks = line.strip().split(',')[4]
                #Stores the user information in the current_user object.
                current_user.update(username, password, email, notifications, tasks)
                return redirect(url_for("main_home_page"))
            else:
                #If what the user has inputted is incorrect then an error will occur.
                error = "Invalid username or password, try again"
    #Displays the login page with the corresponding html file and any errors.
    return render_template("login_page.html", error = error)


#Register page:
@app.route("/register", methods = ["POST", "GET"])
def register_page():
    '''
    :input: username, password, email, notifications and tasks.
    :return: a new user for the web app which will be stored in the users file.
    '''

    #Default variables to be used in the future.
    error = None
    number_count = 0
    upper_count = 0
    lower_count = 0
    if request.method == "POST":
        #Stores the user input as variables.
        username = request.form['username']
        password = request.form['password']
        reenter = request.form['re-enter']
        email = request.form['email']
        notifications = request.form['notifications']
        tasks = 0
        #Goes through a series of if statements to see if the password is secure or not.
        for char in password:
            if char.isdigit():
                number_count += 1
            elif char.isupper():
                upper_count += 1
            elif char.islower():
                lower_count += 1
        if password != reenter:
            error = "The passwords do not match, try again"
        elif len(password) < 8:
            error = "The length of the password is too short, should be a minimum of 8 characters"
        elif number_count == 0:
            error = "The password doesn't have any numbers"
        elif upper_count == 0:
            error = "The password doesn't have any uppercase characters"
        elif lower_count == 0:
            error = "The password doesn't have any lowercase characters"
        elif email.find("@") != True:
            error = "Please use an actual email"
        #If the information user input isn't blank and they have passed the password checker then their information is stored in the users text file.
        elif username != "" and password != "" and reenter != "" and email != "" and notifications != "":
            file = open("users.txt", "a")
            file.write(f"\n{username},{password},{email},{notifications},{tasks}")
            file.close()
            return redirect(url_for("main_home_page"))
        #Updates the user object with what the user has inputted.
        current_user.update(username, password, email, notifications, int(tasks))
    return render_template("register_page.html", error = error)



#Main home page:
@app.route("/main_home_page", methods = ["POST", "GET"])
def main_home_page():
    '''
    :input:information such as tasks to display in the calendar.
    :return: page returns a calendar and a task counter.
    '''
    file = open("tasks.txt", "r")
    calendar = []
    #Goes through the tasks file and uses .split() and .strip() to check which tasks belong to the current user.
    for line in file:
        if line.strip().split(",")[0] == current_user.username:
            #Stores the tasks information as variables such as name, date and priority.
            task = line.strip().split(",")[1]
            end_date = line.strip().split(",")[4]
            priority = line.strip().split(",")[5]
            #Appends the variables to a 2D array which can be used to display information to web pages.
            calendar.append([task, end_date, priority])

    #Length checker for the calendar array as the calendar only holds 3 tasks at a time, so it replaces empty elements with None values.
    if len(calendar) == 0:
        for x in range(3):
            calendar.append([None, None, None])
    elif len(calendar) == 1:
        for x in range(2):
            calendar.append([None, None, None])
    elif len(calendar) == 2:
        calendar.append([None, None, None])

    #If the complete button for any of the tasks has been pressed. It will remove the task from the text file.
    if request.method == "POST":
        complete = request.form['complete']
        if complete == calendar[0][0]:
            #Stores the tasks file in a variable called lines.
            file = open("tasks.txt", "r")
            lines = file.readlines()
            #Reopens the file in write format.
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                #Checks if the task that is done is equal to a line in the task file, if it is it won't include it.
                if task != complete:
                    file.write(line)
            #Decreases the task counter by 1 and updates the user object.
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        #What has happened in the above if statement is the same for the future elif statements in this function but for different tasks.
        elif complete == calendar[1][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == calendar[2][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)


        #Reopens and resets the calendar array to update the web page and array.
        file = open("tasks.txt", "r")
        calendar = []
        for line in file:
            if line.strip().split(",")[0] == current_user.username:
                task = line.strip().split(",")[1]
                end_date = line.strip().split(",")[4]
                priority = line.strip().split(",")[5]
                calendar.append([task, end_date, priority])

        if len(calendar) == 0:
            for x in range(3):
                calendar.append([None, None, None])
        elif len(calendar) == 1:
            for x in range(2):
                calendar.append([None, None, None])
        elif len(calendar) == 2:
            calendar.append([None, None, None])

        file.close()
        #When displaying the web page it uses the calendar array to store variables in the html file.
        return render_template("main_home_page.html", tasks=current_user.tasks, name1=calendar[0][0], date1=calendar[0][1], priority1=calendar[0][2], name2=calendar[1][0],date2=calendar[1][1], priority2=calendar[1][2], name3=calendar[2][0],date3=calendar[2][1], priority3=calendar[2][2])
    else:
        return render_template("main_home_page.html", tasks = current_user.tasks, name1 = calendar[0][0], date1 = calendar[0][1], priority1 = calendar[0][2], name2 = calendar[1][0], date2 = calendar[1][1], priority2 = calendar[1][2], name3 = calendar[2][0], date3 = calendar[2][1], priority3 = calendar[2][2])


#To do list main page
@app.route("/todo_main", methods = ['POST', 'GET'])
def todo_main():
    '''
    :input: Maximum of 5 tasks from both General and Work types, 10 in total.
    :return: Displays a table of tasks with all the information in the task file excluding the username.
    '''
    file = open("tasks.txt", "r")
    general = []
    work = []
    #Loops through the task file to separate the general and work tasks in 2 different arrays.
    for line in file:
        if line.strip().split(",")[0] == current_user.username and line.strip().split(",")[6] == "General":
            task = line.strip().split(",")[1]
            description = line.strip().split(",")[2]
            start_date = line.strip().split(",")[3]
            end_date = line.strip().split(",")[4]
            priority = line.strip().split(",")[5]
            type = line.strip().split(",")[6]
            general.append([task, description, start_date, end_date, priority, type])

        elif line.strip().split(",")[0] == current_user.username and line.strip().split(",")[6] == "Work":
            task = line.strip().split(",")[1]
            description = line.strip().split(",")[2]
            start_date = line.strip().split(",")[3]
            end_date = line.strip().split(",")[4]
            priority = line.strip().split(",")[5]
            type = line.strip().split(",")[6]
            work.append([task, description, start_date, end_date, priority, type])

    file.close()
    #Does the same as the previous function when filling blank elements with None values.
    if len(general) == 0:
        for x in range(5):
            general.append([None, None, None, None, None, None])
    elif len(general) == 1:
        for x in range(4):
            general.append([None, None, None, None, None, None])
    elif len(general) == 2:
        for x in range(3):
            general.append([None, None, None, None, None, None])
    elif len(general) == 3:
        for x in range(2):
            general.append([None, None, None, None, None, None])
    elif len(general) == 4:
        general.append([None, None, None, None, None, None])

    if len(work) == 0:
        for x in range(5):
            work.append([None, None, None, None, None, None])
    elif len(work) == 1:
        for x in range(4):
            work.append([None, None, None, None, None, None])
    elif len(work) == 2:
        for x in range(3):
            work.append([None, None, None, None, None, None])
    elif len(work) == 3:
        for x in range(2):
            work.append([None, None, None, None, None, None])
    elif len(work) == 4:
        work.append([None, None, None, None, None, None])

    #Button checks:
    if request.method == "POST":
        complete = request.form['complete']
        #Does the same as the last function where if any of the tasks complete button is clicked, it removes the task from the file when refreshing/updating the page.
        if complete == general[0][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        # The following if statements does the same as the last if statements but for the rest of the tasks.
        elif complete == general[1][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == general[2][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == general[3][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == general[4][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        if complete == work[0][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == work[1][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username,current_user.password,current_user.email,current_user.notifications,current_user.tasks)

        elif complete == work[2][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == work[3][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)

        elif complete == work[4][0]:
            file = open("tasks.txt", "r")
            lines = file.readlines()
            file = open("tasks.txt", "w")
            for line in lines:
                task = line.strip().split(",")[1]
                if task != complete:
                    file.write(line)
            current_user.tasks = int(current_user.tasks) - 1
            current_user.update(current_user.username, current_user.password, current_user.email,
                                current_user.notifications, current_user.tasks)


        #Resets the general and work arrays and updates them without the removed tasks.
        file = open("tasks.txt", "r")
        general = []
        work = []
        for line in file:
            if line.strip().split(",")[0] == current_user.username and line.strip().split(",")[6] == "General":
                task = line.strip().split(",")[1]
                description = line.strip().split(",")[2]
                start_date = line.strip().split(",")[3]
                end_date = line.strip().split(",")[4]
                priority = line.strip().split(",")[5]
                type = line.strip().split(",")[6]
                general.append([task, description, start_date, end_date, priority, type])

            if line.strip().split(",")[0] == current_user.username and line.strip().split(",")[6] == "Work":
                task = line.strip().split(",")[1]
                description = line.strip().split(",")[2]
                start_date = line.strip().split(",")[3]
                end_date = line.strip().split(",")[4]
                priority = line.strip().split(",")[5]
                type = line.strip().split(",")[6]
                work.append([task, description, start_date, end_date, priority, type])
        file.close()

        #Rechecks the length of the arrays and fills missing elements with None values.
        if len(general) == 0:
            for x in range(5):
                general.append([None, None, None, None, None, None])
        elif len(general) == 1:
            for x in range(4):
                general.append([None, None, None, None, None, None])
        elif len(general) == 2:
            for x in range(3):
                general.append([None, None, None, None, None, None])
        elif len(general) == 3:
            for x in range(2):
                general.append([None, None, None, None, None, None])
        elif len(general) == 4:
            general.append([None, None, None, None, None, None])

        if len(work) == 0:
            for x in range(5):
                work.append([None, None, None, None, None, None])
        elif len(work) == 1:
            for x in range(4):
                work.append([None, None, None, None, None, None])
        elif len(work) == 2:
            for x in range(3):
                work.append([None, None, None, None, None, None])
        elif len(work) == 3:
            for x in range(2):
                work.append([None, None, None, None, None, None])
        elif len(work) == 4:
            work.append([None, None, None, None, None, None])

        #Displays the todo main page with alot of passed variables to the html file.
        return render_template("todo_main.html", general_task1=general[0][0], general_description1=general[0][1], general_start_date1=general[0][2], general_end_date1=general[0][3], general_priority1=general[0][4], general_type1=general[0][4], general_task2=general[1][0], general_description2=general[1][1], general_start_date2=general[1][2], general_end_date2=general[1][3], general_priority2=general[1][4], general_type2=general[1][4], general_task3=general[2][0], general_description3=general[2][1], general_start_date3=general[2][2], general_end_date3=general[2][3], general_priority3=general[2][4], general_type3=general[2][4], general_task4=general[3][0], general_description4=general[3][1], general_start_date4=general[3][2], general_end_date4=general[3][3], general_priority4=general[3][4], general_type4=general[3][4], general_task5=general[4][0], general_description5=general[4][1], general_start_date5=general[4][2], general_end_date5=general[4][3], general_priority5=general[4][4], general_type5=general[4][4], work_task1=work[0][0], work_description1=work[0][1], work_start_date1=work[0][2], work_end_date1=work[0][3], work_priority1=work[0][4], work_type1=work[0][4], work_task2=work[1][0], work_description2=work[1][1], work_start_date2=work[1][2], work_end_date2=work[1][3], work_priority2=work[1][4], work_type2=work[1][4], work_task3=work[2][0], work_description3=work[2][1], work_start_date3=work[2][2], work_end_date3=work[2][3], work_priority3=work[2][4], work_type3=work[2][4], work_task4=work[3][0], work_description4=work[3][1], work_start_date4=work[3][2], work_end_date4=work[3][3], work_priority4=work[3][4], work_type4=work[3][4], work_task5=work[4][0], work_description5=work[4][1], work_start_date5=work[4][2], work_end_date5=work[4][3], work_priority5=work[4][4], work_type5=work[4][4])
    else:
        return render_template("todo_main.html", general_task1 = general[0][0], general_description1 = general[0][1], general_start_date1 = general[0][2], general_end_date1 = general[0][3], general_priority1 = general[0][4], general_type1 = general[0][4], general_task2 = general[1][0], general_description2 = general[1][1], general_start_date2 = general[1][2], general_end_date2 = general[1][3], general_priority2 = general[1][4], general_type2 = general[1][4], general_task3 = general[2][0], general_description3 = general[2][1], general_start_date3 = general[2][2], general_end_date3 = general[2][3], general_priority3 = general[2][4], general_type3 = general[2][4], general_task4 = general[3][0], general_description4 = general[3][1], general_start_date4 = general[3][2], general_end_date4 = general[3][3], general_priority4 = general[3][4], general_type4 = general[3][4], general_task5 = general[4][0], general_description5 = general[4][1], general_start_date5 = general[4][2], general_end_date5 = general[4][3], general_priority5 = general[4][4], general_type5 = general[4][4], work_task1=work[0][0], work_description1=work[0][1], work_start_date1=work[0][2], work_end_date1=work[0][3], work_priority1=work[0][4], work_type1=work[0][4], work_task2=work[1][0], work_description2=work[1][1], work_start_date2=work[1][2], work_end_date2=work[1][3], work_priority2=work[1][4], work_type2=work[1][4], work_task3=work[2][0], work_description3=work[2][1], work_start_date3=work[2][2], work_end_date3=work[2][3], work_priority3=work[2][4], work_type3=work[2][4], work_task4=work[3][0], work_description4=work[3][1], work_start_date4=work[3][2], work_end_date4=work[3][3], work_priority4=work[3][4], work_type4=work[3][4], work_task5=work[4][0], work_description5=work[4][1], work_start_date5=work[4][2], work_end_date5=work[4][3], work_priority5=work[4][4], work_type5=work[4][4])


#Creating a to do list page:
@app.route("/todo_create", methods = ['POST', 'GET'])
def todo_create():
    '''
    :inputs: What the user inputs in the form displayed in the web page.
    :return: Returns back to the main home page with the new task displayed.
    '''
    if request.method == "POST":
        #Stores the button called task.
        task = request.form['task']
        #Checks if the create button has been clicked.
        if task == "create":
            #Stores the user inputs as variables.
            name = request.form['name']
            description = request.form['description']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            priority = request.form['priority']
            type = request.form['type']
            file = open("tasks.txt", "a")
            #Increases the current user object tasks by 1 and updates the object.
            current_user.tasks = int(current_user.tasks) + 1
            current_user.update(current_user.username, current_user.password, current_user.email, current_user.notifications, current_user.tasks)
            #Appends the tasks file with the new task that has been created.
            file.write(f"\n{current_user.username},{name},{description},{start_date},{end_date},{priority},{type}")
            file.close()
            return redirect(url_for("todo_main"))
        #If the delete button has been pressed it simply goes straight back to the todo main page.
        elif task == "delete":
            return redirect(url_for("todo_main"))
    else:
        return render_template("todo_create.html")


#Notes main page:
@app.route("/notes_main", methods = ['POST', 'GET'])
def notes_main():
    '''
    :input: Maximum of 10 notes from notes file.
    :return: Table of notes which is displayed on the web page.
    '''
    file = open("notes.txt", "r")
    notes = []
    #Opens and stores 10 notes in an array from the notes text file.
    for line in file:
        if line.strip().split("`")[0] == current_user.username:
            note_name = line.strip().split("`")[1]
            description = line.strip().split("`")[2]
            notes.append([note_name, description])


    #Quicker way to check and add None values to arrays if they are missing elements.
    if len(notes) != 10:
        y = 10 - len(notes)
        for x in range(y):
            notes.append([None,None])

    #Goes through each document and checks if the open button is clicked, if it is, it redirects them to the text editor page.
    if request.method == "POST":
        #Uses session to stores variables and use them in different functions, basically makes it a global variable.
        session['button'] = request.form['button']
        button = session.get('button')
        #Checks which note is being opened and redirects the user to the text editor.
        if button == notes[0][0]:
            return redirect(url_for("note_document"))
        elif button == notes[1][0]:
            return redirect(url_for("note_document"))
        elif button == notes[2][0]:
            return redirect(url_for("note_document"))
        elif button == notes[3][0]:
            return redirect(url_for("note_document"))
        elif button == notes[4][0]:
            return redirect(url_for("note_document"))
        elif button == notes[5][0]:
            return redirect(url_for("note_document"))
        elif button == notes[6][0]:
            return redirect(url_for("note_document"))
        elif button == notes[7][0]:
            return redirect(url_for("note_document"))
        elif button == notes[8][0]:
            return redirect(url_for("note_document"))
        elif button == notes[9][0]:
            return redirect(url_for("note_document"))

        #Another button called delete where it deletes the note from the notes text file. Same with the other elif statements below.
        elif button == f"delete_{notes[0][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[0][0]:
                    file.write(line)

        elif button == f"delete_{notes[1][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[1][0]:
                    file.write(line)

        elif button == f"delete_{notes[2][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[2][0]:
                    file.write(line)

        elif button == f"delete_{notes[3][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[3][0]:
                    file.write(line)
        elif button == f"delete_{notes[4][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[4][0]:
                    file.write(line)

        elif button == f"delete_{notes[5][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[5][0]:
                    file.write(line)

        elif button == f"delete_{notes[6][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[6][0]:
                    file.write(line)

        elif button == f"delete_{notes[7][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[7][0]:
                    file.write(line)

        elif button == f"delete_{notes[8][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[8][0]:
                    file.write(line)

        elif button == f"delete_{notes[9][0]}":
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note = line.strip().split("`")[1]
                if note != notes[9][0]:
                    file.write(line)

        #Resets and updates the notes array which stores the notes variables.
        file = open("notes.txt", "r")
        notes = []
        for line in file:
            if line.strip().split("`")[0] == current_user.username:
                note_name = line.strip().split("`")[1]
                description = line.strip().split("`")[2]
                notes.append([note_name, description])

        if len(notes) != 10:
            y = 10 - len(notes)
            for x in range(y):
                notes.append([None, None])
        #Displays the notes main web page with the note names being passed to html.
        return render_template("notes_main.html", note1 = notes[0][0], note2 = notes[1][0], note3 = notes[2][0], note4 = notes[3][0], note5 = notes[4][0], note6 = notes[5][0], note7 = notes[6][0], note8 = notes[7][0], note9 = notes[8][0], note10 = notes[9][0])
    else:
        return render_template("notes_main.html", note1 = notes[0][0], note2 = notes[1][0], note3 = notes[2][0], note4 = notes[3][0], note5 = notes[4][0], note6 = notes[5][0], note7 = notes[6][0], note8 = notes[7][0], note9 = notes[8][0], note10 = notes[9][0])


#Text editor for the note document
@app.route("/note_document", methods = ["POST", "GET"])
def note_document():
    '''
    :input: Note from the notes file which corresponds with what the user inputted last function.
    :return: Displays a text editor where the user can make changes to notes.
    '''
    #Stores the button variable used in the last function into notes using session.
    note = session.get('button')
    file = open("notes.txt", "r")
    note_document_display = []
    #Goes through a loop and checks which note is being opened and stores the description in a 2D array.
    for line in file:
        if line.strip().split("`")[1] == note:
            description = line.strip().split("`")[2]
            note_document_display.append([note, description])
    file.close()

    if request.method == "POST":
        button = request.form["button"]
        #When the "GO BACK" button is pressed it redirects the user to the previous note main page.
        if button == "go_back":
            return redirect(url_for("notes_main"))
        #When the save button is pressed. It deletes the previous old note using the same method to remove note.
        elif button == "save":
            updated_note = request.form["description"]
            file = open("notes.txt", "r")
            lines = file.readlines()
            file = open("notes.txt", "w")
            for line in lines:
                note_line = line.strip().split("`")[1]
                if note != note_line:
                    file.write(line)
            #Appends the new updated version of the note to the notes file using a fstring.
            file = open("notes.txt", "a")
            file.write(f"\n{current_user.username}`{note_document_display[0][0]}`{updated_note}")
            return redirect(url_for("notes_main"))
    return render_template("note_document.html", note = note_document_display[0][0], description = note_document_display[0][1])

#Settings main page
@app.route("/settings_main", methods = ["POST","GET"])
def settings_main():
    '''
    :inputs:Buttons the user can click to go through different settings.
    :return:
    '''
    if request.method == "POST":
        #Stores the button values in a variable called button and just redirects them to corresponding web page when button is clicked.
        button = request.form["button"]
        if button == "notifications":
            return redirect(url_for("settings_notifications"))
        elif button == "change_password":
            return redirect(url_for("change_password"))
        else:
            return render_template("settings_main.html")
    return render_template("settings_main.html")


#Settings notifications page
@app.route("/settings_notifications", methods = ["POST","GET"])
def settings_notifications():
    '''
    :inputs: Any changes the user has made with the options given to them.
    :return: Updates to the user object and the users file in terms of notifications.
    '''
    if request.method == "POST":
        button = request.form["button"]
        #If the go back button is pressed it just goes back to the settings main page.
        if button == "go_back":
            return redirect(url_for("settings_main"))
        #If the make changes button is pressed, it does the same with as the notes_document page when updating the users file with different settings.
        elif button == "make_changes":
            daily_notifications = request.form["daily"]
            current_user.notifications = daily_notifications
            current_user.update(current_user.username, current_user.password, current_user.email, current_user.notifications, current_user.tasks)
            file = open("users.txt", "r")
            lines = file.readlines()
            file = open("users.txt", "w")
            for line in lines:
                user_line = line.strip().split(",")[0]
                if user_line != current_user.username:
                    file.write(line)
            file = open("users.txt", "a")
            file.write(f"\n{current_user.username},{current_user.password},{current_user.email},{current_user.notifications},{current_user.tasks}")
            return redirect(url_for("settings_main"))

    return render_template("settings_notifications.html")

#Change password main page:
@app.route("/change_password", methods = ["POST","GET"])
def change_password():
    '''
    :inputs: Old password to check if it's the right user, New password the user has inputted.
    :return: Updated version of the users file with new password.
    '''
    #Default values which are used with the password checker.
    number_count = 0
    upper_count = 0
    lower_count = 0
    error = None
    if request.method == "POST":
        button = request.form["button"]
        #If the go back button is pressed it simply redirects to the previous web page.
        if button == "go_back":
            return redirect(url_for("settings_main"))
        #If the submit button is pressed, it goes through a series of checks to make sure the new password is suitable.
        elif button == "submit":
            new_password = request.form["new_password"]
            re_enter = request.form["re_enter"]
            old_password = request.form["old_password"]
            for char in new_password:
                if char.isdigit():
                    number_count += 1
                elif char.isupper():
                    upper_count += 1
                elif char.islower():
                    lower_count += 1
            #First checks if the old password the user has inputted is correct.
            if current_user.password != old_password:
                error = "Your old password isn't correct"
            #Goes through the same checks as the register page to make sure the password is suitable.
            elif new_password != re_enter:
                error = "The passwords do not match, try again"
            elif old_password == "" or new_password == "" or re_enter == "":
                error = "Please fill in all the details"
            elif len(new_password) < 8:
                error = "The length of the password is too short, should be a minimum of 8 characters"
            elif number_count == 0:
                error = "The password doesn't have any numbers"
            elif upper_count == 0:
                error = "The password doesn't have any uppercase characters"
            elif lower_count == 0:
                error = "The password doesn't have any lowercase characters"
            else:
                current_user.update(current_user.username, new_password, current_user.email,
                                    current_user.notifications, current_user.tasks)
                #Updates the users text file with the new password.
                file = open("users.txt", "r")
                lines = file.readlines()
                file = open("users.txt", "w")
                for line in lines:
                    user_line = line.strip().split(",")[0]
                    if user_line != current_user.username:
                        file.write(line)
                file = open("users.txt", "a")
                file.write(
                    f"\n{current_user.username},{current_user.password},{current_user.email},{current_user.notifications},{current_user.tasks}")
                return redirect(url_for("settings_main"))
    return render_template("change_password.html", error = error)

#Runs the new whole app.
if __name__ == "__main__":
    app.run()
