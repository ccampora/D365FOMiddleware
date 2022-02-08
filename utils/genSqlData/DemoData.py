import json
import logging
import random
import os
import uuid
from CreateSchemas import CreateSchemas

import sys
sys.path.append('../modules')
from d365fo import D365FOConnection

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# REPLACE HERE
D365FOENV_URL = "<D365FO URL without trailing slash>"
CLIENT_APP_ID = "Client App Id"
SECRET = "Client App Secret"


COMPANY = "USMF"
URLS = {
    "MetadataEntities": f'{D365FOENV_URL}/Metadata/DataEntities',
    "CustomersV2": f"{D365FOENV_URL}/data/CustomersV2?$format=json&cross-company=true&$select=CustomerAccount,dataAreaId&$filter=dataAreaId eq '{COMPANY}'",
    "CustomerPaymentMethods": f"{D365FOENV_URL}/data/CustomerPaymentMethods?$format=json&cross-company=true&$select=Name&$filter=dataAreaId eq '{COMPANY}'",
    "ReleasedProductsV2": f"{D365FOENV_URL}/data/ReleasedProductsV2?$format=json&cross-company=true&$select=ItemNumber&$filter=dataAreaId eq '{COMPANY}'"
}

def pretty_json(ugly_json):
    return json.dumps(ugly_json, indent=2)

# Print Collection

conn = D365FOConnection()
conn.client_id = CLIENT_APP_ID
conn.client_id_secret = SECRET
conn.d365fo_url = D365FOENV_URL

if conn.try_connection() is False:
    logging.debug("Connection Unsucessful :(")
else:
    logging.debug("Connection Sucessful")

    ## PRODUCE SALES ORDERS HEADER DATA
    # Get CustomerV2 data
    CustomersV2 = conn.get_d365fo_from_url(URLS["CustomersV2"])
    # Get CustomerPaymentmethods
    CustomerPaymentMethods = conn.get_d365fo_from_url(URLS["CustomerPaymentMethods"])
    # Get ReleasedProductsV2
    ReleasedProductsV2 = conn.get_d365fo_from_url(URLS["ReleasedProductsV2"])

    # Create a random price list for each product
    ReleasedProductsV2PriceList = {}
    for p in ReleasedProductsV2:
        unitPrice =  round(random.random() * random.randrange(1, 10), 2)
        ReleasedProductsV2PriceList[p["ItemNumber"]] = unitPrice
        

    logging.debug(pretty_json(ReleasedProductsV2PriceList))

    # For each customer create a random number of sales order headers
    salesOrders = []
    for c in CustomersV2: 
        for s in range(0, random.randint(0, 20)):
            salesOrderLines = []
            for l in range(0, random.randint(2,100)):
                ItemNumber = random.choice(ReleasedProductsV2)["ItemNumber"]
                line = {
                    "ItemNumber": ItemNumber,
                    "SoldQuantity": random.randint(1, 100),
                    "PricePerUnit": ReleasedProductsV2PriceList.get(ItemNumber),
                    "Linenum": l + 1,
                }
                salesOrderLines.append(line.copy())
            
            salesOrder = {
                "ExternalSalesId": random.randint(100000,200000),
                "CustomerAccount": c["CustomerAccount"],
                "PaymentMethod": random.choice(CustomerPaymentMethods)["Name"],
                "Company": COMPANY,
                "Lines": salesOrderLines.copy()
            }
            salesOrders.append(salesOrder.copy())

    source_batch_identifier = uuid.uuid4()
    sql = CreateSchemas()
    sqltext = sql.get_create_table_sentences()

    for h in salesOrders:
        sql.add_sql_sentence_sales_order_header(h, source_identifier=source_batch_identifier)
        for l in salesOrder["Lines"]:
            l["ExternalSalesId"] = h["ExternalSalesId"]
            sql.add_sql_sentences_sales_order_lines(l, source_identifier=source_batch_identifier)

    sqltext = sqltext + '\n'
    sqltext = sqltext + sql.get_sentences()

    with open("output.sql", "w") as outfile:
        outfile.write(sqltext)


    
    
