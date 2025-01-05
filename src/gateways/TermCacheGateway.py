import os
import tempfile
import json
import logging
LOGGER = logging.getLogger(__name__)

class TermCacheGateway:
    def __init__(self):        
        self.term_cache_file = os.path.join(tempfile.gettempdir(), 'term_cache.txt')
        if not os.path.exists(self.term_cache_file):
            with open(self.term_cache_file, 'w') as f:
                json.dump({}, f)                
        self.term_cache = self.load_cache()

    def load_cache(self):        
        LOGGER.info(f"Loading term cache from {self.term_cache_file}")
        with open(self.term_cache_file, 'r') as f:
            return json.load(f)
        
    def save_cache(self):
        with open(self.term_cache_file, 'w') as f:
            json.dump(self.term_cache, f)

    def get_term(self, term):
        return self.term_cache.get(term, None)

    def delete_term(self, term):
        if term in self.term_cache:
            del self.term_cache[term]
            self.save_cache()

    def set_term(self, term, definition):
        self.term_cache[term] = definition        
        self.save_cache()