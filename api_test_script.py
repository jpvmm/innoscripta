import requests

# define the base url
base_url = 'http://localhost:8885'  # replace with your actual server address and port

# define the endpoint
endpoint = "/company/"

# define the parameters for the GET request
params = {
    "company_name": "OpenAI",
    "company_country": "USA",
    "company_website": "https://www.openai.com",
}

# send a GET request
response = requests.get(base_url + endpoint, params=params)

# print the response
print(response.json())