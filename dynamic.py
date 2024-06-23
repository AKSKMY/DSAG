import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Path to your CSV file
csv_file_path = r"DSAG\Dataset\filtered_transactions.csv"
#filtered csv alr --> single transactions removed

# Read the CSV file
df = pd.read_csv(csv_file_path)
#print(df)

transactions = df['Product'].apply(lambda x: x.strip('[]').replace("'", "").split(', ')).tolist()
#print(transactions)

# Initialize TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)

# Create a DataFrame with the transaction data
df_trans = pd.DataFrame(te_ary, columns=te.columns_)

# Apply the Apriori algorithm to find frequent itemsets
min_support = 0.0588  # Adjust the min_support as needed
frequent_itemsets = apriori(df_trans, min_support=min_support, use_colnames=True)

frequent_itemsets['support_count'] = (frequent_itemsets['support'] * len(transactions)).astype(int)
frequent_itemsets = frequent_itemsets[frequent_itemsets['support_count'] >= 2]

frequent_itemsets = frequent_itemsets.drop(columns=['support'])

frequent_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x) > 1)]

#check if frequent_itemsets is empty
if frequent_itemsets.empty:
    print("No frequent itemsets found.")

else:
    print("Frequent Itemsets that appear in at least 2 transactions:")
    print(frequent_itemsets)


