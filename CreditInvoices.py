###
### Script name: Credit invoices
### Description: Credits a batch of invoices specified by id.
### Version: 1.0
### Author: Goran Stefanovic
###
### Parameters:
### invoiceIds - Array of invoice ID's to credit
###    example: [ "5332eba0-f6aa-4b57-a340-9c141f9d252f", "0a019a00-6c62-49f7-a251-d04829beaff8" ]

import System

rn = 0

for id in invoiceIds:

    gid = System.Guid(id)
    rn += 1
    print("%04d - Crediting invoice with id: %s" %(rn,id)),

    try:
        invoice = billingApi.GetInvoiceById(gid)
        status = invoice.Status
        if str(status) != "Sent":
            print(" -- Skipped because status is %s" % status)
            continue

        creditedInvoice = billingApi.CreateCreditedInvoiceFromInvoice(gid)

        if (creditedInvoice is None):
            print(" -- Skipped because creditedInvoice is None")
            continue

        if (creditedInvoice.InvoiceLines != None and len(creditedInvoice.InvoiceLines) != 0):
            for invoiceLine in creditedInvoice.InvoiceLines:
                invoiceLine.Credit = invoiceLine.Quantity * (invoiceLine.Price - invoiceLine.Discount)

        invoice = billingApi.CalculateCreditedInvoiceTotals(creditedInvoice)

        createdCredInvoice = billingApi.CreateCreditedInvoice(invoice, False)

        print(" -- Done created credited invoice with id %s" % createdCredInvoice.Id)

    except Exception as e:
        print(" -- Failed with exception: %s" % e)

print "-------------"
print "Script Finished"