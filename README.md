# fetchConvert
This Python script fetches product data from a Shopify store via the /products.json endpoint and converts it into one or more CSV files suitable for Shopify import. The script fetches all available pages from a specified domain and splits the CSV output into manageable chunks, ensuring each file stays within the 15MB limit required by Shopify.
