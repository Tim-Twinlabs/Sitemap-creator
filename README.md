
# Sitemap Generator

This is a Python script that generates a `sitemap.xml` file for a given website by crawling its pages. It only includes pages that belong to the specified domain and excludes external links.

## Features

- **Domain-Specific Crawling**: Ensures only URLs within the starting domain are included in the sitemap.
- **Proper URL Encoding**: Handles spaces and special characters in URLs.
- **Error Handling**: Skips non-HTML content and logs errors for inaccessible pages.
- **User-Agent Simulation**: Mimics browser behavior to bypass bot detection.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `beautifulsoup4`
  - `lxml`

Install the required libraries using pip:
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

1. Save the script to a file, e.g., `generate_sitemap.py`.
2. Run the script:
   ```bash
   python generate_sitemap.py
   ```
3. Enter the starting URL when prompted.
4. The script will crawl the website and generate a `sitemap.xml` file in the same directory.

## Example

If the starting URL is:
```
http://example.com
```

The script will crawl all pages under `example.com` and save a `sitemap.xml` file that looks like this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://example.com/</loc>
  </url>
  <url>
    <loc>http://example.com/page1</loc>
  </url>
</urlset>
```

## Notes

- **Exclusions**:
  - The script excludes external links.
  - Pages with non-standard URL patterns can be ignored by adding additional filtering logic.

- **Customizing the Script**:
  - You can update the `headers` in the `get_links` function to mimic specific browser behavior.

## Limitations

- The script does not handle JavaScript-generated links.
- Very large websites may take time to process.

## Contributing

If you'd like to contribute or suggest improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
