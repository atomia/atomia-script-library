###
### Script name: Mass product switch
### Description: Use this script to switch products on a list of subscriptions. For example from DN-COM to DN-COM-2
### Author: Nemanja Petrovic
### Version: 1.0
###
### Parameters:
### fromProduct - Article number of a product you want to switch from
###    example: "DN-COM"
### toProduct - Article number of a product you want to switch to
###    example: "DN-COM-2"
### listOfCustomers - List of customers with subscriptions to switch products
###    example: [ "500600", "130200", "500400" ]
### listOfSubscriptions - List of customers subscriptions in the exact order customer-subscription
###    example: [ "5332eba0-f6aa-4b57-a340-9c141f9d252f", "0a019a00-6c62-49f7-a251-d04829beaff8" ]

### Default import
import sys
import System
from System import Array
import datetime
from System import DateTime

### Import some specific Atomia reference
import clr
clr.AddReference('Atomia.Web.Plugin.ServiceReferences')
import Atomia.Web.Plugin.ServiceReferences.AtomiaBillingApi
from Atomia.Web.Plugin.ServiceReferences.AtomiaBillingApi import AccountNote
from Atomia.Web.Plugin.ServiceReferences.AtomiaBillingApi import AccountNoteType

### Import Csharp Linq
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

# Get required items
productFrom = billingApi.GetItemByArticleNumber(fromProduct)
productTo = billingApi.GetItemByArticleNumber(toProduct)

lenCustomers = len(listOfCustomers)
lenSubs = len(listOfSubscriptions)

if (lenCustomers != lenSubs):
    print ("Error - Length is not the same customers ", lenCustomers, " subscriptions ", lenSubs)
    sys.exit()

for index in range(lenCustomers):
    customerNumber = listOfCustomers[index]
    subscriptionId = listOfSubscriptions[index]

    # Get Account
    account = billingApi.GetAccountByName(customerNumber)
    if(account is None):
        print ("Account is NULL ", customerNumber)
        continue

    # Get subscription to change item
    subToUpdate = billingApi.GetSubscriptionById(System.Guid(subscriptionId), account)
    if(subToUpdate is None):
        print ("Sub to update is NULL ",subscriptionId)
        continue

    if (subToUpdate.Item.ArticleNumber != fromProduct):
    	print ("Error - Subscription ", subToUpdate.FriendlyId ," is not ", fromProduct, " subscription")
    	continue
    if (subToUpdate.State != "OK"):
    	print ("Error - Subscription ", subToUpdate.FriendlyId ," is not in OK state it is in ", subToUpdate.State, " state.")
    	continue
    if (subToUpdate.ProvisioningStatus != "PROVISIONED"):
    	print ("Error - Subscription ", subToUpdate.FriendlyId, " is not PROVISIONED.")
    	continue
    if (subToUpdate.Item.Id != productFrom.Id):
    	print ("Error - Item Id in subscription is not the same as Id of", fromProduct," Item")
    	continue

    print "Processing account: " + account.Name
    print "Processing subscription: " + subToUpdate.FriendlyId
    print ("START - Switching from", fromProduct, "to ", toProduct)
    subToUpdate.ItemId = productTo.Id
    billingApi.UpdateSubscription(subToUpdate)

    check = billingApi.GetSubscriptionById(System.Guid(subscriptionId), account)
    if (check.Item.ArticleNumber != toProduct):
    	print ("Error - Unsuccessful Switch from", fromProduct, "to ", toProduct)
    	sys.exit()
    else:
    	print ("DONE - Switching from", fromProduct, "to ", toProduct)
    	accountDetails = billingApi.GetAccountDetails(account.Id)
    	if accountDetails is not None:
    		note = AccountNote()

    		note.Note = ("Switch from " + fromProduct + " to " + toProduct)
    		note.Date = DateTime.Now
    		note.CreatedByAccount = account.ParentAccountId
    		note.CreatedByUser = "Administrator"
    		note.CreatedTime = DateTime.Now
    		note.UpdatedByAccount = account.ParentAccountId
    		note.UpdatedByUser = "Administrator"
    		note.LastChangeTime = DateTime.Now
    		note.Status = 0
    		note.NoteType = AccountNoteType.Subscription
    		note.ExternalId = check.Id
    		note.ExternalNumber = check.FriendlyId
    		note.VisibleToCustomer = False
    		note.ExpirationDate = DateTime.Now.AddYears(99)

    		# Required conversation from array-list and vice versa
    		accountNotes = accountDetails.AccountNotes.ToList()
    		accountNotes.Add(note)
    		accountDetails.AccountNotes = accountNotes.ToArray()

    		billingApi.UpdateAccountDetails(accountDetails)
    		print "NOTE ADDED"