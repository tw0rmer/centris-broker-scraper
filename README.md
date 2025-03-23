# 🕵️‍♂️ Centris Broker Scraper

![Python](https://img.shields.io/badge/Python-3.10-blue.svg) ![Selenium](https://img.shields.io/badge/Selenium-WebDriver-brightgreen.svg) ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parser-orange.svg) ![TQDM](https://img.shields.io/badge/TQDM-Progress%20Bar-yellowgreen.svg) ![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-blueviolet.svg)

## 🚀 Project Overview

The **Centris Broker Scraper** is an intuitive Python script designed to automate the scraping of real estate broker data from [Centris.ca](https://www.centris.ca). Built with modern tools like **Selenium**, **BeautifulSoup**, and featuring real-time progress bars using **TQDM**, this scraper efficiently navigates through dynamic pages, extracts crucial broker details, and provides output in both simple text and a stylish, responsive HTML report powered by **TailwindCSS**.

Whether you're a Python enthusiast or a seasoned developer, this project provides clear, step-by-step instructions for easy setup and usage. Environment management is made simple through the use of **Miniconda**.

---

## 🌟 Key Features

- ✅ **Minimal Setup:** Automatic installation of required packages.
- 🔄 **Dynamic Navigation:** Selenium-powered automatic page traversal—no manual interaction required.
- 📊 **Progress Tracking:** Real-time scraping progress displayed with TQDM.
- 📇 **Comprehensive Data Extraction:** Broker names, titles, phone numbers, websites, images, broker IDs, and contact links.
- 📁 **Flexible Output:** Export results to plain text and beautifully designed HTML reports.
- ⏱ **Detailed Logging:** Timing logs for each page and final summary statistics.
- 🐍 **Miniconda Ready:** Easy Python environment management for smooth setup.

---

## ⚙️ Requirements & Installation

### Step 1: Environment Setup

- **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)** (Recommended)
  ```bash
  conda create -n brokerscrape python=3.10
  conda activate brokerscrape
  ```

### Step 2: Chrome & WebDriver

- **Install [Google Chrome](https://www.google.com/chrome/)**
- **ChromeDriver**:
  - Visit [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) and download a matching version.
  - Place the downloaded `chromedriver.exe` in a known directory (e.g., Desktop).
  - Update `driver_path` inside the script (`sel_scrapper.py`) with the location of your driver.

### Step 3: Install Dependencies

- The script automatically installs missing Python packages:
  ```bash
  python sel_scrapper.py
  ```

---

## 🚦 Usage

Run the script:

```bash
python sel_scrapper.py
```

You'll be prompted to provide:

- The URL from Centris (e.g., [Centris Brokers](https://www.centris.ca/en/real-estate-brokers?view=Thumbnail&pback=true&uc=0))
- The number of pages you wish to scrape
- Your preferred export format (Text, HTML, or Both)

The scraper then automatically:

- Navigates each page
- Extracts broker data
- Logs scraping progress
- Generates an `output_data.txt` and/or `output_data.html` report

---

## 🔍 Scraping Process (Step-by-Step)

1. **Initialization:** Installs missing dependencies automatically.
2. **User Input:** You provide URL and scraping preferences.
3. **Launching Browser:** Headless Chrome session launched with Selenium.
4. **Data Extraction:** Parses HTML with BeautifulSoup, extracting detailed broker information.
5. **Real-Time Feedback:** TQDM progress bar updates continuously during the scraping.
6. **Final Reporting:** Saves data into clean, well-designed HTML or simple text formats.

---

## 🛠️ Troubleshooting

- Ensure ChromeDriver version matches your installed Chrome version.
- If experiencing issues (0 brokers or errors), check for special cookies or headers required by Centris.
- Antivirus or firewall may block Selenium. Temporarily disable if browser launch fails.

---

## 🙏 Acknowledgments

Special thanks to maintainers and contributors of:

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [TQDM](https://github.com/tqdm/tqdm)
- [Colorama](https://github.com/tartley/colorama)
- [TailwindCSS](https://tailwindcss.com/)

---

📌 **© 2025, Broker Scraper Project | Developed by Jason**

Happy scraping! 🕷️📑✨

