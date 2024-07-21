import tkinter as tk
from tkinter import messagebox, PhotoImage
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

def getweather():
    try:
        city = textfield.get()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        if not location:
            raise Exception("Location not found")

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        if not result:
            raise Exception("Timezone not found")

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # weather
        api_key = "0fe7924b7cd3ed1f624aae44a00c3f29"  # replace with your actual API key
        lat = location.latitude
        lon = location.longitude
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        print("API URL:", api_url)  # Print the API URL for debugging
        response = requests.get(api_url)
        print("Response content:", response.content)  # Print the response content for debugging

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        json_data = response.json()
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = json_data['main']['temp']
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | SEEMS LIKE {temp}°C")

        w.config(text=f"{wind} m/s")
        h.config(text=f"{humidity} %")
        d.config(text=description.capitalize())
        p.config(text=f"{pressure} hPa")

    except Exception as e:
        messagebox.showerror("Weather App", f"Invalid Entry!!\n{e}")

root = tk.Tk()
root.title("My Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# search box
Search_image = PhotoImage(file="C:/Users/Saurav Singh/Desktop/Internship Projects/Coding Samurai/Images/Copy of search.png")
myimage = tk.Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "italic"), bg="white", border=0, fg="red")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="C:/Users/Saurav Singh/Desktop/Internship Projects/Coding Samurai/Images/Copy of search_icon.png")
myimage_icon = tk.Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
myimage_icon.place(x=400, y=34)

# Logo
Logo_image = PhotoImage(file="C:/Users/Saurav Singh/Desktop/Internship Projects/Coding Samurai/Images/Copy of logo.png")
logo = tk.Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom Box
Frame_image = PhotoImage(file="C:/Users/Saurav Singh/Desktop/Internship Projects/Coding Samurai/Images/Copy of box.png")
frame_myimage = tk.Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=tk.BOTTOM)

# time
name = tk.Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = tk.Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# label
Label1 = tk.Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="deep sky blue")
Label1.place(x=120, y=400)

Label2 = tk.Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="deep sky blue")
Label2.place(x=250, y=400)

Label3 = tk.Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="deep sky blue")
Label3.place(x=430, y=400)

Label4 = tk.Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="deep sky blue")
Label4.place(x=650, y=400)

t = tk.Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = tk.Label(font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w = tk.Label(text="...", font=("arial", 20, "bold"), bg="deep sky blue")
w.place(x=120, y=430)
h = tk.Label(text="...", font=("arial", 20, "bold"), bg="deep sky blue")
h.place(x=280, y=430)
d = tk.Label(text="...", font=("arial", 20, "bold"), bg="deep sky blue")
d.place(x=450, y=430)
p = tk.Label(text="...", font=("arial", 20, "bold"), bg="deep sky blue")
p.place(x=670, y=430)

root.mainloop()
