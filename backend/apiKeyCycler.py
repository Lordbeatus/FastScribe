"""
API Key Cycler for OpenAI
Rotates through multiple API keys to distribute load and avoid rate limits
"""

import threading
import os


class APIKeyCycler:
    """Thread-safe API key rotation manager"""
    
    def __init__(self, api_keys=None):
        """
        Initialize with list of API keys
        Args:
            api_keys: List of API keys, or None to load from environment
        """
        if api_keys:
            self.api_keys = api_keys
        else:
            # Load from environment variable (comma-separated)
            keys_str = os.getenv('OPENAI_API_KEYS', '')
            if keys_str:
                self.api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
            else:
                # Fallback to single key
                single_key = os.getenv('OPENAI_API_KEY')
                self.api_keys = [single_key] if single_key else []
        
        if not self.api_keys:
            raise ValueError("No API keys provided. Set OPENAI_API_KEYS or OPENAI_API_KEY environment variable.")
        
        self.current_index = 0
        self.lock = threading.Lock()
        print(f"API Key Cycler initialized with {len(self.api_keys)} key(s)")
    
    def get_next_key(self):
        """Get next API key in rotation (thread-safe)"""
        with self.lock:
            key = self.api_keys[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.api_keys)
            return key
    
    def get_key_count(self):
        """Return total number of keys"""
        return len(self.api_keys)


# Global instance
_cycler = None


def get_api_key_cycler(api_keys=None):
    """Get or create global API key cycler instance"""
    global _cycler
    if _cycler is None:
        _cycler = APIKeyCycler(api_keys)
    return _cycler


def get_next_api_key():
    """Convenience function to get next key from global cycler"""
    cycler = get_api_key_cycler()
    return cycler.get_next_key()



def get_next_api_key():
    """Convenience function to get next API key"""
    cycler = get_api_key_cycler()
    return cycler.get_next_key()
