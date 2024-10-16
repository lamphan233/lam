import tkinter as tk
from tkinter import messagebox, ttk, Menu
import psycopg2

# Hàm kết nối tới cơ sở dữ liệu
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname=db_name_entry.get().strip(),
            user=db_user_entry.get().strip(),
            password=db_password_entry.get().strip(),
            host=db_host_entry.get().strip(),
            port=db_port_entry.get().strip()
        )
        messagebox.showinfo("Success", "Database connection successful!")
        create_new_window(connection)
        connection_window.destroy()  # Đóng cửa sổ kết nối sau khi kết nối thành công
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Tạo bảng trong cơ sở dữ liệu nếu chưa có
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                gender VARCHAR(10),
                notes TEXT
            );
        """)
        connection.commit()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cursor.close()

# Hàm thêm dữ liệu vào database
def submit_data(name_entry, age_entry, gender_var, notes_text, connection):
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()   
    notes = notes_text.get("1.0", tk.END).strip()

    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
    elif not age or not age.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid age.")
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, age, gender, notes) VALUES (%s, %s, %s, %s)",
                           (name, int(age), gender, notes))
            connection.commit()
            cursor.close()
            messagebox.showinfo("Success", f"Data for {name} has been saved successfully!")
            reload_data(connection)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

# Hàm cập nhật dữ liệu trong database
def update_data(connection, name_entry, age_entry, gender_var, notes_text):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Update Error", "Please select a record to update.")
        return

    record_id = tree.item(selected_item)['values'][0]
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not name or not age.isdigit():
        messagebox.showerror("Input Error", "Please enter valid details.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET name = %s, age = %s, gender = %s, notes = %s WHERE id = %s",
            (name, int(age), gender, notes, record_id)
        )
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "Record updated successfully!")
        reload_data(connection)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Hàm tìm kiếm dữ liệu trong database
def search_data(connection, search_entry):
    search_term = search_entry.get().strip()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name ILIKE %s", ('%' + search_term + '%',))
        rows = cursor.fetchall()
        cursor.close()

        for row in tree.get_children():
            tree.delete(row)
        if rows:
            for row in rows:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Search Result", "No records found.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Hàm xóa dữ liệu khỏi database
def delete_data(connection):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Delete Error", "No record selected for deletion.")
        return

    record_id = tree.item(selected_item)['values'][0]
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (record_id,))
        connection.commit()
        cursor.close()
        tree.delete(selected_item)
        messagebox.showinfo("Success", f"Record with ID {record_id} has been deleted.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Hàm load lại dữ liệu từ database
def reload_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()

        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Tạo cửa sổ nhập liệu và bảng hiển thị dữ liệu
def create_new_window(connection):
    new_window = tk.Toplevel(win)
    new_window.title("User Information")
    new_window.geometry("800x500")

    # Tạo Menu
    menu_bar = Menu(new_window)
    new_window.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New File", command=lambda: messagebox.showinfo("New File", "New file created!"))
    file_menu.add_command(label="Save", command=lambda: messagebox.showinfo("Save", "Data saved!"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit Database", command=new_window.destroy)

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help", command=lambda: messagebox.showinfo("Help", "User Guide: \n1. Enter user information.\n2. Click 'Add New' to save data.\n3. You can search, update or delete records."))
    
    # Thay đổi màu sắc
    new_window.config(bg="#f0f0f0")
    
    label_frame = tk.LabelFrame(new_window, text="User Information", padx=10, pady=10, bg="#f0f0f0")
    label_frame.pack(padx=10, pady=10)

    # Form nhập liệu
    name_label = tk.Label(label_frame, text="Name:", bg="#f0f0f0")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(label_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    age_label = tk.Label(label_frame, text="Age:", bg="#f0f0f0")
    age_label.grid(row=1, column=0, padx=5, pady=5)
    age_entry = tk.Entry(label_frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)

    gender_var = tk.StringVar(value="Male")
    gender_label = tk.Label(label_frame, text="Gender:", bg="#f0f0f0")
    gender_label.grid(row=2, column=0, padx=5, pady=5)
    male_rb = tk.Radiobutton(label_frame, text="Male", variable=gender_var, value="Male", bg="#f0f0f0")
    male_rb.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    female_rb = tk.Radiobutton(label_frame, text="Female", variable=gender_var, value="Female", bg="#f0f0f0")
    female_rb.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    notes_label = tk.Label(label_frame, text="Notes:", bg="#f0f0f0")
    notes_label.grid(row=3, column=0, padx=5, pady=5)
    notes_text = tk.Text(label_frame, height=4, width=30)
    notes_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    # Nút thêm mới và cập nhật
    submit_button = tk.Button(new_window, text="Add New",
                              command=lambda: submit_data(name_entry, age_entry, gender_var, notes_text, connection))
    submit_button.pack(pady=10)

    update_button = tk.Button(new_window, text="Update",
                              command=lambda: update_data(connection, name_entry, age_entry, gender_var, notes_text))
    update_button.pack(pady=10)

    # Treeview để hiển thị dữ liệu từ database
    global tree
    tree_frame = tk.Frame(new_window)
    tree_frame.pack(pady=20)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
    tree_scroll.config(command=tree.yview)

    tree['columns'] = ("ID", "Name", "Age", "Gender", "Notes")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("ID", anchor=tk.CENTER, width=50)
    tree.column("Name", anchor=tk.W, width=150)
    tree.column("Age", anchor=tk.CENTER, width=50)
    tree.column("Gender", anchor=tk.CENTER, width=100)
    tree.column("Notes", anchor=tk.W, width=200)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("ID", text="ID", anchor=tk.CENTER)
    tree.heading("Name", text="Name", anchor=tk.W)
    tree.heading("Age", text="Age", anchor=tk.CENTER)
    tree.heading("Gender", text="Gender", anchor=tk.CENTER)
    tree.heading("Notes", text="Notes", anchor=tk.W)

    tree.pack(pady=20)

    # Nút tìm kiếm
    search_frame = tk.Frame(new_window)
    search_frame.pack(pady=10)
    
    search_label = tk.Label(search_frame, text="Search by Name:")
    search_label.pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_data(connection, search_entry))
    search_button.pack(side=tk.LEFT, padx=5)

    # Nút xóa
    delete_button = tk.Button(new_window, text="Delete", command=lambda: delete_data(connection))
    delete_button.pack(pady=10)

    # Tải dữ liệu từ database
    create_table(connection)
    reload_data(connection)

# Cửa sổ kết nối cơ sở dữ liệu
def connect_db_window():
    global connection_window, db_name_entry, db_user_entry, db_password_entry, db_host_entry, db_port_entry

    connection_window = tk.Toplevel(win)
    connection_window.title("Connect to Database")

    tk.Label(connection_window, text="Database Name:").pack(pady=5)
    db_name_entry = tk.Entry(connection_window)
    db_name_entry.pack(pady=5)

    tk.Label(connection_window, text="User:").pack(pady=5)
    db_user_entry = tk.Entry(connection_window)
    db_user_entry.pack(pady=5)

    tk.Label(connection_window, text="Password:").pack(pady=5)
    db_password_entry = tk.Entry(connection_window, show="*")
    db_password_entry.pack(pady=5)

    tk.Label(connection_window, text="Host:").pack(pady=5)
    db_host_entry = tk.Entry(connection_window)
    db_host_entry.pack(pady=5)

    tk.Label(connection_window, text="Port:").pack(pady=5)
    db_port_entry = tk.Entry(connection_window)
    db_port_entry.pack(pady=5)

    connect_button = tk.Button(connection_window, text="Connect", command=connect_db)
    connect_button.pack(pady=20)

# Cửa sổ chính
win = tk.Tk()
win.title("Database Management")
win.geometry("300x200")

open_connect_window_button = tk.Button(win, text="Connect to Database", command=connect_db_window)
open_connect_window_button.pack(pady=20)

win.mainloop()
