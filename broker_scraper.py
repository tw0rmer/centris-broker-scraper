import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import concurrent.futures
import threading
from colorama import init, Fore, Style
import os
import pathlib
import sys
from time import sleep

# Initialize colorama for colored output
init()

url = "https://www.centris.ca/Broker/GetBrokers"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Get the directory where the script is located
SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()
OUTPUT_DIR = SCRIPT_DIR / 'output'

def ensure_output_dir():
    """Ensure output directory exists"""
    OUTPUT_DIR.mkdir(exist_ok=True)

def print_slow(text, delay=0.03):
    """Print text character by character"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    print()

def show_loading_animation():
    """Show a loading animation"""
    animation = "|/-\\"
    for i in range(20):
        sys.stdout.write(f"\r{Fore.CYAN}Loading... {animation[i % len(animation)]}{Style.RESET_ALL}")
        sys.stdout.flush()
        sleep(0.1)
    print()

def show_startup_animation():
    """Show startup animation with ASCII art and credits"""
    clear_screen()
    
    # ASCII Art for "BROKER SCRAPER"
    ascii_art = f"""{Fore.CYAN}
    ╔══╗ ╔═══╗ ╔══╗ ╔═╗╔═╗ ╔═══╗ ╔═══╗
    ║╔╗║ ║╔═╗║ ║╔╗║ ║║╚╝║║ ║╔══╝ ║╔═╗║
    ║╚╝╚╗║╚═╝║ ║║║║ ║╔╗╔╗║ ║╚══╗ ║╚═╝║
    ║╔═╗║║╔╗╔╝ ║║║║ ║║║║║║ ║╔══╝ ║╔╗╔╝
    ║╚═╝║║║║╚╗ ║╚╝║ ║║║║║║ ║╚══╗ ║║║╚╗
    ╚═══╝╚╝╚═╝ ╚══╝ ╚╝╚╝╚╝ ╚═══╝ ╚╝╚═╝
    {Style.RESET_ALL}"""
    
    print(ascii_art)
    sleep(1)
    
    # Animate "Created by Jason"
    creator_text = f"{Fore.GREEN}Created by {Fore.YELLOW}Jason{Style.RESET_ALL}"
    print_slow(creator_text, 0.05)
    sleep(1)
    
    # Clear the creator text (move cursor up and clear line)
    sys.stdout.write('\033[F')  # Move cursor up
    sys.stdout.write('\033[K')  # Clear line
    sleep(0.5)
    
    # Show loading animation
    show_loading_animation()
    
    # Final preparation message
    print(f"{Fore.GREEN}Initializing scraper...{Style.RESET_ALL}")
    sleep(0.5)
    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear_screen()
    print(f"{Fore.CYAN}====================================")
    print("       Broker Scraper Menu")
    print("===================================={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1) Set broker scrape limit")
    print("2) Start scraping with no limit")
    print("3) Exit{Style.RESET_ALL}")
    
    while True:
        try:
            choice = input(f"\n{Fore.GREEN}Enter your choice (1-3): {Style.RESET_ALL}")
            if choice == "1":
                while True:
                    try:
                        limit = int(input(f"{Fore.GREEN}Enter broker limit (minimum 20): {Style.RESET_ALL}"))
                        if limit >= 20:
                            return limit
                        else:
                            print(f"{Fore.RED}Limit must be at least 20{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
            elif choice == "2":
                return None
            elif choice == "3":
                print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                exit()
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")

def display_time_elapsed(start_time):
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def fetch_brokers(start_position):
    """Fetch broker data starting at specified position"""
    payload = {"startPosition": start_position}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        html_content = json_data['d']['Result']['Html']
        
        # For debugging - save the raw HTML to a file
        if start_position == 0:
            raw_html_path = OUTPUT_DIR / "raw_broker_html.html"
            with open(raw_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"{Fore.GREEN}Raw HTML saved to output/raw_broker_html.html{Style.RESET_ALL}")
            
        soup = BeautifulSoup(html_content, 'html.parser')
        broker_elements = soup.find_all('div', class_='broker-thumbnail-item')
        return start_position, broker_elements
    else:
        print(f"{Fore.RED}Request failed with status code: {response.status_code}{Style.RESET_ALL}")
        return start_position, []

def process_broker(broker, broker_index):
    """Extract broker information from HTML element"""
    # Find the broker-info div which contains most of the data
    broker_info_div = broker.find('div', class_='broker-info')
    
    # Extract name
    name_element = broker.find('h1', class_='broker-info__broker-title')
    name = name_element.text.strip() if name_element else "N/A"

    # Extract job title
    job_title_element = broker.find('div', class_='p1', itemprop='jobTitle')
    job_title = job_title_element.text.strip() if job_title_element else "N/A"

    # Extract phone
    phone_element = broker.find('a', itemprop='telephone')
    phone = phone_element.text.strip() if phone_element and hasattr(phone_element, 'text') else "N/A"
    if phone_element and 'content' in phone_element.attrs:
        phone = phone_element['content']

    # Extract image URL
    img_element = broker.find('img', class_='broker-info-broker-image')
    img_url = img_element['src'] if img_element and 'src' in img_element.attrs else ""

    # Extract website if available
    website = ""
    website_elements = broker.find_all('a', class_='btn')
    for element in website_elements:
        icon = element.find('i', class_='fa-globe')
        if icon and 'href' in element.attrs:
            website = element['href']
            break

    # Extract broker ID from data attribute
    broker_id = ""
    if broker_info_div and 'data-broker-id' in broker_info_div.attrs:
        broker_id = broker_info_div['data-broker-id']

    # Extract profile ID from data attribute
    profile_id = "4ccca8259b5446cf9c67cd2da1c82324"  # Default value from example
    if broker_info_div and 'data-profile-id' in broker_info_div.attrs:
        profile_id = broker_info_div['data-profile-id']
    
    # Extract contact URL
    contact_url = ""
    contact_element = broker.find('a', class_='GTM-contact-broker')
    if contact_element and 'href' in contact_element.attrs:
        contact_path = contact_element['href']
        contact_path = contact_path.replace('/fr/contact-courtier/', '/en/contact-broker/')
        contact_url = f"https://www.centris.ca{contact_path}"
    else:
        if broker_id:
            contact_url = f"https://www.centris.ca/en/contact-broker/{broker_id}"

    return {
        "index": broker_index,
        "name": name,
        "job_title": job_title,
        "phone": phone,
        "img_url": img_url,
        "website": website,
        "broker_id": broker_id,
        "profile_id": profile_id,
        "contact_url": contact_url
    }

def main():
    # Ensure output directory exists
    ensure_output_dir()
    
    # Get broker limit from menu
    broker_limit = display_menu()
    limit_text = f"(Limit: {broker_limit})" if broker_limit else "(No limit)"
    
    start_time = time.time()
    print(f"{Fore.CYAN}Starting broker data collection... {limit_text}{Style.RESET_ALL}")

    html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Broker Scrape Results</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100">
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Broker Scrape Results</h1>
"""

    # Step 1: Discover all available positions
    all_positions = []
    start_position = 0
    empty_count = 0

    # First, discover all the positions with data
    while empty_count < 3:  # Try a few empty results to confirm we're done
        position, broker_elements = fetch_brokers(start_position)
        
        if not broker_elements:
            empty_count += 1
            print(f"{Fore.YELLOW}No brokers found at position {position}{Style.RESET_ALL}")
        else:
            empty_count = 0
            all_positions.append(position)
            elapsed_time = display_time_elapsed(start_time)
            print(f"{Fore.GREEN}Found {len(broker_elements)} brokers at position {position} | Time elapsed: {elapsed_time}{Style.RESET_ALL}")
            
            # Check if we've reached the broker limit during discovery
            total_brokers = len(all_positions) * 20
            if broker_limit and total_brokers >= broker_limit:
                break
        
        start_position += 20

    print(f"{Fore.CYAN}Discovery complete. Found {len(all_positions)} positions with broker data.{Style.RESET_ALL}")

    # Step 2: Process all broker data in parallel
    all_brokers = []
    broker_index = 0
    index_lock = threading.Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all positions for processing
        future_to_position = {executor.submit(fetch_brokers, pos): pos for pos in all_positions}

        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_position):
            position, broker_elements = future.result()
            
            if not broker_elements:
                continue
                
            broker_batch = []
            for broker in broker_elements:
                with index_lock:
                    broker_index += 1
                    current_index = broker_index
                    
                    # Check if we've reached the broker limit
                    if broker_limit and broker_index > broker_limit:
                        break
                    
                    if broker_index % 20 == 0:
                        elapsed_time = display_time_elapsed(start_time)
                        print(f"{Fore.GREEN}Processed {broker_index} brokers | Time elapsed: {elapsed_time}{Style.RESET_ALL}")
                        
                broker_data = process_broker(broker, current_index)
                broker_batch.append(broker_data)
                
            all_brokers.extend(broker_batch)
            
            # Check if we've reached the broker limit
            if broker_limit and len(all_brokers) >= broker_limit:
                all_brokers = all_brokers[:broker_limit]
                break

    # Sort brokers by index to ensure correct order
    all_brokers.sort(key=lambda x: x['index'])
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{Fore.CYAN}Total time elapsed: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total brokers processed: {len(all_brokers)}{Style.RESET_ALL}")

    # Format start and end times
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
    
    html_report += f"""    <p>Total brokers found: {len(all_brokers)}</p>
    
    <p>Start time: {start_time_str}</p>
    <p>End time: {end_time_str}</p>
    <p>Elapsed: {elapsed_time:.2f} seconds</p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
"""

    for broker in all_brokers:
        # Handle empty website URLs
        website_link = ""
        if broker['website']:
            website_link = f"""<a href="{broker['website']}" class="underline" target="_blank">{broker['website']}</a>"""
        
        # Create contact link
        contact_link = ""
        if broker['contact_url']:
            contact_link = f"""<a href="{broker['contact_url']}" class="underline" target="_blank">Contact Broker</a>"""
        
        html_report += f"""
      <div class="bg-gray-800 rounded p-4 shadow-lg">
        <img src="{broker['img_url']}" class="rounded mb-2"/>
        <h2 class="text-xl font-semibold">{broker['name']}</h2>
        <p>Title: {broker['job_title']}</p>
        <p>Phone: {broker['phone']}</p>
        <p>Website: {website_link}</p>
        <p>Broker ID: {broker['broker_id']}</p>
        <p>Profile ID: {broker['profile_id']}</p>
        <p>Contact: {contact_link}</p>
      </div>"""

    html_report += """
    </div>
  </div>
</body>
</html>"""

    report_path = OUTPUT_DIR / "broker_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    
    print(f"{Fore.GREEN}Report saved to output/broker_report.html{Style.RESET_ALL}")

if __name__ == "__main__":
    show_startup_animation()
    main()