import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read CSV file
def load_data():
    try:
        df = pd.read_csv("temps.csv")

        # Check required columns
        required_columns = ["Date", "Temp_C"]

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        # Convert date into datetime format
        df["Date"] = pd.to_datetime(
            df["Date"], errors="coerce"
        )

        # Convert temperature into numeric values
        df["Temp_C"] = pd.to_numeric(
            df["Temp_C"], errors="coerce"
        )

        # Handle invalid dates and temperatures
        invalid = df["Date"].isna() | df["Temp_C"].isna()

        for _, row in df[invalid].iterrows():
            print(
                f"Invalid reading on {row['Date']}: "
                f"{row['Temp_C']}. Value ignored (NaN)."
            )

        # Remove invalid readings
        df = df.dropna(subset=["Date", "Temp_C"])

        if df.empty:
            print("No valid temperature readings found.")
            return None

        return df

    except FileNotFoundError:
        print("Error: temps.csv file not found.")
        return None

    except ValueError as error:
        print("Error:", error)
        return None


# Step 2: Calculate statistics
def show_statistics(df):
    temperatures = df["Temp_C"]

    mean = np.mean(temperatures)
    median = np.median(temperatures)
    maximum = np.max(temperatures)
    minimum = np.min(temperatures)
    std_dev = np.std(temperatures, ddof=0)

    print("\n--- Temperature Statistics ---")
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Max: {maximum:g}")
    print(f"Min: {minimum:g}")
    print(f"Std Dev: {std_dev:.2f}")

    # Detect hot days
    hot_days = df[df["Temp_C"] > 35]

    if hot_days.empty:
        print("No days above 35 C")
    else:
        print("Hot days:")
        for _, row in hot_days.iterrows():
            print(
                row["Date"].strftime("%Y-%m-%d"),
                row["Temp_C"]
            )

    # Detect outliers using IQR
    q1 = temperatures.quantile(0.25)
    q3 = temperatures.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[
        (temperatures < lower) |
        (temperatures > upper)
    ]

    print("\nOutliers:")
    if outliers.empty:
        print("No outliers found.")
    else:
        print(outliers[["Date", "Temp_C"]].to_string(index=False))


# Step 3: Plot graphs
def plot_graphs(df):
    # Line chart
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Date"],
        df["Temp_C"],
        marker="o",
        label="Temperature"
    )

    plt.title("Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (C)")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

    # Histogram
    plt.figure(figsize=(8, 5))

    plt.hist(
        df["Temp_C"],
        bins="auto",
        edgecolor="black"
    )

    plt.title("Temperature Distribution")
    plt.xlabel("Temperature (C)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.show()


# Step 4: Convert Celsius to Fahrenheit
def convert_to_fahrenheit(df):
    fahrenheit = df["Temp_C"] * 9 / 5 + 32

    print("\n--- Temperature in Fahrenheit ---")

    for value in fahrenheit:
        print(f"{value:.2f} F")


# Step 5: Main menu
def main():
    df = load_data()

    if df is None:
        return

    while True:
        print("\n===== Temperature Data Analyzer =====")
        print("1. Show Statistics")
        print("2. Plot Graphs")
        print("3. Convert to Fahrenheit")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_statistics(df)

        elif choice == "2":
            plot_graphs(df)

        elif choice == "3":
            convert_to_fahrenheit(df)

        elif choice == "4":
            print("Thank you for using Temperature Data Analyzer!")
            break

        else:
            print("Invalid choice. Please enter 1 to 4.")


# Run program
if __name__ == "__main__":
    main()