from flask import Flask, render_template
import json
import os

app = Flask(__name__)

# Load data dari file JSON (absolute path agar kompatibel dengan Vercel)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data', 'mesin.json'), 'r', encoding='utf-8') as f:
    mesin_data = json.load(f)

# Filter untuk format Rupiah
@app.template_filter('format_rupiah')
def format_rupiah(value):
    return "Rp {:,.0f}".format(value).replace(",", ".")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    return render_template('katalog.html', mesin=mesin_data)

@app.route('/detail/<kapasitas>')
def detail(kapasitas):
    mesin_item = next((item for item in mesin_data if item['kapasitas'] == kapasitas), None)
    if mesin_item:
        return render_template('detail.html', mesin=mesin_item)
    return render_template('404.html'), 404

@app.route('/kontak')
def kontak():
    return render_template('contact.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)