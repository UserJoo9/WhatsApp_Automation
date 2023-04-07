import os
import threading
import time
from tkinter import messagebox
import customtkinter
from tkcalendar import Calendar
import customtkinter as ctk
from tktimepicker import AnalogPicker, AnalogThemes, constants
import pywhatkit
import pyautogui
import datetime
from win32api import GetSystemMetrics
from PIL import Image

windowWidth = GetSystemMetrics(0) / 3
windowHight = GetSystemMetrics(1) / 8
acpectRatio = f'{int(windowWidth)}+{int(windowHight)}'

photoRatio = 20
ph_send_message = customtkinter.CTkImage(light_image=Image.open("img/send_message.png"),
                                  dark_image=Image.open("img/send_message.png"),
                                  size=(photoRatio, photoRatio))

scheduled_message = customtkinter.CTkImage(light_image=Image.open("img/scheduled.png"),
                                  dark_image=Image.open("img/scheduled.png"),
                                  size=(photoRatio, photoRatio))

add_contact = customtkinter.CTkImage(light_image=Image.open("img/add.png"),
                                  dark_image=Image.open("img/add.png"),
                                  size=(photoRatio, photoRatio))

delete = customtkinter.CTkImage(light_image=Image.open("img/delete.png"),
                                  dark_image=Image.open("img/delete.png"),
                                  size=(photoRatio, photoRatio))

send = customtkinter.CTkImage(light_image=Image.open("img/send.png"),
                                  dark_image=Image.open("img/send.png"),
                                  size=(photoRatio, photoRatio))

customtkinter.set_appearance_mode("System")

class Whatsapp():

    def __init__(self):
        if not os.path.exists("database"):
            os.mkdir("database")
        threading.Thread(target=self.scheduled_Messages).start()

    def WAUI(self):
        self.top = customtkinter.CTk()
        self.top.geometry(acpectRatio)
        self.top.title("WA Automation")
        self.top.resizable(False, False)

        self.wa_banner_label = customtkinter.CTkLabel(self.top, text="Contacts list", font=("cairo", 20, "bold"), width=300,
                                                 corner_radius=15)
        self.wa_banner_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.contact_list = customtkinter.CTkTextbox(self.top, width=400, height=400, state="disabled",
                                                font=("cairo", 18, "bold"),
                                                corner_radius=15)
        self.contact_list.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        self.manage_label = customtkinter.CTkLabel(self.top, text="Manage contacts", font=("cairo", 16, "bold"),
                                              corner_radius=15)
        self.manage_label.grid(row=2, column=1, pady=10, padx=5)

        self.add_contact_button = customtkinter.CTkButton(self.top, text="Add contact", font=("cairo", 14, "bold"), width=180,
                                                     command=self.addContact, corner_radius=15,
                                                     image=add_contact, compound="right")
        self.add_contact_button.grid(row=3, column=1, pady=(0,10))

        self.delete_contact_button = customtkinter.CTkButton(self.top, text="Delete contact", font=("cairo", 14, "bold"),
                                                        width=180, image=delete, compound="right",
                                                        fg_color="brown", hover_color="red", command=self.delContact,
                                                        corner_radius=15)
        self.delete_contact_button.grid(row=4, column=1, pady=(0, 10))

        self.manage_message_label = customtkinter.CTkLabel(self.top, text="Manage messages", font=("cairo", 16, "bold"),
                                                      corner_radius=15)
        self.manage_message_label.grid(row=2, column=0, pady=10, padx=5)

        self._message = customtkinter.CTkButton(self.top, image=ph_send_message, text="Send message", font=("cairo", 14, "bold"),
                                           width=180, corner_radius=15, command=self.msgui, compound="right")
        self._message.grid(row=3, column=0, pady=(0,10))

        self.timed_message = customtkinter.CTkButton(self.top, image=scheduled_message, text="Scheduled", font=("cairo", 14, "bold"), width=180,
                                                corner_radius=15, command=self.scheduledui, compound="right")
        self.timed_message.grid(row=4, column=0, pady=(0,10))

        self.top.protocol("WM_DELETE_WINDOW", self.stopWA)
        self.readSavedContact()
        self.top.mainloop()

    def stopWA(self):
        try:
            self.top.destroy()
        except:
            pass

    def readSavedContact(self):
        try:
            self.contact_list.configure(state="normal")
            self.contact_list.delete("1.0", "end")
            with open("database/contacts.caap", "r") as f:
                self.contacts = f.read()
            f.close()
            self.contacts = self.contacts.split("\n")
            for i in self.contacts:
                i = i.split("~")
                self.contact_list.insert("end", f"{i[0]}\n{i[1][:15]}******\n\n")
        except:
            pass
        self.contact_list.configure(state="disabled")

    def addContact(self):
        try:
            self.add.destroy()
        except:
            pass

        self.add = customtkinter.CTkToplevel(self.top)
        self.add.resizable(False, False)
        self.add.title("Add Contact")
        self.add.geometry(acpectRatio)

        self.add_banner_label = customtkinter.CTkLabel(self.add, text="Add contact", font=("cairo", 20, "bold"), width=300,
                                                 corner_radius=15)
        self.add_banner_label.pack(pady=(10,0), padx=10)

        self.name_entry = customtkinter.CTkEntry(self.add, placeholder_text="Contact name", width=300,
                                            corner_radius=15)
        self.name_entry.pack(pady=20, padx=10)

        self.number_entry = customtkinter.CTkEntry(self.add, placeholder_text="Contact number", width=300,
                                              corner_radius=15)
        self.number_entry.pack(padx=10)
        self.number_entry.bind("<Return>", self.saveContact)

        self.save_button = customtkinter.CTkButton(self.add, text="Save", image=add_contact, width=200, command=self.saveContact,
                                              corner_radius=15, compound="right")
        self.save_button.pack(pady=10, padx=10)

        self.add.after(100, self.add.lift)

    def saveContact(self, *args):
        name = self.name_entry.get()
        number = self.number_entry.get()
        if not number.startswith("+"):
            messagebox.showerror("number error!", "the number is invalid!\ntry to write it with country code!", parent=self.add)
        elif len(name) < 4:
            messagebox.showerror("name error!", "the name is too short!", parent=self.add)
        else:
            self.name_entry.delete("0", "end")
            self.number_entry.delete("0", "end")
            data = ''
            try:
                with open("database/contacts.caap", "r") as f:
                    data = f.read()
                f.close()
                data = data.split("\n")
            except:
                pass
            added = False
            for i in data:
                i = i.split("~")
                try:
                    if i[0] == "Name: "+name or i[1] == "Number: "+number:
                        added = True
                        messagebox.showerror("error", "this name already exists!!", parent=self.add)
                except:
                    pass
            if not added:
                with open("database/contacts.caap", "a") as f:
                    f.write(f"Name: {name}~Number: {number}\n")
                f.close()
            self.readSavedContact()

    def delContact(self):
        try:
            self.dell.destroy()
        except:
            pass
        self.dell = customtkinter.CTkToplevel(self.top)
        self.dell.resizable(False, False)
        self.dell.title("Delete Contact")
        self.dell.geometry(acpectRatio)

        self.dell_banner_label = customtkinter.CTkLabel(self.dell, text="Delete contact", font=("cairo", 20, "bold"), width=300,
                                                  corner_radius=15)
        self.dell_banner_label.pack(pady=(10,0), padx=10)

        self.xname = customtkinter.CTkEntry(self.dell, placeholder_text="Contact name", width=300, corner_radius=15)
        self.xname.pack(pady=20, padx=10)
        self.xname.bind("<Return>", self.trashContact)

        self.save_button = customtkinter.CTkButton(self.dell, text="Delete", width=200, fg_color="brown", hover_color="red",
                                              command=self.trashContact, corner_radius=15, image=delete,
                                              compound="right")
        self.save_button.pack(pady=10, padx=10)

        self.dell.after(100, self.dell.lift)

    def trashContact(self, *args):
        name = self.xname.get()
        self.xname.delete("0", "end")
        with open("database/contacts.caap", "r") as f:
            data = f.read()
        f.close()
        data = data.split("\n")
        trashed = False
        for i in data:
            i = i.split("~")
            if i[0] == "Name: "+name:
                trashed = True
                i = i[0]+"~"+i[1]
                data.pop(data.index(i))
                data.pop(-1)
                with open("database/contacts.caap", "w") as f:
                    pass
                f.close()
                for x in data:
                    with open("database/contacts.caap", "a") as f:
                        f.write(x+"\n")
                    f.close()

        if not trashed:
            messagebox.showwarning("not found!!", "this name not fount in contacts!!", parent=self.dell)

        self.readSavedContact()

    def scheduledui(self):
        try:
            self.scheduled.destroy()
        except:
            pass
        self.scheduled = customtkinter.CTkToplevel(self.top)
        self.scheduled.resizable(False, False)
        self.scheduled.title("scheduled messages")
        self.scheduled.geometry(acpectRatio)
        self.scheduled_banner_label = customtkinter.CTkLabel(self.scheduled, text="Scheduled list", font=("cairo", 20, "bold"), width=150,
                                                 corner_radius=15)
        self.scheduled_banner_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.scheduled_list = customtkinter.CTkTextbox(self.scheduled, width=300, height=580, state="disabled",
                                                font=("cairo", 16, "bold"),
                                                corner_radius=15)
        self.scheduled_list.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        cont = ['']
        try:
            with open("database/contacts.caap", "r") as f:
                contacts = f.read()
            f.close()
            contacts = contacts.split("\n")
            for i in contacts:
                i = i.split("~")
                cont.append(i[0][6:])

        except:
            pass

        self.select_name = customtkinter.CTkOptionMenu(self.scheduled, values=cont[1:-1], width=250, corner_radius=15,
                                                font=("cairo", 12, "bold"))
        self.select_name.grid(row=2, column=0, columnspan=2, pady=(0,10), padx=10)
        self.select_name.set(cont[1])

        self.message = customtkinter.CTkEntry(self.scheduled, placeholder_text="Message", width=250, corner_radius=15)
        self.message.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10))

        self.scheduled_button = customtkinter.CTkButton(self.scheduled, text="Confirm", corner_radius=15, font=("cairo", 14, "bold"),
                                                   width=250, command=self.set_scheduled_message, image=scheduled_message,
                                                   compound="right")
        self.scheduled_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.delete_label = customtkinter.CTkLabel(self.scheduled, text="Delete scheduled message", font=("cairo", 16, "bold"))
        self.delete_label.grid(row=2, column=2)

        self.iid = customtkinter.CTkEntry(self.scheduled, placeholder_text="Scheduled ID", width=250, corner_radius=15)
        self.iid.grid(row=3, column=2, padx=10, pady=(0, 10))

        self.delete_scheduled_button = customtkinter.CTkButton(self.scheduled, text="Delete", corner_radius=15, font=("cairo", 14, "bold"),
                                                          width=250, command=self.del_scheduled_message, fg_color="brown",
                                                          image=delete, compound="right")
        self.delete_scheduled_button.grid(row=4, column=2, pady=(0, 10))

        self.date_banner_label = customtkinter.CTkLabel(self.scheduled, text="Date & time", font=("cairo", 20, "bold"),
                                                        width=150,
                                                        corner_radius=15)
        self.date_banner_label.grid(row=0, column=2, pady=10, padx=10)
        self.date_frame = customtkinter.CTkFrame(self.scheduled, corner_radius=15)
        self.date_frame.grid(row=1, column=2, padx=10, pady=10)

        self.cal = Calendar(self.date_frame, selectmode='day', locale='en_US', disabledforeground='red',
                       cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                       selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        self.cal.pack(padx=10, pady=5, fill="both", expand=True)

        self.time_picker = AnalogPicker(self.date_frame, type=constants.HOURS24)
        self.theme = AnalogThemes(self.time_picker)
        self.theme.setDracula()
        self.time_picker.pack(padx=10, pady=5)

        self.button = ctk.CTkButton(self.date_frame, text="Check", corner_radius=15, command=self.get_time)
        self.button.pack(padx=10, pady=5)

        self.label = ctk.CTkLabel(self.date_frame, text="")
        self.label.pack(padx=10, pady=5)
        self.check_scheduled_messages()

        self.scheduled.after(100, self.scheduled.lift)

    def get_time(self):
        self.date = self.cal.get_date()
        self.data = self.date.split("/")
        self.day = self.data[1]
        self.month = self.data[0]
        self.year = self.data[2]
        self.time = self.time_picker.time()
        self.hour = self.time[0]
        if len(str(self.hour)) < 2:
            hour = "0"+str(self.hour)
        self.minute = self.time[1]
        if len(str(self.minute)) < 2:
            minute = "0"+str(self.minute)
        self.label.configure(text=f"time:{self.hour}:{self.minute} - date:{self.day}-{self.month}-20{self.year}")

    def check_scheduled_messages(self):
        self.pid=0
        try:
            self.scheduled_list.configure(state="normal")
            self.scheduled_list.delete("1.0", "end")
            with open("database/scheduled_messages.caap", "r") as f:
                contacts = f.read()
            f.close()
            contacts = contacts.split("\n")
            for i in contacts:
                i = i.split("~")
                self.scheduled_list.insert("end", f"{i[0]}\n{i[1]}\n{i[2]}\n{i[3]}\n\n")
                self.pid = int(i[0][3:])
        except:
            pass
        self.scheduled_list.configure(state="disabled")

    def set_scheduled_message(self):
        self.name = self.select_name.get()
        self.time = ''
        self.date = ''
        try:
            self.time = str(self.hour)+":"+str(self.minute)
            self.date = self.day+"-"+self.month+"-"+self.year
        except:
            messagebox.showerror("configure error!", "date & time must be set !", parent=self.scheduled)
        self.mesag = str(self.message.get())
        if self.name == "" or self.name.startswith(" "):
            messagebox.showerror("name error!", "Select name first!", parent=self.scheduled)
        elif len(self.mesag) < 1:
            messagebox.showwarning("message error!", "must be write a message!!", parent=self.scheduled)
        else:
            self.message.delete("0", "end")
            self.check_scheduled_messages()
            try:
                if self.time != "" and self.date != "":
                    with open("database/scheduled_messages.caap", "a") as f:
                        f.write(f"id:{self.pid+1}~Name: {self.name}~Time: {self.time} - {self.date}~Msg:{self.mesag}\n")
                    f.close()
            except:
                pass
            self.check_scheduled_messages()

    def del_scheduled_message(self):
        self.idd = self.iid.get()
        self.iid.delete("0", "end")
        if len(self.idd) < 1:
            messagebox.showerror("ID error!", "Check if ID is valid!", parent=self.scheduled)
        else:
            with open("database/scheduled_messages.caap", "r") as s:
                data = s.read()
            s.close()
            data = data.split("\n")
            trashed = False
            for i in data:
                q = i.split("~")
                if q[0] == "id:" + self.idd:
                    trashed = True
                    # i = i[0]+"~"+i[1]+"~"+i[2]+"~"+i[3]
                    data.pop(data.index(i))
                    print(data)
                    os.remove("database/scheduled_messages.caap")
                    for x in data:
                        if x == '':
                            continue
                        with open("database/scheduled_messages.caap", "a") as a:
                            a.write(x+"\n")
                        a.close()
            if not trashed:
                messagebox.showwarning("not found!!", "this name not fount in contacts!!", parent=self.dell)
        self.check_scheduled_messages()

    def msgui(self):
        self.msg = customtkinter.CTkToplevel(self.top)
        self.msg.title("Send message")
        self.msg.resizable(False, False)
        self.msg.geometry(acpectRatio)

        self.send_banner_label = customtkinter.CTkLabel(self.msg, text="Send message", font=("cairo", 20, "bold"), width=300,
                                                   corner_radius=15)
        self.send_banner_label.pack(pady=(10, 0), padx=10)

        conts = ['']
        try:
            with open("database/contacts.caap", "r") as f:
                contacts = f.read()
            f.close()
            contacts = contacts.split("\n")
            for i in contacts:
                i = i.split("~")
                conts.append(i[0][6:])
        except:
            pass

        self.cname = customtkinter.CTkOptionMenu(self.msg, values=conts[1:-1], width=300, corner_radius=15)
        self.cname.pack(pady=20, padx=10)
        self.cname.set(conts[1])

        self.cmsg = customtkinter.CTkEntry(self.msg, placeholder_text="Message", width=300, corner_radius=15)
        self.cmsg.pack(pady=(0,20), padx=10)

        self.couner = customtkinter.CTkEntry(self.msg, placeholder_text="Times to send message (1) default", width=300,
                                        corner_radius=15)
        self.couner.pack(pady=(0, 20))

        self.send_button = customtkinter.CTkButton(self.msg, text="Send", corner_radius=15, width=300,
                                              command=lambda: threading.Thread(target=self.send_message,
                                                                               args=(self.cname.get(), self.cmsg.get(),
                                                                                     self.couner.get())).start())
        self.send_button.pack(pady=(0,10))

        self.stop_button = customtkinter.CTkButton(self.msg, text="Stop", corner_radius=15, width=150,
                                              command=self.stopSpamming, fg_color="brown")
        self.stop_button.pack(pady=(0, 20))

        self.msg.after(100, self.msg.lift)

    def send_message(self, name, mesg, cnt):
        if not cnt:
            count = "1"
        else:
            count = str(cnt)
        if name == "" or name == " ":
            messagebox.showerror("name error!", "must be select a contact name!", parent=self.msg)
        elif len(mesg) < 1:
            messagebox.showerror("message error!", "the message is too short!", parent=self.msg)
        elif count.startswith("0"):
            messagebox.showerror("counter error!", "Type a valid number in counter!", parent=self.msg)
        else:
            try:
                count = int(count)
                with open("database/contacts.caap", "r") as f:
                    data = f.read()
                f.close()
                data = data.split("\n")
                for i in data:
                    i = i.split("~")
                    if i[0] == "Name: "+name:
                        if count == 1:
                            pywhatkit.sendwhatmsg_instantly(i[1][8:], mesg, 20, True)
                        else:
                            pywhatkit.sendwhatmsg_instantly(i[1][8:], mesg, 20, False)
                            while count >= 1:
                                pyautogui.typewrite(mesg)
                                pyautogui.press("enter")
                                count -= 1
                                time.sleep(0.5)
                        break
            except:
                messagebox.showerror("404", "contact not found!")

    def stopSpamming(self):
        self.count = 0

    def updateDeviceTime(self):
        while 1:
            time.sleep(2)
            self.timenow = datetime.datetime.now().strftime('%H:%M')
            self.timenow = self.timenow.split(":")
            self.h = self.timenow[0]
            self.m = self.timenow[1]

            self.datenow = str(datetime.date.today())
            self.datenow = self.datenow.split("-")
            self.yr = self.datenow[0]
            self.mo = self.datenow[1]
            if self.mo.startswith("0"):
                self.mo = str(self.mo[1:])
            self.dy = self.datenow[2]
            if self.dy.startswith("0"):
                self.dy = str(self.dy[1:])

    def scheduled_Messages(self):
        threading.Thread(target=self.updateDeviceTime).start()
        while 1:
            time.sleep(3)
            try:
                with open("database/scheduled_messages.caap", "r") as x:
                    con = x.read()
                x.close()
                con = con.split("\n")
                for o in con:
                    if len(o) < 2:
                        continue
                    print("o: ", o)
                    o = o.split("~")
                    ifitnow = o[2].split("-")
                    H = ifitnow[0][6:8]
                    M = ifitnow[0][9:11]
                    DY = ifitnow[1][1:]
                    MO = ifitnow[2]
                    YR = "20"+ifitnow[3]
                    print(self.yr, " ", YR, " - ", self.mo, " ", MO, " - ", self.dy, " ", DY, " - ",
                          self.h, " ", H, " - ", self.m, " ", M)
                    if self.yr == YR and self.mo == MO and self.dy == DY and self.h == H and self.m == M:
                        name = o[1][6:]
                        with open("database/contacts.caap", "r") as f:
                            data = f.read()
                        f.close()
                        data = data.split("\n")
                        for i in data:
                            i = i.split("~")
                            if i[0] == "Name: " + name:
                                pywhatkit.sendwhatmsg_instantly(i[1][8:], o[3][4:], 15, False, 5)
                                break
            except:
                pass

Whatsapp().WAUI()