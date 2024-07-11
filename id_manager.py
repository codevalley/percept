# id_manager.py

import random
from pymongo.errors import DuplicateKeyError

class IDManager:
    def __init__(self, db, collection_name='id_reserve', min_reserve=1000):
        self.db = db
        self.reserve = self.db[collection_name]
        self.min_reserve = min_reserve

    def initialize_reserve(self, word_list):
        """Initialize the reserve with a list of words."""
        self.reserve.insert_many([{'_id': word, 'status': 'available'} for word in word_list], ordered=False)
        self.replenish_if_needed()

    def get_ids(self, count=1, preferred=None):
        """Get a list of available IDs, including preferred if available."""
        ids = []
        if preferred and self.is_id_available(preferred):
            ids.append(preferred)
            count -= 1

        cursor = self.reserve.find({'status': 'available'}).limit(count)
        ids.extend([doc['_id'] for doc in cursor])

        self.replenish_if_needed()
        return ids

    def mark_id_as_used(self, id):
        """Mark an ID as used."""
        self.reserve.update_one({'_id': id}, {'$set': {'status': 'used'}})

    def is_id_available(self, id):
        """Check if an ID is available."""
        doc = self.reserve.find_one({'_id': id})
        return doc is not None and doc.get('status') == 'available'

    def add_custom_id(self, id):
        """Add a custom ID to the reserve and mark it as used."""
        try:
            self.reserve.insert_one({'_id': id, 'status': 'used'})
        except DuplicateKeyError:
            # If the ID already exists, just mark it as used
            self.mark_id_as_used(id)

    def replenish_if_needed(self):
        """Replenish the reserve if it's running low."""
        available_count = self.reserve.count_documents({'status': 'available'})
        if available_count < self.min_reserve:
            self.replenish_reserve(self.min_reserve - available_count)

    def replenish_reserve(self, count):
        """Add new IDs to the reserve."""
        new_ids = self.generate_new_ids(count)
        self.reserve.insert_many([{'_id': id, 'status': 'available'} for id in new_ids], ordered=False)

    def generate_new_ids(self, count):
        """Generate new unique IDs. Implement your word combination logic here."""
        # This is a placeholder. Replace with your actual word combination logic.
        adjectives = ['happy', 'brave', 'calm', 'kind', 'wise', 'clever', 'bold', 'eager']
        nouns = ['fox', 'owl', 'bear', 'wolf', 'eagle', 'lion', 'tiger', 'deer']
        new_ids = set()
        while len(new_ids) < count:
            new_id = f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(1, 999)}"
            if not self.reserve.find_one({'_id': new_id}):
                new_ids.add(new_id)
        return list(new_ids)

# Usage in your main application:
# id_manager = IDManager(mongo.db)
# id_manager.initialize_reserve(your_initial_word_list)

# To get new IDs:
# new_ids = id_manager.get_ids(count=5, preferred='desired-id')

# To mark an ID as used:
# id_manager.mark_id_as_used(chosen_id)

# To check if an ID is available:
# is_available = id_manager.is_id_available(some_id)

# To add a custom ID:
# id_manager.add_custom_id('custom-user-id')