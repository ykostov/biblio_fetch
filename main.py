import requests
import os
import time
import re
from urllib.parse import urljoin
import sys

# ANSI color codes for terminal output (works on most Unix/Mac terminals and Windows 10+)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD} {text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"{Colors.BLUE}{Colors.BOLD}[STEP {step_num}] {text}{Colors.END}")

def print_info(text):
    """Print information text"""
    print(f"{Colors.BLUE}{text}{Colors.END}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}{text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}{Colors.BOLD}WARNING: {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}{Colors.BOLD}ERROR: {text}{Colors.END}")

def download_book_pages(base_url, start_num, end_num,
                       filename_pattern="{prefix}_{num:03d}{suffix}.jpg",
                       prefix="gjuzelev_vasil", suffixes=[""],
                       output_dir="downloaded_pages",
                       jsessionid=None, dspacc=None):
    """
    Download book pages from a website with customizable naming pattern.

    Args:
        base_url (str): Base URL of the website
        start_num (int): Starting page number
        end_num (int): Ending page number
        filename_pattern (str): Pattern for generating filenames
        prefix (str): Prefix of the book filenames
        suffixes (list): List of suffixes to use after the page number (before extension)
        output_dir (str): Directory to save downloaded files
        jsessionid (str): Custom JSESSIONID cookie value
        dspacc (str): Custom dspacc cookie value
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print_info(f"Created output directory: {output_dir}")

    # Create a session to maintain cookies
    session = requests.Session()

    # Set cookies - either custom or default from Wireshark capture
    cookies = {
        'JSESSIONID': jsessionid if jsessionid else 'D810FC33786200A9C5444EA15BB6DC83',
        'dspacc': dspacc if dspacc else 'U1VMOlVMMDQ1NzM3OlNVTFJEUgAAAABnw-b6.Seux4wOrbJ35AfjgtP1a6g'
    }

    # Set exact headers from the successful request
    headers = {
        'Host': 'unilib-dspace.nasledstvo.bg',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    # Update session with cookies and headers
    session.cookies.update(cookies)
    session.headers.update(headers)

    # Counter for successful downloads
    successful_downloads = 0
    failed_downloads = 0
    consecutive_failures = 0

    print_header("DOWNLOAD CONFIGURATION")
    print_info(f"Base URL: {base_url}")
    print_info(f"Page range: {start_num} to {end_num if end_num != 9999 else 'until failures'}")
    print_info(f"Filename pattern: {filename_pattern}")
    print_info(f"Prefix: {prefix}")
    print_info(f"Suffixes: {', '.join(suffixes) if suffixes else '[none]'}")
    print_info(f"Using {'custom' if jsessionid or dspacc else 'default'} authentication cookies")

    # Generate example filenames
    example_filenames = [filename_pattern.format(prefix=prefix, num=start_num, suffix=suffix) for suffix in suffixes]
    print_info(f"Example filenames: {', '.join(example_filenames)}")

    # Test connection before starting batch download
    print_header("TESTING CONNECTION")
    first_suffix = suffixes[0] if suffixes else ""
    test_filename = filename_pattern.format(prefix=prefix, num=start_num, suffix=first_suffix)
    test_url = urljoin(base_url, test_filename)

    try:
        print_info(f"Testing download of: {test_url}")
        response = session.get(test_url, stream=True, timeout=10)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            content_length = int(response.headers.get('Content-Length', 0))

            if 'image' in content_type or content_length > 10000:
                print_success("Test successful! ✓ Authentication is working.")
                print_success(f"Content-Type: {content_type}")
                print_success(f"File size: {content_length} bytes")

                # Save the test file
                test_path = os.path.join(output_dir, test_filename)
                with open(test_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print_success(f"Test file saved to: {test_path}")
            else:
                print_error("Test failed! ✗ Received non-image content.")
                print_error(f"Content-Type: {content_type}")
                print_error(f"File size: {content_length} bytes")

                # Save error content for debugging
                debug_path = os.path.join(output_dir, f"debug_test.html")
                with open(debug_path, 'wb') as f:
                    f.write(response.content)
                print_info(f"Saved error content to: {debug_path}")

                proceed = input(f"\n{Colors.YELLOW}Continue with batch download anyway? (y/n): {Colors.END}").lower() == 'y'
                if not proceed:
                    print_info("Download canceled. Please check authentication and try again.")
                    return
        else:
            print_error(f"Test failed! ✗ HTTP status code: {response.status_code}")
            proceed = input(f"\n{Colors.YELLOW}Continue with batch download anyway? (y/n): {Colors.END}").lower() == 'y'
            if not proceed:
                print_info("Download canceled. Please check authentication and try again.")
                return

    except Exception as e:
        print_error(f"Test connection failed with error: {e}")
        proceed = input(f"\n{Colors.YELLOW}Continue with batch download anyway? (y/n): {Colors.END}").lower() == 'y'
        if not proceed:
            print_info("Download canceled. Please check your network connection and try again.")
            return

    # Begin batch download
    print_header("STARTING BATCH DOWNLOAD")
    start_time = time.time()

    # Download files
    for num in range(start_num, end_num + 1):
        # Reset consecutive failures for each new page number
        page_failures = 0

        # Try each suffix for this page number
        for suffix in suffixes:
            # Format the filename according to the pattern
            filename = filename_pattern.format(prefix=prefix, num=num, suffix=suffix)
            file_url = urljoin(base_url, filename)

            output_path = os.path.join(output_dir, filename)

            try:
                print_info(f"Downloading: {filename}")
                response = session.get(file_url, stream=True, timeout=10)

                # Check if the request was successful
                if response.status_code == 200:
                    # Check content type
                    content_type = response.headers.get('Content-Type', '')
                    content_length = int(response.headers.get('Content-Length', 0))

                    # Check if it's an image or HTML
                    if 'text/html' in content_type or content_length < 5000:
                        print_warning(f"Received possible error page ({content_length} bytes, type: {content_type})")
                        # Save the HTML for debugging
                        debug_path = os.path.join(output_dir, f"debug_{num:03d}{suffix}.html")
                        with open(debug_path, 'wb') as f:
                            f.write(response.content)
                        failed_downloads += 1
                        page_failures += 1
                        continue

                    # Save the file
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print_success(f"✓ Downloaded: {filename} ({content_length} bytes)")
                    successful_downloads += 1
                    consecutive_failures = 0

                    # Add a small delay to avoid overwhelming the server
                    time.sleep(0.5)
                else:
                    print_error(f"✗ Failed to download {filename}: HTTP status code {response.status_code}")
                    failed_downloads += 1
                    page_failures += 1

            except Exception as e:
                print_error(f"✗ Error downloading {filename}: {e}")
                failed_downloads += 1
                page_failures += 1

        # If all suffixes for this page failed, increment consecutive failures counter
        if page_failures == len(suffixes):
            consecutive_failures += 1
            print_warning(f"All variations of page {num} failed. Consecutive page failures: {consecutive_failures}")

            # If we've had too many consecutive page failures, break out of the loop
            if consecutive_failures > 5:
                print_warning("Multiple consecutive page failures, stopping download...")
                break
        else:
            # Reset consecutive failures if at least one suffix succeeded
            consecutive_failures = 0

        # Show progress every 10 pages
        if num % 10 == 0 and num > start_num:
            elapsed_time = time.time() - start_time
            pages_per_minute = ((num - start_num) / elapsed_time) * 60
            print_info(f"Progress: Processed {num - start_num + 1} pages ({pages_per_minute:.1f} pages/min)")

    # Calculate total time
    total_time = time.time() - start_time
    minutes, seconds = divmod(total_time, 60)

    print_header("DOWNLOAD COMPLETE")
    print_success(f"Successfully downloaded: {successful_downloads} files")
    print_info(f"Failed downloads: {failed_downloads}")
    print_info(f"Time taken: {int(minutes)} minutes, {int(seconds)} seconds")
    print_info(f"Files saved to: {os.path.abspath(output_dir)}")

    # Check if we had successful downloads
    if successful_downloads == 0:
        print_header("TROUBLESHOOTING SUGGESTIONS")
        print_info("1. The authentication cookies might have expired.")
        print_info("2. Follow these steps to get fresh cookies:")
        print_info("   - Open your browser and navigate to the book viewer")
        print_info("   - Press F12 to open Developer Tools")
        print_info("   - Go to Application tab (Chrome) or Storage tab (Firefox)")
        print_info("   - Select Cookies from the left sidebar")
        print_info("   - Find and copy the values for JSESSIONID and dspacc cookies")
        print_info("   - Run this script again with the 'Use custom cookies' option")


def show_intro():
    """Display introduction and instructions"""
    print_header("BOOK PAGE DOWNLOADER")
    print_info("This script helps you download book pages from a digital library.")
    print_info("It works by accessing image files that follow a predictable naming pattern.")
    print_info("\nThe script requires authentication cookies to access protected content.")
    print_info("Default cookies are provided, but you may need to supply fresh ones.")

    print_header("REQUIRED INFORMATION")
    print_info("You will need to provide:")
    print_info("1. Base URL - The URL path to where the book images are stored")
    print_info("2. Filename pattern - How the image files are named")
    print_info("3. Page number range - The starting and ending page numbers to download")
    print_info("4. Authentication cookies - If the defaults don't work")


def get_user_input():
    """Get all required parameters from the user"""
    print_step(1, "ENTER BASE URL")
    print_info("This is the URL path where the book images are stored.")
    print_info("Example: http://unilib-dspace.nasledstvo.bg/xmlui/bitstream/handle/nls/29904/")
    base_url = input("> Base URL: ").strip()
    while not base_url.startswith("http"):
        print_warning("URL must start with http:// or https://")
        base_url = input("> Base URL: ").strip()

    # Make sure URL ends with /
    if not base_url.endswith('/'):
        base_url += '/'

    print_step(2, "CONFIGURE FILENAME PATTERN")
    print_info("Define how the book's image files are named.")

    # Get prefix
    print_info("First, enter the PREFIX (the part before the page number)")
    print_info("Example 1: For 'gjuzelev_vasil_006.jpg', the prefix is 'gjuzelev_vasil'")
    print_info("Example 2: For 'satr_bitie_part2 - 0004.jpg', the prefix is 'satr_bitie_part2'")
    print_info("Example 3: For 'document0001.jpg' with no separator, the prefix is 'document'")
    prefix = input("> Prefix: ").strip()

    # Get separator
    print_info("\nWhat separator is used between the prefix and page number? (leave empty for no separator)")
    print_info("Example 1: For 'gjuzelev_vasil_006.jpg', enter '_'")
    print_info("Example 2: For 'satr_bitie_part2 - 0004.jpg', enter ' - '")
    print_info("Example 3: For 'prefix0001.jpg', leave empty")
    separator = input("> Separator (default: '_'): ")

    # Handle the empty separator case
    if separator.strip() == "":
        print_info("You've selected no separator - the number will immediately follow the prefix.")
        separator = ""
    else:
        separator = separator.strip() or "_"

    # Get number format
    print_info("\nHow many digits are used for page numbers?")
    print_info("Example 1: If pages are numbered like '001', '002', etc., enter '3'")
    print_info("Example 2: If pages are numbered like '0004', '0005', etc., enter '4'")
    try:
        num_digits = int(input("> Number of digits (default: 3): ").strip() or "3")
    except ValueError:
        print_warning("Invalid input, using default: 3")
        num_digits = 3

    # Get suffix options
    print_info("\nDoes this book have multiple page types (like left/right pages)?")
    has_multiple_types = input("> Multiple page types? (y/n, default: n): ").lower() == "y"

    suffixes = []
    if has_multiple_types:
        print_info("\nEnter the SUFFIXES for different page types. Examples:")
        print_info("- For left/right pages: '_1L' and '_2R'")
        print_info("- For different image versions: '_color' and '_bw'")
        print_info("Enter one suffix per line. When finished, enter a blank line.")

        while True:
            suffix = input("> Enter suffix: ").strip()
            if not suffix:
                break
            suffixes.append(suffix)

        if not suffixes:
            print_warning("No suffixes entered, using empty suffix")
            suffixes = [""]
    else:
        print_info("\nEnter any SUFFIX between the number and the file extension (if any)")
        print_info("Example: For 'gjuzelev_vasil_006_scan.jpg', the suffix is '_scan'")
        print_info("         For 'gjuzelev_vasil_006.jpg', leave empty")
        suffix = input("> Suffix (or leave empty for none): ").strip()
        suffixes = [suffix]

    # Get file extension
    print_info("\nWhat file extension do the images have?")
    extension = input("> File extension (default: jpg): ").strip() or "jpg"
    if not extension.startswith('.'):
        extension = '.' + extension

    # Create the filename pattern
    filename_pattern = f"{{prefix}}{separator}{{num:0{num_digits}d}}{{suffix}}{extension}"
    print_info(f"\nGenerated filename pattern: {filename_pattern}")

    # Show example for each suffix
    for suffix in suffixes:
        example = filename_pattern.format(prefix=prefix, num=1, suffix=suffix)
        print_info(f"Example filename: {example}")

    # Confirm pattern
    confirm = input("> Is this pattern correct? (y/n, default: y): ").lower() != "n"
    if not confirm:
        print_info("Please restart the script and try again with a different pattern.")
        sys.exit(0)

    print_step(3, "ENTER PAGE RANGE")
    print_info("Specify the starting and ending page numbers.")

    while True:
        try:
            start_input = input("> Starting page number: ").strip()
            start_num = int(start_input)
            break
        except ValueError:
            print_warning("Please enter a valid number")

    while True:
        try:
            end_input = input("> Ending page number (or -1 for automatic): ").strip()
            end_num = int(end_input)
            break
        except ValueError:
            print_warning("Please enter a valid number")

    # If end_num is -1, use a very large number and let the script stop on failures
    if end_num == -1:
        end_num = 9999

    print_step(4, "SET OUTPUT DIRECTORY")
    print_info("This is where the downloaded files will be saved.")
    output_dir = input("> Output directory (default: downloaded_pages): ").strip() or "downloaded_pages"

    print_step(5, "AUTHENTICATION SETTINGS")
    print_info("The script needs authentication cookies to access protected content.")
    print_info("Default cookies are provided, but they may have expired.")
    print_info("If the download fails, you'll need to provide fresh cookies.")
    use_custom_cookies = input("> Do you want to use custom cookies? (y/n, default: n): ").lower() == "y"

    jsessionid = None
    dspacc = None

    if use_custom_cookies:
        print_info("\nTo find these cookies:")
        print_info("1. Open your browser and go to the book viewer page")
        print_info("2. Press F12 to open Developer Tools")
        print_info("3. Go to Application tab (Chrome) or Storage tab (Firefox)")
        print_info("4. Select Cookies from the left sidebar")
        print_info("5. Find the values for JSESSIONID and dspacc\n")

        jsessionid = input("> Enter JSESSIONID cookie value: ").strip()
        dspacc = input("> Enter dspacc cookie value: ").strip()

    return base_url, prefix, suffixes, start_num, end_num, filename_pattern, output_dir, jsessionid, dspacc


if __name__ == "__main__":
    # Check for color support
    if sys.platform == "win32":
        os.system('color')

    # Show introduction
    show_intro()

    # Get user inputs
    base_url, prefix, suffixes, start_num, end_num, filename_pattern, output_dir, jsessionid, dspacc = get_user_input()

    # Download the book pages
    download_book_pages(base_url, start_num, end_num, filename_pattern, prefix, suffixes, output_dir, jsessionid, dspacc)
