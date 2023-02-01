import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path
import openai
import regex
import nltk
import datetime
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import time
import re
from tkinter import scrolledtext
from tkinter import filedialog
import pickle
import datetime
import threading
import importlib
import speech_recognition as sr

       
# Use your OpenAI API key
openai.api_key = "USE YOUR OWN KEY"

_script = sys.argv[0]
_location = os.path.dirname(_script)

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light' 

loadinga = False
count = 0

def start_talk_conversation(conversation_context, chatbox, avatar1, avatar2, get_response_thread):
    thread = threading.Thread(target=talk_conversation, args=(conversation_context, chatbox, avatar1, avatar2, get_response_thread))
    thread.start()

        
def talk_conversation(conversation_context, chatbox, avatar1, avatar2, get_response_thread):
    global count
    if count == 0:
        chatbox.tag_config('left', foreground='black', justify='left', background='light green', wrap='word')
        new_avatar = avatar2.copy()
        chatbox.insert('end', "\n ", 'left')
        chatbox.window_create('end', window=tk.Label(chatbox, image=avatar2,bd=0,padx=50))
        chatbox.insert('end',' \n\n' + " This is the Voice to text button, click then talk and your message will be sent to me!" + ' \n\n\n', 'left')
        count += 1
    else:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            user_message = r.recognize_google(audio)
            chatbox.insert(END, "\n")
            chatbox.tag_config('right', foreground='black', justify='right', background='light blue', wrap='word')
            new_avatar = avatar1.copy()
            chatbox.insert('end', "\n ", 'right')
            chatbox.window_create('end', window=tk.Label(chatbox, image=avatar1,bd=0,padx=50))
            chatbox.insert('end',' \n\n' + user_message + ' \n\n\n', 'right')
            chatbox.insert(END, "\n")
            thread = threading.Thread(target=get_response_thread, args=(user_message,))
            thread.start()

        
def detect_code(string, languages=['html','css','php','ruby','python']):
    code_detected = re.search("(```("+'|'.join(languages)+")\n[\s\S]*?```)",string)
    if code_detected:
        return code_detected.group(1)
    else:
        return None

def add_code_tags(string):
    code = detect_code(string)
    if code:
        string = string.replace(code, "<code>" + code + "</code>")
    return string

def save_conversation(conversation_context):
    filepath = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "wb") as f:
            pickle.dump(conversation_context, f)
        print("Conversation saved to {}".format(filepath))

def clear_conversation(conversation_context, chatbox,):
    conversation_context.clear()
    chatbox.delete(1.0, END)
    chatbox.insert(END, """-----------------------------------------Chat-GPT----------------------------------------\n""")

def load_conversation(conversation_context, chatbox, avatar1, avatar2):
    filepath = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")])
    file_name = os.path.basename(filepath)
    if filepath:
        with open(filepath, "rb") as f:
            conversation = pickle.load(f)
        conversation_context += conversation
        for index, element in enumerate(conversation):
            if index % 2 == 0:
                chatbox.tag_config('right', foreground='black', justify='right', background='light blue', wrap='word')
                new_avatar = avatar1.copy()
                chatbox.insert('end', "\n ", 'right')
                chatbox.window_create('end', window=tk.Label(chatbox, image=avatar1,bd=0,padx=50))
                chatbox.insert('end', ' \n\n' + element + ' \n\n\n', 'right')
                chatbox.insert(END, "\n")
            else:
                new_avatar = avatar2.copy()
                chatbox.tag_config('left', foreground='black', background='light green', wrap='word')
                chatbox.insert('end', "\n ", 'left')
                chatbox.window_create('end', window=tk.Label(chatbox, image=avatar2,bd=0,padx=50))
                chatbox.insert('end', '\n ' + element + '\n\n\n', 'left')
                chatbox.insert(END, "\n")
                
        return conversation_context, file_name
        
    else:
        return conversation_context, file_name

        
def send_file(conversation_context, chatbox, avatar1, get_response_thread):
    filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    file_name = os.path.basename(filepath)
    if filepath:
        with open(filepath, "r") as f:
            conversation = f.read()
        conversation_context.append(conversation)
        user_message = conversation
        user_message = file_name + "\n\n" + user_message
        chatbox.tag_config('right', foreground='black', justify='right', background='light blue', wrap='word')
        new_avatar = avatar1.copy()
        chatbox.insert('end', "\n ", 'right')
        chatbox.window_create('end', window=tk.Label(chatbox, image=avatar1,bd=0,padx=50))
        chatbox.insert('end',' \n\n' + user_message + ' \n\n\n', 'right')
        chatbox.insert(END, "\n")
        thread = threading.Thread(target=get_response_thread, args=(user_message,))
        thread.start()

def loading(Label1):
    while True:
        try:
            while loadinga:
                Label1.config(text="""\\""")
                time.sleep(0.2)
                Label1.config(text="""|""")
                time.sleep(0.2)
                Label1.config(text="""/""")
                time.sleep(0.2)
                Label1.config(text="""-""")
                time.sleep(0.2)

            Label1.config(text="""""")
        except Exception as e:
            print(e)
        time.sleep(1)

        
class Toplevel1:
    def __init__(self, top=None):
        
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x650+468+138")
        top.minsize(600, 450)
        top.maxsize(600, 750)
        top.resizable(1,  1)
        top.title("Chat-GPT")
        top.configure(background="#3c4773")

        self.top = top

        
        
        self.chatbox = scrolledtext.ScrolledText(self.top)
        self.chatbox.place(relx=0.007, rely=0.067, relheight=0.787, relwidth=0.9845)
        self.chatbox.configure(background="#2d2d2e")
        self.chatbox.configure(font="-family {Segoe UI} -size 12")
        self.chatbox.configure(foreground="white")
        self.chatbox.configure(highlightbackground="#d9d9d9")
        self.chatbox.configure(highlightcolor="black")
        self.chatbox.configure(insertbackground="black")
        self.chatbox.configure(selectbackground="#c4c4c4")
        self.chatbox.configure(selectforeground="black")
        self.chatbox.configure(wrap='word',padx=10,pady=10)
        self.chatbox.insert(END, """-----------------------------------------Chat-GPT----------------------------------------\n""")
        

        
        self.userinput = tk.Text(self.top)
        self.userinput.place(relx=0.017, rely=0.867, relheight=0.12, relwidth=0.74)
        self.userinput.configure(background="#2d2d2e")
        self.userinput.configure(font="TkTextFont")
        self.userinput.configure(foreground="white")
        self.userinput.configure(highlightbackground="#d9d9d9")
        self.userinput.configure(highlightcolor="black")
        self.userinput.configure(insertbackground="black")
        self.userinput.configure(selectbackground="#c4c4c4")
        self.userinput.configure(selectforeground="black")
        self.userinput.configure(wrap="word")
        
        self.send = tk.Button(self.top)
        self.send.place(relx=0.767, rely=0.867, height=44, width=107)
        self.send.configure(activebackground="#4b65bc")
        self.send.configure(activeforeground="black")
        self.send.configure(background="#4b65bc")
        self.send.configure(compound='left')
        self.send.configure(disabledforeground="#a3a3a3")
        self.send.configure(font="-family {Segoe UI} -size 14 -weight bold")
        self.send.configure(foreground="#000000")
        self.send.configure(highlightbackground="#354b94")
        self.send.configure(highlightcolor="black")
        self.send.configure(pady="0")
        self.send.configure(text='''Send''')
        self.send.configure(command=self.handle_conversation)
        
        self.avatar2 = tk.PhotoImage(file="chat.png")
        
        self.avatar1 = tk.PhotoImage(file="avatar.png")

        self.save_conversation = tk.Button(self.top, command=lambda: save_conversation(self.conversation_context))
        self.save_conversation.place(relx=0.8, rely=0.01, height=24, width=50)
        self.save_conversation.configure(text='Save')
        self.save_conversation.configure(background="#4b65bc")
        self.save_conversation.configure(highlightbackground="#354b94")
        self.save_conversation.configure(activebackground="#354b94")
        
        self.load_conversation = tk.Button(self.top, command=lambda: load_conversation(self.conversation_context,self.chatbox, self.avatar1, self.avatar2))
        self.load_conversation.place(relx=0.9, rely=0.01, height=24, width=50)
        self.load_conversation.configure(text='Load')
        self.load_conversation.configure(background="#4b65bc")
        self.load_conversation.configure(highlightbackground="#354b94")
        self.load_conversation.configure(activebackground="#354b94")

        self.clear_conversation = tk.Button(self.top, command=lambda: clear_conversation(self.conversation_context,self.chatbox))
        self.clear_conversation.place(relx=0.7, rely=0.01, height=24, width=50)
        self.clear_conversation.configure(text='Clear')
        self.clear_conversation.configure(background="#4b65bc")
        self.clear_conversation.configure(highlightbackground="#354b94")
        self.clear_conversation.configure(activebackground="#354b94")

       

        self.talk_conversation = tk.Button(self.top, command=lambda: start_talk_conversation(self.conversation_context, self.chatbox, self.avatar1, self.avatar2, self.get_response_thread))
        self.talk_conversation.place(relx=0.77, rely=0.94, height=24, width=50)
        self.talk_conversation.configure(text='Talk')
        self.talk_conversation.configure(background="#4b65bc")
        self.talk_conversation.configure(highlightbackground="#354b94")
        self.talk_conversation.configure(activebackground="#354b94")
        
        self.photo = tk.PhotoImage(file="photo.png")
        self.send_file = tk.Button(self.top,image=self.photo, command=lambda: send_file(self.conversation_context, self.chatbox, self.avatar1, self.get_response_thread))
        self.send_file.place(relx=0.955, rely=0.9, height=20, width=20)
        self.send_file.configure(text='↑')
        self.send_file.configure(background="#4b65bc")
        self.send_file.configure(highlightbackground="#354b94")
        self.send_file.configure(activebackground="#354b94")

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.737, rely=0.95, height=21, width=10)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#2d2d2e")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="white")
        self.Label1.configure(text='''''')

        self.conversation_context = []

    

    def get_response(self, prompt):
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=3000)
        return response["choices"][0]["text"]

    def handle_conversation(self): 
        user_message = self.userinput.get("1.0", 'end-1c')
        if user_message == "":
            pass
        else:
            self.chatbox.tag_config('right', foreground='black', justify='right', background='light blue', wrap='word')
            new_avatar = self.avatar1.copy()
            self.chatbox.insert('end', "\n ", 'right')
            self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar1,bd=0,padx=50))
            self.chatbox.insert('end', ' \n\n' + user_message + ' \n\n\n', 'right')
            self.chatbox.insert(END, "\n")
            thread = threading.Thread(target=self.get_response_thread, args=(user_message,))
            thread.start()
            global loadinga
            loadinga = True
            thread = threading.Thread(target=loading, args=(self.Label1,))
            thread.start()
    

    
    def get_response_thread(self, user_message):
        try:
            self.chatbox.see(END)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt='\n'.join(self.conversation_context) + user_message,
                max_tokens=1048,
                temperature=0
            )
            bot_response = response["choices"][0]["text"]
            bot_response = add_code_tags(bot_response)
            self.chatbox.tag_config('left', foreground='black', background='light green', wrap='word')
        
            if bot_response == "":
                self.conversation_context.pop()# remove the last appended user_message
                self.get_response_thread(user_message)
            else:
                self.chatbox.insert('end', "\n ", 'left')
                self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar2,bd=0,padx=50))
                self.chatbox.insert('end', bot_response + '\n\n\n', 'left')
            self.conversation_context.append(user_message)
            self.conversation_context.append(bot_response)
            self.userinput.delete("1.0", 'end')
            self.chatbox.see(END)
            self.chatbox.insert(END, "\n")
            global loadinga
            loadinga = False
        except openai.error.InvalidRequestError as e:
            print(e)
            self.chatbox.tag_config('left', foreground='black', background='light green', wrap='word')
            self.chatbox.insert('end', "\n ", 'left')
            self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar2,bd=0,padx=50))
            self.chatbox.insert('end', '\n' + str(e) + '\n\n\n', 'left')
            #global loadinga
            loadinga = False
        
    
            

    

if __name__ == '__main__':
    top = tk.Tk()
    top.withdraw()
    top.update_idletasks()
    x = (top.winfo_screenwidth() - top.winfo_reqwidth()) / 2
    y = (top.winfo_screenheight() - top.winfo_reqheight()) / 2
    top.geometry("+%d+%d" % (x, y))
    top.deiconify()
    Toplevel1(top)
    top.mainloop()

