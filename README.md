# Python SDK for Secure Native

## How to get it?
the python SDK is published to PyPi so you can just use `pip` to install it:
```bash
pip install securenative
```

## Initialize the SDK
Go to the settings page of your SecureNative account and find your API key, afterwards add this line on your application main module.
```python
import securenative

# Many lines of code ...

if __name__=='__main__':
    # Your bootstrap code
    securenative.init('API_KEY') # Should be called before any other call to secure native
```

## Tracking Events (async)
Once the SDK has been initialized, you can start sending new events with the `track` function:
```python
import securenative
from securenative.event_options import Event, User

def my_login_function():
    # Many lines of code ...
    
    event = Event( # Build the event from the request's context
        event_type=securenative.event_types.login,
        ip='35.199.23.1',
        remote_ip='35.199.23.2',
        user_agent='Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
        sn_cookie_value='eyJjaWQiOiJkYzgyYjdhZS00ODFkLTQyODItYTMyZC0xZTU1Njk2ZjNmZTQiLCJmcCI6Ijk5NGYzZjVjZTRiYWUwODQzMTRhOTFkNzgyN2I1MWYuMjQ3MDBmOWYxOTg2ODAwYWI0ZmNjODgwNTMwZGQwZWQifQ',
        user=User(
            user_id='1',
            user_email='1@example.com',
            user_name='example example'
        )
    )
    
    # Track it:
    securenative.track(event)
    
    # Many lines of code ...

```

## Verification Events (sync)
Once the SDK has been initialized, you can protect sensitive operation by calling the `verify` function, this function will return the risk analysis of the current user.

```python
import securenative
from securenative.event_options import Event, User

def my_change_password_function():
    # Many lines of code...
    
    event = Event( # Build the event from the request's context
            event_type=securenative.event_types.verify,
            ip='35.199.23.1',
            remote_ip='35.199.23.2',
            user_agent='Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
            sn_cookie_value='eyJjaWQiOiJkYzgyYjdhZS00ODFkLTQyODItYTMyZC0xZTU1Njk2ZjNmZTQiLCJmcCI6Ijk5NGYzZjVjZTRiYWUwODQzMTRhOTFkNzgyN2I1MWYuMjQ3MDBmOWYxOTg2ODAwYWI0ZmNjODgwNTMwZGQwZWQifQ',
            user=User(
                user_id='1',
                user_email='1@example.com',
                user_name='example example'
            )
        )
     
    result = securenative.verify(event)
    if result['riskLevel'] == 'high':
        return 'Cannot change password'
    elif result['riskLevel'] == 'medium':
        return 'MFA'
     
     # Many lines of code...
```

## Verifying Incoming Webhooks
You can use the SDK to verify incoming webhooks from Secure Native, just call the `veriy_webhook` function which return a boolean which indicates if the webhook came from Secure Native servers.
```python
import securenative

@post('/sn/webhook')
def sn_webhook_handler(headers, body):
    sig_header = headers["X-SecureNative"]
    if securenative.verify_webhook(sig_header, body):
        # Handle the webhook
        level = body['riskLevel']
        pass
    else:
        # This reqeust wasn't sent from Secure Native servers, you can dismiss/investigate it
        pass
    
```

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
  <a href="https://codecov.io/gh/securenative/securenative-python">
    <img src="https://codecov.io/gh/securenative/securenative-java/branch/master/graph/badge.svg" />
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

When using Maven, add the following dependency to your `pom.xml` file:
```xml
<dependency>
    <groupId>com.securenative.java</groupId>
    <artifactId>sdk-base</artifactId>
    <version>LATEST</version>
</dependency>
```

When using Gradle, add the following dependency to your `build.gradle` file:
```gradle
compile group: 'com.securenative.java', name: 'sdk-parent', version: '0.3.1', ext: 'pom'
```

When using SBT, add the following dependency to your `build.sbt` file:
```sbt
libraryDependencies += "com.securenative.java" % "sdk-parent" % "0.3.1" pomOnly()
```

## Initialize the SDK

To get your *API KEY*, login to your SecureNative account and go to project settings page:

### Option 1: Initialize via Config file
SecureNative can automatically load your config from *securenative.properties* file or from the file that is specified in your *SECURENATIVE_CONFIG_FILE* env variable:

```java
SecureNative secureNative =  SecureNative.init();
```
### Option 2: Initialize via API Key

```java
SecureNative secureNative =  SecureNative.init("YOUR_API_KEY");
```

### Option 3: Initialize via ConfigurationBuilder
```java
SecureNative secureNative = SecureNative.init(SecureNative.configBuilder()
                                        .withApiKey("API_KEY")
                                        .withMaxEvents(10)
                                        .withLogLevel("error")
                                        .build()); 
```

## Getting SecureNative instance
Once initialized, sdk will create a singleton instance which you can get: 
```java
SecureNative secureNative = SecureNative.getInstance();
```

## Tracking events

Once the SDK has been initialized, tracking requests sent through the SDK
instance. Make sure you build event with the EventBuilder:

 ```java
SecureNative secureNative = SecureNative.getInstance();

SecureNativeContext context = SecureNative.contextBuilder()
        .withIp("127.0.0.1")
        .withClientToken("SECURED_CLIENT_TOKEN")
        .withHeaders(Maps.defaultBuilder()
                    .put("user-agent", "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405")
                    .build())
        .build();

EventOptions eventOptions = EventOptionsBuilder.builder(EventTypes.LOG_IN)
        .userId("USER_ID")
        .userTraits("USER_NAME", "USER_EMAIL")
        .context(context)
        .properties(Maps.builder()
                .put("prop1", "CUSTOM_PARAM_VALUE")
                .put("prop2", true)
                .put("prop3", 3)
                .build())
        .timestamp(new Date())
        .build();

secureNative.track(eventOptions);
 ```

You can also create request context from HttpServletRequest:

```java
@RequestMapping("/track")
public void track(HttpServletRequest request, HttpServletResponse response) {
    SecureNativeContext context = SecureNative.contextBuilder()
                                              .fromHttpServletRequest(request)
                                              .build();

    EventOptions eventOptions = EventOptionsBuilder.builder(EventTypes.LOG_IN)
            .userId("USER_ID")
            .userTraits("USER_NAME", "USER_EMAIL")
            .context(context)
            .properties(Maps.builder()
                    .put("prop1", "CUSTOM_PARAM_VALUE")
                    .put("prop2", true)
                    .put("prop3", 3)
                    .build())
            .timestamp(new Date())
            .build();
    
    secureNative.track(eventOptions);
}
```

## Verify events

**Example**

```java
@RequestMapping("/track")
public void track(HttpServletRequest request, HttpServletResponse response) {
    SecureNativeContext context = SecureNative.contextBuilder()
                                              .fromHttpServletRequest(request)
                                              .build();

    EventOptions eventOptions = EventOptionsBuilder.builder(EventTypes.LOG_IN)
            .userId("USER_ID")
            .userTraits("USER_NAME", "USER_EMAIL")
            .context(context)
            .properties(Maps.builder()
                    .put("prop1", "CUSTOM_PARAM_VALUE")
                    .put("prop2", true)
                    .put("prop3", 3)
                    .build())
            .timestamp(new Date())
            .build();
    
    VerifyResult verifyResult = secureNative.verify(eventOptions);
    verifyResult.getRiskLevel() // Low, Medium, High
    verifyResult.score() // Risk score: 0 -1 (0 - Very Low, 1 - Very High)
    verifyResult.getTriggers() // ["TOR", "New IP", "New City"]
}
```

## Webhook signature verification

Apply our filter to verify the request is from us, example in spring:

```java
@RequestMapping("/webhook")
public void webhookEndpoint(HttpServletRequest request, HttpServletResponse response) {
    SecureNative secureNative = SecureNative.getInstance();
    
    // Checks if request is verified
    Boolean isVerified = secureNative.verifyRequestPayload(request);
}
 ```