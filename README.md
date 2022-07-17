# Tweet-Schedular

#### Create virtual environment
<pre>python -m venv venv</pre>

#### Install requirements
<pre>pip install -r requirements.txt</pre>

#### Create a project in Google Developers Console
- Create a new project <br/>
- Add Google Drive API and Google Sheets API <br/>
- Download the credentials in JSON format <br/>
- Copy the `gsheet_credenetials_dev.json` to `gsheet_credenetials.json` <br/>
- Enter the credentials in gsheet_credenetials.json file <br/>
- Copy client_email from credentials <br/>
- Open the Google Sheets and find the `Share` option. Paste the email there and share<br/>
- Copy the `.env_development` to `.env` and paste the google spreadsheet api key <br/>
- You will find your key in `https://docs.google.com/spreadsheets/d/YOUR_KEY/edit#gid=0` your spreadhseet URL

#### Create app in Twitter Developers Account
- Create APP from developers dashboard
- Copy the APP key, secret_key, access_token, access_token_secret
- Paste them into `.env` file

#### Set flask app to terminal
+ Windows: set FLASK_APP=app/main.py
+ MacOS: export FLASK_APP=app/main.py

#### Run the server
<pre>flask run</pre>

#### Run the worker script
- Open new terminal
- Go to project root directory and run below command
<pre>python tweet.py</pre>


#### Note
If you deploy your app to heroku, please don't push the `gsheet_credentials.json` and `.env` file, you have to setup the environment variables from the heroku dashboard.