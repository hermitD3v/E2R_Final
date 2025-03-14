import requests

# Function to read the entire CSV file and return its content as a string
def read_csv_as_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Read the CSV file
csv_content = read_csv_as_string('Chasis\hbi.csv')

# TeamCity API details
url = "https://hdmtteamcity.intel.com/httpAuth/app/rest/buildQueue"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiAiVENWMiJ9.ZWxXdUx4LU45WWNGRHRXakZodVlSV0hCaDUw.ZWVkNzAzYWItNjhhYi00ZmM1LTkwMjAtMzg2OGQzNzNiZGUz"
}

# JSON payload with the CSV content as a parameter and specifying the agent
data = {
    "buildType": {
        "id": "Hdmt3x_Sandbox_E2r_TriggerPartFlows"
    },
    "agent": {
        "id": "KM-HBI-10065"  # Replace with the actual agent ID
    },
    "properties": {
        "property": [
            {
                "name": "input_csv",
                "value": csv_content
            }
        ]
    }
}
proxies = {
    "http": "http://proxy-iind.intel.com:912",
    "https": "http://proxy-iind.intel.com:912",
}

response = requests.post(url, json=data, headers=headers, proxies=proxies)


# Check the response
if response.status_code in [200, 201]:
    print("Build triggered successfully with CSV content on specified agent!")
else:
    print("Failed to trigger build:", response.text)