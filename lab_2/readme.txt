create env: py -3 -m venv venv
activate the env: venv\Scripts\activate

set up development mode: $env:FLASK_ENV = "development"
set up main file: $env:FLASK_APP = "app" (app is DEFAULT)

start server: flask run