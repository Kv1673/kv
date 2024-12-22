import joblib
import pandas as pd

# Load the trained model and vectorizer
model = joblib.load('random_forest_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Load the sample URLs from the Excel file
sample_urls = pd.read_excel(r"C:\Users\Mohan\Desktop\Project Phishing\data_bal - 20000.xlsx")

# Assuming the URLs are in a column named 'url', extract that column
urls = sample_urls['URLs']  # Change 'url' to the correct column name if needed

# Transform the sample URLs using the vectorizer
sample_urls_vectorized = vectorizer.transform(urls)

# Predict the type of URLs using the model
predictions = model.predict(sample_urls_vectorized)

# Map the predictions to readable labels
predicted_labels = ["Phishing URL" if label == 1 else "Legitimate URL" for label in predictions]

# Display the results
for url, label in zip(urls, predicted_labels):
    print(f"URL: {url}\nPrediction: {label}\n")
