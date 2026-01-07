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
        if api_keys:
            _cycler = APIKeyCycler(api_keys)
        else:
            # Try to load predefined keys
            predefined_keys = [
                'sk-abcdef1234567890abcdef1234567890abcdef12',
                'sk-1234567890abcdef1234567890abcdef12345678',
                'sk-abcdefabcdefabcdefabcdefabcdefabcdef12',
                'sk-7890abcdef7890abcdef7890abcdef7890abcd',
                'sk-1234abcd1234abcd1234abcd1234abcd1234abcd',
                'sk-abcd1234abcd1234abcd1234abcd1234abcd1234',
                'sk-5678efgh5678efgh5678efgh5678efgh5678efgh',
                'sk-efgh5678efgh5678efgh5678efgh5678efgh5678',
                'sk-ijkl1234ijkl1234ijkl1234ijkl1234ijkl1234',
                'sk-mnop5678mnop5678mnop5678mnop5678mnop5678',
                'sk-qrst1234qrst1234qrst1234qrst1234qrst1234',
                'sk-uvwx5678uvwx5678uvwx5678uvwx5678uvwx5678',
                'sk-1234ijkl1234ijkl1234ijkl1234ijkl1234ijkl',
                'sk-5678mnop5678mnop5678mnop5678mnop5678mnop',
                'sk-qrst5678qrst5678qrst5678qrst5678qrst5678',
                'sk-uvwx1234uvwx1234uvwx1234uvwx1234uvwx1234',
                'sk-1234abcd5678efgh1234abcd5678efgh1234abcd',
                'sk-5678ijkl1234mnop5678ijkl1234mnop5678ijkl',
                'sk-abcdqrstefghuvwxabcdqrstefghuvwxabcdqrst',
                'sk-ijklmnop1234qrstijklmnop1234qrstijklmnop',
                'sk-1234uvwx5678abcd1234uvwx5678abcd1234uvwx',
                'sk-efghijkl5678mnopabcd1234efghijkl5678mnop',
                'sk-mnopqrstuvwxabcdmnopqrstuvwxabcdmnopqrst',
                'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop',
                'sk-abcd1234efgh5678abcd1234efgh5678abcd1234',
                'sk-1234ijklmnop5678ijklmnop1234ijklmnop5678',
                'sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh',
                'sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl',
                'sk-abcd5678efgh1234abcd5678efgh1234abcd5678',
                'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop',
                'sk-1234qrstuvwxabcd1234qrstuvwxabcd1234qrst',
                'sk-efghijklmnop5678efghijklmnop5678efghijkl',
                'sk-mnopabcd1234efghmnopabcd1234efghmnopabcd',
                'sk-ijklqrst5678uvwxijklqrst5678uvwxijklqrst',
                'sk-1234ijkl5678mnop1234ijkl5678mnop1234ijkl',
                'sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst',
                'sk-ijklmnopuvwx1234ijklmnopuvwx1234ijklmnop',
                'sk-efgh5678abcd1234efgh5678abcd1234efgh5678',
                'sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst',
                'sk-1234uvwxabcd5678uvwxabcd1234uvwxabcd5678',
                'sk-ijklmnop5678efghijklmnop5678efghijklmnop',
                'sk-abcd1234qrstuvwxabcd1234qrstuvwxabcd1234',
                'sk-1234efgh5678ijkl1234efgh5678ijkl1234efgh',
                'sk-5678mnopqrstuvwx5678mnopqrstuvwx5678mnop',
                'sk-abcdijkl1234uvwxabcdijkl1234uvwxabcdijkl',
                'sk-ijklmnopabcd5678ijklmnopabcd5678ijklmnop',
                'sk-1234efghqrstuvwx1234efghqrstuvwx1234efgh',
                'sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl',
                'sk-abcd1234efgh5678abcd1234efgh5678abcd1234',
                'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop',
            ]
            _cycler = APIKeyCycler(predefined_keys)
    return _cycler


def get_next_api_key():
    """Convenience function to get next API key"""
    cycler = get_api_key_cycler()
    return cycler.get_next_key()
