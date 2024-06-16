# NOT COMPLETED - IN PROGRESS / TESTING

from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from itertools import combinations

app = Flask(__name__)

#Keep track of counts of itemsets of size 2
class hashTable:
    def __init__(self, hash_table_size):
        self.hash_table = [0] * hash_table_size

    def add_itemset(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        self.hash_table[hash_index] += 1

    def get_itemset_count(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        return self.hash_table[hash_index]



# Generate and prune the candidate itemsets for next level using
# frequent itemsets of the current level
def generateCandidateItemsets(level_k, level_frequent_itemsets):

    n_frequent_itemsets = len(level_frequent_itemsets)
    candidate_frequent_itemsets = []

    for i in range(n_frequent_itemsets):
        j = i+1
        while (j<n_frequent_itemsets) and (level_frequent_itemsets[i][:level_k-1] == level_frequent_itemsets[j][:level_k-1]):
            candidate_itemset = level_frequent_itemsets[i][:level_k-1] + [level_frequent_itemsets[i][level_k-1]] + [level_frequent_itemsets[j][level_k-1]]
            candidate_itemset_pass = False

            #current level number
            if level_k == 1:
                candidate_itemset_pass = True
            elif (level_k == 2) and (candidate_itemset[-2:] in level_frequent_itemsets):
                candidate_itemset_pass = True
            elif all((list(_)+candidate_itemset[-2:]) in level_frequent_itemsets for _ in combinations(candidate_itemset[:-2], level_k-2)):
                candidate_itemset_pass = True

            if candidate_itemset_pass:
                candidate_frequent_itemsets.append(candidate_itemset)

            j += 1

    return candidate_frequent_itemsets

#Extract frequent itemsets from transactions using hash table and transaction reuduction
def aprioriAlgorithm(transactions, min_support_count):

    # Create a mapping of item names to integers
    item_mapping = {
        'eggs': 1,
        'vegetables': 2,
        'milk': 3,
        'bread': 4,
        'cheese': 5,
        'apple': 6,
        'banana': 7
    }

    reverse_item_mapping = {v: k for k, v in item_mapping.items()}

    # Convert transactions to integer form using the mapping
    transactions_int = []
    for transaction in transactions:
        transactions_int.append({item_mapping[item] for item in transaction})

    # Extract the list of items in the transactions
    items = set()
    for transaction in transactions_int:
        items.update(transaction)
    items = sorted(list(items))

    # The list of frequent itemsets in the transaction
    frequent_itemsets = []

    level_k = 1  # The current level number
    level_frequent_itemsets = []  # Level 0: Frequent itemsets
    candidate_frequent_itemsets = [[item] for item in items]  # Level 1: Candidate itemsets

    # Initialize the hash table
    hash_tb = hashTable(7)

    while candidate_frequent_itemsets:

        # Count the support of all candidate frequent itemsets and remove transactions using transaction reduction
        candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

        for transaction in transactions_int:
            # Add the count of itemsets of size 2 to hashtable
            if level_k == 1:
                for itemset in combinations(transaction, 2):
                    hash_tb.add_itemset(itemset)

            for i, itemset in enumerate(candidate_frequent_itemsets):
                if all(_item in transaction for _item in itemset):
                    candidate_freq_itemsets_cnts[i] += 1

        # Generate the frequent itemsets of level k by pruning infrequent itemsets
        level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support_count]
        frequent_itemsets.extend([set(level_frequent_itemset) for level_frequent_itemset in level_frequent_itemsets])

        # Generate candidates Ck+1 from Ck (using generate and prune)
        candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)
        level_k += 1

        # Prune C_2 using hash table generated during L_1
        if level_k == 2:
            for itemset in candidate_frequent_itemsets:
                if hash_tb.get_itemset_count(itemset) < min_support_count:
                    print('Pruned itemset', itemset)
                    candidate_frequent_itemsets.remove(itemset)

    # Convert frequent itemsets back to item names
    frequent_itemsets_named = []
    for itemset in frequent_itemsets:
        frequent_itemsets_named.append({reverse_item_mapping[item] for item in itemset})

    return frequent_itemsets_named


@app.route('/')
def index():
    # Example transactions data
    transactions = [
        {'eggs', 'milk', 'bread'},
        {'vegetables', 'bread'},
        {'vegetables', 'milk'},
        {'eggs', 'vegetables', 'bread'},
        {'milk', 'cheese'},
        {'vegetables', 'milk'},
        {'milk', 'cheese'},
        {'eggs', 'milk', 'bread'},
        {'eggs', 'vegetables', 'milk'},
        {'eggs', 'bread'},
        {'milk', 'bread', 'cheese'}
    ]

    min_support_count = 3

    # Generate frequent itemsets using the Apriori algorithm
    frequent_itemsets = aprioriAlgorithm(transactions, min_support_count)

    # Create the plot
    plt.rcParams['figure.figsize'] = (18, 7)
    color = plt.cm.magma(np.linspace(0, 1, 40))
    data = pd.Series([item for sublist in transactions for item in sublist])
    ax = data.value_counts().head(40).plot.bar(color=color)
    plt.title('Frequency of Most Popular Items', fontsize=20)
    plt.xticks(rotation=90)
    plt.grid()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Clear the current plot
    plt.close()

    # HTML template with embedded image and frequent itemsets
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <style>
    img {
        width:70%;
        height:70%;
    }
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Apriori Algorithm Results</title>
    </head>
    <body>
        <h1>Frequency of Most Popular Items</h1>
        <img src="data:image/png;base64,{{ plot_url }}">
        <h2>Frequent Itemsets (Min Support Count = {{ min_support_count }})</h2>
        <ul>
        {% for itemset in frequent_itemsets %}
            <li>{{ itemset }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template, plot_url=plot_url, frequent_itemsets=frequent_itemsets, min_support_count=min_support_count)

if __name__ == '__main__':
    app.run(debug=True)
    
    #Example of transactions as data
    # transactions = [
    #     {'eggs', 'milk', 'bread'},
    #     {'vegetables', 'bread'},
    #     {'vegetables', 'milk'},
    #     {'eggs', 'vegetables', 'bread'},
    #     {'milk', 'cheese'},
    #     {'vegetables', 'milk'},
    #     {'milk', 'cheese'},
    #     {'eggs', 'milk', 'bread'},
    #     {'eggs', 'vegetables', 'milk'},
    #     {'eggs', 'bread'},
    #     {'milk', 'bread', 'cheese'}
    # ]

    #min_support_count = 3

    # Generate list of all frequent itemsets using Transaction Reduction based Apriori
    # frequent_itemsets = aprioriAlgorithm(transactions, min_support_count)

    # print("\nFREQUENT ITEMSETS (Min Support Count = {})".format(min_support_count))
    # for frequent_itemset in frequent_itemsets:
    #     print(frequent_itemset)
