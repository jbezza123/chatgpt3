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

# Use your OpenAI API key
openai.api_key = "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"

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

def load_conversation(conversation_context):
    filepath = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "rb") as f:
            conversation = pickle.load(f)
        conversation_context = conversation

        
class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x450+468+138")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Chat-GPT")
        top.configure(background="#7588cc")

        self.top = top
        
        self.chatbox = scrolledtext.ScrolledText(self.top)
        self.chatbox.place(relx=0.007, rely=0.067, relheight=0.787, relwidth=0.9845)
        self.chatbox.configure(background="white")
        self.chatbox.configure(font="-family {Segoe UI} -size 12")
        self.chatbox.configure(foreground="black")
        self.chatbox.configure(highlightbackground="#d9d9d9")
        self.chatbox.configure(highlightcolor="black")
        self.chatbox.configure(insertbackground="black")
        self.chatbox.configure(selectbackground="#c4c4c4")
        self.chatbox.configure(selectforeground="black")
        self.chatbox.configure(wrap='word')
        
        self.userinput = tk.Text(self.top)
        self.userinput.place(relx=0.017, rely=0.867, relheight=0.12, relwidth=0.74)
        self.userinput.configure(background="white")
        self.userinput.configure(font="TkTextFont")
        self.userinput.configure(foreground="black")
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
        self.send.configure(highlightbackground="#d9d9d9")
        self.send.configure(highlightcolor="black")
        self.send.configure(pady="0")
        self.send.configure(text='''Send''')
        self.send.configure(command=self.handle_conversation)
        
        self.avatar2 = tk.PhotoImage(file="chat.png")
        self.avatar1 = tk.PhotoImage(file="avatar.png")

        self.save_conversation = tk.Button(self.top, command=lambda: save_conversation(self.conversation_context))
        self.save_conversation.place(relx=0.8, rely=0.01, height=24, width=50)
        self.save_conversation.configure(text='Save')
        self.load_conversation = tk.Button(self.top, command=lambda: load_conversation(self.conversation_context))
        self.load_conversation.place(relx=0.9, rely=0.01, height=24, width=50)
        self.load_conversation.configure(text='Load')


        self.conversation_context = []

    def get_response(self, prompt):
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=3000)
        return response["choices"][0]["text"]

    def handle_conversation(self):
        user_message = self.userinput.get("1.0", 'end-1c')
        self.chatbox.tag_config('right', foreground='black', justify='right', background='light blue')
        new_avatar = self.avatar1.copy()
        self.chatbox.insert('end', "\n ", 'right')
        self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar1))
        self.chatbox.insert('end', '\n\n' + user_message + '\n\n\n', 'right')


        thread = threading.Thread(target=self.get_response_thread, args=(user_message,))
        thread.start()

    
    def get_response_thread(self, user_message):    
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='\n'.join(self.conversation_context) + user_message,
            max_tokens=1000
        )
        bot_response = response["choices"][0]["text"]
        bot_response = add_code_tags(bot_response)
        if bot_response == "":

            self.chatbox.tag_config('left', foreground='black', background='light green')
            self.new_avatar = self.avatar2.copy()
            self.chatbox.insert('end', "\n ", 'left')
            self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar2))
            self.chatbox.insert('end', '\n\n' +"[No Response given]"+ '\n\n\n', 'left')
            self.timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.conversation_context.append(user_message)
            self.conversation_context.append(bot_response)
            self.userinput.delete("1.0", 'end')
        else:
            self.chatbox.tag_config('left', foreground='black', background='light green')
            self.new_avatar = self.avatar2.copy()
            self.chatbox.insert('end', "\n ", 'left')
            self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar2))
            self.chatbox.insert('end', bot_response + '\n\n\n', 'left')
            self.timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.conversation_context.append(user_message)
            self.conversation_context.append(bot_response)
            self.userinput.delete("1.0", 'end')
        self.chatbox.see(END)
            



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

