#!/usr/bin/env python3
import requests
import random
import time
import argparse
import sys
import traceback
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Configure logging to console and file
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ebay_viewer.log')
    ]
)
logger = logging.getLogger('ebay_viewer')

# List of common user agents to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
]

# Screen resolutions for browser fingerprinting
SCREEN_RESOLUTIONS = [
    '1920x1080', '1366x768', '1440x900', '1536x864', '2560x1440', '1280x720',
    '1600x900', '1024x768', '1680x1050', '2560x1600', '1280x800', '1920x1200'
]

# Color depths for browser fingerprinting
COLOR_DEPTHS = [24, 32, 16]

# Platforms for browser fingerprinting
PLATFORMS = ['Win32', 'MacIntel', 'Linux x86_64', 'iPhone', 'iPad']

# Referrers for simulating traffic sources
REFERRERS = [
    'https://www.google.com/search?q=ebay+items',
    'https://www.google.com/search?q=buy+online',
    'https://www.bing.com/search?q=ebay+products',
    'https://www.ebay.com/sch/i.html?_nkw=items',
    'https://www.ebay.com/b/Collectibles/1/bn_1858810',
    'https://www.reddit.com/r/flipping/',
    'https://duckduckgo.com/?q=ebay',
    'https://www.facebook.com/',
    'https://www.instagram.com/',
    'https://twitter.com/',
]

# Proxy format: "http://user:pass@ip:port" or "http://ip:port"
PROXIES = []  # Add your proxies here if you have them

def validate_ebay_url(url):
    """Validate if the provided URL is a valid eBay listing URL."""
    parsed_url = urlparse(url)
    
    # Check if the domain is ebay
    if not any(ebay_domain in parsed_url.netloc for ebay_domain in ['ebay.com', 'ebay.ca', 'ebay.co.uk', 'ebay.de', 'ebay.fr', 'ebay.it', 'ebay.es', 'ebay.com.au']):
        return False
    
    # Check if the URL contains 'itm' which is common in eBay item listings
    if '/itm/' not in parsed_url.path:
        return False
    
    return True

def get_random_proxy():
    """Get a random proxy from the list."""
    if not PROXIES:
        return None
    return random.choice(PROXIES)

def get_random_user_agent():
    """Get a random user agent from the list."""
    return random.choice(USER_AGENTS)

def get_random_fingerprint():
    """Generate random browser fingerprint data."""
    return {
        'screen_resolution': random.choice(SCREEN_RESOLUTIONS),
        'color_depth': random.choice(COLOR_DEPTHS),
        'platform': random.choice(PLATFORMS),
        'timezone_offset': random.randint(-12, 12) * 60,
    }

def generate_session_id():
    """Generate a random eBay session ID with high entropy."""
    timestamp = int(time.time() * 1000)
    random_component = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=24))
    return f"{timestamp}_{random_component}"

def view_listing(url, session_id=None, use_proxies=False):
    """
    View an eBay listing with a specific session ID.
    Returns True if successful, False otherwise.
    """
    if session_id is None:
        session_id = generate_session_id()
        
    fingerprint = get_random_fingerprint()
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': random.choice(REFERRERS),
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Cache-Control': 'max-age=0',
    }
    
    # Random viewport size based on the screen resolution
    resolution = fingerprint['screen_resolution'].split('x')
    viewport_width = int(int(resolution[0]) * random.uniform(0.7, 1.0))
    viewport_height = int(int(resolution[1]) * random.uniform(0.7, 1.0))
    
    cookies = {
        'ebay': f'ci={session_id}',
        'dp1': f'bpbf/{session_id}^',
        'nonsession': f'{random.randint(10000000, 99999999)}',
        's': f'{random.randint(10000000, 99999999)}',
        'ds2': f'envid={random.randint(0, 9999)}',
        'cid': f'{random.randint(1000000000, 9999999999)}',
        'cssg': f'{random.randint(1000000000, 9999999999)}',
        'ns1': f'{random.randint(10000, 99999)}',
    }
    
    proxy_config = None
    if use_proxies:
        proxy = get_random_proxy()
        if proxy:
            proxy_config = {
                'http': proxy,
                'https': proxy
            }
    
    try:
        with requests.Session() as session:
            # First, make a request to a different eBay page to simulate natural browsing
            referer_url = random.choice([
                'https://www.ebay.com/sch/i.html',
                'https://www.ebay.com/b/Collectibles/1/bn_1858810',
                'https://www.ebay.com/deal/daily',
                'https://www.ebay.com/help/home'
            ])
            
            try:
                session.get(referer_url, headers=headers, cookies=cookies, proxies=proxy_config, timeout=15)
            except Exception:
                # If referer request fails, continue anyway
                pass
            
            # Then visit the actual item page
            start_time = time.time()
            response = session.get(url, headers=headers, cookies=cookies, proxies=proxy_config, timeout=20)
            
            # Simulate user viewing time (between 10-60 seconds)
            view_time = random.uniform(10, 60)
            elapsed = time.time() - start_time
            if elapsed < view_time:
                remaining_time = view_time - elapsed
                # Only wait a portion of the time to speed up the bot
                time.sleep(min(remaining_time * 0.2, 5))
            
            if response.status_code == 200:
                logger.info(f"[+] Successfully viewed listing with session {session_id[:8]}... - Status: {response.status_code}")
                return True
            else:
                logger.warning(f"[-] Failed to view listing with session {session_id[:8]}... - Status: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"[-] Error viewing listing with session {session_id[:8]}...: {str(e)}")
        return False

def add_view(url, use_proxies=False):
    """Add a view to the eBay listing."""
    session_id = generate_session_id()
    return view_listing(url, session_id, use_proxies)

def add_views(url, count, max_workers=1, use_proxies=False, delay_min=2, delay_max=5, callback=None):
    """
    Add multiple views to an eBay listing.
    
    Args:
        url: eBay listing URL
        count: Number of views to add
        max_workers: Maximum number of concurrent workers
        use_proxies: Whether to use proxies
        delay_min: Minimum delay between views in seconds
        delay_max: Maximum delay between views in seconds
        callback: Callback function to report progress
    """
    successful_views = 0
    
    logger.info(f"[*] Starting eBay view bot for: {url}")
    logger.info(f"[*] Target: {count} views")
    logger.info(f"[*] Using proxies: {'Yes' if use_proxies else 'No'}")
    logger.info(f"[*] Maximum concurrent workers: {max_workers}")
    logger.info(f"[*] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("-" * 60)
    
    if callback:
        callback(0, count)
    
    if max_workers > 1:
        # Multithreaded approach
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for i in range(count):
                future = executor.submit(add_view, url, use_proxies)
                futures.append(future)
                # Add delay between spawning threads
                time.sleep(random.uniform(delay_min / max_workers, delay_max / max_workers))
                
                # Update progress
                if callback and (i + 1) % 5 == 0:
                    completed = sum(1 for f in futures if f.done())
                    callback(completed, count)
            
            # Wait for all futures to complete
            for i, future in enumerate(futures):
                try:
                    if future.result():
                        successful_views += 1
                except Exception as e:
                    logger.error(f"Error in thread: {str(e)}")
                
                # Update progress
                if callback and (i + 1) % 5 == 0:
                    callback(i + 1, count)
    else:
        # Sequential approach
        for i in range(count):
            success = add_view(url, use_proxies)
            if success:
                successful_views += 1
            
            # Update progress
            if callback:
                callback(i + 1, count)
            
            if i + 1 < count:  # Don't delay after the last view
                delay = random.uniform(delay_min, delay_max)
                logger.info(f"[*] Waiting {delay:.2f} seconds before next view...")
                time.sleep(delay)
            
            if (i + 1) % 10 == 0 or i + 1 == count:
                logger.info(f"[*] Progress: {i + 1}/{count} views (Successful: {successful_views})")
    
    logger.info("-" * 60)
    logger.info(f"[*] Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"[*] Views added: {successful_views}/{count}")
    
    if callback:
        callback(count, count)
    
    return successful_views

def main():
    """Main function to parse arguments and run the bot."""
    parser = argparse.ArgumentParser(description='eBay Views Bot - Add views to eBay listings')
    parser.add_argument('url', type=str, help='eBay listing URL')
    parser.add_argument('-c', '--count', type=int, default=10, help='Number of views to add (default: 10)')
    parser.add_argument('-w', '--workers', type=int, default=1, help='Number of concurrent workers (default: 1)')
    parser.add_argument('-p', '--proxies', action='store_true', help='Use proxies if available')
    parser.add_argument('--min-delay', type=float, default=2.0, help='Minimum delay between views in seconds (default: 2.0)')
    parser.add_argument('--max-delay', type=float, default=5.0, help='Maximum delay between views in seconds (default: 5.0)')
    
    args = parser.parse_args()
    
    # Validate eBay URL
    if not validate_ebay_url(args.url):
        logger.error("Error: The provided URL doesn't appear to be a valid eBay listing.")
        logger.error("Please provide a URL in the format: https://www.ebay.com/itm/item_number")
        sys.exit(1)
    
    # Check if using proxies but none are configured
    if args.proxies and not PROXIES:
        logger.warning("Warning: Proxy usage enabled but no proxies configured.")
        logger.warning("Add proxies to the PROXIES list in the script or run without the -p flag.")
    
    # Add views
    add_views(
        args.url, 
        args.count, 
        args.workers, 
        args.proxies, 
        args.min_delay, 
        args.max_delay
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)