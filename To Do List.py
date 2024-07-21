from tkinter import *
from tkinter import font
from tkinter import filedialog
import pickle

root = Tk()
root.title("ToDo List")
root.geometry("500x450")
root.config(bg="beige")

my_font = font.Font(
    family="consolas",
    size=23,
    weight="bold")
my_frame = Frame(root)
my_frame.pack(pady=10)

my_list = Listbox(my_frame,
                  font=my_font,
                  width=27,
                  height=7,
                  bg="SystemButtonFace",
                  bd=2,
                  fg="black",
                  highlightthickness=0,
                  selectbackground="green",
                  activestyle="none"
                  )

my_list.pack()

stuff = ["Hello"]
for item in stuff:
    my_list.insert(END, item)

my_entry = Entry(root, font=("helvetica", 22), width=29)
my_entry.pack(pady=20)

button_frame = Frame(root)
button_frame.pack(pady=20)

def delete_task():
    my_list.delete(ANCHOR)

def add_task():
    task = my_entry.get()
    if task:
        my_list.insert(END, task)
        my_entry.delete(0, END)

def mark_completed_task():
    for index in my_list.curselection():
        my_list.itemconfig(index, fg="red")

def mark_incomplete_task():
    for index in my_list.curselection():
        my_list.itemconfig(index, fg="black")

def save_list():
    file_name = filedialog.asksaveasfilename(
        initialdir="D:/Data.dat",
        title="Save file",
        filetypes=(("Dat Files", "*.dat"),
                   ("All Files", "."))
    )
    if file_name:
        if not file_name.endswith(".dat"):
            file_name += ".dat"

        count = 0
        while count < my_list.size():
            if my_list.itemcget(count, "fg") == "#dedede":
                my_list.delete(count)
            else:
                count += 1

        stuff = my_list.get(0, END)

        with open(file_name, 'wb') as output_file:
            pickle.dump(stuff, output_file)

def open_list():
    file_name = filedialog.askopenfilename(
        initialdir="D:/Task 1 ToDoList",
        title="Open file",
        filetypes=(("Dat Files", "*.dat"),
                   ("All Files", "."))
    )
    if file_name:
        my_list.delete(0, END)

        with open(file_name, 'rb') as input_file:
            stuff = pickle.load(input_file)

        for item in stuff:
            my_list.insert(END, item)

def delete_list():
    my_list.delete(0, END)

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File",menu=file_menu)

file_menu.add_command(label="Save list",command=save_list)
file_menu.add_command(label="Open list", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear list", command=delete_list)

add_button = Button(button_frame, text='Add Task',bg="yellow", command=add_task)
delete_button = Button(button_frame, text='Delete Task',bg="yellow", command=delete_task)
mark_complete_button = Button(button_frame, text='Task Completed',bg="yellow", command=mark_completed_task)
mark_incomplete_button = Button(button_frame, text='Incomplete',bg="yellow", command=mark_incomplete_task)

add_button.grid(row=0, column=0)
delete_button.grid(row=0, column=1, padx=40)
mark_complete_button.grid(row=0, column=2)
mark_incomplete_button.grid(row=0, column=4, padx=40)

root.mainloop()