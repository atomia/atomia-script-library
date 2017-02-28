###
### Script name: Send invoices
### Description: Sends a batch of invoices specified by id.
### Version: 1.0
### Author: Jimmy Bergman
###
### Parameters:
### invoice_ids - Array of invoice ID:s to send
###    example: [System.Guid("5332eba0-b55d-44a4-a94a-a960a4f25d04"), System.Guid("0a019a00-562a-4ae4-acff-6a1607021255")]

import System

invoice_ids = [System.Guid("5332eba0-b55d-44a4-a94a-a960a4f25d04"), System.Guid("0a019a00-562a-4ae4-acff-6a1607021255")]

billingApi.SendInvoices(System.Array[System.Guid](invoice_ids), None)

print str(len(invoice_ids)) + " invoices sent"