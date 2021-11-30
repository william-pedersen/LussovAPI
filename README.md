# LussovAPI 
[![forthebadge](https://forthebadge.com/images/badges/built-with-grammas-recipe.svg)](https://forthebadge.com) 
[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](https://forthebadge.com) <br>
[![forthebadge](https://forthebadge.com/images/badges/as-seen-on-tv.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/kinda-sfw.svg)](https://forthebadge.com) <br>

**TL;DR**: py API container, pip install -r [requirements.txt](./requirements.txt), [example](./apis/test/ping.py), [main configuration](./main.py)

**Long version**:

## Install Dependancies

Download file [requirements.txt](./requirements.txt) <br>

requirements.txt
```
Flask>=2.0.2
Flask_RESTful>=0.3.9
pymongo>=3.12.1
requests>=2.26.0
...
```
<br>
Install pip dependancies by running the following command inside of cmd or a shell based application <br>

cmd / shell
```
pip install -r requirements.txt
```
<br>
🎉 Congratulations!

## Initialization and Setup

Create or use a previously existing file that represents your entry script. <br>
A simple example can be found within the repository at [main.py](./main.py) <br>

main.py
``` python
from server import Server



def main():
    server = Server(

    )

if __name__ == '__main__':
    main()
``` 
<br>

There are several configuration options available directly from the initialization of the Server object. <br>
These are passed to the opject as loose type parameters. <br>

``` python
name: str = 'Server', 
 # name of the server
host: str = 'localhost', 
 # server hosting ip
port: Optional[Union[int, str]] = 5000,
 # server hosting port
config: Optional[Union[str, dict]] = 'config.json', 
 # server configuration & value store
apidir: Optional[str] = 'apis',
 # the directory in which endpoints exist
```

#### Endpoints and Hierarchy

Each endpoint represents its own API directory, similar to how classes contain functions. <br>
For example, both the *default* **Ping** and **Test** endpoints represent the **test** API endpoint. <br><br>
*How does this apply within our file structure?* <br>

``` python
.
├── ...
├── apis                    # Alternatively, directory defined in apidir
│   ├── ...                 # ...
│   └── test                # API endpoint test, all endpoints inherit prefix
|   │   ├── ...                 # ...
|   │   └── ping.py                # Contains endpoints Ping and Test
└── ...
```
<br>
Within this example, an API endpoint from ping.py would look as follows: <br>

```
http://localhost:5000/test/{endpoint}?content={}
```
<br>
Within the file itself, it becomes clear that these endpoints function similar to React routing, requiring functional exporting.
<br>

``` python
...

""" 
Endpoints
"""

class Ping(Endpoint):
    def __init__(self, **kwargs) -> Endpoint:
        super().__init__(**kwargs)

    @Endpoint.RequiresArgs()
    def get(self, args: dict) -> tuple:
        print(args)

        return {'response' : 'Pong'}, Endpoint.Codes.OK

class Test(Endpoint):
    def __init__(self, **kwargs) -> Endpoint:
        super().__init__(**kwargs)

    def get(self) -> tuple:

        return {}, Endpoint.Codes.OK

"""
Router
"""

def route() -> Optional[set]:
    return [
        Ping,
        Test
    ]
```
<br>

#### Methods <br>

Within each endpoint, there are several HTTP methods available for utilizing, such as:
<br>get
``` python
def get(self) -> tuple:
  return {}, Endpoint.Codes.OK
```
<br>post
``` python
def post(self) -> tuple:
  return {}, Endpoint.Codes.OK
```
<br>put
``` python
def put(self) -> tuple:
  return {}, Endpoint.Codes.OK
```
<br>delete
``` python
def delete(self) -> tuple:
  return {}, Endpoint.Codes.OK
```
<br>... and more <br>

A list of all modern HTTP methods and their descriptions can be found [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)<br>

#### Decorators <br>

You may also notice that there are several applicable **decorators** available.<br>
Decorators are not required to maintain the functionality of the application, but are required if you wish to pass arguments to HTTP methods.<br>

default arguments decorator
``` python
@Endpoint.RequiresArgs()
# Passes arguments from content to keyword args
```
*Requires keyword **content** to be present within the query. All values passed to args should be passed through content as a string, per conventions.*
<br>





<br><br>
That's all, folks
##### Bottom text
