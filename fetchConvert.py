import requests
import csv
import re
import math

# Define the columns you want in the Shopify CSV
csv_columns = ['Title', 'Body', 'Vendor', 'Product Type', 'Tags', 'Price', 'SKU', 'Image Src']
PRODUCTS_PER_FILE = 1000  # Adjust this number based on your requirements

def fetch_json_data(domain, page):
    """Fetch JSON data from the specified domain and page number."""
    url = f"https://{domain}/products.json?limit=250&page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('products', [])  # Return the products list, which could be empty
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None  # Return None on failure

def process_products(products):
    """Process product data and extract relevant fields for the CSV."""
    processed_data = []
    
    for product in products:
        title = product.get('title', '')
        body = product.get('body_html', '')
        vendor = product.get('vendor', '')
        product_type = product.get('product_type', '')
        tags = ', '.join(product.get('tags', []))  # Joining tags into a comma-separated string
        
        # Get the first variant (for price and SKU)
        first_variant = product['variants'][0] if product.get('variants') else {}
        price = first_variant.get('price', '')
        sku = first_variant.get('sku', '')
        
        # Get the first image
        first_image = product['images'][0]['src'] if product.get('images') else ''
        
        # Append the data to be processed
        processed_data.append({
            'Title': title,
            'Body': body,
            'Vendor': vendor,
            'Product Type': product_type,
            'Tags': tags,
            'Price': price,
            'SKU': sku,
            'Image Src': first_image
        })
    
    return processed_data

def save_to_csv(domain, all_products):
    """Save product data to CSV files with a limit on the number of products per file."""
    total_products = len(all_products)
    safe_domain = re.sub(r'\W+', '_', domain)  # Sanitize the domain name for file naming
    
    # Calculate the number of files needed
    num_files = math.ceil(total_products / PRODUCTS_PER_FILE)
    
    for i in range(num_files):
        # Get the products for the current file
        start_index = i * PRODUCTS_PER_FILE
        end_index = start_index + PRODUCTS_PER_FILE
        chunk = all_products[start_index:end_index]

        # Create a filename for this chunk
        output_csv = f'shopify_inventory_{safe_domain}_part_{i+1}.csv'

        # Write chunk to CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(chunk)
        
        print(f"Data saved to {output_csv} ({len(chunk)} products)")

def shopify_to_csv(domain):
    """Fetch data from all pages of the given Shopify domain and save to multiple CSV files."""
    all_products = []
    page = 1

    # Continue fetching until an empty 'products' list is hit
    while True:
        products = fetch_json_data(domain, page)
        
        # Check if the 'products' list is empty or None
        if products is None:
            break  # Stop on a failure to fetch data
        elif not products:  # Stop when 'products' is empty
            print(f"No more products found on page {page}. Stopping...")
            break

        print(f"Fetched {len(products)} products from page {page}")
        all_products.extend(process_products(products))
        page += 1

    # Save all products to multiple CSV files if necessary
    save_to_csv(domain, all_products)

# Get domain from user
domain = input("Enter the Shopify store domain (e.g., toysrus.com): ")

# Run the script
shopify_to_csv(domain)
