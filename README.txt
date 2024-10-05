
## Introduction

Development and deployment of sales forecasting models for American Retailer Co, a growing US retailer. The models aim to provide insights into sales performance across the company's 10 stores to improve decision-making in budgeting, staffing, and inventory management.


## Features

- A predictive model for item-level sales forecasting.
- A forecasting model for overall revenue prediction.

## Launch Tool
To launch the tool you have to open both the API and the Streamlit from end webservice serperately
https://amla-at2-api-1.onrender.com
https://fast-api-1-0.onrender.com


## Pages in Streamlit



## API Endpoints

### GET /sales/national

- **Description**: Fetch national sales forecast for a specific date.
- **Parameters**:
    - `target_date` (required): The target date for the sales forecast. Example: 2015-12-25.
- **Success Response**:
    - **Code**: 200 OK
    - **Content**: JSON object with the sales forecast.
- **Error Responses**:
    - **Code**: 422 Unprocessable Entity
    - **Content**: { "detail": "Date must be between 2015-04-18 and 2020-12-31" }


### GET /sales/stores/items

- **Description**: Fetch sales predictions for a specific store and item.
- **Parameters**:
    - `target_date` (required): The target date for the prediction in YYYY-MM-DD format. Example: 2015-12-25.
    - `item_id` (required): The item ID for the prediction. Example: FOODS_3_301.
    - `store_id` (required): The store ID for the prediction. Example: CA_1.
- **Success Response**:
    - **Code**: 200 OK
    - **Content**: JSON object with the sales predictions.
- **Error Responses**:
    - **Code**: 400 Bad Request
    - **Content**: { "detail": "Parameter name is required" }
    - **Code**: 422 Unprocessable Entity
    - **Content**: JSON object with validation error details.

### Folder structure
fast-api/
    |-ml_stuff/
        |-data/
        |-models/
            |-predictive/
            |-forecasting/
            |-transformation/
        |-transforms.py
        |-predict.py
        |-__init__.py
    |-app/
        |-main.py
    |-Dockerfile
    |-requirements.txt

streamlit/
    |-app/
        |-main.py
    |-Dockerfile
    |-requirements 



### Prerequisites

List any prerequisites that need to be installed before your project can be used.

- Python 3.11.4
- pip

### Clone the Repository

```sh
git clone https://github.com/raym2828/AMLA_AT2_API
cd AMLA_AT2_API
```

### Install Dependencies

```sh
pip install -r requirements.txt
```