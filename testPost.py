import requests

# Replace with your actual API URL
api_url = "http://127.0.0.1:5000/weather/2"

# JSON payload for the POST request
data = {
    "name": "chonburi",
    "temp": "29",
    "weather": "hot",
    "people": "5000"
}

# Send a POST request
response = requests.post(api_url, json=data)

# Print the response status code
print(f"Response Status Code: {response.status_code}")

# Print the response content regardless of whether it's valid JSON
print("Response Content:")
print(response.text)
