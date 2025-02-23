# api-hijacker

This module was built to easily create python wrappers onto existing APIs.\
Using the [cloudscraper](https://github.com/VeNoMouS/cloudscraper) module most website's endpoints can be accessed without issues.

## Installation 

[![PyPI version](https://img.shields.io/pypi/v/api-hijacker.svg)](https://pypi.org/project/api-hijacker/)

You can install this package using pip:
```sh
pip install api-hijacker
```

## Use case example:

<pre>
Project/
├── main.py
└── Service/
    └── api.py
</pre>

api.py:
```python
import apiCore
from apiCore import request

BASE_URL = "https://api.example.com/users"

# Error-handled function to fetch user data
@request()
def fetch_user(user_id, **kwargs):
    return apiCore.get(f"{BASE_URL}/{user_id}", **kwargs)

# Error-handled function to create a new user
@request(errorHandler=apiCore.HTTPErrorHandler().allow(429))
# in this example status code 429 indicates that captcha authentication is required
# thanks to the .allow() method this statu code will not be retried / excepted
def create_user(data, **kwargs):
    return apiCore.post(BASE_URL, json=data, **kwargs)

# Error-handled function to update user data
@request(retries=10, exponentialBackoff=True)
# more retries and each time wait longer before next retry
def update_user(user_id, data, **kwargs):
    return apiCore.put(f"{BASE_URL}/{user_id}", json=data, **kwargs)

# Error-handled function to delete a user
@request()
def delete_user(user_id, **kwargs):
    return apiCore.delete(f"{BASE_URL}/{user_id}", **kwargs)
```

main.py:
```python
from Service import api

api.fetch_user(userId)  # returns requests.Response

# proxy example
proxy = {
    "http": "http://http-proxy.example:1234",
    "https": "https://https-proxy.example:1234"
}

api.create_user(user_data, proxy=proxy)  # proxy keyword argument is passed to handle.request()

```

**With cloudscraper this module allows for fast integration with webscraping to easily interact with websites lacking API documentation and/or python libraries.**