<p align="center">
  <a href="https://www.securenative.com"><img src="https://user-images.githubusercontent.com/45174009/77826512-f023ed80-7120-11ea-80e0-58aacde0a84e.png" alt="SecureNative Logo"/></a>
</p>

<p align="center">
  <b>A Cloud-Native Security Monitoring and Protection for Modern Applications</b>
</p>
<p align="center">
  <a href="https://github.com/securenative/securenative-python">
    <img alt="Github Actions" src="https://github.com/securenative/securenative-java/workflows/CI/badge.svg">
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


secureative =  SecureNative.init()
```
### Option 2: Initialize via API Key

```python
from securenative.securenative import SecureNative


securenative =  SecureNative.init_with_api_key("YOUR_API_KEY")
```

### Option 3: Initialize via ConfigurationBuilder
```python
from securenative.securenative import SecureNative


securenative = SecureNative.init_with_options(SecureNative.config_builder()
                                        .with_api_key("API_KEY")
                                        .with_max_events(10)
                                        .with_log_level("ERROR")
                                        .build())
```

## Getting SecureNative instance
Once initialized, sdk will create a singleton instance which you can get: 
```python
from securenative.securenative import SecureNative


secureNative = SecureNative.get_instance()
```

## Tracking events

Once the SDK has been initialized, tracking requests sent through the SDK
instance. Make sure you build event with the EventBuilder:

 ```python
from securenative.securenative import SecureNative
from securenative.event_options_builder import EventOptionsBuilder
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


securenative = SecureNative.get_instance()

context = SecureNative.context_builder().\
        with_ip("127.0.0.1").\
        with_client_token("SECURED_CLIENT_TOKEN").\
        with_headers({"user-agent", "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"}).\
        build()

event_options = EventOptionsBuilder(EventTypes.LOG_IN).\
with_user_id("USER_ID").\
        with_user_traits(UserTraits("USER_NAME", "USER_EMAIL")).\
        with_context(context).\
        with_properties({"prop1": "CUSTOM_PARAM_VALUE", "prop2": True, "prop3": 3}).\
        build()

securenative.track(event_options)
 ```

You can also create request context from requests:

```python
from securenative.securenative import SecureNative
from securenative.event_options_builder import EventOptionsBuilder
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


def track(request):
    securenative = SecureNative.get_instance()
    context = SecureNative.context_builder().from_http_request(request).build()

    event_options = EventOptionsBuilder(EventTypes.LOG_IN).\
        with_user_id("USER_ID").\
        with_user_traits(UserTraits("USER_NAME", "USER_EMAIL")).\
        with_context(context).\
        with_properties({"prop1": "CUSTOM_PARAM_VALUE", "prop2": True, "prop3": 3}).\
        build()
    
    securenative.track(event_options)
```

## Verify events

**Example**

```python
from securenative.securenative import SecureNative
from securenative.event_options_builder import EventOptionsBuilder
from securenative.enums.event_types import EventTypes
from securenative.models.user_traits import UserTraits


def track(request):
    securenative = SecureNative.get_instance()
    context = SecureNative.context_builder().from_http_request(request).build()

    event_options = EventOptionsBuilder(EventTypes.LOG_IN).\
        with_user_id("USER_ID").\
        with_user_traits(UserTraits("USER_NAME", "USER_EMAIL")).\
        with_context(context).\
        with_properties({"prop1": "CUSTOM_PARAM_VALUE", "prop2": True, "prop3": 3}).\
        build()
    
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
    