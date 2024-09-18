import csv
import sqlite3
#CRUD operation

def create_connection():
    # Connect to the SQLite3 database
    try:
        con = sqlite3.connect('users.sqlite3')
        return con 
    except Exception as e:
        print(e)
        return None  # Return None if there's an error

INPUT_STRING = """
Enter the options:
    1.CREATE TABLE
    2.DUMP USERS FROM CSV INTO USERS TABLE
    3.ADD NEW USER INTO USER TABLE
    4.QUERY ALL USERS FROM TABLE
    5.QUERY USER BY ID FROM TABLE
    6.QUERY SPECIFIED NO. OF RECORDS FROM TABLE
    7.DELETE ALL  USERS
    8.DELETE USER BY ID
    9.UPDATE USER
    10.PRESS ANY KEY TO EXIT
"""

# Creating table function
def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            country CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL, 
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web TEXT
        );
    """
    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    con.commit()  # Commit the changes
    print('User table was created successfully.')

#reading csv file and dump in table
def read_csv():
    users =[]
    with open("sample_users.csv",'r') as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]

def insert_users(con, users):
    user_add_query = """
        INSERT INTO users(
            first_name,
            last_name,
            company_name,
            address,
            city,
            country,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()
    print(f"{len(users)} users were imported sucessfully....")
def select_users(con, no_of_users):
    cur = con.cursor()
    if no_of_users:
        users = cur.execute(f"SELECT * FROM users LIMIT {no_of_users}")
    else:
        users= cur.execute("SELECT * FROM users")
    for user in users:
        print(user)
def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users where id = ?", (user_id))
    for user in users:
        print(user)
def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users")
    con.commit()
    print("All  users deleted")
def delete_users_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users where id =?",(user_id))
    con.commit()
    print(f"User with id [{user_id}] was sucessfully deleted]")
columns =(
            'first_name',
            'last_name',
            'company_name',
            'address',
            'city',
            'country',
            'state',
            'zip',
            'phone1',
            'phone2',
            'email',
            'web',)
def update_user_by_id(con,user_id,column_name,column_value):
    update_query=f"UPDATE users set {column_name}=? where id = ?;"
    cur = con.cursor()
    cur.execute(update_query, (column_name,user_id))
    con.commit()
    print(
        f"[{column_name} was updated with the value [{column_value}] of user with id [{user_id}]]"
    )
# This is the main function
def main():
    con = create_connection()
    if con:
    
        user_input = input(INPUT_STRING)
        if user_input == '1':
            create_table(con)
        elif user_input == '2':
            users =  read_csv()
            insert_users(con, users)
        elif user_input == '3':
            #sabai input lini
            user_data = []
            for column in columns:
                column_value = input(f'Enter the value of {column}')
                user_data.append(column_value)
            insert_users(con,[tuple(user_data)])

        elif user_input == '4':
            select_users(con)
        elif user_input == '5':
            user_id = input("enter the user_id:")
            if user_id.isnumeric():
                select_user_by_id(con,user_id)
            else:
                print("Enter the correct user id...please")
        elif user_input == '6':
            no_of_users = input("Enter the number of users")
            if no_of_users.isnumeric():
                select_users(con, no_of_users)
            else:
                print("Enter valid nummber")
        elif user_input == '7':
            print("do you want to delete (y/n)? ")
            choice = input()
            if choice == 'y':
                delete_users(con)
            else:
                print("Thank God")
        elif user_input == '8':
            user_id = input("Enter the user_id you want to delete")
            if user_id.isnumeric():
                delete_users_by_id(con,user_id)
            else:
                print("Enter the valid id in number")
        elif user_input == '9':
            user_id = input("enter the user id")
            if user_id.isnumeric():
                column_name = input(
                    f"Enter the column name you want to edit. please make sure column is with in {columns}:"

                )
                if column_name in columns:
                    column_value = input("enter the value of {column_name}:")
                    update_user_by_id(con,user_id, column_name, column_value)
            else:
                exit()
        
        elif user_input == '10':
            print('Exiting the program.')
        else:
            print('Invalid option, please try again.')
            exit()

        con.close()  # Close the connection when done
main()

