import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt
from tkcalendar import DateEntry

class AlohaCorpApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aloha Corp")
        self.geometry("500x300")
        self.configure(bg="white")

        # Custom fonts for headings
        self.header_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.sub_font = tkfont.Font(family="Segoe UI", size=12)

        # Mode flag: "login" or "create"
        self.current_mode = None

        # For store or role selection
        self.selected_store = None
        self.selected_role = None

        # ----------------------------------------------------------------
        # DATABASE CONNECTION & TABLE CREATION
        # ----------------------------------------------------------------
        try:
            self.connection = mysql.connector.connect(
                host="localhost",    # or your host address
                user="root",         # replace with your MySQL username
                password="root",     # replace with your MySQL password
                database="triall"    # replace with your database name
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.create_users_table()  # Create (or confirm) the users table if it doesn't exist
                self.create_invoices_table()
                self.create_merchandise_table()
                self.create_expenses_table()
                self.create_employee_bonus_table()
                self.create_employee_rates_table()
                self.create_withdrawals_table()
                self.create_payroll_table()
                self.create_day_closeout_table()
            else:
                print("Connection failed")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

        # Create the top menu bar
        self.create_top_bar()

        #self.initiate_login()


        # Main content area
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(expand=True, fill="both")

        # Show the welcome screen
        self.show_welcome_screen()

    def create_users_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating users table: {err}")

    def create_invoices_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    date_received DATE,
    company VARCHAR(255),
    invoice_number VARCHAR(50),
    amount DECIMAL(10,2),
    date_due DATE
)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating invoices table: {err}")

    def create_expenses_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_type VARCHAR(255),
    expense_value DECIMAL(10,2),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating expenses table: {err}")

    def create_merchandise_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS merchandise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merchandise_type VARCHAR(255),
    merchandise_value DECIMAL(10,2),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating merchandise table: {err}")

    def create_withdrawals_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS withdrawals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    user_id INT,
    amount DECIMAL(10,2)
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating withdrawals table: {err}")

    def create_employee_bonus_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee_bonus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    bonus_amount DECIMAL(10,2)
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating bonus table: {err}")

    def create_employee_rates_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    bonus_rate DECIMAL(5,2),
    rate_per_hour DECIMAL(10,2),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating rates table: {err}")

    def create_payroll_table(self):
        create_table_query = """
                CREATE TABLE IF NOT EXISTS payroll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATE,
    end_date DATE,
    multiple_weeks_view BOOLEAN
)
                """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating payroll table: {err}")

    def create_day_closeout_table(self):
            create_table_query = """
                CREATE TABLE IF NOT EXISTS day_closeout (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_username VARCHAR(255),
    cash DECIMAL(10,2),
    credit DECIMAL(10,2),
    total DECIMAL(10,2),
    difference DECIMAL(10,2),
    date DATE,
    notes TEXT
)
                """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
                print("Users table is ready.")
            except Error as err:
                print(f"Error creating users table: {err}")

    def initiate_login(self):
        # function to create initial owner login
        pass1 = 'pass'
        hashed_pass1 = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt())
        insert_query = "INSERT INTO users (ID, name, password, role) VALUES (%s, %s, %s, %s)"
        cursor = self.connection.cursor()
        cursor.execute(insert_query, (123, 'andrew', hashed_pass1, 'Owner'))
        self.connection.commit()


    def create_top_bar(self):
        top_bar = tk.Frame(self, bg="white", height=40)
        top_bar.pack(side="top", fill="x")

        # Back button
        back_button = tk.Button(
            top_bar,
            text="← Back",
            bg="white",
            fg="black",
            bd=0,
            activebackground="white",
            command=self.go_back
        )
        back_button.pack(side="left", padx=10, pady=5)

        # 3-dot menu button
        menu_button = tk.Menubutton(
            top_bar,
            text="⋮",
            bg="white",
            fg="black",
            bd=0,
            activebackground="white"
        )
        menu_button.pack(side="right", padx=10, pady=5)

        dot_menu = tk.Menu(menu_button, tearoff=0)
        dot_menu.add_command(label="Option 1", command=self.option1_action)
        dot_menu.add_command(label="Option 2", command=self.option2_action)
        menu_button["menu"] = dot_menu

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ----------------------------------------------------------------
    # WELCOME SCREEN
    # ----------------------------------------------------------------
    def show_welcome_screen(self):
        self.current_mode = None
        self.clear_main_frame()


        heading_label = tk.Label(
            self.main_frame,
            text="Welcome To Aloha Corp.",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(40, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Sign in to continue.",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Login button
        login_button = tk.Button(
            self.main_frame,
            text="Login",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.login_action
        )
        login_button.pack(pady=5)

        # Create New Account button
        create_account_button = tk.Button(
            self.main_frame,
            text="Create New Account",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.create_account_action
        )
        create_account_button.pack(pady=5)

    # ----------------------------------------------------------------
    # LOGIN FLOW
    # ----------------------------------------------------------------
    def login_action(self):
        self.current_mode = "login"
        self.show_store_selection()

    def show_store_selection(self):
        self.clear_main_frame()
        heading_label = tk.Label(
            self.main_frame,
            text="Login",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Select Location",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 10))

        # Displaying store selection (not used in DB queries here)
        stores = ["Store 1", "Store 2", "Store 3", "Full Access"]
        self.store_var = tk.StringVar()
        self.store_var.set(stores[0])
        store_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.store_var,
            values=stores,
            state="readonly"
        )
        store_dropdown.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.handle_store_selection
        )
        submit_button.pack(pady=10)

    def handle_store_selection(self):
        self.selected_store = self.store_var.get()
        self.show_login_form()

    def show_login_form(self):
        self.clear_main_frame()

        label = tk.Label(
            self.main_frame,
            text=f"Login - {self.selected_store}",
            bg="white",
            fg="black",
            font=self.header_font
        )
        label.pack(pady=(20, 10))

        # Username field (stored in DB as 'name')
        username_label = tk.Label(
            self.main_frame,
            text="Username:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(5, 2))
        self.username_entry = tk.Entry(self.main_frame, width=30)
        self.username_entry.pack(pady=(0, 20))  # extra space after username

        # Password field
        password_label = tk.Label(
            self.main_frame,
            text="Password:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        password_label.pack(pady=(0, 2))
        self.password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 10))

        login_btn = tk.Button(
            self.main_frame,
            text="Login",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_login
        )
        login_btn.pack(pady=10)

    def process_login(self):
        """
        Logs in a user (e.g., employees, managers, owners).
        If the user has a 'Manager' or 'Owner' role, we can direct them
        to the manager/owner home screens after verifying the password.
        If 'Employee', show employee home screen.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id, password, role FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Login Error", "Invalid username.")
                return

            user_id, stored_password, role = result

            self.user_role = role

            # Verify the password using bcrypt.
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                messagebox.showinfo("Success", f"Welcome, {username}!")
                if role == "Manager":
                    self.show_manager_home()
                elif role == "Owner":
                    self.show_owner_home()
                elif role == "Employee":
                    self.show_employee_home()
                else:
                    # For other roles, you could show a different screen
                    messagebox.showinfo("Info", f"No specific home screen for role: {role}")
            else:
                messagebox.showerror("Login Error", "Incorrect password.")
        except Error as err:
            messagebox.showerror("Database Error", f"Error during login: {err}")

    # ----------------------------------------------------------------
    # CREATE ACCOUNT FLOW (Manager/Owner login only)
    # ----------------------------------------------------------------
    def create_account_action(self):
        self.current_mode = "create"
        self.show_role_selection()

    def show_role_selection(self):
        self.clear_main_frame()
        heading_label = tk.Label(
            self.main_frame,
            text="Create New Account",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Select Role",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 10))

        roles = ["Manager", "Owner"]
        self.role_var = tk.StringVar()
        self.role_var.set(roles[0])

        role_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.role_var,
            values=roles,
            state="readonly"
        )
        role_dropdown.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.handle_role_selection
        )
        submit_button.pack(pady=10)

    def handle_role_selection(self):
        self.selected_role = self.role_var.get()
        # For demonstration, we'll default managers/owners to "Store 1"
        self.selected_store = "Store 1"
        self.show_manager_owner_login_form()

    def show_manager_owner_login_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Login",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You are logging in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Username field (stored in DB as 'name')
        username_label = tk.Label(
            self.main_frame,
            text="USERNAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(0, 2))
        self.new_username_entry = tk.Entry(self.main_frame, width=30)
        self.new_username_entry.pack(pady=(0, 20))  # extra space after username

        # Password field
        password_label = tk.Label(
            self.main_frame,
            text="PASSWORD",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        password_label.pack(pady=(0, 2))
        self.new_password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.new_password_entry.pack(pady=(0, 10))

        create_btn = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_manager_owner_login
        )
        create_btn.pack(pady=10)

    def process_manager_owner_login(self):
        """
        Attempts to log in an existing Manager/Owner (no new account insertion).
        """
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id, password FROM users WHERE name = %s AND role = %s"
            cursor.execute(query, (username, self.selected_role))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Login Error", "User not found or role mismatch.")
                return

            user_id, stored_password = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                messagebox.showinfo("Welcome", f"You are logged in as {username} ({self.selected_role}).")
                if self.selected_role == "Manager":
                    self.show_manager_home()
                else:
                    self.show_owner_home()
            else:
                messagebox.showerror("Login Error", "Incorrect password.")

        except Error as err:
            messagebox.showerror("Database Error", f"Error during login: {err}")

    # ----------------------------------------------------------------
    # EMPLOYEE HOME & FORMS
    # ----------------------------------------------------------------
    def show_employee_home(self):
        """
        Displays the Employee Home screen with the three buttons:
        1) Enter Day Closeout
        2) Enter In/Out Balance
        3) Enter Expense
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Employee Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        employee_options = [
            "Enter Day Closeout",
            "Enter In/Out Balance",
            "Enter Expense"
        ]

        for option in employee_options:
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.employee_option_action(opt)
            )
            btn.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_employee_actions
        )
        submit_button.pack(pady=20)

    def employee_option_action(self, option):
        if option == "Enter Day Closeout":
            self.show_day_closeout_form()
        elif option == "Enter In/Out Balance":
            self.show_in_out_balance_form()
        elif option == "Enter Expense":
            self.show_expense_form()
        else:
            messagebox.showinfo("Employee Action", f"You clicked: {option}")

    def submit_employee_actions(self):
        messagebox.showinfo("Submit", "Employee actions submitted (placeholder).")

    def show_day_closeout_form(self):
        """
        Displays a form for entering day closeout data.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter Day Closeout",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Employee 1 in Store 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Employee Username
        emp_label = tk.Label(self.main_frame, text="EMPLOYEE USERNAME", bg="white", fg="black", font=self.sub_font)
        emp_label.pack(pady=(0, 2))
        self.dayclose_emp_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_emp_entry.pack(pady=(0, 10))

        # Cash
        cash_label = tk.Label(self.main_frame, text="CASH", bg="white", fg="black", font=self.sub_font)
        cash_label.pack(pady=(0, 2))
        self.dayclose_cash_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_cash_entry.pack(pady=(0, 10))

        # Credit
        credit_label = tk.Label(self.main_frame, text="CREDIT", bg="white", fg="black", font=self.sub_font)
        credit_label.pack(pady=(0, 2))
        self.dayclose_credit_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_credit_entry.pack(pady=(0, 10))

        # Total
        total_label = tk.Label(self.main_frame, text="TOTAL", bg="white", fg="black", font=self.sub_font)
        total_label.pack(pady=(0, 2))
        self.dayclose_total_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_total_entry.pack(pady=(0, 10))

        # Difference
        diff_label = tk.Label(self.main_frame, text="DIFFERENCE", bg="white", fg="black", font=self.sub_font)
        diff_label.pack(pady=(0, 2))
        self.dayclose_diff_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_diff_entry.pack(pady=(0, 10))

        # Date (dropdown)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        dayclose_date_dropdown = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        dayclose_date_dropdown.pack(pady=(0, 10))

        # Notes
        notes_label = tk.Label(self.main_frame, text="NOTES", bg="white", fg="black", font=self.sub_font)
        notes_label.pack(pady=(0, 2))
        self.dayclose_notes_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_notes_entry.pack(pady=(0, 10))

        # sign up (submit) button
        signup_button = tk.Button(
            self.main_frame,
            text="sign up",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_day_closeout
        )
        signup_button.pack(pady=10)

    def process_day_closeout(self):
        """
        Just shows a message for now (no DB insert).
        """
        emp_username = self.dayclose_emp_entry.get()
        cash = self.dayclose_cash_entry.get()
        credit = self.dayclose_credit_entry.get()
        total = self.dayclose_total_entry.get()
        diff = self.dayclose_diff_entry.get()
        date_val = self.dayclose_date_var.get()
        notes = self.dayclose_notes_entry.get()

        messagebox.showinfo(
            "Day Closeout",
            f"Employee: {emp_username}\nCash: {cash}\nCredit: {credit}\nTotal: {total}\n"
            f"Difference: {diff}\nDate: {date_val}\nNotes: {notes}"
        )

    def show_in_out_balance_form(self):
        """
        Displays a form for entering In/Out Balance data.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter In/Out Balance",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Employee 1 in Store 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Employee Username
        emp_label = tk.Label(self.main_frame, text="EMPLOYEE USERNAME", bg="white", fg="black", font=self.sub_font)
        emp_label.pack(pady=(0, 2))
        self.inout_emp_entry = tk.Entry(self.main_frame, width=30)
        self.inout_emp_entry.pack(pady=(0, 10))

        # In Balance
        in_label = tk.Label(self.main_frame, text="IN BALANCE", bg="white", fg="black", font=self.sub_font)
        in_label.pack(pady=(0, 2))
        self.in_balance_entry = tk.Entry(self.main_frame, width=30)
        self.in_balance_entry.pack(pady=(0, 10))

        # Out Balance
        out_label = tk.Label(self.main_frame, text="OUT BALANCE", bg="white", fg="black", font=self.sub_font)
        out_label.pack(pady=(0, 2))
        self.out_balance_entry = tk.Entry(self.main_frame, width=30)
        self.out_balance_entry.pack(pady=(0, 10))

        # Clock-In Time
        cin_label = tk.Label(self.main_frame, text="CLOCK-IN TIME", bg="white", fg="black", font=self.sub_font)
        cin_label.pack(pady=(0, 2))
        self.clockin_entry = tk.Entry(self.main_frame, width=30)
        self.clockin_entry.pack(pady=(0, 10))

        # Clock-Out Time
        cout_label = tk.Label(self.main_frame, text="CLOCK-OUT TIME", bg="white", fg="black", font=self.sub_font)
        cout_label.pack(pady=(0, 2))
        self.clockout_entry = tk.Entry(self.main_frame, width=30)
        self.clockout_entry.pack(pady=(0, 10))

        # Date (dropdown)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        inout_date_dropdown = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        inout_date_dropdown.pack(pady=(0, 10))

        # sign up (submit) button
        signup_button = tk.Button(
            self.main_frame,
            text="sign up",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_in_out_balance
        )
        signup_button.pack(pady=10)

    def process_in_out_balance(self):
        """
        Just shows a message for now (no DB insert).
        """
        emp_username = self.inout_emp_entry.get()
        in_balance = self.in_balance_entry.get()
        out_balance = self.out_balance_entry.get()
        clock_in = self.clockin_entry.get()
        clock_out = self.clockout_entry.get()
        date_val = self.inout_date_var.get()

        messagebox.showinfo(
            "In/Out Balance",
            f"Employee: {emp_username}\nIn Balance: {in_balance}\nOut Balance: {out_balance}\n"
            f"Clock-In: {clock_in}\nClock-Out: {clock_out}\nDate: {date_val}"
        )

    def show_expense_form(self):
        """
        Displays a form for entering an expense.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter Expense",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager 1 in Store 1",  # Or adapt for Employee/Owner
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Expense Type
        type_label = tk.Label(self.main_frame, text="EXPENSE TYPE", bg="white", fg="black", font=self.sub_font)
        type_label.pack(pady=(0, 2))
        self.expense_type_entry = tk.Entry(self.main_frame, width=30)
        self.expense_type_entry.pack(pady=(0, 10))

        # Expense Value
        val_label = tk.Label(self.main_frame, text="EXPENSE VALUE", bg="white", fg="black", font=self.sub_font)
        val_label.pack(pady=(0, 2))
        self.expense_value_entry = tk.Entry(self.main_frame, width=30)
        self.expense_value_entry.pack(pady=(0, 10))

        # Date (dropdown)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        expense_date_dropdown = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        expense_date_dropdown.pack(pady=(0, 10))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_expense
        )
        submit_button.pack(pady=10)

    def process_expense(self):
        """
        Just shows a message for now (no DB insert).
        """
        expense_type = self.expense_type_entry.get()
        expense_value = self.expense_value_entry.get()
        date_val = self.expense_date_var.get()

        messagebox.showinfo(
            "Enter Expense",
            f"Expense Type: {expense_type}\nExpense Value: {expense_value}\nDate: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (expense_type and expense_value and date_val):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO expenses (expense_type, expense_value, date) VALUES (%s, %s, %s)"
            cursor.execute(query, (expense_type, expense_value, date_val))
            self.connection.commit()
            messagebox.showinfo("Success", "Expense added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Expense not added")

    # ----------------------------------------------------------------
    # MANAGER & OWNER HOME SCREENS
    # ----------------------------------------------------------------
    def show_manager_home(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Manager Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        manager_options = [
            "Enter Invoice",
            "Enter Expense",
            "Enter Day Gross Sales",
            "Enter Withdraw",
            "Calculate Employee Bonus",
            "Add Employee",
            "Set Employee Rates",
            "View Records",
            "Payroll",
            "Enter Merchandise"
        ]

        for i, option in enumerate(manager_options):
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.manager_option_action(opt)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_manager_actions
        )
        submit_button.pack(pady=20)

    def manager_option_action(self, option):
        if option == "Add Employee":
            self.show_add_employee_form()
        elif option == "Enter Expense":
            # Manager can also see the expense form
            self.show_expense_form()
        elif option == "Enter Invoice":
            self.show_invoice_form()
        elif option == "Calculate Employee Bonus":
            self.show_calc_bonus_form()
        elif option == "Set Employee Rates":
            self.show_set_rates_form()
        elif option == "Enter Merchandise":
            self.show_merchandise_form()
        elif option == "Enter Withdraw":
            self.show_withdraw_form()
        elif option == "Payroll":
            self.show_payroll_form()
        else:
            messagebox.showinfo("Manager Action", f"You clicked: {option}")

    def submit_manager_actions(self):
        messagebox.showinfo("Submit", "Manager actions submitted (placeholder).")

    def show_owner_home(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Owner Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        owner_options = [
            "Enter Invoice",
            "Enter Expense",
            "Enter Day Closeout",
            "Enter Withdraw",
            "Calculate Employee Bonus",
            "Add Employee",
            "Set Employee Rates",
            "View Records",
            "Payroll",
            "Enter Merchandise"
        ]

        for i, option in enumerate(owner_options):
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.owner_option_action(opt)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_owner_actions
        )
        submit_button.pack(pady=20)

    def owner_option_action(self, option):
        if option == "Add Employee":
            self.show_add_employee_form()
        elif option == "Enter Expense":
            self.show_expense_form()
        elif option == "Enter Day Closeout":
            self.show_day_closeout_form()
        elif option == "Enter Invoice":
            self.show_invoice_form()
        elif option == "Calculate Employee Bonus":
            self.show_calc_bonus_form()
        elif option == "Set Employee Rates":
            self.show_set_rates_form()
        elif option == "Enter Merchandise":
            self.show_merchandise_form()
        elif option == "Enter Withdraw":
            self.show_withdraw_form()
        elif option == "Payroll":
            self.show_payroll_form()
        else:
            messagebox.showinfo("Owner Action", f"You clicked: {option}")

    def submit_owner_actions(self):
        messagebox.showinfo("Submit", "Owner actions submitted (placeholder).")

    def show_invoice_form(self):
        self.clear_main_frame()

        # Heading: same style as "Create New Account" but with invoice-specific text.
        heading_label = tk.Label(
            self.main_frame,
            text="Add Invoice",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading
        sub_label = tk.Label(
            self.main_frame,
            text="Enter Invoice Details",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Invoice Number field
        invoice_num_label = tk.Label(
            self.main_frame,
            text="Invoice Number:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        invoice_num_label.pack(pady=(0, 2))
        self.invoice_num_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_num_entry.pack(pady=(0, 10))

        # Company field
        company_label = tk.Label(
            self.main_frame,
            text="Company:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        company_label.pack(pady=(0, 2))
        self.invoice_company_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_company_entry.pack(pady=(0, 10))

        # Amount field
        amount_label = tk.Label(
            self.main_frame,
            text="Amount:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        amount_label.pack(pady=(0, 2))
        self.invoice_amount_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_amount_entry.pack(pady=(0, 10))

        # Date Received field
        date_received_label = tk.Label(
            self.main_frame,
            text="Date Received:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_received_label.pack(pady=(0, 2))
        self.invoice_date_received_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.invoice_date_received_entry.pack(pady=(0, 10))

        # Date Due field
        date_due_label = tk.Label(
            self.main_frame,
            text="Date Due:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_due_label.pack(pady=(0, 2))
        self.invoice_date_due_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.invoice_date_due_entry.pack(pady=(0, 10))

        # Submit button – same style as in Add Employee form.
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_invoice
        )
        submit_button.pack(pady=10)


    def process_invoice(self):
        # For now, simply display the entered values.
        invoice_num = self.invoice_num_entry.get()
        company = self.invoice_company_entry.get()
        amount = self.invoice_amount_entry.get()
        date_received = self.invoice_date_received_entry.get()
        date_due = self.invoice_date_due_entry.get()
        status = "Not Paid"

        messagebox.showinfo(
            "Invoice Submitted",
            f"Invoice Number: {invoice_num}\n"
            f"Company: {company}\n"
            f"Amount: {amount}\n"
            f"Date Received: {date_received}\n"
            f"Date Due: {date_due}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (invoice_num and company and amount and date_received and date_due):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO invoices (status, date_received, company, invoice_number, amount, date_due) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (status, date_received, company, invoice_num, amount, date_due))
            self.connection.commit()
            messagebox.showinfo("Success", "Invoice added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Invoice not added")


    def show_payroll_form(self):
        """
        Displays a Payroll form with:
          - FROM date dropdown
          - TO date dropdown
          - Optional 'Multiple Weeks View' checkbox
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Payroll",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading (e.g. "You're logged in as Manager")
        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # FROM date
        from_label = tk.Label(
            self.main_frame,
            text="FROM",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        from_label.pack(pady=(0, 2))

        self.from_date_var = tk.StringVar()
        # Example list of date ranges
        from_dates = ["2/4 - 2/8", "2/11 - 2/15", "2/18 - 2/22"]
        self.from_date_var.set(from_dates[0])
        from_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.from_date_var,
            values=from_dates,
            state="readonly",
            width=28
        )
        from_dropdown.pack(pady=(0, 10))

        # TO date
        to_label = tk.Label(
            self.main_frame,
            text="TO",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        to_label.pack(pady=(0, 2))

        self.to_date_var = tk.StringVar()
        # Example list of date ranges
        to_dates = ["2/4 - 2/8", "2/11 - 2/15", "2/18 - 2/22"]
        self.to_date_var.set(to_dates[0])
        to_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.to_date_var,
            values=to_dates,
            state="readonly",
            width=28
        )
        to_dropdown.pack(pady=(0, 10))

        # Optional: Multiple Weeks View checkbox
        self.multiple_weeks_var = tk.BooleanVar(value=False)
        multiple_weeks_check = tk.Checkbutton(
            self.main_frame,
            text="Multiple Weeks View",
            bg="white",
            fg="black",
            variable=self.multiple_weeks_var,
            onvalue=True,
            offvalue=False
        )
        multiple_weeks_check.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_payroll
        )
        submit_button.pack()

    def process_payroll(self):
        """
        Collects the payroll date range and checkbox state,
        and displays them in a message.
        (No DB insert or calculation yet.)
        """
        from_date = self.from_date_var.get()
        to_date = self.to_date_var.get()
        multiple_weeks = self.multiple_weeks_var.get()  # True/False

        # For now, just show a message
        messagebox.showinfo(
            "Payroll Submission",
            f"FROM: {from_date}\n"
            f"TO: {to_date}\n"
            f"Multiple Weeks View: {multiple_weeks}"
        )

    # Later, you could query your DB to calculate payroll, etc.

    #from tkcalendar import DateEntry
    def show_withdraw_form(self):
        """
        Displays a form for entering a withdrawal.
        Fields:
          - Username
          - ID
          - Amount
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Enter Withdrawal",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading: "You're logged in as Manager 1 in Store 1" (adapt as needed)
        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager 1 in Store 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Username field
        username_label = tk.Label(
            self.main_frame,
            text="USERNAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(0, 2))
        self.withdraw_username_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_username_entry.insert(0, "Jora Martins")  # Example placeholder
        self.withdraw_username_entry.pack(pady=(0, 10))

        # ID field
        id_label = tk.Label(
            self.main_frame,
            text="ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        id_label.pack(pady=(0, 2))
        self.withdraw_id_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_id_entry.insert(0, "0.0")  # Example placeholder
        self.withdraw_id_entry.pack(pady=(0, 10))

        # Amount field
        amount_label = tk.Label(
            self.main_frame,
            text="AMOUNT",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        amount_label.pack(pady=(0, 2))
        self.withdraw_amount_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_amount_entry.insert(0, "0.0")  # Example placeholder
        self.withdraw_amount_entry.pack(pady=(0, 10))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_withdraw
        )
        submit_button.pack(pady=10)

    def process_withdraw(self):
        """
        Collects the withdrawal data and displays it in a message.
        (No DB insert yet.)
        """
        username = self.withdraw_username_entry.get()
        user_id = self.withdraw_id_entry.get()
        amount = self.withdraw_amount_entry.get()

        # For demonstration, just show a message:
        messagebox.showinfo(
            "Withdrawal Submitted",
            f"Username: {username}\nID: {user_id}\nAmount: {amount}"
        )

        if not (username and user_id and amount):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT name, id FROM users WHERE name = %s AND id = %s"
            cursor.execute(query, (username, user_id))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID and username not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO withdrawals (username, user_id, amount) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, user_id, amount))
            self.connection.commit()
            messagebox.showinfo("Success", "Withdrawal added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Withdrawal not added")

    def show_merchandise_form(self):
        """
        Displays a form for entering merchandise data.
        Fields:
          - Merchandise Type
          - Merchandise Value
          - Date (dropdown or DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Enter Merchandise",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading: "You're logged in as Manager 1 in Store 1" (adapt as needed)
        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager 1 in Store 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # MERCHANDISE TYPE field
        merch_label = tk.Label(
            self.main_frame,
            text="MERCHANDISE TYPE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        merch_label.pack(pady=(0, 2))
        self.merch_type_entry = tk.Entry(self.main_frame, width=30)
        self.merch_type_entry.pack(pady=(0, 10))

        # MERCHANDISE VALUE field
        val_label = tk.Label(
            self.main_frame,
            text="MERCHANDISE VALUE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        val_label.pack(pady=(0, 2))
        self.merch_value_entry = tk.Entry(self.main_frame, width=30)
        self.merch_value_entry.insert(0, "0.0")  # Example placeholder
        self.merch_value_entry.pack(pady=(0, 10))

        # DATE field (dropdown or DateEntry)
        date_label = tk.Label(
            self.main_frame,
            text="DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_label.pack(pady=(0, 2))

        self.merch_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.merch_date_entry.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_merchandise
        )
        submit_button.pack()

    def process_merchandise(self):
        """
        Collects the merchandise data and displays it in a message.
        (No DB insert yet.)
        """
        merch_type = self.merch_type_entry.get()
        merch_value = self.merch_value_entry.get()



        date_val = self.merch_date_entry.get_date()

        messagebox.showinfo(
            "Enter Merchandise",
            f"Merchandise Type: {merch_type}\n"
            f"Merchandise Value: {merch_value}\n"
            f"Date: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (merch_type and merch_value and date_val):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO merchandise (merchandise_type, merchandise_value, date) VALUES (%s, %s, %s)"
            cursor.execute(query, (merch_type, merch_value, date_val))
            self.connection.commit()
            messagebox.showinfo("Success", "Merchandise added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Merchandise not added")


    def show_calc_bonus_form(self):
        """
        Displays a form for calculating an employee's bonus.
        Fields:
          - Employee ID
          - Location (dropdown)
          - Start Date (DateEntry)
          - End Date (DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Calculate Employee Bonus",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading (for demonstration, "You're logged in as Manager 1")
        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Employee ID
        emp_id_label = tk.Label(
            self.main_frame,
            text="EMPLOYEE ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        emp_id_label.pack(pady=(0, 2))
        self.bonus_emp_id_entry = tk.Entry(self.main_frame, width=30)
        self.bonus_emp_id_entry.pack(pady=(0, 10))

        # Location (dropdown)
        location_label = tk.Label(
            self.main_frame,
            text="LOCATION",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        location_label.pack(pady=(0, 2))
        self.location_var = tk.StringVar()
        # Example location list
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.location_var.set(locations[0])
        location_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.location_var,
            values=locations,
            state="readonly",
            width=28
        )
        location_dropdown.pack(pady=(0, 10))

        # Start Date (DateEntry)
        start_label = tk.Label(
            self.main_frame,
            text="START DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        start_label.pack(pady=(0, 2))

        self.start_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.start_date.pack(pady=(0, 10))

        # End Date (DateEntry)
        end_label = tk.Label(
            self.main_frame,
            text="END DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        end_label.pack(pady=(0, 2))
        self.end_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.end_date.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_calc_bonus
        )
        submit_button.pack()


    def show_set_rates_form(self):
        """
        Displays a form for setting employee rates.
        Fields:
          - Location (dropdown)
          - Employee ID
          - Bonus Rate
          - Rate Per Hour
          - Date (DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Set Employee Rates",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading: "You're logged in as Manager 1" (adapt as needed)
        sub_label = tk.Label(
            self.main_frame,
            text="You're logged in as Manager 1",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Location (dropdown)
        loc_label = tk.Label(self.main_frame, text="LOCATION", bg="white", fg="black", font=self.sub_font)
        loc_label.pack(pady=(0, 2))
        self.rates_location_var = tk.StringVar()
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.rates_location_var.set(locations[0])
        loc_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.rates_location_var,
            values=locations,
            state="readonly",
            width=28
        )
        loc_dropdown.pack(pady=(0, 10))

        # Employee ID
        empid_label = tk.Label(self.main_frame, text="EMPLOYEE ID", bg="white", fg="black", font=self.sub_font)
        empid_label.pack(pady=(0, 2))
        self.rates_empid_entry = tk.Entry(self.main_frame, width=30)
        self.rates_empid_entry.pack(pady=(0, 10))

        # Bonus Rate
        bonus_label = tk.Label(self.main_frame, text="BONUS RATE", bg="white", fg="black", font=self.sub_font)
        bonus_label.pack(pady=(0, 2))
        self.rates_bonus_entry = tk.Entry(self.main_frame, width=30)
        self.rates_bonus_entry.insert(0, "0.02")  # Example default
        self.rates_bonus_entry.pack(pady=(0, 10))

        # Rate Per Hour
        rate_label = tk.Label(self.main_frame, text="RATE PER HOUR", bg="white", fg="black", font=self.sub_font)
        rate_label.pack(pady=(0, 2))
        self.rates_hour_entry = tk.Entry(self.main_frame, width=30)
        self.rates_hour_entry.insert(0, "16.00")  # Example default
        self.rates_hour_entry.pack(pady=(0, 10))

        # Date (DateEntry)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        self.rates_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.rates_date_entry.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_set_rates
        )
        submit_button.pack()

    def process_set_rates(self):
        """
        Collects the data from the Set Employee Rates form
        and displays it in a message. (No DB insert yet.)
        """
        location = self.rates_location_var.get()
        emp_id = self.rates_empid_entry.get()
        bonus_rate = self.rates_bonus_entry.get()
        rate_per_hour = self.rates_hour_entry.get()
        date_val = self.rates_date_entry.get_date()  # .get_date() returns a Python date object

        # For now, just show the collected data in a messagebox
        messagebox.showinfo(
            "Set Employee Rates",
            f"Location: {location}\n"
            f"Employee ID: {emp_id}\n"
            f"Bonus Rate: {bonus_rate}\n"
            f"Rate Per Hour: {rate_per_hour}\n"
            f"Date: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (location and emp_id and bonus_rate and rate_per_hour and date_val):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM users WHERE id = %s"
            cursor.execute(query, (emp_id))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO employee_rates (employee_id, location, bonus_rate, rate_per_hour, date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (emp_id, location, bonus_rate, rate_per_hour, date_val))
            self.connection.commit()
            messagebox.showinfo("Success", "Rates added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Rates not added")

    def process_calc_bonus(self):
        """
        Gathers the data from the bonus form fields
        and displays a message. (No DB insert yet.)
        """
        emp_id = self.bonus_emp_id_entry.get()
        location = self.location_var.get()
        start_date_val = self.start_date.get_date()  # .get_date() returns a Python date object
        end_date_val = self.end_date.get_date()

        # For demonstration, just show a message with the values:
        messagebox.showinfo(
            "Calculate Employee Bonus",
            f"Employee ID: {emp_id}\n"
            f"Location: {location}\n"
            f"Start Date: {start_date_val}\n"
            f"End Date: {end_date_val}"
        )

        # If you want to do more, e.g., database queries, you can do it here.

    # ----------------------------------------------------------------
    # ADD EMPLOYEE FORM
    # ----------------------------------------------------------------
    def show_add_employee_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Create New Account",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Already Registered? Login",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # ROLE
        role_label = tk.Label(
            self.main_frame,
            text="ROLE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        role_label.pack(pady=(0, 2))

        self.emp_role_var = tk.StringVar()
        roles = ["Employee", "Manager", "Owner"]
        self.emp_role_var.set(roles[0])
        role_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.emp_role_var,
            values=roles,
            state="readonly"
        )
        role_dropdown.pack(pady=(0, 10))

        # ID (not stored in the DB with this table structure)
        emp_id_label = tk.Label(
            self.main_frame,
            text="ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        emp_id_label.pack(pady=(0, 2))
        self.emp_id_entry = tk.Entry(self.main_frame, width=30)
        self.emp_id_entry.pack(pady=(0, 10))

        # NAME
        name_label = tk.Label(
            self.main_frame,
            text="NAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        name_label.pack(pady=(0, 2))
        self.emp_name_entry = tk.Entry(self.main_frame, width=30)
        self.emp_name_entry.pack(pady=(0, 10))

        # PASSWORD
        pass_label = tk.Label(
            self.main_frame,
            text="PASSWORD",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        pass_label.pack(pady=(0, 2))
        self.emp_pass_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.emp_pass_entry.pack(pady=(0, 10))

        # Sign Up button
        signup_button = tk.Button(
            self.main_frame,
            text="sign up",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_add_employee
        )
        signup_button.pack(pady=10)

    def process_add_employee(self):
        role = self.emp_role_var.get()
        _ignored_id = self.emp_id_entry.get()
        name = self.emp_name_entry.get()
        password = self.emp_pass_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (role and name and password):
            messagebox.showerror("Error", "Role, Name, and Password are required.")
            return

        try:
            cursor = self.connection.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = "INSERT INTO users (name, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, hashed_password, role))
            self.connection.commit()
            messagebox.showinfo("Success", f"New user '{name}' added with role '{role}'.")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", f"Error creating user: {err}")

    # ----------------------------------------------------------------
    # NAVIGATION & MISC
    # ----------------------------------------------------------------
    def go_back(self):
        if hasattr(self, "user_role"):
            if self.user_role == "Manager":
                self.show_manager_home()
            elif self.user_role == "Owner":
                self.show_owner_home()
            elif self.user_role == "Employee":
                self.show_employee_home()
            else:
                messagebox.showerror("Error", "Unknown role. Returning to welcome screen.")
                self.show_welcome_screen()
        else:
            # If no role is stored, return to the welcome screen
            self.show_welcome_screen()

    def option1_action(self):
        print("Option 1 selected.")

    def option2_action(self):
        print("Option 2 selected.")


if __name__ == "__main__":
    app = AlohaCorpApp()
    app.mainloop()
