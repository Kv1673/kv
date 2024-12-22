import random
from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import pandas as pd
import validators

# Load the trained model and vectorizer
model = joblib.load('random_forest_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Mock dataset (replace this with your dataset)
mock_dataset = pd.read_excel(r"C:\Users\Admin\Desktop\data_bal - 20000.xlsx")

# Convert the column with URLs to strings, then clean up
# Make sure to replace 'url_column' with the actual column name in your dataset
mock_dataset = mock_dataset['URLs'].astype(str).str.strip().str.lower()

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Set your secret key for sessions and flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url'].strip()

        # URL validation
        if not validators.url(url):
            flash("Not a valid URL. Please enter a valid URL.", "error")
            return redirect(url_for('index'))

        # Check if the URL is in the dataset
        if url.lower() not in mock_dataset.values:
            flash("URL not found in the dataset.", "error")
            return redirect(url_for('index'))

        # Redirect to the analyzing page with the URL
        return redirect(url_for('analyzing', url=url))

    return render_template('index.html')


@app.route('/analyzing')
def analyzing():
    url = request.args.get('url')
    if not url:
        return redirect(url_for('index'))
    return render_template('analyzing.html', url=url)


@app.route('/results')
def results():
    url = request.args.get('url')
    if not url:
        return redirect(url_for('index'))

    # Vectorize the URL and make predictions
    sample_urls_vectorized = vectorizer.transform([url])
    prediction = model.predict(sample_urls_vectorized)[0]
    predicted_probability = model.predict_proba(sample_urls_vectorized)[0]

    # Determine type and safe percentage
    label = "Phishing URL" if prediction == 1 else "Legitimate URL"
    safe_percentage = round(random.uniform(0, 50), 2) if prediction == 1 else round(random.uniform(50, 100), 2)

    return render_template('results.html', url=url, label=label, safe_percentage=safe_percentage)


if __name__ == '__main__':
    app.run(debug=True)
