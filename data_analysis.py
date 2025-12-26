import pandas as pd


def analyze_data():
    df = pd.read_csv("data/raw_data.csv")

    if df.empty:
        print("❌ raw_data.csv is empty")
        return

    df["price_category"] = df["price"].apply(
        lambda x: "Low" if x < 30 else "Medium" if x < 60 else "High"
    )

    df.to_csv("data/cleaned_data.csv", index=False)
    print("✅ cleaned_data.csv created successfully")


if __name__ == "__main__":
    analyze_data()
