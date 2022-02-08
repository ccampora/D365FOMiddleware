Replace environment variables in DemoData.py

```
# REPLACE HERE
D365FOENV_URL = "<D365FO URL without trailing slash>"
CLIENT_APP_ID = "Client App Id"
SECRET = "Client App Secret"
```
run ```python DemoData.py``` and look for the file output.sql. Import the script into the staging DB using SQL Server Management 
