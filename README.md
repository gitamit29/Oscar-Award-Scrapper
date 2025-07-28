#  Oscar Award-Winning Films Scraper

This project is a web scraper built using **Python** and **BeautifulSoup** to extract data on Oscar award-winning films from a target website. The data includes film titles, categories, award years, and whether the film won or was nominated.

## 📌 Features

* Scrapes structured data of Oscar-winning/nominated movies
* Extracts details like:

  * Movie Title
  * Award Category (e.g., Best Picture, Best Actor)
  * Year of the Award
  * Winner/Nominee status
* Saves the data into a clean **CSV file** or **Pandas DataFrame** for further analysis

## 🧰 Tech Stack

* **Python 3.x**
* **BeautifulSoup (bs4)**
* **Requests**
* **Pandas**

## 🧪 Use Cases

* Perform data analysis on Oscar trends
* Train machine learning models to predict award outcomes
* Generate visual insights (e.g., genre vs. award wins)

## 🚀 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/oscar-scraper.git
   cd oscar-scraper
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python oscar_scraper.py
   ```

4. The output will be saved as `oscar_films.csv`.

## 📊 Sample Output

| Title         | Category      | Year | Winner |
| ------------- | ------------- | ---- | ------ |
| The Godfather | Best Picture  | 1973 | Yes    |
| Titanic       | Best Director | 1998 | Yes    |
| La La Land    | Best Actress  | 2017 | No     |

## 📁 File Structure

```
oscar-scraper/
│
├── oscar_scraper.py        # Main scraping script
├── requirements.txt        # Python dependencies
├── oscar_films.csv         # Output CSV (generated)
└── README.md               # Project documentation
```

## 📌 Note

* Make sure the source website allows scraping (respect **robots.txt**).
* This project is for educational purposes.

## 👨‍💻 Author

**Amit Shinde** – [GitHub](https://github.com/gitamit29)


