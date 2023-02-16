### Installation
- Make sure you have `pip` and `venv` installed. 

        To install virtualenv: python3 -m venv venv
        
        To install packages: pip install -r requirements.txt

- Create `.env` file and copy `.env.example` content in `.env`

      CONFIG_ENV=dev
      SECRET_KEY=your-secret-key
      PATH_TO_GCS_PRIVATE_KEY=path/to/gcs/private/key
      FLASK_RUN_PORT=8000
      EMULATE_GCS_SERVER=False
      EMULATED_GCS_SERVER_ENDPOINT=http://localhost:4443
      BUCKET_NAME=stored-configuration-files

- Run application
         
      python manage.py

- For Run Tests
      
      pytest

### Terminal commands by using make
Note: make sure you have `pip` and `venv` installed.

    Initial installation: make install

    To run test: make tests

    To run application: make run

    To run all commands at once : make all


### Viewing the app ###
    http://127.0.0.1:5000/

## Config API

#### Details of config
#### Endpoint: “/config/“
#### Request Method: GET
#### Status Code: 200
#### Content-Type: JSON

#### Response:
```json
{
  "firstName": "Ashik", 
  "secondName": "Rafat",
  "address": "Dhaka, Bangladesh",
  "ageInYears": 10,
  "creditScore": 1.22
}
```

#### Create or Update of config
#### Endpoint: “/config/“
#### Request Method: POST
#### Status Code: 200
#### Content-Type: JSON

### Payload
| field name  |  Type   | Required |
|-------------|:-------:|---------:|
| firstName   | string  |     True |
| secondName  | string  |     True |
| address     | string  |     True |
| ageInYears  | integer |     True |
| creditScore |  float  |     True |

#### Response:
```json
{
  "message": "Configuration successfully Updated."
}
```