# NOT COMPLETED - IN PROGRESS / TESTING

from itertools import combinations

class hashTable:
    def __init__(self, hash_table_size):
        self.hash_table = [0] * hash_table_size

    def add_itemset(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        self.hash_table[hash_index] += 1

    def get_itemset_count(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        return self.hash_table[hash_index]

def generateCandidateItemsets(level_k, level_frequent_itemsets):

    n_frequent_itemsets = len(level_frequent_itemsets)
    candidate_frequent_itemsets = []

    for i in range(n_frequent_itemsets):
        j = i+1
        while (j<n_frequent_itemsets) and (level_frequent_itemsets[i][:level_k-1] == level_frequent_itemsets[j][:level_k-1]):
            candidate_itemset = level_frequent_itemsets[i][:level_k-1] + [level_frequent_itemsets[i][level_k-1]] + [level_frequent_itemsets[j][level_k-1]]
            candidate_itemset_pass = False

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

if __name__ == '__main__':
    """ Example 4.4: Data Mining - Arjun K Pujari """
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

    # Generate list of all frequent itemsets using Transaction Reduction based Apriori
    frequent_itemsets = aprioriAlgorithm(transactions, min_support_count)

    print("\nFREQUENT ITEMSETS (Min Support Count = {})".format(min_support_count))
    for frequent_itemset in frequent_itemsets:
        print(frequent_itemset)
