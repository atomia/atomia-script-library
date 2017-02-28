###
### Script name: Clone product
### Description: Clones a product and makes it available for a reseller.
### Version: 1.0
### Author: Jimmy Bergman
###
### Parameters:
### resellerName - The name of the reseller
###    example: "100000"
### articleNumber - The article number of the product to clone
###    example: "DMN-INFO"
### newArticleNumber - The article number of the new cloned product
###    example: "DMN-INFO-CLONED"

import System.Guid

itemToClone = billingApi.GetItemByArticleNumber(articleNumber)
itemToClone.Id = System.Guid.Empty
itemToClone.ArticleNumber = newArticleNumber
resellerAccount = billingApi.GetAccountByName(resellerName)

clonedItem = billingApi.CreateItem(itemToClone, resellerAccount)

print "Item cloned, go to the relative URL below to edit:"
print "/Products/" + clonedItem.Id.ToString() + "/Edit"