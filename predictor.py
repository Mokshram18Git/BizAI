import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def predict_sales(company_name):
    # 1. Search query to get revenue data
    search_url = f"https://www.google.com/search?q={company_name}+annual+revenue+by+year"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    # 2. Extract year-revenue pairs (very simple regex-based for now)
    import re
    pattern = r"(20[0-9]{2})[^0-9]{1,20}?(\$?[0-9,.]+ ?(million|billion|crore|lakh)?)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    # 3. Clean and convert
    data = []
    for match in matches:
        year = int(match[0])
        rev_str = match[1].lower().replace(",", "").replace("$", "")
        multiplier = 1
        if "billion" in rev_str:
            multiplier = 1e9
        elif "million" in rev_str:
            multiplier = 1e6
        elif "crore" in rev_str:
            multiplier = 1e7
        elif "lakh" in rev_str:
            multiplier = 1e5
        num = re.findall(r"\d+\.?\d*", rev_str)
        if num:
            revenue = float(num[0]) * multiplier
            data.append((year, revenue))

    if len(data) < 3:
        return None, "❌ Not enough historical data found."

    df = pd.DataFrame(data, columns=["Year", "Revenue"])
    df = df.sort_values("Year").drop_duplicates("Year")

    # 4. Fit polynomial regression model
    X = df["Year"].values.reshape(-1, 1)
    y = df["Revenue"].values
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    next_year = df["Year"].max() + 1
    next_year_poly = poly.transform(np.array([[next_year]]))
    prediction = model.predict(next_year_poly)[0]

    return df, round(prediction, 2)
