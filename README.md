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
[
  {
    "firstName": "Ashik", 
    "secondName": "Rafat",
    "address": "Dhaka, Bangladesh",
    "ageInYears": 10,
    "creditScore": 1.22
  }
]

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


### Pytest Result
```bash
❯ pytest
collected 16 items                                                                                                           

app/test/unit/test_controllers.py::TestConfigurationController::test_get_config_request_will_give_200 PASSED           [  6%]
app/test/unit/test_controllers.py::TestConfigurationController::test_if_config_file_does_not_exists_it_will_give_404_status_code PASSED [ 12%]
app/test/unit/test_controllers.py::TestConfigurationController::test_invalid_json_schema_post_request_will_give_400_status PASSED [ 18%]
app/test/unit/test_controllers.py::TestConfigurationController::test_valid_json_schema_post_request_will_give_200_status PASSED [ 25%]
app/test/unit/test_controllers.py::TestConfigurationController::test_uploaded_json_data_and_retrieved_json_data_is_same PASSED [ 31%]
app/test/unit/test_controllers.py::TestHealthCheck::test_application_health_check_will_give_200_status PASSED          [ 37%]
app/test/unit/test_services.py::TestStorageService::test_emulated_gcs_client_will_give_404_if_bucket_doesnt_exists PASSED [ 43%]
app/test/unit/test_services.py::TestStorageService::test_emulated_gcs_client_will_give_404_if_config_json_file_does_not_exist_it_will_give_404_request PASSED [ 50%]
app/test/unit/test_services.py::TestStorageService::test_if_path_of_private_key_not_given_it_will_throw_400_status PASSED [ 56%]
app/test/unit/test_services.py::TestStorageService::test_if_bucket_name_does_not_exist_it_will_give_404_request PASSED [ 62%]
app/test/unit/test_services.py::TestStorageService::test_if_config_json_file_does_not_exist_it_will_give_404_request PASSED [ 68%]
app/test/unit/test_services.py::TestStorageService::test_get_config_file_from_gcs PASSED                               [ 75%]
app/test/unit/test_services.py::TestStorageService::test_upload_config_data_as_json_in_gcs PASSED                      [ 81%]
app/test/unit/test_services.py::TestConfigurationService::test_get_configuration PASSED                                [ 87%]
app/test/unit/test_services.py::TestConfigurationService::test_invalid_json_schema_will_throw_400_status PASSED        [ 93%]
app/test/unit/test_services.py::TestConfigurationService::test_valid_json_config_data_will_upload_gcs_server PASSED    [100%]

===================================================== 16 passed in 0.09s =====================================================
```
