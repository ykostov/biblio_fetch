# Book Page Downloader

## IMPORTANT LEGAL DISCLAIMER

**This tool must only be used to download content for which you have explicit permission from the copyright holder or website owner.** Unauthorized downloading of copyrighted materials may constitute copyright infringement and could result in legal action. The author of this script accepts no responsibility for any misuse of this tool.

**By using this tool, you confirm that:**
1. You have been granted explicit permission to download the materials
2. You are authorized to access the content on the website
3. Your use complies with the website's terms of service
4. You will not distribute or use the downloaded content in any unauthorized manner

If you do not meet ALL of these conditions, you must not use this tool.

## Overview

This script helps you download book pages from a digital library when you have proper authorization. It works by accessing image files that follow a predictable naming pattern and requires proper authentication credentials to access protected content.

## Features

- Downloads book pages in sequence from a digital repository
- Works with any file naming pattern
- Supports authentication via cookies
- Tests connection before starting batch download
- Provides real-time progress tracking
- Color-coded interface for better readability
- Detailed troubleshooting assistance

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Ensure you have Python installed on your system
2. Install the required library:
   ```
   pip install requests
   ```

## Usage Instructions

### Basic Usage

Run the script with:
```
python3 main.py
```

The script will guide you through the setup process with clear step-by-step instructions.

### Step 1: Enter Base URL

This is the URL path where the book images are stored. It should end with a forward slash (`/`).

Example:
```
http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/29904/
```

### Step 2: Configure Filename Pattern

The script will help you build the correct filename pattern by asking for:

1. **Prefix**: The part of the filename that comes before the page number
   - Example: For `hristianska_0012_1L.jpg`, the prefix is `hristianska`
   - Example: For `gjuzelev_vasil_006.jpg`, the prefix is `gjuzelev_vasil`

2. **Number of digits**: How many digits are used in the page numbering
   - Example: For `006`, enter `3`
   - Example: For `0012`, enter `4`

3. **Suffix**: Any text between the page number and file extension
   - Example: For `hristianska_0012_1L.jpg`, the suffix is `_1L`
   - Example: For `gjuzelev_vasil_006.jpg`, leave empty

4. **File extension**: The file format (default is `jpg`)

### Step 3: Enter Page Range

Specify:
- **Starting page number**: The first page to download
- **Ending page number**: The last page to download (or enter `-1` to continue until failures)

### Step 4: Set Output Directory

Specify where downloaded files should be saved (default: `downloaded_pages`)

### Step 5: Authentication Settings

The script may need authentication cookies to access protected content:

- Default cookies are provided but may not work for all books
- If download fails, you'll need to provide fresh cookies from your browser

#### How to Get Fresh Cookies:

1. Open your browser and navigate to the book viewer page
2. Press F12 to open Developer Tools
3. Go to Application tab (Chrome) or Storage tab (Firefox)
4. Select Cookies from the left sidebar
5. Find and copy the values for `JSESSIONID` and `dspacc`

## Examples

### Example 1: Downloading "hristianska" book with left/right pages

- Base URL: `http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/29904/`
- Prefix: `hristianska`
- Number of digits: `4`
- Suffix: `_1L` for left pages, `_2R` for right pages
- Starting page: `12`
- Ending page: `100`

### Example 2: Downloading "gjuzelev_vasil" book with sequential pages

- Base URL: `http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/12345/`
- Prefix: `gjuzelev_vasil`
- Number of digits: `3`
- Suffix: (leave empty)
- Starting page: `6`
- Ending page: `-1` (automatic)

## Troubleshooting

If downloads fail, try:

1. **Check authentication**: Your cookies may have expired. Get fresh ones as described above.
2. **Verify URL**: Make sure the base URL is correct and includes the full path up to the filenames.
3. **Check filename pattern**: Examine a working URL in your browser and verify your pattern.
4. **Network issues**: Check your internet connection and try again.
5. **Server restrictions**: The server may limit download rates. Try increasing the delay between downloads.

## Legal and Ethical Use

This tool is intended for legitimate research and archival purposes where proper authorization has been obtained. Always:

1. Respect copyright laws and intellectual property rights
2. Obtain necessary permissions before downloading content
3. Follow the website's terms of service
4. Use downloaded materials only for authorized purposes

## License

This script is provided for educational purposes. Use responsibly.
