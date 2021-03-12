# atomia-script-library

Atomia Script Library is a feature in our AdminPanel which allows us to use Python and write custom scripts which are being executed through AdminPanel and have access to Atomia APIs:

- Billing API
- Account API
- Core API
- User API

All scripts are being executed inside AdminPanel process in a separate Thread created for each script run.

## Docs

*In the following section we will cover all major things for you to get started with writing scripts and all faq.*

### **AdminPanel script menu**

In order to execute scripts you must enter AdminPanel and go to System > Scripting. In this page on the left you will see a widget containing three pages:

- Script console
> Used to write/run scripts

- Local scripts
> These are the scripts installed on your VM

- Script library
> This is a page which is fetching scripts from the GitHub.

### **How to install scripts**

In order to install scripts and have it on your VM so you don't always do manual copy/pasting and running via script console you can use Local scripts feature. This page is listing all installed scripts on your VM.

**To install you must copy {file-name}.py file inside with a unique name:**

```
C:\Program Files (x86)\Atomia\AdminPanel\App_Data\LocalScripts
```

If you are missing some folder, create it manually.


Now it is important to add that each script placed in `LocalScripts` folder must have the exact structure and rules must be followed:

In each file at the start you must add the following Python comments in the exact order and look. These comments on the start of the file are processed by Atomia in order to populate some data in the frontend of the Local scripts page. Especially the important part are the **parameters**. The parameters are input data which Administrator can use to provide data to the script in order to achieve desired execution.

Parameters have its structure which must be followed:

```
...
### Parameters:
### {Variable_Name} - some description of this variable which will be written on the fronted
###    example: "under these quotes you write an example of this variable data which Administrator should enter"
```

Take a look at this below. The script has two parameters `customerNumber` and `domainName` and these two parameters are used inside the script and you can use them directly:


```
###
### Script name: Some random script name
### Description: Some random description.
### Author: Nemanja Petrovic
### Version: 1.0
###
### Parameters:
### customerNumber - Customer which TOOL you want to do a deassign on
###    example: "500600"
### domainName - Domain name which is assigned to TOOL
###    example: "somedomainname.ch"

import System

print "Script start"
print ("Prining customer number", customerNumber)
print ("Printing domain name", domainName)
```

**Installing scripts does not restart the AdminPanel process and it is not needed to restart it in order to install and use some script**


### **How to access Atomia APIs via Python**

- Billing API

```
import System

billingApi.TerminateSubscription(System.Guid(id), "some reason")
```

- Account API

```
import System

accountApi...
```

- Core API

```
import System

coreApi.ModifyService(someService, customerNumber)
```

- User API

```
import System

userApi...
```


### **Accessing C# LINQ**

In order to access C# LINQ function use the following:

```
import System
from System import Array
from System.Collections.Generic import List

### Import Csharp LINQ
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

```

### **Using some custom DLL and Atomia model**

Sometimes you will probably need some model from Atomia Billing API in order to populate it with data and add it to the database. In order to achieve this lets cover customer Note adding example. The same process goes for other models.


```
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

# some random data
customerNumber = "500600"
subscriptionId= "1F6AAC99-9904-43C8-988B-4D023521E962"

account = billingApi.GetAccountByName(customerNumber)
subscription = billingApi.GetSubscriptionById(System.Guid(subscriptionId), account)
accountDetails = billingApi.GetAccountDetails(account.Id)

if accountDetails is not None:
	note = AccountNote()

	note.Note = "Some random note data"
	note.Date = DateTime.Now
	note.CreatedByAccount = account.ParentAccountId
	note.CreatedByUser = "Administrator"
	note.CreatedTime = DateTime.Now
	note.UpdatedByAccount = account.ParentAccountId
	note.UpdatedByUser = "Administrator"
	note.LastChangeTime = DateTime.Now
	note.Status = 0
	note.NoteType = AccountNoteType.Subscription
	note.ExternalId = subscription.Id
	note.ExternalNumber = subscription.FriendlyId
	note.VisibleToCustomer = False
	note.ExpirationDate = DateTime.Now.AddYears(99)

	# Required conversation array-to-list and vice versa
	accountNotes = accountDetails.AccountNotes.ToList()
	accountNotes.Add(note)
	accountDetails.AccountNotes = accountNotes.ToArray()

	billingApi.UpdateAccountDetails(accountDetails)
    print "NOTE ADDED"
```



## Scripts

Description of the scripts in this repostiory and what are they used for.

- [HelloWorld.py](HelloWorld.py) - Hello world example
- [CloneProduct.py](CloneProduct.py) - Used to clone some product and give it a new Article Number. Usefull when you need to create multiple products with the same data as original one, but only different article number.
- [TerminateSubscriptions.py](TerminateSubscriptions.py) - Terminate some subscription with a specific reason
- [SendInvoices.py](SendInvoices.py) - Send a list of invoices to their customers
- [CreditInvoices.py](CreditInvoices.py) - Credits a batch of invoices specified by id.
- [MassProductSwitch.py](MassProductSwitch.py) - Script to switch products on a list of subscriptions. For example from DN-COM to DN-COM-2.