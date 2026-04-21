📊 Python Selenium Web Scraper

A Python-based web scraping tool built with Selenium that continuously extracts data from a target website and stores it in dynamically generated Excel files. The scraper is designed to run until manually stopped, ensuring real-time data collection while preventing duplicate entries.

🚀 Features
🔄 Continuous data scraping (runs until stopped)
📁 Automatically generates Excel files with timestamps
❌ Duplicate data detection and removal
⚡ Efficient and automated data extraction using Selenium
📊 Structured data storage for easy analysis
🛠️ Tech Stack
Python
Selenium
Pandas / OpenPyXL (for Excel handling)
📦 Installation
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:
pip install -r requirements.txt
Download and set up WebDriver (e.g., ChromeDriver) compatible with your browser.
▶️ Usage

Run the scraper:

python main.py
The script will start scraping data from the target website.
Data will be saved into an Excel file with a timestamp.
The scraper will continue running until you manually stop it (CTRL + C).
📁 Output
Excel files are automatically created with the current date and time.
Duplicate entries are filtered out to maintain clean datasets.
⚙️ Configuration

You can modify:

Target website URL
Scraping intervals
Data fields to extract
Output file naming format
