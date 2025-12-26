from scraper.web_scraper import scrape_competitors
from analysis.data_analysis import analyze_data


def main():
    print("🚀 Starting Competitor Benchmarking Project...\n")

    scrape_competitors()
    analyze_data()

    print("\n✅ Project completed successfully!")
    print("👉 Run the dashboard using:")
    print("   streamlit run dashboard/dashboard.py")


if __name__ == "__main__":
    main()
