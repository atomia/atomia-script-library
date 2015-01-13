###
### Script name: Terminate subscriptions
### Description: Terminates a batch of subscriptions specified by id.
### Version: 1.0
### Author: Jimmy Bergman
###
### Parameters:
### subscriptionIds - Array of subscription ID:s to terminate
###    example: [ "5332eba0-f6aa-4b57-a340-9c141f9d252f", "0a019a00-6c62-49f7-a251-d04829beaff8" ]
### reason - Reason for terminating
###    example: "Some reason"

import System

for id in subscriptionIds:
	print "Terminating subscription with id " + id
	billingApi.TerminateSubscription(System.Guid(id), reason)