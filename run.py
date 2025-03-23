import requests

# TeamCity API details
url = "https://hdmtteamcity.intel.com/app/rest/buildQueue"
token = "eyJ0eXAiOiAiVENWMiJ9.ZWxXdUx4LU45WWNGRHRXakZodVlSV0hCaDUw.ZWVkNzAzYWItNjhhYi00ZmM1LTkwMjAtMzg2OGQzNzNiZGUz"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# JSON payload with the CSV content as a parameter and specifying the agent
data = {
    "buildType": {
        "id": "Hdmt3x_Sandbox_E2r_TriggerPartFlows"
    },
    "agent": {
        "id": "353063"  # Replace with the actual agent ID       KM-HBI-10065 43996        KM-HBI-10066 353063
    },
    "properties": {
        "property": [
            {
                "name": "SessionID",
                "value": "hbi"
            }
        ]
    }
}

response = requests.post(url, json=data, headers=headers, verify=False)


# Check the response
if response.status_code in [200, 201]:
    print("Build triggered successfully with CSV content on specified agent!")
else:
    print("Failed to trigger build:", response.text)