class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # buckets for chaining

    def hash_function(self, key):
        return hash(key) % self.size  # map key to index

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        # update value if key already exists
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return True

        # otherwise add new pair
        bucket.append([key, value])
        return True

    def get(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        # find value by key
        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        return None  # key not found

    def delete(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        # search and delete key-value pair
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                return True  # deleted

        return False  # key not found


# test
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))    # 10
print(H.get("orange"))   # 20
print(H.get("banana"))   # 30

print(H.delete("orange"))  # True
print(H.get("orange"))     # None
print(H.delete("orange"))  # False
