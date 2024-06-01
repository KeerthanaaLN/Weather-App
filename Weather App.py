import requests

def fetch_weather(city):
    api_key = '6dec399dff56ab1e70133209878cf451'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def display_weather(data):
    if data['cod'] == 200:
        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']

        print(f"Weather in {city}, {country}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Weather Conditions: {weather_desc}")
    else:
        print("City not found. Please enter a valid city name.")
def main():
    city = input("Enter the city name: ")
    weather_data = fetch_weather(city)
    display_weather(weather_data)

if __name__ == "__main__":
    main()