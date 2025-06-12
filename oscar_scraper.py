from flask import Flask, request
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <title>Oscar Awards Scraper</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2880/2880731.png">
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
      background: #6c63ff;
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
    {table}
    <div class="footer">
      ❤️ Developed by Shinde Amit using Flask & BeautifulSoup ❤️
    </div>
  </div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    table = ''
    url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films'
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')

            Film, Year, Award, Nomination = [], [], [], []
            count = 0
            for i in soup.find_all('td'):
                text = re.sub('^<td>.*">|<td>|</td>|<.*?>|\n', "", str(i))
                if count == 0:
                    Film.append(text)
                    count += 1
                elif count == 1:
                    Year.append(text)
                    count += 1
                elif count == 2:
                    Award.append(text)
                    count += 1
                else:
                    Nomination.append(text)
                    count = 0

            df = pd.DataFrame({
                "Films": Film[:1387],
                "Years": Year[:1387],
                "Awards": Award[:1387],
                "Nominations": Nomination[:1387]
            })
            table = df.to_html(classes="table table-bordered table-striped", index=False)
        except Exception as e:
            table = f"<p class='text-danger'>Error: {str(e)}</p>"
    return HTML_TEMPLATE.format(table=table, url=url)

if __name__ == '__main__':
    import os
    os.environ["FLASK_ENV"] = "development"  # Optional
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_reloader=False)

