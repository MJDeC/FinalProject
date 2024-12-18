#UNWSP Programming Final Project--Micah DeCaro & Andrew Bittner
import sqlite3
#main function
def main():
    #connect to database
    connection = sqlite3.connect('info.db')
    #get cursor
    cursor = connection.cursor()
    #add table
    info_table(cursor)
    #commit changes and close connection
    connection.commit()
    connection.close()
  
def info_table(cursor):
    #if table exists, drop it
    cursor.execute('DROP TABLE IF EXISTS YearLookup')
    cursor.execute('DROP TABLE IF EXISTS Info')
    #create table
    cursor.execute('''CREATE TABLE YearLookup (YearID INTEGER PRIMARY KEY NOT NULL, YearName TEXT)''')
    cursor.execute('''CREATE TABLE Info (IDNum INTEGER PRIMARY KEY NOT NULL, Name TEXT, YearID, Email TEXT, PhoneNum TEXT, Address TEXT, GPA DECIMAL, FOREIGN KEY(YearID) REFERENCES YearLookup(YearID))''')
    #add rows to table
    info_rows = [(1, 'Freshman'), (2, 'Sophomore'), (3, 'Junior'), (4, 'Senior')]
    cursor.executemany("insert into YearLookup values (?,?)", info_rows)
    info_rows = [(1,'Glu Tton', 1, 'glutton.free@college.edu', '612-648-8420', 'McDonald\'s, 1480 85th Ave N, Brooklyn Park, MN 55444', 3.7),
              (2,'Guill Otine', 3, 'frenchrev1789@college.edu', '763-501-6629', 'Palais Bourbon, 126 Rue de l\'Université, 75007 Paris, France', 2.8),
              (3,'Pedalto Themedal', 2, 'gottagofast@college.edu', '612-295-4398', 'Sumitomo Fudosan Osaki Garden Tower 9F, 1-1-1 Nishi-Shinagawa, Shinagawa-ku, Tokyo 141-0033, Japan', 3.3),
              (4,'Badprog Rammer', 4, 'whoneedscomments@college.edu', '952-254-8163', 'One Apple Park Way, Cupertino, CA 95014', 1.9),
              (5,'Sadn Ess', 2, 'icanteven@college.edu', '763-892-5678', '1200 Grand Central Ave, Glendale, CA 91201', 3.1)]
    cursor.executemany("insert into info values (?,?,?,?,?,?,?)", info_rows)

    #print contents of database
    print("Here are the current contents of the database to be edited from:")
    for row in cursor.execute("select * from info"):
        print(row)
    #get user input for editing purposes
    cont = 'y'
    if cont =='y':
        row_id = input("Enter the ID of the row to edit:")
        column_name = input("Enter the name of the column you would like to edit from:")
        replacement = input("Enter the value you would like to add:")
        #sql query
        query = f"UPDATE Info SET {column_name} = %s WHERE id = %s"
        cursor.execute(query, (replacement, row_id))
        connection.commit()
        print("Success! Info database has been updated. Here are the new contents:")
        for row in cursor.execute("select * from info"):
            print(row)
        cont=input("Enter y if you would like to continue editing. Else, press another key.")
        #except sqlite3.Error:
            #print("There was an error updating the database. Please try again!")
            #cont = input("Press y to continue editing, or else press another key to quit.")
    else:
        print("Thank you for updating the database! Here are the final contents:")
        for row in cursor.execute("select * from info"):
            print(row)
        
    

    # for row in cursor.execute('''SELECT Info.IDNum, Info.Name, YearLookup.YearName, Info.Email, Info.PhoneNum, Info.Address, Info.GPA FROM YearLookup, Info WHERE YearLookup.IDNum == Info.YearNum'''):
    #     print(row)


if __name__ == '__main__':
    main()
