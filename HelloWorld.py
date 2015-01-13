###
### Script name: Hello world
### Description: Prints Hello World a user specified number of times
###				 through billingApi.Echo as an demonstration of how 
###				 to write a script for the Atomia Scripting system.
### Version: 1.0
### Author: Jimmy Bergman
###
### Parameters:
### n - Times to say hello
###    example: 10
###

import time

for i in range(1, n + 1):
    print billingApi.Echo("Hello World and sleeping for 1 second (" + str(i) + "/" + str(n) + ")")
    time.sleep(1)