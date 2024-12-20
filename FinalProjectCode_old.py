#UNWSP Programming Final Project--Micah DeCaro & Andrew Bittner
import sqlite3

class DBInterface:
    def __init__(self, database, table, table_query, sample_data):

        # Initialize attributes.
        self.database = database
        self.table = table
        self.table_query = table_query
        self.sample_data = sample_data
        self.conn = None
        self.cur = None
        self.data_list = None
        self.columns_list = None
        self.params = None
        self.help_msg = ('Choose operation from following:\n\n    "read" to read the contents of the entire table\n'
        '    "add" to add a new row\n    "edit" to edit a row\n    "delete" to delete a row\n    "exit" to exit program'
        '\n    "help" for a list of commands\n    "reset" to reset table contents to sample data')
        self.loop_run = False
        self.choice = None

    def connect(self):

        # Connect to database.
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.cur.execute(self.table_query)

        # Start main input loop.
        self.run_inp_loop()

        # Close database connection.
        self.conn.close()

    def run_inp_loop(self):
        while True:

            # Create a list holding contents of table (used for input validation).
            data = self.cur.execute(f'''SELECT * FROM {self.table}''')
            self.data_list = []
            for row in data:
                self.data_list.append(row)

            # Create a list holding column names in table.
            self.columns_list = []
            for row in data.description:
                self.columns_list.append(row)

            # Check to see if loop has already run; if not, display list of commands.
            if not self.loop_run:
                print(self.help_msg)
                self.loop_run = True

            # Get input and perform the corresponding command.
            self.choice = input('\n> ')
            if self.choice.lower() == 'read':
                self.read_table()
            elif self.choice.lower() == 'add':
                self.add_row()
            elif self.choice.lower() == 'edit':
                self.edit_row()
            elif self.choice.lower() == 'delete':
                self.delete_row()
            elif self.choice.lower() == 'help':
                self.show_help()
            elif self.choice.lower() == 'reset':
                self.reset()
            elif self.choice.lower() == 'exit':
                break
            else:
                print('Please select a valid operation.')

            # Commit changes.
            self.conn.commit()

    def read_table(self):

        # Read and print rows from the table.
        for row in self.cur.execute(f'''SELECT * FROM {self.table}'''):
            display = []
            for ind in range(len(self.columns_list)):
                display.append(f'{self.columns_list[ind][0]}: {str(row[ind])}')
            print(';   '.join(display))
        print('End of data.')

    def add_row(self):
        while True:

            # Get max value in ID column and set ID for new row to that plus 1.
            for row_id in self.cur.execute(f'''SELECT MAX({self.columns_list[0][0]}) FROM {self.table}'''):
                row_id = int(row_id[0]) + 1
            row = [row_id]
            self.params = ', ?' * (len(self.columns_list) - 1)

            # Get input data for each column.
            for column in self.columns_list:
                if not column == self.columns_list[0]:
                    inp = input(f'Enter into column {column[0]}: ')
                    if inp.lower() == 'exit':
                        break
                    row.append(inp)
            if inp.lower() == 'exit':
                break

            # Add row to table.
            self.cur.execute(f'''INSERT INTO {self.table} VALUES (?{self.params})''', row)
            print('Row added successfully.')
            break

    def edit_row(self):

        # Set update flag. Once this equals True, input loop terminates.
        updated = False

        # Input loop for getting row ID.
        while True:
            inp = input('Enter the ID of the row you would like to modify; alternatively, enter "exit" to cancel: ')
            if inp.lower() == 'exit':
                break

            # Verify that input both is an integer and is the ID (primary key) of an existing row.
            try:
                for row in self.data_list:
                    if int(inp) == row[0]:
                        id_sel = int(inp)
                        break
                inp = str(id_sel)

            # If input is invalid, ask the user for new input.
            except (ValueError, UnboundLocalError):
                print('Please select a valid ID.')
            else:
                break

        # Input loop for getting attribute to modify. Once valid ID has been taken from user, program asks the user
        # which specific attribute (or all attributes) in the row they would like to modify.
        while not inp.lower() == 'exit':
            inp = input('Enter the attribute of the row you would like to modify, or "all" for entire row; '
                        'alternatively, enter "exit" to cancel: ')
            if inp.lower() == 'exit':
                break

            # Change all attributes in row, if requested by user.
            if inp.lower() == 'all':
                columns_sel = []
                values_sel = []

                # Get input data for each column.
                for column in self.columns_list:
                    if not column == self.columns_list[0]:
                        inp = input(f'Enter into column {column[0]}: ')
                        if inp.lower() == 'exit':
                            break
                        columns_sel.append(column[0])
                        values_sel.append(inp)
                if inp.lower() == 'exit':
                    break

                # Update attributes in table.
                for ind in range(len(columns_sel)):
                    self.cur.execute(
                        f'''UPDATE {self.table} SET {columns_sel[ind]} = ? WHERE {self.columns_list[0][0]} == ?''',
                        (values_sel[ind], id_sel))
                print('Row updated successfully.')
                updated = True

            # Change specific attribute in row, or if no valid attribute is given, restart loop.
            else:

                # Check if input is equal to an existing column.
                for column in self.columns_list:
                    if (inp.lower() == column[0].lower() and not column == self.columns_list[0][
                        0] and not inp.lower()
                                   == 'exit'):
                        inp = input(f'Enter into column {column[0]}: ')
                        if inp.lower() == 'exit':
                            break
                        self.cur.execute(
                            f'''UPDATE {self.table} SET {column[0]} = ? WHERE {self.columns_list[0][0]} == ?''',
                            (inp, id_sel))
                        print('Row updated successfully.')
                        updated = True

            # If row has been updated, or if user wants to cancel the operation, return user to main input loop.
            if updated or inp.lower() == 'exit':
                break

            # If input doesn't match any column, ask user for valid input.
            print('Please select a valid attribute.')

    def delete_row(self):

        # Input loop for getting row ID.
        while True:
            inp = input('Enter the ID of the row you would like to delete; alternatively, enter "exit" to cancel: ')
            if inp.lower() == 'exit':
                break

            # Verify that input both is an integer and is the ID (primary key) of an existing row.
            try:
                for row in self.data_list:
                    if int(inp) == row[0]:
                        row_id = int(inp)
                        break
                inp = str(row_id)
            except (ValueError, UnboundLocalError):
                print('Please select a valid ID.')
            else:

                # Delete row.
                self.cur.execute(f'''DELETE FROM {self.table} WHERE {self.columns_list[0][0]} == ?''', str(row_id))
                print('Contact deleted successfully.')
                break

    def reset(self):

        # If table exists, drop it.
        self.cur.execute(f'''DROP TABLE IF EXISTS {self.table}''')

        # Create table.
        self.cur.execute(self.table_query)

        # Add rows to table.
        self.cur.executemany(f'''INSERT INTO {self.table} VALUES (?{self.params})''', self.sample_data)
        print(f'Table {self.table} reset.')

    def show_help(self):
        print(self.help_msg)

def exit_sequence():

    # Function to keep console/window open until user ends program.
    input('\nProgram finished.\nPress [enter] to exit... ')

def main():

    # Set parameters.
    table_query = '''CREATE TABLE IF NOT EXISTS Info (IDNum INTEGER PRIMARY KEY NOT NULL, Name TEXT, Year TEXT, Email
    TEXT, PhoneNum TEXT, Address TEXT, GPA DECIMAL)'''
    info_rows = [(1, 'Glu Tton', 'Freshman', 'glutton.free@college.edu', '612-648-8420',
                  'McDonald\'s, 1480 85th Ave N, Brooklyn Park, MN 55444', 3.7),
                 (2, 'Guill Otine', 'Junior', 'frenchrev1789@college.edu', '763-501-6629',
                  'Palais Bourbon, 126 Rue de l\'Université, 75007 Paris, France', 2.8),
                 (3, 'Pedalto Themedal', 'Sophomore', 'gottagofast@college.edu', '612-295-4398', 'Sumitomo Fudosan'
                  'Osaki Garden Tower 9F, 1-1-1 Nishi-Shinagawa, Shinagawa-ku, Tokyo 141-0033, Japan', 3.3),
                 (4, 'Badprog Rammer', 'Senior', 'whoneedscomments@college.edu', '952-254-8163',
                  'One Apple Park Way, Cupertino, CA 95014', 1.9),
                 (5, 'Sadn Ess', 'Sophomore', 'icanteven@college.edu', '763-892-5678',
                  '1200 Grand Central Ave, Glendale, CA 91201', 3.1)]

    # Connect to database.
    db_inter_1 = DBInterface('info.db', 'Info', table_query, info_rows)
    db_inter_1.connect()

    # End program.
    exit_sequence()

if __name__ == '__main__':
    main()