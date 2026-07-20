from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ganti-ini-nanti-dengan-string-acak'

@app.route('/')
def index():
    return render_template('index.html', judul="Inventaris UKM Telkom Art")

if __name__ == '__main__':
    app.run(debug=True)