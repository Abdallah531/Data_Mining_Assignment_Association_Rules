import pandas as pd
from collections import Counter
from itertools import combinations
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Read the CSV file and preprocess data
def read_and_preprocess(file_path, percentage):
    # Read the CSV file
    df = pd.read_csv(file_path)
    # Drop the specified columns
    df.drop(columns=['DateTime', 'Daypart', 'DayType'], inplace=True)
    # Remove duplicates
    df.drop_duplicates(inplace=True)

    sampled_df = df.sample(frac=percentage / 100)

    return sampled_df


# Transform data into the desired format
def transform_data(df):
    data = []
    grouped = df.groupby('TransactionNo')['Items'].apply(list)
    for transaction, items in grouped.items():
        data.append([transaction, items])
    return data


# Apriori algorithm to find frequent item sets
def apriori(data, min_support):
    # Extract unique items from transactions
    unique_items = []
    for transaction in data:
        for item in transaction[1]:
            if item not in unique_items:
                unique_items.append(item)
    unique_items = sorted(unique_items)

    # Count occurrences of each unique item
    item_counts = Counter()
    for item in unique_items:
        for transaction in data:
            if item in transaction[1]:
                item_counts[item] += 1

    # Filter items that meet the minimum support
    frequent_items = Counter()
    for item in item_counts:
        if item_counts[item] >= min_support:
            frequent_items[frozenset([item])] += item_counts[item]

    # Initialize frequent item sets
    frequent_item_sets = frequent_items

    # Iterate over potential item set sizes
    for item_set_size in range(2, 10000):
        new_candidates = set()
        previous_item_sets = list(frequent_item_sets)

        # Generate larger item sets
        for i in range(0, len(previous_item_sets)):
            for j in range(i + 1, len(previous_item_sets)):
                combined_set = previous_item_sets[i].union(previous_item_sets[j])
                if len(combined_set) == item_set_size:
                    new_candidates.add(previous_item_sets[i].union(previous_item_sets[j]))

        candidate_counts = Counter()
        # Count occurrences of candidate item sets
        for candidate in new_candidates:
            candidate_counts[candidate] = 0
            for transaction in data:
                transaction_items = set(transaction[1])
                if candidate.issubset(transaction_items):
                    candidate_counts[candidate] += 1

        filtered_item_sets = Counter()
        # Filter candidate item sets based on minimum support
        for item_set in candidate_counts:
            if candidate_counts[item_set] >= min_support:
                filtered_item_sets[item_set] += candidate_counts[item_set]

        # Terminate if no more frequent item sets are found
        if len(filtered_item_sets) == 0:
            break

        frequent_item_sets = filtered_item_sets

    return frequent_item_sets


# Calculate association rules and confidence
def calculate_association_rules(frequent_item_sets, data, min_confidence):
    association_rules = {}

    # Iterate over each frequent item set
    for frequent_set in frequent_item_sets:

        # Generate all possible subsets of the frequent item set
        subsets = [frozenset(subset) for subset in combinations(frequent_set, len(frequent_set) - 1)]

        # Iterate over each subset to generate candidate rules
        for subset in subsets:
            complement_subset = frequent_set - subset
            combined_set = frequent_set

            # Initialize counts for support
            support_combined = 0
            support_subset = 0
            support_complement = 0

            # Count occurrences of item sets in transactions
            for transaction in data:
                items_in_transaction = set(transaction[1])
                if subset.issubset(items_in_transaction):
                    support_subset += 1
                if complement_subset.issubset(items_in_transaction):
                    support_complement += 1
                if combined_set.issubset(items_in_transaction):
                    support_combined += 1

            # Skip if the support count of the subset is zero to avoid division by zero
            if support_subset == 0:
                continue

            # Calculate confidence for the A => B rule
            confidence_a_to_b = support_combined / support_subset * 100
            if confidence_a_to_b >= min_confidence:
                antecedent = ", ".join(list(subset))
                consequent = ", ".join(list(complement_subset))
                association_rules[f"{antecedent} => {consequent}"] = confidence_a_to_b

            # Skip if the support count of the complement subset is zero to avoid division by zero
            if support_complement == 0:
                continue

            # Calculate confidence for the B => A rule
            confidence_b_to_a = support_combined / support_complement * 100
            if confidence_b_to_a >= min_confidence:
                antecedent = ", ".join(list(complement_subset))
                consequent = ", ".join(list(subset))
                association_rules[f"{antecedent} => {consequent}"] = confidence_b_to_a

    return association_rules

# Function to display the analysis result in the GUI
def display_results(result_text, frequent_item_sets, association_rules):
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, "Frequent Item Sets:\n")
    for item_set, support in frequent_item_sets.items():
        items = ", ".join(list(item_set))
        result_text.insert(tk.END, f"{items}: {support}\n")

    result_text.insert(tk.END, "\nAssociation Rules:\n")
    for rule, confidence in association_rules.items():
        result_text.insert(tk.END, f"{rule}: {confidence}%\n")

    result_text.config(state=tk.DISABLED)


# Function to browse and select a file
def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


# Main function to create and configure the GUI
def main():
    root = tk.Tk()
    root.title("Association Rule Mining")

    # Create and place input fields
    file_label = tk.Label(root, text="Select CSV File:")
    file_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(file_entry))
    browse_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

    percentage_label = tk.Label(root, text="Percentage of Data to Read:")
    percentage_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    percentage_entry = tk.Entry(root, width=10)
    percentage_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    min_support_label = tk.Label(root, text="Minimum Support Count:")
    min_support_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    min_support_entry = tk.Entry(root, width=10)
    min_support_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    min_confidence_label = tk.Label(root, text="Minimum Confidence (%):")
    min_confidence_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    min_confidence_entry = tk.Entry(root, width=10)
    min_confidence_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

    # Create and place buttons
    analyze_button = tk.Button(root, text="Analyze", command=lambda: analyze(file_entry.get(), percentage_entry.get(), min_support_entry.get(), min_confidence_entry.get()))
    analyze_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    # Create and place result text widget
    result_text = tk.Text(root, width=80, height=20)
    result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
    result_text.config(state=tk.DISABLED)

    # Function to perform analysis
    def analyze(file_path, percentage, min_support, min_confidence):
        try:
            percentage = float(percentage)
            min_support = int(min_support)
            min_confidence = float(min_confidence)

            df = read_and_preprocess(file_path, percentage)
            data = transform_data(df)

            frequent_item_sets = apriori(data, min_support)
            association_rules = calculate_association_rules(frequent_item_sets, data, min_confidence)

            display_results(result_text, frequent_item_sets, association_rules)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root.mainloop()


if __name__ == "__main__":
    main()
