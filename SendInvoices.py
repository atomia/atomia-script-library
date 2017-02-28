###
### Script name: Send invoices
### Description: Sends a batch of invoices specified by id.
### Version: 1.1
### Author: Jimmy Bergman
###
### Parameters:
### invoice_ids - Array of invoice ID:s to send
###    example: [ "5332eba0-f6aa-4b57-a340-9c141f9d252f", "0a019a00-6c62-49f7-a251-d04829beaff8" ]

import System

billingApi.SendInvoices(System.Array[System.Guid](map(System.Guid,invoice_ids)), None)

print str(len(invoice_ids)) + " invoices sent"