# Web Crawler with Multithreading and Page Saving

This Python script is a fast and efficient web crawler that recursively visits pages within a target website, extracts internal links, and saves each visited page’s HTML content locally. It leverages multithreading to speed up the crawling process and provides clear, colored console output to track progress.

---

## Features

- Recursive crawling with configurable maximum depth  
- Multithreaded requests using ThreadPoolExecutor for faster scanning  
- Only follows links within the same domain as the target URL  
- Resolves relative URLs to absolute URLs correctly  
- Saves full HTML content of each visited page in a local `pages` directory  
- Prints page URLs and their titles in the console for easy tracking  
- Prevents revisiting the same URLs to avoid redundancy  
- Summarizes total pages visited and total crawl duration at the end  

---

## Requirements

- Python 3.x  
- `requests` library  
- `beautifulsoup4` library  

Install dependencies via pip:

pip install requests beautifulsoup4
---

## Usage Instructions

1. Place the crawler script file (e.g., `crawler.py`) and run it via terminal or command prompt:


2. When prompted, enter:  
   - **Target URL:** The base URL of the website to crawl (e.g., `https://example.com`)  
   - **Max crawl depth:** How many link levels deep to crawl (default is 2)  
   - **Max threads:** Number of parallel threads to speed up crawling (default is 10)  

3. The crawler will start visiting pages, printing each page’s URL and title.  

4. All visited pages’ HTML content will be saved in the `pages` folder created in the script’s directory.  

5. When complete, the script prints a summary including how many pages were visited and how long it took.

---

## Important Notes

- The crawler **only follows internal links** within the specified domain. External links are ignored.  
- Relative links on pages are resolved to absolute URLs using the current page URL as the base.  
- Make sure you have permission to crawl the target website to comply with legal and ethical guidelines.  
- Large websites or high thread counts may consume significant resources; adjust settings based on your environment.  
- The script handles HTTP errors and skips inaccessible pages gracefully.

---

## License

This project is open source and released under the MIT License.

---

Feel free to modify and extend this crawler to fit your specific needs, such as adding data extraction, exporting results, or integrating asynchronous requests for even better performance.
