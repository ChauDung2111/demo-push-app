from tkinter import *
import json, os
from Database import *
import re

# ================================ VARIABLE GLOBAL ================================ 
error_pw_label = None
# ================================ INFORMATION FORMATH =============================
def check_password(password):
    is_valid = bool(re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#_]).+$', password))
    return is_valid

# =============================== JSON PROCESSING ===============================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# # =============================== Forget_passord_windown ===============================
def open_forget_password(pw_win):
    pw_win.withdraw()
    fpw = Toplevel()
    fpw.title("Forget Password")
    fpw.geometry("350x250+580+140")
    fpw.resizable(False, False)
    Label(fpw, text="FORGET PASSWORD", font=('Arial', 16, 'bold')).place(x=70, y=10)
    # Username / Email
    Label(fpw, text="Username/Email:", font=('Arial', 11, 'bold')).place(x=12, y=60)
    username_email_entry = Entry(fpw, width=30)
    username_email_entry.place(x=150, y=60)
    # New Password
    Label(fpw, text="New Password:", font=('Arial', 11, 'bold')).place(x=12, y=100)
    new_pw_entry = Entry(fpw, width=30, show="*")
    new_pw_entry.place(x=150, y=100)
    # Confirm Password
    Label(fpw, text="Confirm Password:", font=('Arial', 11, 'bold')).place(x=12, y=140)
    confirm_pw_entry = Entry(fpw, width=30, show="*")
    confirm_pw_entry.place(x=150, y=140)
    msg = Label(fpw, text="", font=('Arial', 10, 'bold'))
    msg.place(x=70, y=180)

    # ==== Show/ hide password ====
    def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')
    eye1 = Button(fpw, text='👁️‍🗨️', relief='flat',
                  command=lambda: toggle_pw(new_pw_entry, eye1))
    eye1.place(x=320, y=98)
    eye2 = Button(fpw, text='👁️‍🗨️', relief='flat',
                  command=lambda: toggle_pw(confirm_pw_entry, eye2))
    eye2.place(x=320, y=138)

    # ==== Reset Password ====
    def reset_password():
        global error_pw_label
        users = load_users()
        name_or_email = username_email_entry.get().strip()
        new_pw = new_pw_entry.get()
        confirm_pw = confirm_pw_entry.get()
        if not name_or_email or not new_pw or not confirm_pw:
            msg.config(text="⚠️ Vui lòng nhập đủ thông tin", fg="red")
            return
        found_user = None
        for username, info in users.items():
            if name_or_email == username or name_or_email == info.get("email", ""):
                found_user = username
                break
        if not found_user:
            msg.config(text="❌ Không tìm thấy tài khoản", fg="red")
            return
        if error_pw_label:
            error_pw_label.destroy()
            error_pw_label = None
        if not check_password(new_pw):
            error_pw_label = Label(fpw, text="Password phải chứa ít nhất kí tự viết hoa, kí đặc biệt và chữ số", fg="red")
            error_pw_label.place(x=15, y=120)
            return
        if new_pw != confirm_pw:
            msg.config(text="⚠️ Mật khẩu không khớp", fg="red")
            return
        # Save new password
        users[found_user]["password"] = new_pw
        save_users(users)
        msg.config(text="✅ Đổi mật khẩu thành công!", fg="green")
        new_pw_entry.delete(0, END)
        confirm_pw_entry.delete(0, END)
        username_email_entry.delete(0, END)
    Button(fpw, text="Reset", bg="blue", fg="white", font=('Arial', 12, 'bold'),
           command=reset_password).place(x=135, y=200)
    
    # =============================== Back to Login ===============================
    def back():
        fpw.destroy()
        pw_win.deiconify()
        for widget in pw_win.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, END)
    Button(fpw, text="Back", relief='flat', command=back).place(x=10, y=220)
    fpw.protocol("WM_DELETE_WINDOW", lambda: None)
