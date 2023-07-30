# Daraz Product Web Scraper

This web scraper was created in connection to an assignment in the course AIC557 at Kathmandu University. The scraper reads product price history from the web store Daraz. It is currently limited to read prices from products under "Mens fashion".

## Technologies
**Scrapy** is used as the library for scraping information and navigating between relevant pages. In addition to this, **Playwright** is used to render the pages before reading information. This was required due to Daraz's reliability on javascript rendering for information, which resultet in information not beging revieled to Scrapy.

## Data
The scraped data can be found in [products.csv](./products.csv]), the data schame is as follows:
```js
{
  "datetime" : DateTime,
  "sku" : String
  "name" : String,
  "brand" : String,
  "price" : Number,
  "categories" : String[]
}
```
Each enterence is specifed with a datetime of when the enterence occured. Every product is uniquly identified by its SKU. Prices are specified in NPR.

## Pipeline
The scraper does the following:
1. Load a product result page
2. Read all product result cards for product link
3. Enter all product links and fetch the information by CSS-Classes
4. Repeat step 1 with the next product result page, until no more product result pages exist.

All product prices are appended to [products.csv](./products.csv]).

This pipeline is automatically triggered by GitHub actions every 12 hours, which then adds new entries to [products.csv](./products.csv]).
