from flask import Flask, request, make_response, url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <title>Oscar Awards Scraper</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2880/2880731.png">
  <link href="https://unpkg.com/ionicons@4.5.10-0/dist/css/ionicons.min.css" rel="stylesheet">
  <style>
    body {{
      background: linear-gradient(to right, #e0eafc, #cfdef3);
      font-family: 'Segoe UI', sans-serif;
      padding-top: 60px;
    }}
    .container {{
      max-width: 800px;
      background: white;
      padding: 30px 40px;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    h2 {{
      font-weight: bold;
      color: #343a40;
    }}
    .form-label {{
      font-weight: 500;
    }}
    .btn-primary {{
      background: #4f46e5;
      border: none;
    }}
    .btn-primary:hover {{
      background: #574fd6;
    }}
    textarea {{
      resize: none;
    }}
    .footer {{
      margin-top: 40px;
      text-align: center;
      color: #777;
      font-size: 0.9em;
    }}

/* Custom Download Button */
.custom-download-btn {{
  display: block;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  
  /* --- Smaller Size --- */
  padding: 8px 20px;
  font-size: 16px;
  border-radius: 8px;
  /* --- End Smaller Size --- */
  
  font-weight: 500;
  color: #007bff;
  background-color: #ffffff;
  border: 2px solid #007bff;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 123, 255, 0.15);
}}

.custom-download-btn:hover {{
  background-color: #007bff;
  color: #ffffff;
  text-decoration: none;
  box-shadow: 0 5px 14px rgba(0, 123, 255, 0.3);
}}

.custom-download-btn i {{
  margin-right: 6px;
  font-size: 18px;
  vertical-align: middle;
}}
  </style>
</head>
<body>
  <div class="container">
    <div class="text-center mb-4">
      <img src="https://cdn-icons-png.flaticon.com/512/2880/2880731.png" width="60" />
      <h2 class="mt-3">Oscar Awards Scraper</h2>
    </div>
    <form method="POST">
      <div class="mb-3">
        <label for="url" class="form-label">Paste Wikipedia Link:</label>
        <textarea name="url" class="form-control" rows="2" required>{url}</textarea>
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-primary btn-lg">🎬 Scrape Data</button>
      </div>
    </form>
    <hr class="my-4">
    {download_button}
    {table}
    <div class="footer">
      ❤️ Developed by Shinde Amit using Flask & BeautifulSoup ❤️
    </div>
  </div>
</body>
</html>
'''

# ✅ New Download Button Matching Your Image
DOWNLOAD_BUTTON_HTML = '''
<div class="text-center mt-4">
  <a href="{url}" class="custom-download-btn" download>
    <i class="icon ion-md-download"></i> Downloads
  </a>
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    table_html = ''
    download_button = ''
    url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films'

    if request.method == 'POST':
        url = request.form.get('url')
        try:
            req = requests.get(url)
            req.raise_for_status()
            soup = BeautifulSoup(req.content, 'html.parser')

            target_table = soup.find('table', {'class': 'wikitable sortable'})
            if not target_table:
                raise ValueError("Could not find the awards table on the page.")

            Film, Year, Award, Nomination = [], [], [], []
            for row in target_table.find('tbody').find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    Film.append(cells[0].get_text(strip=True))
                    year_raw = cells[1].get_text(strip=True)
                    cleaned_year = year_raw.split('/')[0].strip() if '/' in year_raw else year_raw.strip()
                    Year.append(cleaned_year)
                    award_raw = cells[2].get_text(strip=True)
                    cleaned_award = re.sub(r'\s*\(\d+\)', '', award_raw)
                    Award.append(cleaned_award)
                    Nomination.append(cells[3].get_text(strip=True))

            df = pd.DataFrame({
                "Film": Film,
                "Year": Year,
                "Awards": Award,
                "Nominations": Nomination
            })

            table_html = df.to_html(classes="table table-bordered table-striped", index=False)

            with open("scraped_table.html", "w", encoding="utf-8") as f:
                f.write(table_html)

            download_button = DOWNLOAD_BUTTON_HTML.format(url=url_for('download_pdf'))

        except Exception as e:
            table_html = f"<p class='text-danger'>Error: {str(e)}</p>"
            if os.path.exists("scraped_table.html"):
                os.remove("scraped_table.html")
    else:
        if os.path.exists("scraped_table.html"):
            os.remove("scraped_table.html")

    return HTML_TEMPLATE.format(table=table_html, url=url, download_button=download_button)

@app.route('/download-pdf')
def download_pdf():
    if not os.path.exists("scraped_table.html"):
        return "No data to download. Please scrape data first.", 404

    try:
        with open("scraped_table.html", "r", encoding="utf-8") as f:
            html_for_pdf = f.read()

        pdf_html_doc = f'''
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>Oscar Awards Data</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style> body {{ font-family: sans-serif; }} h2 {{ text-align: center; }} </style>
          </head>
          <body>
            <h2>Oscar-Winning Films</h2>
            {html_for_pdf}
          </body>
        </html>
        '''

        pdf_file = HTML(string=pdf_html_doc).write_pdf()

        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=oscar_awards_list.pdf'

        return response

    except Exception as e:
        return f"An error occurred while generating the PDF: {str(e)}", 500

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_reloader=False)
