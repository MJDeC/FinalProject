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
  cursor.execute('DROP TABLE IF EXISTS Info')
  #create table
  cursor.execute('''CREATE TABLE Info (IDNum INTEGER PRIMARY KEY NOT NULL, Name TEXT)''')
  #add rows to table
  info_rows = [(1,'Glu Tton'),
              (2,'Guill Otine'),
              (3,'Pedalto Themedal'),
              (4,'Badprog Rammer'),
              (5,'Sadn Ess')]
    cursor.executemany("insert into info values (?,?)", info_rows)

    #print contents of database
    print("Here are the current contents of the database:")
    for row in cursor.execute("select * from info"):
        print(row)

if __name__ == '__main__':
    main()
