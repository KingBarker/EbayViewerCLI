# EbayViewerCLI V1.00

**Educational Use Only**

A simple Python CLI tool to simulate views on eBay listings by rotating user-agents, adding basic fingerprint variation, and optionally using proxies.

![image](https://github.com/user-attachments/assets/07632dad-4688-483c-a869-5f219423260d)


## Prerequisites

- Python 3.6 or higher  
- Pip (for dependency installation)  
- (Optional) A `proxy.txt` file in the same directory for proxy support  

---

## Installation

1. Clone or download the repository to your local machine.  
2. Place `EbayViewerCLI.py` in your working directory.  
3. Ensure the file is executable (on UNIX/Linux/macOS):  
   ```bash
   chmod +x EbayViewerCLI.py
   ```

---

## Usage

Run the script without arguments to enter interactive mode:

```bash
python EbayViewerCLI.py
```

You will be prompted for:  
1. **eBay listing URL** (the `/itm/<ID>` link)  
2. **Number of views** to simulate  
3. **Worker count** (parallel threads)  
4. **Minimum delay** (seconds)  
5. **Maximum delay** (seconds)  
6. **Use proxies?** (Y/N)  

### Example

```text
Enter eBay listing URL: https://www.ebay.com/itm/1234567890
Number of views to add: 25
Workers (default 1): 2
Min delay (s): 1.0
Max delay (s): 2.5
Use proxies? (y/N): N
```

The script will report progress and log to `ebay_viewer.log`.

---

## Proxy Support

To enable proxies, create a `proxy.txt` file in the same directory:

```
# Comment lines begin with '#'
http://username:password@host:port
http://host:port
```

When prompted, choose **Y** to load proxies from this file.

---

## Author

Created by **KingBarker**  
GitHub: [https://github.com/KingBarker](https://github.com/KingBarker)

---

## License

MIT License. See [LICENSE](LICENSE) for details.  
