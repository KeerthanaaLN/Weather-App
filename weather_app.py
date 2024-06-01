from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests

def getWeather():
    city = location_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", "City not found")
            return
        
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        if not result:
            messagebox.showerror("Error", "Timezone not found")
            return
        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        current_time_label.config(text=current_time)
        current_weather_label.config(text="CURRENT WEATHER")

        api_key = "9ded0cbf5450b9177dbc1fcbc73ef807"  
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(weather_url)
        weather_data = response.json()

        if weather_data["cod"] != 200:
            messagebox.showerror("Error", weather_data["message"])
            return

        temperature = weather_data["main"]["temp"]
        wind = weather_data["wind"]["speed"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        description = weather_data["weather"][0]["description"]
        icon_code = weather_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        temp_entry.config(state=NORMAL)
        wind_entry.config(state=NORMAL)
        humidity_entry.config(state=NORMAL)
        pressure_entry.config(state=NORMAL)
        description_entry.config(state=NORMAL)

        temp_entry.delete(0, END)
        wind_entry.delete(0, END)
        humidity_entry.delete(0, END)
        pressure_entry.delete(0, END)
        description_entry.delete(0, END)

        temp_entry.insert(0, f"{temperature} °C")
        wind_entry.insert(0, f"{wind} m/s")
        humidity_entry.insert(0, f"{humidity} %")
        pressure_entry.insert(0, f"{pressure} hPa")
        description_entry.insert(0, description.capitalize())

        temp_entry.config(state="readonly")
        wind_entry.config(state="readonly")
        humidity_entry.config(state="readonly")
        pressure_entry.config(state="readonly")
        description_entry.config(state="readonly")

        # Fetch and display the weather icon
        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.config(image=icon)
        icon_label.image = icon

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = Tk()
root.title("Weather App")
root.geometry("350x450")
root.resizable(False, False)
root.config(background="#66c2ff")

font1 = ('Times', 18, 'bold')
font2 = ('Times', 12)
font3 = ('Times', 10)

location_label = tk.Label(root, text="Location", font=font1,fg="black",bg="#66c2ff")
location_label.place(x=20, y=20)
location_entry = tk.Entry(root, font=font2, width=15)
location_entry.place(x=140, y=26)
location_entry.focus()

search_button = tk.Button(root, text="Search", font=font3, command=getWeather)
search_button.place(x=290, y=24)

current_weather_label = tk.Label(root, text="CURRENT WEATHER", font=('poppins', 12, 'bold'),fg="black",bg="#66c2ff")
current_weather_label.place(x=90, y=70)
current_time_label = tk.Label(root, text="", font=('poppins', 15, 'bold'),fg="black",bg="#66c2ff")
current_time_label.place(x=130, y=100)

icon_label = tk.Label(root, text="",fg="black",bg="#66c2ff")
icon_label.place(x=125, y=325)

temp_label = tk.Label(root, text="Temperature", font=font2,fg="black",bg="#66c2ff")
temp_label.place(x=20, y=140)
temp_entry = tk.Entry(root, font=font2, width=15)
temp_entry.place(x=140, y=140)
temp_entry.config(state="readonly")

wind_label = tk.Label(root, text="Wind", font=font2,fg="black",bg="#66c2ff")
wind_label.place(x=20, y=180)
wind_entry = tk.Entry(root, font=font2, width=15)
wind_entry.place(x=140, y=180)
wind_entry.config(state="readonly")

humidity_label = tk.Label(root, text="Humidity", font=font2,fg="black",bg="#66c2ff")
humidity_label.place(x=20, y=220)
humidity_entry = tk.Entry(root, font=font2, width=15)
humidity_entry.place(x=140, y=220)
humidity_entry.config(state="readonly")

pressure_label = tk.Label(root, text="Pressure", font=font2,fg="black",bg="#66c2ff")
pressure_label.place(x=20, y=260)
pressure_entry = tk.Entry(root, font=font2, width=15)
pressure_entry.place(x=140, y=260)
pressure_entry.config(state="readonly")

description_label = tk.Label(root, text="Description", font=font2,fg="black",bg="#66c2ff")
description_label.place(x=20, y=300)
description_entry = tk.Entry(root, font=font2, width=15)
description_entry.place(x=140, y=300)
description_entry.config(state="readonly")

root.mainloop()
