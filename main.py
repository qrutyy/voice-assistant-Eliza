import shutil
import subprocess
import wolframalpha
import pyttsx3
import random
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import json
import feedparser
import smtplib
import datetime
import requests
from twilio.rest import Client
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import tkinter
import time
from pyowm import OWM
from cv2 import *
import pyaudio
from yandex_music import Client
import win10toast  # биб для уведомлений
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import sqlite3
from sqlite3 import Error
import pyautogui
import pyfiglet
import tkinterset
from tkinter.ttk import Checkbutton
import psutil


# sqlite coonection
conn = sqlite3.connect(r'V-A-V4.db')
cur = conn.cursor()

# notification send settings
toaster = win10toast.ToastNotifier()

# opening browser settings
operagx_path = "C:\\Users\\quadk\\AppData\\Local\\Programs\\Opera GX\\opera.exe %s"
webbrowser.register('operagx', None, webbrowser.BackgroundBrowser(operagx_path))

# tkinter gui code

# Creating the main window
wn = tkinter.Tk()
wn.title("Eliza - Voice Assistant (made by @qruty)")
wn.geometry('700x300')
wn.config(bg='LightBlue1')

tkinter.Label(wn, text='Welcome to meet the Voice Assistant by qruty', bg='LightBlue1',
              fg='black', font=('Courier', 15)).place(x=50, y=10)
# Button to convert PDF to Audio form
tkinter.Button(wn, text="Start", bg='gray', font=('Courier', 15),
               command='callVoiceAssistant').place(x=290, y=100)
showCommand = tkinter.StringVar()
cmdLabel = tkinter.Label(wn, textvariable=showCommand, bg='LightBlue1',
                         fg='black', font=('Courier', 15))
cmdLabel.place(x=250, y=150)

# CheckButton settings

chk_state = tkinter.IntVar()
chk_state.set(True)  # задайте проверку состояния чекбокса
chk = Checkbutton(wn, text='Mute the sound (?)', var=chk_state).place(x=270, y=200)
chk_state.set(0)  # False
chk_state.set(1)  # True

# Runs the window till it is closed
wn.mainloop()

# voice settings

voiceEngine = pyttsx3.init('sapi5')
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[1].id)
newVoiceRate = 180
voiceEngine.setProperty('rate', newVoiceRate)


def speak(text):
    voiceEngine.say(text)
    voiceEngine.runAndWait()


def wish():
    print('Wishing.')
    time = int(datetime.datetime.now().hour)
    global uname, asname
    if time >= 0 and time < 12:
        speak("Good Morning sir!")

    elif time < 18:
        speak("Good Afternoon sir!")

    else:
        speak("Good Evening sir!")
    asname = "Eliza"
    speak("I am your Voice Assistant from qqruty")
    speak(asname)
    pyfig_wish = pyfiglet.figlet_format("I am your Voice Assistant from qruty, ", font="slant")
    print(pyfig_wish +asname)

def order():
    print("What kind of food do you want to order")
    speak("What kind of food do you want to order")
    food_kind = takeCommand()
    if food_kind == "chinese" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=kitajskaya&shippingType=delivery&sort=", new=1)
    elif food_kind == "georgian" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=gruzinskaya&shippingType=delivery")
    elif food_kind == "burger" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=burger&shippingType=delivery")
    elif food_kind == "pizza" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=pizza&shippingType=delivery")
    elif food_kind == "sushi" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=sushi&shippingType=delivery")
    elif food_kind == "italian" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=italyanskaya&shippingType=delivery")
    elif food_kind == "shaurma" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=shaurma&shippingType=delivery")
    elif food_kind == "fastfood" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=fastfood&shippingType=delivery")
    elif food_kind == "steak" in command:
        print("Redirecting you to ordering form")
        speak("Redirecting you to ordering form")
        webbrowser.get('operagx').open("https://eda.yandex.ru/spb?quickfilter=stejki&shippingType=delivery")

def getName():
    global uname
    speak("Can I please know your name?")
    uname = takeCommand()
    cur.execute("SELECT * FROM users where uname='Mike'")
    all_results = cur.fetchall()
    print(all_results)
    if all_results == 'Mike':
        pass
    else:
        cur.execute("INSERT INTO users(uname) VALUES(?);", [uname])
    print("Name:", uname)
    speak("Im glad to know you!")
    columns = shutil.get_terminal_size().columns
    speak("How can I help you?")
    speak(uname)


def takeCommand():
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening to the user")
        recog.pause_threshold = 1
        userInput = recog.listen(source)
    try:
        print("Recognizing the command")
        command = recog.recognize_google(userInput, language='en-in')
        print(f"Command is: {command}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize the voice.")
        return "None"
    return command


def sendEmail(to, content):
    print("Sending mail to ", to)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # paste your email id and password in the respective places
    server.login('your email id', 'password')
    server.sendmail('your email id', to, content)
    server.close()


def getWeather(city_name):
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"  # base url from where we extract weather report
    url = baseUrl + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + cityName
    response = requests.get(url)
    x = response.json()
    # If there is no error, getting all the weather conditions
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"]
        temp -= 273
        pressure = y["pressure"]
        humidity = y["humidity"]
        desc = x["weather"]
        info = (" Temperature= " + str(temp) + "°C" + "\n atmospheric pressure (hPa) =" + str(
            pressure) + "\n humidity = " + str(humidity) + "%" + "\n ")
        print(info)
        speak("Here is the weather report at")
        speak(city_name)
        speak(info)
    else:
        speak(" City Not Found ")

def show_pictures():
    pass


def getNews():
    try:
        response = requests.get('https://www.bbc.com/news')
        b4soup = BeautifulSoup(response.text, 'html.parser')
        headLines = b4soup.find('body').find_all('h3')
        unwantedLines = ['BBC World News TV', 'BBC World Service Radio',
                         'News daily newsletter', 'Mobile app', 'Get in touch']
        for x in list(dict.fromkeys(headLines)):
            if x.text.strip() not in unwantedLines:
                print(x.text.strip())
    except Exception as e:
        print(str(e))

def cpu():
    usage = str(psutil.cpu_percent) #Get CPU usage Percent
    speak("CPU is at "+ usage+" %")
    battery = psutil.sensors_battery() #Get Battery Percent
    speak("battery is at "+str(battery.percent) +" %")

if __name__ == '__main__':
    uname = ''
    asname = 'Eliza'
    os.system('cls')
    wish()
    getName()
    print(uname)
    while True:
        command = takeCommand().lower()
        print(command)
        if "Eliza" in command:
            wish()

        elif "callVoiceAssistant" in command:
            va_path = "D:\Python Projects\V-A-v4\main.py"
            os.system(va_path)

        elif 'how are you' in command:
            speak("I am fine, Thank you")
            speak("How are you, ")
            speak(uname)

        elif "good morning" in command or "good afternoon" in command or "good evening" in command:
            speak("A very" + command)
            speak("Thank you for wishing me! Hope you are doing well!")

        elif 'fine' in command or "good" in command:
            speak("It's good to know that your fine")

        elif "who are you" in command:
            speak("I am your virtual assistant.")

        elif "change my name to" in command:
            speak("What would you like me to call you, Sir or Madam ")
            uname = takeCommand()
            speak('Hello again,')
            speak(uname)

        elif "change name" in command:
            speak("What would you like to call me, Sir or Madam ")
            assname = takeCommand()
            speak("Thank you for naming me!")

        elif "what's your name" in command:
            speak("People call me")
            speak(assname)

        # Time content #
        elif 'time' in command:
            strTime = datetime.datetime.now()
            curTime = str(strTime.hour) + "hours" + str(strTime.minute) + "minutes" + str(strTime.second) + "seconds"
            speak(uname)
            speak(f" the time is {curTime}")
            print(curTime)
            toaster.show_toast('V-A Eliza',
                               'Time is: ' + strTime.hour + ":" + strTime.minute + ":" + strTime.second + ":",
                               icon_path='Dream_TradingCard.ico', duration=7)

        elif "timer" in command:
            local_time = command.replace('timer', '')
            local_time_s = local_time * 60
            toaster.show_toast('V-A Eliza', 'Set timer for:' + local_time_s, icon_path='Dream_TradingCard.ico',
                               duration=7)
            time.sleep(local_time_s)
            toaster.show_toast('V-A Eliza', local_time_s + 'minutes timer ended', icon_path='Dream_TradingCard.ico',
                               duration=7)

        elif 'wikipedia' in command:
            speak('Searching Wikipedia')
            command = command.replace("wikipedia", "")
            results_wiki = wikipedia.summary(command, sentences=3)
            speak("These are the results from Wikipedia")
            print(results_wiki)
            speak(results_wiki)
            toaster.show_toast('V-A Eliza', 'These are the results on wikipedia:' + results_wiki,
                               icon_path='Dream_TradingCard.ico', duration=7)

        elif 'open youtube' in command:
            speak("Here you go, the Youtube is opening\n")
            webbrowser.get('operagx').open("https://youtube.com/", new=1)

        elif 'open vk' in command:
            speak("Opening VK\n")
            webbrowser.get('operagx').open("https://vk.com/feed", new=1)

        elif 'open google' in command:
            speak("Opening Google\n")
            webbrowser.get('operagx').open("google.com", new=1)

        elif 'play music' in command or "play song" in command:
            speak("Enjoy the music!")
            song_title = command.replace("play song", "")
            search_link = "https://music.yandex.ru/search?text=" + song_title
            search_result = requests.get(search_link).text
            soup = BeautifulSoup(search_result, 'html.parser')
            music = soup.select("d-track__play d-track__hover")
            if not music:
                raise KeyError("Не найдено такой песни")

            print(song_title + 'is playing.')

        elif 'screenshot' in command:
            speak("Making the screenshot!")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(r'image.png')



        elif 'joke' in command:
            speak(pyjokes.get_joke())

        elif 'mail' in command:
            try:
                speak("Whom should I send the mail")
                to = input()
                speak("What is the body?")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent successfully !")
            except Exception as e:
                print(e)
                speak("I am sorry, not able to send this email")

        elif 'exit' in command:
            speak("Thanks for giving me your time")
            exit()

        elif "will you be my girlfriend" in command or "will you be my boyfriend" in command:
            speak("I'm not sure about that, may be you should give me some time")

        elif "lets play" in command:
            speak("What game would you love to play?"
                  "Rock paper scissors, dice, coin toss")
            game_choice = takeCommand()
            if "rock paper scissors" in command:
                speak("Go on!")
                user_action = takeCommand()
                va_possible_actions = ["rock", "paper", "scissors"]
                va_action = random.choice(va_possible_actions)
                print(f"\n You chose {user_action}, V-A chose {va_action}. \n")
                if user_action == va_action:
                    print(f"Both players selected {user_action}. It's a tie!")
                elif user_action == "rock":
                    if va_action == "scissors":
                        print("Rock smashes scissors! You win!")
                        speak("Rock smashes scissors! You win!")
                    else:
                        print("Paper covers rock! You lose.")
                        speak("Paper covers rock! You lose.")
                elif user_action == "paper":
                    if va_action == "rock":
                        print("Paper covers rock! You win!")
                        speak("Paper covers rock! You win!")
                    else:
                        print("Scissors cuts paper! You lose.")
                        speak("Scissors cuts paper! You lose.")
                elif user_action == "scissors":
                    if va_action == "paper":
                        print("Scissors cuts paper! You win!")
                        speak("Scissors cuts paper! You win!")
                    else:
                        print("Rock smashes scissors! You lose.")
                        speak("Rock smashes scissors! You lose.")

            elif "toss coin" in command:
                print("Tossing the coin!")
                speak("Tossing the coin!")
                coin_possible_sides = ["Heads", "Tails"]
                coin_toss = random.choice(coin_possible_sides)
                print(coin_toss + "fell out")
                speak(coin_toss + "fell out")

            elif "dice" in command:
                print("Rolling the dice!")
                speak("Rolling the dice!")
                dice_possible = ["1", "2", "3", "4", "5", "6"]
                dice_roll = random.choice(dice_possible)
                print(dice_roll + "fell out)")
                speak(dice_roll + "fell out)")


        elif "i love you" in command:
            speak("I love you too! But, It's a pleasure to hear it from you.")

        elif "weather" in command:
            speak(" Please tell your city name ")
            print("City name : ")
            cityName = takeCommand()
            getWeather(cityName)

        elif "what is" in command or "who is" in command:

            client = wolframalpha.Client("KUGHH3-U3KTWWQX48")
            res = client.query(command)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No results")

        elif 'search' in command:
            command = command.replace("search", "")
            webbrowser.get('operagx').open(command, new=1)

        elif 'current news' in command:
            url = "https://www.fontanka.ru"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.find_all('div', class_='JHahp')
            speak("These are the current news:" + items)
            toaster.show_toast('V-A Eliza', 'Current news' + items, icon_path='Dream_TradingCard.ico',
                               duration=7)

        elif "don't listen" in command or "stop listening" in command:
            speak("for how much time you want to stop me from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "camera" in command or "take a photo" in command:
            pass
            # TODO

        elif 'shut down system' in command:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call("shutdwn \s \t 1")
            toaster.show_toast('V-A Eliza', 'Shutting down the system. Goodbye!', icon_path='Dream_TradingCard.ico',
                               duration=7)

        elif "restart" in command:
            subprocess.call(["shutdown", "/r"])

        elif "sleep" in command:
            speak("Setting in sleep mode")
            subprocess.call("shutdown / h")

        elif "logout" in command:
            speak("Logging out")
            subprocess.call("shutdown -l")

        elif "cpu" in command or "battery" in command:
            cpu()

        elif "write a note" in command:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('V-A-note.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "password generation" in command:
            speak("How many symbols in password you need?")
            chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            length = takeCommand()
            password_gen = ''
            for i in range(length):
                password_gen += random.choice(chars)
            print("Your password: " + password_gen)
            speak("Here is your password!")

        elif "food" or "order" in command:
            order()
            print("Enjoy your meal")
            speak("Enjoy your meal")

        # CUSTOM COMMANDS

        elif "im home" or "hi eliza" in command:
            print("Starting custom awakeness")
            speak("Great, i was waiting you honey!")
            os.system()




        # ADMIN COMMANDS #
        elif "admin panel" in command:
            speak("Please, enter the password:")
            userpass = takeCommand()
            password = 'qruty'
            if userpass == password:
                speak("You are in!")
                speak("These are the commands for admins:")
                pyfig = pyfiglet.figlet_format("Admin Panel", font="slant")
                print(pyfig)
                admin_command = input("made by qruty\n"
                                      "1 -- Inspect the database\n2 -- Stop the V-A\n"
                                      "3 -- Stop the V-A")
                if admin_command == 1:
                    print("Showing the database...")
                    cur.execute("SELECT * FROM users")
                    all_results = cur.fetchall()
                    print(all_results)
                elif admin_command == 2:
                    admin_sure = input("Are you sure:")
                    if admin_sure == "Yes":
                        cur.execute()
                elif admin_command == 3:
                    print("Stopping the V-A. Thanks for using!")

        elif "help" in command:
            speak("Here are all the commands:")
            print("Eliza V-A commands: \n"
                  "1 -- Time (current time) \n"
                  "2  -- Timer (set the timer) \n"
                  "3  -- Wikipedia (searching on wikipedia) \n"
                  "4  -- Open Youtube \n"
                  "5  -- Open Vk \n"
                  "6  -- Open Google \n"
                  "7  -- Play music/song \n"
                  "8  -- Screenshot \n"
                  "9  -- Joke \n"
                  "10 -- Mail \n"
                  "11 -- Lets play (rock paper scissors, coin toss, dice) \n"
                  "12 -- Weather \n"
                  "13 -- What is \n"
                  "14 -- Search \n"
                  "15 -- Current news \n"
                  "16 -- Shutdown system \n"
                  "17 -- Restart \n"
                  "18 -- Sleep \n"
                  "19 -- Write a note \n"
                  "20 -- Admin panel \n"
                  "21 -- Exit \n")
                #TODO

        elif "notes" in command:
            speak()

        else:
            speak("Sorry, I am not able to understand you. If you want to see all the commands, please say help")
