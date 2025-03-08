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
- Supports multiple file naming patterns and separators
- Handles multiple page types (like left/right pages) in a single run
- Supports authentication via cookies with detailed extraction guidance
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
3. Save the script to a file (e.g., `book_downloader.py`)

## Usage Instructions

### Basic Usage

Run the script with:
```
python book_downloader.py
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
   - Example: For `gjuzelev_vasil_006.jpg`, the prefix is `gjuzelev_vasil`
   - Example: For `satr_bitie_part2 - 0004.jpg`, the prefix is `satr_bitie_part2`
   - Example: For `document0001.jpg` with no separator, the prefix is `document`

2. **Separator**: The character(s) between the prefix and the page number
   - Example: For `gjuzelev_vasil_006.jpg`, enter `_`
   - Example: For `satr_bitie_part2 - 0004.jpg`, enter ` - ` (space-hyphen-space)
   - Example: For `document0001.jpg`, leave empty (no separator)

3. **Number of digits**: How many digits are used in the page numbering
   - Example: For `006`, enter `3`
   - Example: For `0004`, enter `4`

4. **Suffix**: Any text between the page number and file extension
   - Example: For `hristianska_0012_1L.jpg`, the suffix is `_1L`
   - Example: For `gjuzelev_vasil_006.jpg`, leave empty

5. **Multiple page types**: For books with left/right pages or different image versions
   - You can specify multiple suffixes to download in a single run (e.g., `_1L` and `_2R`)

6. **File extension**: The file format (default is `jpg`)

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

#### How to Extract Fresh Cookies:

**Chrome:**
1. Navigate to the book viewer page (the actual page where you can see the book)
2. Press F12 (or Ctrl+Shift+I) to open Developer Tools
3. Select the "Application" tab
4. In the left sidebar, expand "Cookies" and click on the website domain
5. Look for two specific cookies:
   - `JSESSIONID` - The server session identifier
   - `dspacc` - The authentication token specific to this digital library
6. Copy the value of each cookie (not the name)

**Firefox:**
1. Navigate to the book viewer page
2. Press F12 to open Developer Tools
3. Select the "Storage" tab
4. Click on "Cookies" in the left sidebar
5. Find and note the values for `JSESSIONID` and `dspacc`

**Safari:**
1. First enable Developer Tools: Safari → Preferences → Advanced → "Show Develop menu"
2. Navigate to the book viewer
3. Click Develop → Show Web Inspector
4. Go to the "Storage" tab
5. Under "Cookies", find the two authentication tokens

**Edge:**
1. Navigate to the book viewer page
2. Press F12 to open Developer Tools
3. Select the "Application" tab
4. Expand "Cookies" in the left sidebar and click on the website
5. Find and copy the values for `JSESSIONID` and `dspacc`

## Examples

### Example 1: Downloading "hristianska" book with left/right pages

- Base URL: `http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/29904/`
- Prefix: `hristianska`
- Separator: `_`
- Number of digits: `4`
- Multiple page types: Yes
  - Suffix 1: `_1L` for left pages
  - Suffix 2: `_2R` for right pages
- Starting page: `12`
- Ending page: `100`

### Example 2: Downloading "gjuzelev_vasil" book with sequential pages

- Base URL: `http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/12345/`
- Prefix: `gjuzelev_vasil`
- Separator: `_`
- Number of digits: `3`
- Suffix: (leave empty)
- Starting page: `6`
- Ending page: `-1` (automatic)

### Example 3: Downloading "satr_bitie_part2" book with space-hyphen-space separator

- Base URL: `http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/38305/`
- Prefix: `satr_bitie_part2`
- Separator: ` - ` (space-hyphen-space)
- Number of digits: `4`
- Suffix: (leave empty)
- Starting page: `4`
- Ending page: `-1` (automatic)

### Example 4: Downloading a book with no separator between prefix and number

- Base URL: `http://example.org/books/12345/`
- Prefix: `document`
- Separator: (leave empty)
- Number of digits: `4`
- Suffix: (leave empty)
- Starting page: `1`
- Ending page: `200`

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
