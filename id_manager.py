# id_manager.py

import random
import nltk
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo.errors import DuplicateKeyError

nltk.download('words', quiet=True)
nltk.download('vader_lexicon', quiet=True)

MIN_LEMMA_LEN = 3
MAX_LEMMA_LEN = 10

class IDManager:
    def __init__(self, db, collection_name='id_reserve', min_reserve=1000):
        self.db = db
        self.reserve = self.db[collection_name]
        self.min_reserve = min_reserve
        self.sia = SentimentIntensityAnalyzer()
    
    def initialize_reserve(self, count=1000):
        """Initialize the reserve with a given count of generated IDs."""
        new_ids = self.generate_new_ids(count)
        print(new_ids)
        self.reserve.insert_many([{'_id': id, 'status': 'available'} for id in new_ids], ordered=False)
    
    def get_id(self):
        """Get a single available ID from the reserve."""
        id_doc = self.reserve.find_one_and_update(
            {'status': 'available'},
            {'$set': {'status': 'used'}},
            return_document=True
        )
        if id_doc:
            self.replenish_if_needed()
            return id_doc['_id']
        else:
            raise Exception("No available IDs in the reserve")

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
        if doc is None:
            # ID is not in the reserve, so it's available
            return True
        # If the ID is in the reserve, it's available only if its status is 'available'
        return doc['status'] == 'available'

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
        print(new_ids)
        self.reserve.insert_many([{'_id': id, 'status': 'available'} for id in new_ids], ordered=False)

    def generate_new_ids(self, count):
        """Generate new unique IDs using noun-adjective combinations."""
        new_ids = set()
        attempts = 0
        max_attempts = 5  # Maximum number of attempts to generate required IDs

        while len(new_ids) < count and attempts < max_attempts:
            # Generate more combinations than needed to increase chances of finding unique IDs
            combinations = self.generate_noun_adjective_pairs(count * 2)
            
            # Check which combinations are not in the database and add them to new_ids
            existing_ids = set(doc['_id'] for doc in self.reserve.find({'_id': {'$in': combinations}}))
            new_ids.update(set(combinations) - existing_ids)

            # If we have enough IDs, break the loop
            if len(new_ids) >= count:
                break

            attempts += 1

        if len(new_ids) == 0:
            raise ValueError(f"Unable to generate any unique IDs after {max_attempts} attempts")

        if len(new_ids) < count:
            print(f"Warning: Only generated {len(new_ids)} unique IDs out of {count} requested")

        return list(new_ids)[:count]

    def generate_noun_adjective_pairs(self, count=100):
        """Generate multiple noun-adjective pairs using WordNet."""
        adj_count = min(count, 20)  # Number of adjectives to fetch
        noun_count = min(count, 20)  # Number of nouns to fetch
        
        adjectives = [self.get_random_lemma(wn.ADJ) for _ in range(adj_count)]
        nouns = [self.get_random_lemma(wn.NOUN) for _ in range(noun_count)]
        
        combinations = [
            f"{adj}-{noun}" for adj in adjectives for noun in nouns
            if self.is_safe_word(f"{adj}-{noun}")
        ]
        
        # Shuffle the combinations and return up to the requested count
        random.shuffle(combinations)
        return combinations[:count]

    def get_random_lemma(self, pos):
        """Get a random lemma from WordNet."""
        while True:
            words = list(wn.all_synsets(pos))
            word = random.choice(words).lemmas()[0].name().replace('_', '-')
            if MIN_LEMMA_LEN <= len(word) <= MAX_LEMMA_LEN:
                return word.lower()

    def is_safe_word(self, word):
        """Check if a word is safe using VADER sentiment analysis."""
        sentiment_score = self.sia.polarity_scores(word)['compound']
        return sentiment_score >= 0

# Usage in your main application:
# id_manager = IDManager(mongo.db)
# id_manager.initialize_reserve()

# To get new IDs:
# new_ids = id_manager.get_ids(count=5, preferred='desired-id')

# To mark an ID as used:
# id_manager.mark_id_as_used(chosen_id)

# To check if an ID is available:
# is_available = id_manager.is_id_available(some_id)

# To add a custom ID:
# id_manager.add_custom_id('custom-user-id')