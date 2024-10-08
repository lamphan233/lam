import tkinter as tk
from tkinter import messagebox
import psycopg2

def connect_db():
    try:
        # Kết nối đến cơ sở dữ liệu PostgreSQL
        connection = psycopg2.connect(
            dbname='my_database',
            user='postgres',
            password='liemlam159',
            host='localhost',  # Thay đổi nếu cần
            port='5432'        # Thay đổi nếu cần
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None
    
def create_table(connection):
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
    cursor.close()

def submit_data(name_entry, age_entry, gender_var, notes_text):
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    notes = notes_text.get("1.0", tk.END).strip()
    
    # Kiểm tra nếu trường nào chưa được điền
    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
    elif not age:
        messagebox.showerror("Input Error", "Please enter your age.")
    elif not age.isdigit():
        messagebox.showerror("Input Error", "Age must be a number.")
    else:
        # Kết nối tới cơ sở dữ liệu
        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users (name, age, gender, notes) VALUES (%s, %s, %s, %s)",
                               (name, int(age), gender, notes))
                connection.commit()
                cursor.close()
                
                # Hiển thị kết quả
                result = f"Name: {name}\nAge: {age}\nGender: {gender}\nNotes: {notes}"
                messagebox.showinfo("Submitted Information", result)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                connection.close()

def on_exit():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        win.destroy()

def show_info():
    messagebox.showinfo("Information", "This is an advanced Python project!")

def save_data():
    # Thông báo sau khi bấm nút Save
    messagebox.showinfo("Save", "Your information has been saved successfully!")

def submit_data(name_entry, age_entry, gender_var, notes_text):
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    notes = notes_text.get("1.0", "end-1c").strip()  # Lấy nội dung từ Text widget
    
    # Kiểm tra nếu trường nào chưa được điền
    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
    elif not age:
        messagebox.showerror("Input Error", "Please enter your age.")
    elif not age.isdigit():
        messagebox.showerror("Input Error", "Age must be a number.")
    else:
        # Hiển thị kết quả trong cửa sổ thông báo nếu đã điền đủ
        result = f"Name: {name}\nAge: {age}\nGender: {gender}\nNotes: {notes}"
        messagebox.showinfo("Submitted Information", result)

def create_new_window():
    # Tạo cửa sổ mới
    new_window = tk.Toplevel(win)
    new_window.title("Thông tin cơ bản - New Window")
    new_window.geometry("400x400")
    new_window.config(bg="#D3E4CD")

    # Menu
    menu_bar = tk.Menu(new_window)
    
    # Menu File
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=create_new_window)
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Save", command=save_data)  # Thêm thông báo khi lưu thông tin
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: new_window.destroy())
    menu_bar.add_cascade(label="File", menu=file_menu)
    
    # Menu Help
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=show_info)
    help_menu.add_command(label="User Guide", command=show_user_guide)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    
    new_window.config(menu=menu_bar)

    # Frame chứa các widget
    frame = tk.Frame(new_window, bg="#E8F6EF")
    frame.pack(pady=10)

    label_frame = tk.LabelFrame(frame, text="User Information", padx=10, pady=10, bg="#FFDDC1", fg="black")
    label_frame.pack(padx=10, pady=10)

    # Widgets nhập thông tin
    name_label = tk.Label(label_frame, text="Name:", bg="#FFDDC1", fg="black")
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = tk.Entry(label_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    age_label = tk.Label(label_frame, text="Age:", bg="#FFDDC1", fg="black")
    age_label.grid(row=1, column=0, padx=5, pady=5)

    age_entry = tk.Entry(label_frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)

    # Radio buttons chọn giới tính
    gender_var = tk.StringVar(value="Male")  # Giá trị mặc định là "Male"

    gender_label = tk.Label(label_frame, text="Gender:", bg="#FFDDC1", fg="black")
    gender_label.grid(row=2, column=0, padx=5, pady=5)

    male_rb = tk.Radiobutton(label_frame, text="Male", variable=gender_var, value="Male", bg="#FFDDC1", fg="black")
    male_rb.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    female_rb = tk.Radiobutton(label_frame, text="Female", variable=gender_var, value="Female", bg="#FFDDC1", fg="black")
    female_rb.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    # Khu vực ghi chú
    notes_label = tk.Label(label_frame, text="Notes:", bg="#FFDDC1", fg="black")
    notes_label.grid(row=3, column=0, padx=5, pady=5)

    notes_text = tk.Text(label_frame, height=4, width=30)
    notes_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    # Nút Submit
    submit_button = tk.Button(frame, text="Submit", bg="#A8D5BA", fg="black", command=lambda: submit_data(name_entry, age_entry, gender_var, notes_text))
    submit_button.pack(pady=10)

def show_user_guide():
    guide = (
        "User Guide:\n\n"
        "1. Enter your Name and Age in the respective fields.\n"
        "2. Select your Gender using the radio buttons.\n"
        "3. Add any notes or additional information in the Notes section.\n"
        "4. Click the Submit button to display the entered information.\n"
        "5. You can access this guide anytime via Help -> User Guide."
    )
    messagebox.showinfo("User Guide", guide)

# Cửa sổ chính
win = tk.Tk()
win.title("Thông tin cơ bản")
win.geometry("400x400")

# Kết nối CSDL và tạo bảng
connection = connect_db()
if connection:
    create_table(connection)
    connection.close()

# Menu
menu_bar = tk.Menu(win)

# Menu File
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=create_new_window)  # Gọi hàm mở cửa sổ mới
file_menu.add_command(label="Open")
file_menu.add_command(label="Save", command=save_data)  # Thêm thông báo khi lưu thông tin
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Menu Help
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_info)
help_menu.add_command(label="User Guide", command=show_user_guide)  # Thêm mục User Guide
menu_bar.add_cascade(label="Help", menu=help_menu)

win.config(menu=menu_bar)

# Frame chứa các widget
frame = tk.Frame(win, bg="#E8F6EF")
frame.pack(pady=10)

label_frame = tk.LabelFrame(frame, text="User Information", padx=10, pady=10, bg="#FFDDC1", fg="black")
label_frame.pack(padx=10, pady=10)

# Widgets nhập thông tin
name_label = tk.Label(label_frame, text="Name:", bg="#FFDDC1", fg="black")
name_label.grid(row=0, column=0, padx=5, pady=5)

name_entry = tk.Entry(label_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

age_label = tk.Label(label_frame, text="Age:", bg="#FFDDC1", fg="black")
age_label.grid(row=1, column=0, padx=5, pady=5)

age_entry = tk.Entry(label_frame)
age_entry.grid(row=1, column=1, padx=5, pady=5)

# Radio buttons chọn giới tính
gender_var = tk.StringVar(value="Male")  # Giá trị mặc định là "Male"

gender_label = tk.Label(label_frame, text="Gender:", bg="#FFDDC1", fg="black")
gender_label.grid(row=2, column=0, padx=5, pady=5)

male_rb = tk.Radiobutton(label_frame, text="Male", variable=gender_var, value="Male", bg="#FFDDC1", fg="black")
male_rb.grid(row=2, column=1, padx=5, pady=5, sticky="w")

female_rb = tk.Radiobutton(label_frame, text="Female", variable=gender_var, value="Female", bg="#FFDDC1", fg="black")
female_rb.grid(row=2, column=2, padx=5, pady=5, sticky="w")

# Khu vực ghi chú
notes_label = tk.Label(label_frame, text="Notes:", bg="#FFDDC1", fg="black")
notes_label.grid(row=3, column=0, padx=5, pady=5)

notes_text = tk.Text(label_frame, height=4, width=30)
notes_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

# Nút Submit
submit_button = tk.Button(frame, text="Submit", bg="#A8D5BA", fg="black", command=lambda: submit_data(name_entry, age_entry, gender_var, notes_text))
submit_button.pack(pady=10)

# Bắt đầu vòng lặp chính
win.protocol("WM_DELETE_WINDOW", on_exit)
win.mainloop()
