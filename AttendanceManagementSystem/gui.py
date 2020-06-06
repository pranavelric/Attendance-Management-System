import tkinter
from tkinter import *
from tkinter import Tk
from tkinter import ttk
import datetime as dt
from cv2 import cv2
from PIL import Image, ImageTk
import imutils
import tkinter.simpledialog
import tkinter.filedialog
from tkinter import messagebox
from firebase_admin import credentials, firestore
import firebase_admin


class Video:
    cap = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')

    def __init__(self):
        cap = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbours, color, text):
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(
            grey_img, scaleFactor, minNeighbours)
        cord = []
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cord = [x, y, w, h]
        return cord, len(features)

    def detect(self, img, faceCascade):
        color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0)}
        cord, count = self.draw_boundary(img, faceCascade, 1.2,
                                         10, color['blue'], "")
        return img, count

    def show_frame(self):

        _, frame = self.cap.read()
        # frame = imutils.resize(frame, height=750, width=850)
        frame = cv2.resize(frame, (730,
                                   850), fx=0, fy=0.5)

        frame, count = self.detect(frame, self.faceCascade)
        frame = cv2.flip(frame, 1)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        display1.imgtk = imgtk
        display1.configure(image=imgtk)

        student_number_label.config(text=str(count))
        tab1.after(10, self.show_frame)

    def __del__(self):
        print("")


def save(course_name, student_number, time):

    c = tkinter.simpledialog.askstring(
        "Password", "Enter password:",  show='*')
    if c == "123456":
        num_stud = 0
        retrive_num_stud = database.collection(
            course_name).where('time', '==', time).stream()
        for num in retrive_num_stud:
            num_stud += num.to_dict()['Number of students']

        print(course_name, '    ', student_number, '  ', time)

        data_entry = database.collection(course_name).document(time)
        data_entry.set({
            'time': time,
            'Number of students': int(student_number)+int(num_stud)
        })

        messagebox.showinfo(title="Done", message="Data successfully saved")
        print("Data Saved")
    else:
        messagebox.showerror(title="Error", message="Wrong Password!"
                             )


global d
d = Video()


def ok():
    v = choice_ways_var.get()

    global d
    if v == 1:
        f = tkinter.filedialog.askopenfile(mode='r')

        if f != None:
            image_radio_btn.config(bg="green")
            video_radio_btn.config(bg="yellow")
            center_frame.grid_forget()
            display1.pack_forget()
            try:
                d.cap.release()
                cv2.destroyAllWindows()
                del(d)
            except NameError:
                print("Choosing pic again")

            img = Image.open(f.name)
            img = img.resize((730, 750), Image.ANTIALIAS)
            filename = ImageTk.PhotoImage(img)

            canvas.image = filename
            canvas.create_image(0, 0, anchor='nw', image=filename)
            canvas.pack()

            # image count faces
            faceCascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')
            img = cv2.imread(f.name)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 10)
            count_faces = str(len(faces))
            student_number_label.config(text=str(count_faces))

        # canvas.(row=0, column=0, sticky=N+S+E+W)

    else:
        display1.pack()
        canvas.pack_forget()
        image_radio_btn.config(bg="yellow")
        video_radio_btn.config(bg="green")

        d = Video()
        d.cap = cv2.VideoCapture(0)
        d.show_frame()


def retrive(tab2_course_name):
    course_data_listbox.delete(0, END)

    retrived_data = database.collection(tab2_course_name).stream()
    total = 0
    for data in retrived_data:

        course_data_listbox.insert(END, "")
        course_data_listbox.insert(
            END, f"({data.id}) ::   Number of Students present =>{data.to_dict()['Number of students']}")

        total += int(data.to_dict()["Number of students"])

    course_data_listbox.insert(
        0, f"Total Attendance count for this class is => {total} \n\n\n"
    )
    course_data_listbox.insert(1, "")


if __name__ == "__main__":

    d = Video()
    # initalizing firebase
    cred = credentials.Certificate('firebaseKey.json')
    firebase_admin.initialize_app(cred)
    database = firestore.client()
    # done initalizing

    root = Tk()
    root.geometry("1000x700")
    root.configure(background='gray5', bd=1, relief=SUNKEN,)
    root.minsize(1000, 700)
    root.maxsize(1000, 700)

    root.title("Attendance Management System")
    root.wm_iconbitmap('Webaly.ico')

    # theme for tabs

    myblack = "#000000"
    myyellow = "#FFFF00"

    style = ttk.Style()

    style.theme_create("theme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": "gray5"}, },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": myblack, "foreground": myyellow},
            "map":       {"background": [("selected", myyellow)], "foreground": [("selected", myblack)],
                          "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("theme")

    # theme ended
    top_top_frame = Frame(root, bg="black", relief=SUNKEN)
    top_top_frame.grid(row=0, column=0, sticky="nsew")

    # making tabs
    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text="Home")
    tabControl.grid(row=1, column=0, sticky="nsew")
    # tabControl.pack(expand=True, fill="both")

    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text="Retrive",)
    tabControl.grid(row=1, column=0, sticky="nsew")
    # tabControl.pack(expand=True, fill="both")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # elements of tab1

    top_frame = Frame(tab1, bg='black', relief=SUNKEN)
    center = Frame(tab1, bg='gray2', relief=SUNKEN)
    btm_frame = Frame(tab1, bg='white', relief=SUNKEN)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    tab1.grid_rowconfigure(1, weight=1)
    tab1.grid_columnconfigure(0, weight=1)

    heading_label = Label(top_top_frame, text="Attendance Management System",
                          bd=5, bg="black", fg="white", relief=SUNKEN, font="Verdana 15 bold", anchor=CENTER,)
    heading_label.pack(fill=X)

    center_frame = Frame(center, bg="gray6", relief=SUNKEN, bd=1)
    center_frame.pack(fill=BOTH, side=LEFT, expand=True)

    display1 = Label(center_frame, bg='black')
    display1.pack(fill=BOTH)
    canvas = Canvas(center_frame, height=850, width=730)
    # display1.grid(row=0, column=0, sticky=N+S+W+E)

    right_frame = Frame(center, bg="gray4", relief=SUNKEN,)
    right_frame.pack(side=RIGHT, fill=Y)

    select_course_label = Label(right_frame, text="Select Cource",
                                bd=1, bg="black", fg="white", relief=RAISED, font="Verdana 11 ", anchor=W)
    select_course_label.grid(row=0, column=0, padx=(5, 2),
                             pady=(5, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    course_choice = {'CS206', 'CS205', 'CS203', 'ES205', 'MS201'}
    course_var = StringVar(tab1)
    course_var.set('CS206')
    course_popupmenu = OptionMenu(right_frame, course_var, *course_choice)
    course_popupmenu.grid(row=0, column=1, padx=(5, 2),
                          pady=(5, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)
    course_popupmenu.config(
        background='gray6', foreground='white', activebackground="yellow"
    )
    course_popupmenu["menu"].config(
        background='gray9', foreground='white', activebackground="yellow", activeforeground="black"
    )

    course_name = "CS206"
    student_number = 0

    def getOptionMenuValue(*args):
        global course_name
        course_name = course_var.get()
        print(course_var.get(), ' is selected ')

    course_var.trace('w', getOptionMenuValue)

    # method to count students using radio buttons
    choice_ways_var = IntVar()
    # choice_ways_var.set(1)
    Label(right_frame, text="How do you want to take attendance?", bd=0,
          fg="white", bg="black", font="Verdana 9 bold", relief=SUNKEN).grid(row=1, column=0, columnspan=2, rowspan=1, padx=(5, 2), pady=15, sticky=N+S+W+E)
    image_radio_btn = Radiobutton(
        right_frame, text="Image", padx=5,  activebackground="black", activeforeground="yellow", variable=choice_ways_var, value=1, bg="yellow", bd=0, anchor=W, fg="black", font="Verdana 10")
    image_radio_btn.grid(row=2, column=0, columnspan=2,
                         rowspan=1, padx=(5, 2), pady=1, sticky=N+S+W+E)
    video_radio_btn = Radiobutton(
        right_frame, text="Video", padx=5, activebackground="black", activeforeground="yellow", variable=choice_ways_var, value=2, bg="yellow", bd=0, anchor=W, fg="black", font="Verdana 10")
    video_radio_btn.grid(row=3, column=0, columnspan=2,
                         rowspan=1, padx=(5, 2), pady=(1, 5), sticky=N+S+W+E)

    ok_radio_button = Button(right_frame, activebackground="yellow", activeforeground="black", text="CHECK", bg="black",
                             fg="yellow", font="Verdana 10 bold", relief=RAISED, bd=4, command=ok)
    ok_radio_button.grid(row=4, column=0, padx=(5, 2),
                         pady=(2, 25), sticky=N+S+W+E, columnspan=2, rowspan=1)

    student_present_label = Label(right_frame, text="No. of Students",
                                  bd=1, bg="black", fg="white", relief=RAISED, font="Verdana 11 ", anchor=W)
    student_present_label.grid(row=5, column=0, padx=(5, 2),
                               pady=15, sticky=N+S+W+E, columnspan=1, rowspan=1)

    student_number_label = Label(right_frame, text="0",
                                 bd=1, bg="black", fg="white", relief=SUNKEN, font="Verdana 15 ")
    student_number_label.grid(row=5, column=1, padx=(5, 2),
                              pady=15, sticky=N+S+W+E, columnspan=1, rowspan=1)

    save_button = Button(right_frame, text="Save",
                         bg="yellow", activebackground="black", activeforeground="yellow", fg="black", bd=2, relief=SUNKEN, font="ComicSansMs 12 bold", command=lambda: save(course_name, student_number_label.cget("text"), f"{dt.datetime.now():%a, %b %d %Y}"))
    save_button.grid(row=6, column=0, padx=(0, 0),
                     pady=313, sticky=N+S+W+E, columnspan=2, rowspan=11)

    status_label = Label(btm_frame, text=(f"{dt.datetime.now():%a, %b %d %Y}"),
                         relief=SUNKEN, font="ComicSansMs 10", fg='linen', bg='gray3', bd=0.5, anchor=W)
    status_label.pack(fill=X, side=BOTTOM)
    # elements of tab1 ended

    # elements of tab2

    tab2_top_frame = Frame(tab2, bg='black', relief=SUNKEN)
    tab2_center = Frame(tab2, bg='gray2', relief=SUNKEN)
    tab2_btm_frame = Frame(tab2, bg='white', relief=SUNKEN)

    tab2_top_frame.grid(row=0, sticky="ew")
    tab2_center.grid(row=1, sticky="nsew")
    tab2_btm_frame.grid(row=3, sticky="ew")

    tab2.grid_rowconfigure(1, weight=1)
    tab2.grid_columnconfigure(0, weight=1)

    tab2_center_frame = Frame(tab2_center, bg="gray6", relief=SUNKEN,)
    tab2_center_frame.pack(fill=BOTH, side=LEFT, expand=True)

    tab2_right_frame = Frame(tab2_center, bg="gray4", relief=SUNKEN,)
    tab2_right_frame.pack(side=RIGHT, fill=Y)
    tab2_select_course_label = Label(tab2_right_frame, text="Select Cource",
                                     bd=1, bg="black", fg="white", relief=RAISED, font="Verdana 11 ", anchor=W)
    tab2_select_course_label.grid(row=0, column=0, padx=(5, 2),
                                  pady=(1, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)

    tab2_course_choice = {'CS206', 'CS205', 'CS203', 'ES205', 'MS201'}
    tab2_course_var = StringVar(tab2)
    tab2_course_var.set('CS206')
    tab2_course_popupmenu = OptionMenu(
        tab2_right_frame, tab2_course_var, *tab2_course_choice)
    tab2_course_popupmenu.grid(row=0, column=1, padx=(5, 2),
                               pady=(1, 15), sticky=W+E+N+S, columnspan=1, rowspan=1)
    tab2_course_popupmenu.config(
        background='gray6', foreground='white', activebackground="yellow"
    )
    tab2_course_popupmenu["menu"].config(
        background='gray9', foreground='white', activebackground="yellow", activeforeground="black"
    )

    tab2_course_name = "CS206"

    def tab2_getOptionMenuValue(*args):
        global tab2_course_name
        tab2_course_name = tab2_course_var.get()
        print(tab2_course_var.get(), ' is selected ')

    tab2_course_var.trace('w', tab2_getOptionMenuValue)

    retrive_button = Button(tab2_right_frame, text="Retrive Data", bg="yellow", activebackground="black", activeforeground="yellow",
                            fg="black", bd=2, relief=SUNKEN, font="ComicSansMs 12 bold", command=lambda: retrive(tab2_course_name))

    retrive_button.grid(row=1, column=0, padx=(0, 0), pady=535,
                        sticky=N+S+W+E, columnspan=2, rowspan=11)

    course_data_listbox = Listbox(
        tab2_center_frame, bg="black", fg="yellow", font="Verdana 13 bold", selectbackground="yellow", selectforeground="black", activestyle=None)
    course_data_listbox.pack(expand=True, fill="both")

    status_label = Label(tab2_btm_frame, text=(f"{dt.datetime.now():%a, %b %d %Y}"),
                         relief=SUNKEN, font="ComicSansMs 10", fg='linen', bg='gray3', bd=0.5, anchor=W)
    status_label.pack(fill=X, side=BOTTOM)

    # elements of tab2 ended

    root.mainloop()
