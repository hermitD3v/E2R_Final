@echo off
setlocal

:: Define your TeamCity server URL and access token
set "TEAMCITY_URL=https://hdmtteamcity.intel.com"
set "ACCESS_TOKEN=eyJ0eXAiOiAiVENWMiJ9.ZWxXdUx4LU45WWNGRHRXakZodVlSV0hCaDUw.ZWVkNzAzYWItNjhhYi00ZmM1LTkwMjAtMzg2OGQzNzNiZGUz"

:: Fetch the list of all agents and parse the JSON response using PowerShell
powershell -NoProfile -Command ^
    "$url = '%TEAMCITY_URL%/app/rest/agents?locator=enabled:true,authorized:true&fields=agent(name,build)';" ^
    "$accessToken = '%ACCESS_TOKEN%';" ^
    "$headers = @{ 'Authorization' = 'Bearer ' + $accessToken };" ^
    "$response = Invoke-RestMethod -Uri $url -Headers $headers -UseBasicParsing;" ^
    "$agents = [xml]$response;" ^
    "$idle_agents = $agents.agents.agent | Where-Object { -not $_.build };" ^
    "Write-Host 'Idle Agents:';" ^
    "$idle_agents | ForEach-Object { Write-Host $_.name }"

endlocal
pause
