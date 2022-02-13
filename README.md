# YACURL
Yacurl (short of yet another curl) is an implementation of a tcp socket that tries to connect to a http server and retrieves the main page of the server. It also download the static resources from the page.

## Usage
The implementation of yacurl is found in py directory.
1. `cd py`
2. `python yacurl.py`
Here, you'll be prompted to type the port and the url from the page you want to access.
**Notes:** 
- valid options for port are 80 and 443.
- Make sure of typing well the url as it is shown in browser.

After you give the program the parameters, the requested information will be placed at py/pages/<url>