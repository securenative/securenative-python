<p align="center">
  <a href="https://www.securenative.com"><img src="https://user-images.githubusercontent.com/45174009/77826512-f023ed80-7120-11ea-80e0-58aacde0a84e.png" alt="SecureNative Logo"/></a>
</p>

<p align="center">
  <b>A Cloud-Native Security Monitoring and Protection for Modern Applications</b>
</p>
<p align="center">
  <a href="https://github.com/securenative/securenative-python">
    <img alt="Github Actions" src="https://github.com/securenative/securenative-python/workflows/CI/badge.svg">
  </a>
  <a href="https://codecov.io/gh/securenative/securenative-python">
    <img src="https://codecov.io/gh/securenative/securenative-python/branch/master/graph/badge.svg" />
  </a>
  <a href="https://pypi.org/project/securenative/">
    <img src="https://img.shields.io/pypi/pyversions/securenative" alt="python version" height="20">
  </a>
</p>
<p align="center">
  <a href="https://docs.securenative.com">Documentation</a> |
  <a href="https://docs.securenative.com/quick-start">Quick Start</a> |
  <a href="https://blog.securenative.com">Blog</a> |
  <a href="">Chat with us on Slack!</a>
</p>
<hr/>


[SecureNative](https://www.securenative.com/) performs user monitoring by analyzing user interactions with your application and various factors such as network, devices, locations and access patterns to stop and prevent account takeover attacks.


## Install the SDK

When using PyPi, run the following:
```bash
pip install securenative
```

## Initialize the SDK

To get your *API KEY*, login to your SecureNative account and go to project settings page:

### Option 1: Initialize via Config file
SecureNative can automatically load your config from *securenative.ini* file or from the file that is specified in your *SECURENATIVE_CONFIG_FILE* env variable:

```python
from securenative.securenative import SecureNative


# 1. Config file path is given by environment variable 
securenative = SecureNative.init()

# 2. Config file path is specified directly
securenative = SecureNative.init('path/to/securenative.ini')
```
### Option 2: Initialize via API Key

```python
from securenative.securenative import SecureNative


securenative = SecureNative.init_with_api_key("YOUR_API_KEY")
```

### Option 3: Initialize via ConfigurationBuilder
```python
from securenative.securenative import SecureNative
from securenative.config.securenative_options import SecureNativeOptions


options = SecureNativeOptions(api_key="YOUR_API_KEY", max_events=10, log_level="ERROR")
securenative = SecureNative.init_with_options(options)
```

## Getting SecureNative instance
Once initialized, sdk will create a singleton instance which you can get: 
```python
from securenative.securenative import SecureNative


securenative = SecureNative.get_instance()
```

## Tracking events

Once the SDK has been initialized, tracking requests sent through the SDK
instance. Make sure you build event with the EventBuilder:

 ```python
from securenative.securenative import SecureNative
from securenative.context.securenative_context import SecureNativeContext
from securenative.models.event_options import EventOptions
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


securenative = SecureNative.get_instance()

context = SecureNativeContext(client_token="SECURE_CLIENT_TOKEN",
                                ip="127.0.0.1", 
                                headers={"user-agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"})
event_options = EventOptions(event=EventTypes.LOG_IN,
                                user_id="1234",
                                user_traits=UserTraits("Your Name", "name@gmail.com", "+1234567890"),
                                context=context,
                                properties={"custom_param1": "CUSTOM_PARAM_VALUE", "custom_param2": True, "custom_param3": 3})

securenative.track(event_options)
 ```

You can also create request context from requests:

```python
from securenative.securenative import SecureNative
from securenative.models.event_options import EventOptions
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


def track(request):
    securenative = SecureNative.get_instance()

    context = securenative.from_http_request(request)
    event_options = EventOptions(event=EventTypes.LOG_IN,
                                user_id="1234",
                                user_traits=UserTraits("Your Name", "name@gmail.com", "+1234567890"),
                                context=context,
                                properties={"custom_param1": "CUSTOM_PARAM_VALUE", "custom_param2": True, "custom_param3": 3})
    
    securenative.track(event_options)
```

## Verify events

**Example**

```python
from securenative.securenative import SecureNative
from securenative.models.event_options import EventOptions
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


def verify(request):
    securenative = SecureNative.get_instance()

    context = securenative.from_http_request(request)
    event_options = EventOptions(event=EventTypes.LOG_IN,
                                user_id="1234",
                                user_traits=UserTraits("Your Name", "name@gmail.com", "+1234567890"),
                                context=context,
                                properties={"custom_param1": "CUSTOM_PARAM_VALUE", "custom_param2": True, "custom_param3": 3})
    
    verify_result = securenative.verify(event_options)
    verify_result.risk_level  # Low, Medium, High
    verify_result.score  # Risk score: 0 -1 (0 - Very Low, 1 - Very High)
    verify_result.triggers  # ["TOR", "New IP", "New City"]
```

## Webhook signature verification

Apply our filter to verify the request is from us, for example:

```python
from securenative.securenative import SecureNative


def webhook_endpoint(request):
    securenative = SecureNative.get_instance()
    
    # Checks if request is verified
    is_verified = securenative.verify_request_payload(request)
 ```
    
## Extract proxy headers from cloud providers

You can specify custom header keys to allow extraction of client ip from different providers.
This example demonstrates the usage of proxy headers for ip extraction from Cloudflare.

### Option 1: Using config file
```ini
SECURENATIVE_API_KEY: "YOUR_API_KEY"
SECURENATIVE_PROXY_HEADERS: ["CF-Connecting-IP"]
```

Initialize sdk as shown above.

### Options 2: Using ConfigurationBuilder

```python
from securenative.securenative import SecureNative
from securenative.config.securenative_options import SecureNativeOptions


options = SecureNativeOptions(api_key="YOUR_API_KEY", max_events=10, log_level="ERROR", proxy_headers=['CF-Connecting-IP'])
securenative = SecureNative.init_with_options(options)
```


## Remove PII Data From Headers

By default, SecureNative SDK remove any known pii headers from the received request.
We also support using custom pii headers and regex matching via configuration, for example:

### Option 1: Using config file
```ini
SECURENATIVE_API_KEY: "YOUR_API_KEY"
SECURENATIVE_PII_HEADERS: ["apiKey"]
```

Initialize sdk as shown above.

### Options 2: Using ConfigurationBuilder

```python
from securenative.securenative import SecureNative
from securenative.config.securenative_options import SecureNativeOptions


options = SecureNativeOptions(api_key="YOUR_API_KEY", max_events=10, log_level="ERROR", pii_regex_pattern='((?i)(http_auth_)(\w+)?)')
securenative = SecureNative.init_with_options(options)
```