import random
import nltk
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo.errors import DuplicateKeyError
import time
import re
import os

nltk.download('words', quiet=False)
nltk.download('wordnet', quiet=False)
nltk.download('vader_lexicon', quiet=False)

MIN_LEMMA_LEN = 3
MAX_LEMMA_LEN = 10
MIN_ID_LEN = 5
ID_VALID_PATTERN = re.compile(r'^[a-zA-Z0-9-]+$')
RESERVE_TIMEOUT = 3600  # 1 hour

nltk.data.path.append(os.environ.get('NLTK_DATA', '/workspace/nltk_data'))

class IDManager:
    def __init__(self, db, collection_name='id_reserve', min_reserve=20, reservation_timeout=RESERVE_TIMEOUT):
        self.db = db
        self.reserve = self.db[collection_name]
        self.min_reserve = min_reserve
        self.reservation_timeout = reservation_timeout
        self.sia = SentimentIntensityAnalyzer()
    
    def initialize_reserve(self, count=100):
        """Initialize the reserve with a given count of generated IDs."""
        new_ids = self.generate_new_ids(count)
        print(new_ids)
        self.reserve.insert_many([{'_id': id, 'status': 'available'} for id in new_ids], ordered=False)
    
    def get_ids(self, count=1, preferred=None):
        """Get a list of available IDs, automatically reserving them."""
        self.cleanup_expired_reservations()
        ids = []
        
        if preferred and self.is_id_available(preferred):
            self._reserve_id(preferred)
            ids.append(preferred)
            count -= 1

        cursor = self.reserve.find({'status': 'available'}).limit(count)
        for doc in cursor:
            id = doc['_id']
            if self._reserve_id(id):
                ids.append(id)

        self.replenish_if_needed()
        return ids

    def _reserve_id(self, id):
        """Internally reserve an ID."""
        result = self.reserve.update_one(
            {'_id': id, 'status': 'available'},
            {'$set': {
                'status': 'reserved',
                'reserved_at': time.time()
            }}
        )
        return result.modified_count > 0

    def mark_id_as_used(self, id):
        """Mark an ID as used, whether it was reserved or available."""
        result = self.reserve.update_one(
            {'_id': id, 'status': {'$in': ['available', 'reserved']}},
            {'$set': {'status': 'used'}, '$unset': {'reserved_at': ''}}
        )
        return result.modified_count > 0

    def get_id(self):
        """Get a single available ID and mark it as used."""
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

    def cleanup_expired_reservations(self):
        """Clean up expired reservations."""
        expired_time = time.time() - self.reservation_timeout
        self.reserve.update_many(
            {'status': 'reserved', 'reserved_at': {'$lt': expired_time}},
            {'$set': {'status': 'available'}, '$unset': {'reserved_at': ''}}
        )

    def is_id_available(self, id, include_reserved=False):
        """
        Check if an ID is available and has a valid format.
        
        Args:
            id (str): The ID to check.
            include_reserved (bool): If True, consider reserved IDs as available.
        
        Returns:
            bool: True if the ID is available (and valid), False otherwise.
        """
        if not self.is_valid_id_format(id):
            return False
        self.cleanup_expired_reservations()
        doc = self.reserve.find_one({'_id': id})
        if doc is None:
            return True
        if include_reserved:
            app.logger.warning(f"Checking on both reserved & available")
            return doc['status'] in ['available', 'reserved']
        app.logger.warning(f"Checking only on available")
        return doc['status'] == 'available'
        
    def is_valid_id_format(self, id):
        """Check if the ID has a valid format."""
        return (
            isinstance(id, str) and
            len(id) >= MIN_ID_LEN and
            ID_VALID_PATTERN.match(id) is not None
        )

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