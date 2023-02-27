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
import requests
import json
#import unknown_support

from urllib.request import urlopen
from io import BytesIO
from PIL import Image, ImageTk

QUERY_URL = "https://api.openai.com/v1/images/generations"
       
# Use your OpenAI API key
openai.api_key = "USE YOU OWN"

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
tti = False

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
        chatbox.insert('end',' \n\n' + " Listening!" + ' \n\n\n', 'left')
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
            chatbox.see(END)
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

def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = """
    {
        """
    data += f'"prompt": "{prompt}",'
    data += """
        "num_images":1,
        "size":"1024x1024",
        "response_format":"url"
    }
    """

    resp = requests.post(QUERY_URL, headers=headers, data=data)

    if resp.status_code != 200:
        raise ValueError("Failed to generate image "+resp.text)

    response_text = json.loads(resp.text)
    return response_text['data'][0]['url']


def save_conversation(conversation_context):
    filepath = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "wb") as f:
            pickle.dump(conversation_context, f)
        print("Conversation saved to {}".format(filepath))

def clear_conversation(conversation_context, chatbox,):
    conversation_context.clear()
    chatbox.delete(1.0, END)
    chatbox.insert(END, """----------------------------------------Chat-GPT----------------------------------------\n""")

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
                chatbox.see(END)
            else:
                new_avatar = avatar2.copy()
                chatbox.tag_config('left', foreground='black', background='light green', wrap='word')
                chatbox.insert('end', "\n ", 'left')
                chatbox.window_create('end', window=tk.Label(chatbox, image=avatar2,bd=0,padx=50))
                chatbox.insert('end', '\n ' + element + '\n\n\n', 'left')
                chatbox.insert(END, "\n")
                chatbox.see(END)
                
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
        chatbox.see(END)
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

def togtti():
    global tti
    if tti == True:
        tti = False
        print("Text to Image is turned off")
    elif tti == False:
        tti = True
        print("Text to Image is turned on")
    else:
        print("Could not change!")

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran:
        return
    style = ttk.Style()
    if sys.platform == "win32":
        style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
        [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
        style.map('.',foreground =
            [('selected', 'white'), ('active','white')])
    else:
        style.map('.',foreground =
            [('selected', 'black'), ('active','black')])
    _style_code_ran = 1
    
class Toplevel1:
    def __init__(self, top=None):
        
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("395x588+468+138")
        top.minsize(395, 588)
        top.maxsize(395, 588)
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
        self.chatbox.insert(END, """------------------------Chat-GPT-----------------------\n""")
        

        
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
        self.send.place(relx=0.767, rely=0.867, height=30, width=70)
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
        self.save_conversation.place(relx=0.7, rely=0.01, height=24, width=45)
        self.save_conversation.configure(text='Save')
        self.save_conversation.configure(background="#4b65bc")
        self.save_conversation.configure(highlightbackground="#354b94")
        self.save_conversation.configure(activebackground="#354b94")
        
        self.load_conversation = tk.Button(self.top, command=lambda: load_conversation(self.conversation_context,self.chatbox, self.avatar1, self.avatar2))
        self.load_conversation.place(relx=0.82, rely=0.01, height=24, width=45)
        self.load_conversation.configure(text='Load')
        self.load_conversation.configure(background="#4b65bc")
        self.load_conversation.configure(highlightbackground="#354b94")
        self.load_conversation.configure(activebackground="#354b94")

        self.clear_conversation = tk.Button(self.top, command=lambda: clear_conversation(self.conversation_context,self.chatbox))
        self.clear_conversation.place(relx=0.58, rely=0.01, height=24, width=45)
        self.clear_conversation.configure(text='Clear')
        self.clear_conversation.configure(background="#4b65bc")
        self.clear_conversation.configure(highlightbackground="#354b94")
        self.clear_conversation.configure(activebackground="#354b94")

        self.keyboard = tk.Button(self.top, command=lambda: self.show_keyboard())
        self.keyboard.place(relx=0.77, rely=0.96, height=20, width=55)
        self.keyboard.configure(text='Keyboard')
        self.keyboard.configure(background="#4b65bc")
        self.keyboard.configure(highlightbackground="#354b94")
        self.keyboard.configure(activebackground="#354b94")

       

        self.talk_conversation = tk.Button(self.top, command=lambda: start_talk_conversation(self.conversation_context, self.chatbox, self.avatar1, self.avatar2, self.get_response_thread))
        self.talk_conversation.place(relx=0.77, rely=0.92, height=20, width=45)
        self.talk_conversation.configure(text='Talk')
        self.talk_conversation.configure(background="#4b65bc")
        self.talk_conversation.configure(highlightbackground="#354b94")
        self.talk_conversation.configure(activebackground="#354b94")
        
        self.photo = tk.PhotoImage(file="photo.png")
        self.send_file = tk.Button(self.top,image=self.photo, command=lambda: send_file(self.conversation_context, self.chatbox, self.avatar1, self.get_response_thread))
        self.send_file.place(relx=0.940, rely=0.01, height=20, width=20)
        self.send_file.configure(text='↑')
        self.send_file.configure(background="#4b65bc")
        self.send_file.configure(highlightbackground="#354b94")
        self.send_file.configure(activebackground="#354b94")

        self.tti = tk.PhotoImage(file="tti.png")
        self.send_file = tk.Checkbutton(self.top,image=self.tti, command=lambda: togtti())
        self.send_file.place(relx=0.01, rely=0, height=38, width=60)
        self.send_file.configure(text='↑')
        self.send_file.configure(background="#3c4773")
        self.send_file.configure(highlightbackground="#3c4773")
        self.send_file.configure(activebackground="#3c4773")

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.73, rely=0.87, height=21, width=10)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#2d2d2e")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="white")
        self.Label1.configure(text='''''')

        self.combobox = tk.StringVar()
        _style_code()
        self.TCombobox1 = ttk.Combobox(self.top)
        self.TCombobox1.place(relx=0.2, rely=0.01, relheight=0.040, relwidth=0.25)
        self.TCombobox1.configure(textvariable=self.combobox)
        self.TCombobox1.configure(takefocus="Nightcafe")
        self.TCombobox1['values'] = ['Nightcafe', 'Sprite Sheet', 'Artistic Portait', 'Bon Voyage', 'Photo', 'Epic', 'Dark Fantasy', 'Anime', 'Modern Comic', 'CGI Character', 'Neo Impressionist', 'Pop Art', 'B&W Portrait', 'Color Portrait', 'Oil Painting', 'Cosmic', 'Sinister', 'Candy', 'Cubist', '3D Game', 'Fantasy', 'Gouache', 'Matte', 'Charcoal', 'Horror', 'Surreal', 'Steampunk', 'Cyberpunk', 'Synthwave', 'Heavenly']


        # Create the keyboard frame
        self.keyboard_frame = tk.Frame(self.top, width=300)
        self.keyboard_frame.pack_forget()
        
        # Define the keyboard layout
        self.key_list = ["q",
                    "w",
                    "e",
                    "r",
                    "t",
                    "y",
                    "u",
                    "i",
                    "o",
                    "p",
                    "a",
                    "s",
                    "d",
                    "f",
                    "g",
                    "h",
                    "j",
                    "k",
                    "l",
                    "↩",
                    "z",
                    "x",
                    "c",
                    "v",
                    "b",
                    "n",
                    "m",
                    "↵",
                    "Space",
                    "Exit"]

        # Add the keys to the keyboard frame
        #for i, key in enumerate(self.key_list):
            #self.button = tk.Button(keyboard_frame, text=key, width=3)
            #self.button.grid(row=i//10, column=i%10, padx=2, pady=2)

        for i, key in enumerate(self.key_list):
            self.button = tk.Button(self.keyboard_frame, text=key, width=1)
            self.button.grid(row=i//10, column=i%10, padx=2, pady=2)
    
            # Bind the button click event to a function
            self.button.bind("<Button-1>", self.key_pressed)

    
        self.conversation_context = []
        self.previous_images = []

    
    def show_keyboard(self):
        self.keyboard_frame.pack(side="bottom", pady=90)

    def hide_keyboard(self):
        self.keyboard_frame.pack_forget()
        
    def key_pressed(self, event):
        # Get the text of the button that was pressed
        text = event.widget["text"]
        
    
        # Do something with the text, depending on which key was pressed
        if text == "Space":
            print("Space bar was pressed")
            self.userinput.insert(END, " ")
        elif text == "↵":
            print("Enter key was pressed")
            self.userinput.insert(END, "\n")
        elif text == "↩":
            self.userinput.delete("end-2c", "end-1c") # remove last character 
        elif text == "Exit":
            self.hide_keyboard()                
        else:
            print(f"{text} key was pressed")
            self.userinput.insert(END, f"{text}")

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
            self.chatbox.see(END)
            global tti
            global loadinga
            if tti == True:
                thread = threading.Thread(target=self.get_response_image, args=(user_message,))
                thread.start()
                loadinga = True
                thread = threading.Thread(target=loading, args=(self.Label1,))
                thread.start()

            
            elif tti == False:
                thread = threading.Thread(target=self.get_response_thread, args=(user_message,))
                thread.start()
                loadinga = True
                thread = threading.Thread(target=loading, args=(self.Label1,))
                thread.start()
    def save_image(self, image_url):
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if file_name:
            image_data = urlopen(image_url).read()
            with open(file_name, "wb") as f:
                f.write(image_data)

    def get_response_image(self, user_message):
        selected_value = self.combobox.get()
        print(selected_value)
        if selected_value == "Nightcafe":
            prompt = user_message + " detailed matte painting, deep color, fantastical, intricate detail, splash screen, complementary colors, fantasy concept art, 8k resolution trending on Artstation Unreal Engine 5"
        if selected_value == "Artistic Portait":
            prompt = user_message + " head and shoulders portrait, 8k resolution concept art portrait by Greg Rutkowski, Artgerm, WLOP, Alphonse Mucha dynamic lighting hyperdetailed intricately detailed Splash art trending on Artstation triadic colors Unreal Engine 5 volumetric lighting"
        if selected_value == "Bon Voyage":
            prompt = user_message + " 8k resolution concept art by Greg Rutkowski dynamic lighting hyperdetailed intricately detailed Splash art trending on Artstation triadic colors Unreal Engine 5 volumetric lighting Alphonse Mucha WLOP Jordan Grimmer orange and teal"
        if selected_value == "Photo":
            prompt = user_message + " Professional photography, bokeh, natural lighting, canon lens, shot on dslr 64 megapixels sharp focus"
        if selected_value == "Epic":
            prompt = user_message + " Epic cinematic brilliant stunning intricate meticulously detailed dramatic atmospheric maximalist digital matte painting"
        if selected_value == "Dark Fantasy":
            prompt = user_message + " a masterpiece, 8k resolution, dark fantasy concept art, by Greg Rutkowski, dynamic lighting, hyperdetailed, intricately detailed, Splash screen art, trending on Artstation, deep color, Unreal Engine, volumetric lighting, Alphonse Mucha, Jordan Grimmer, purple and yellow complementary colours"
        if selected_value == "Anime":
            prompt = user_message + " Studio Ghibli, Anime Key Visual, by Makoto Shinkai, Deep Color, Intricate, 8k resolution concept art, Natural Lighting, Beautiful Composition"
        if selected_value == "Modern Comic":
            prompt = user_message + " Mark Brooks and Dan Mumford, comic book art, perfect, smooth"
        if selected_value == "CGI Character":
            prompt = user_message + " Pixar, Disney, concept art, 3d digital art, Maya 3D, ZBrush Central 3D shading, bright colored background, radial gradient background, cinematic, Reimagined by industrial light and magic, 4k resolution post processing"
        if selected_value == "Neo Impressionist":
            prompt = user_message + " neo-impressionism expressionist style oil painting, smooth post-impressionist impasto acrylic painting, thick layers of colourful textured paint"
        if selected_value == "Pop Art":
            prompt = user_message + " Screen print, pop art, splash screen art, triadic colors, digital art, 8k resolution trending on Artstation, golden ratio, symmetrical, rule of thirds, geometric bauhaus"
        if selected_value == "B&W Portrait":
            prompt = user_message + " Close up portrait, ambient light, Nikon 15mm f/1.8G, by Lee Jeffries, Alessio Albi, Adrian Kuipers"
        if selected_value == "Color Portrait":
            prompt = user_message + " Close-up portrait, color portrait, Linkedin profile picture, professional portrait photography by Martin Schoeller, by Mark Mann, by Steve McCurry, bokeh, studio lighting, canon lens, shot on dslr, 64 megapixels, sharp focus"
        if selected_value == "Oil Painting":
            prompt = user_message + " oil painting by James Gurney"
        if selected_value == "Cosmic":
            prompt = user_message + " 8k resolution holographic astral cosmic illustration mixed media by Pablo Amaringo"
        if selected_value == "Sinister":
            prompt = user_message + " sinister by Greg Rutkowski"
        if selected_value == "Candy":
            prompt = user_message + " vibrant colors Candyland wonderland gouache swirls detailed"
        if selected_value == "Cubist":
            prompt = user_message + " abstract cubism Euclidean Georgy Kurasov Albert Gleizes"
        if selected_value == "3D Game":
            prompt = user_message + " trending on Artstation Unreal Engine 3D shading shadow depth"
        if selected_value == "Fantasy":
            prompt = user_message + " ethereal fantasy hyperdetailed mist Thomas Kinkade"
        if selected_value == "Gouache":
            prompt = user_message + " gouache detailed painting"
        if selected_value == "Matte":
            prompt = user_message + " detailed matte painting"
        if selected_value == "Charcoal":
            prompt = user_message + " hyperdetailed charcoal drawing"
        if selected_value == "Horror":
            prompt = user_message + " horror Gustave Doré Greg Rutkowski"
        if selected_value == "Surreal":
            prompt = user_message + " surrealism Salvador Dali matte background melting oil on canvas"
        if selected_value == "Steampunk":
            prompt = user_message + " steampunk engine"
        if selected_value == "Cyberpunk":
            prompt = user_message + " cyberpunk 2099 blade runner 2049 neon"
        if selected_value == "Synthwave":
            prompt = user_message + " synthwave neon retro"
        if selected_value == "Heavenly":
            prompt = user_message + " heavenly sunshine beams divine bright soft focus holy in the clouds"
        elif selected_value == "Sprite Sheet":
            prompt = user_message + "2D sprite sheet of a character that are inspired by medieval fantasy, with a variety of races such as humans, elves, and dwarves. The characters should be wearing different types of armor and wielding various weapons like swords, bows, and hammers. Each character should have unique facial features and expressions. The sprite sheet should include front-facing, back-facing, and side-facing views of each character, with each view having at least 8 different frames of animation, including walking, running, and attacking animations. The sprite sheet should have a resolution of at least 512x512 pixels per character."
        elif selected_value == "":
            prompt = user_message
            
        image_url = generate_image(prompt)
        print(f"Generated image URL: {image_url}")
        
        #--------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------
        

        # Open the URL image, resize it to fit the chatbox, and convert it to a PhotoImage object
        self.image = Image.open(BytesIO(urlopen(image_url).read()))
        self.image.thumbnail((300, 1000), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        
        self.chatbox.tag_config('left', foreground='black', background='light green', wrap='word')
        self.chatbox.insert('end', "\n ", 'left')
        self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.avatar2,bd=0,padx=50))
        self.chatbox.insert('end', '\n       ', 'left')
        # Create a label widget and insert it into the chatbox
        self.previous_images.append(self.image)
        self.chatbox.window_create('end', window=tk.Label(self.chatbox, image=self.image, bd=0, padx=50))
        self.chatbox.insert('end', '       ', 'left')
        self.save_button = tk.Button(self.chatbox, text="Save", command=lambda: self.save_image(image_url))
        self.chatbox.window_create('end', window=self.save_button)
        self.chatbox.insert('end', '\n\n', 'left')
        self.chatbox.insert(END, "\n")
        global loadinga
        loadinga = False
        self.userinput.delete("1.0", 'end')
        self.chatbox.see(END)
    
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

