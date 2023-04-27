# Timer-management-Web-App

Simple timer management web-app with database synchronization. The main goal for this web-site is to make timers that do
not depend on web-page session. If the user leaves the page, the timers of user will be loaded from the server and all
the progress and metadata will be saved.

# Instructions

* To run backend part:

1. Create a new venv:
   python -m venv /path/to/new/virtual/environment
   (note that the python version should be >= 3.10)
2. Activate venv depending on your OS.
3. Install python requirements:
   pip install -r requirements.txt
4. Run server using unicorn:
   fastapi_app.main:app --host=0.0.0.0 --port=8080 --reload


### Link to the Postman collection with all the authorization requests and responses:
![[Authorization collection](https://go.postman.co/workspace/Timers~1e9edfce-1e47-4521-8c6d-28315952eb9b/api/20118925-ecf8-4fe9-8584-b4dc59694c47)](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)


