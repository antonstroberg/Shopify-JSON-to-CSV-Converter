# fetchConvert
This Python script fetches product data from a Shopify store via the /products.json endpoint and converts it into one or more CSV files suitable for Shopify import. The script fetches all available pages from a specified domain and splits the CSV output into manageable chunks, ensuring each file stays within the 15MB limit required by Shopify.


**Features**

* Fetches product data from Shopify using the JSON API.
* Automatically detects how many pages of product data are available.
* Splits the resulting data into multiple CSV files if necessary to avoid file size limits (customizable via product count).
* Includes product details like Title, Body, Vendor, Product Type, Tags, Price, SKU, and Image URL.
* CSV filenames include the store's domain and are numbered for easy identification.

**Requirements**
* Python 3.x
* The following Python libraries are required (which can be installed using pip):

`pip install requests`

**Usage**
* Download fetchConverter.py 
* run the script

`python3 fetchConvert.py`

* Input the domain for Shopify site - example storedomain.com 

**Output**
* The script will generate CSV files in the current directory.
* If necessary, it will split the CSV files into smaller parts (e.g., shopify_inventory_storedomain_com_part_1.csv, shopify_inventory_storedomain_com_part_2.csv, etc.).
* Each file will contain a maximum of 1000 products by default (you can adjust this in the script).
