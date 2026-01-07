"""
Simple test to verify local AI setup (without actually running models)
This checks if dependencies are importable
"""

print("=" * 60)
print("FastScribe Local AI Dependency Check")
print("=" * 60)

# Check Whisper
print("\n1. Checking Whisper...")
try:
    import whisper
    print("   ✓ openai-whisper installed")
    print(f"   Available models: {whisper.available_models()}")
except ImportError as e:
    print(f"   ✗ openai-whisper NOT installed: {e}")

# Check PyTorch
print("\n2. Checking PyTorch...")
try:
    import torch
    print(f"   ✓ torch installed (v{torch.__version__})")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    print(f"   Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
except ImportError as e:
    print(f"   ✗ torch NOT installed: {e}")

# Check Transformers
print("\n3. Checking Transformers...")
try:
    import transformers
    print(f"   ✓ transformers installed (v{transformers.__version__})")
except ImportError as e:
    print(f"   ✗ transformers NOT installed: {e}")

# Check Accelerate
print("\n4. Checking Accelerate...")
try:
    import accelerate
    print(f"   ✓ accelerate installed")
except ImportError as e:
    print(f"   ✗ accelerate NOT installed: {e}")

print("\n" + "=" * 60)
print("Dependency Check Complete")
print("=" * 60)

# Estimate disk space needed
print("\nDisk Space Requirements:")
print("  - Whisper base model: ~74 MB")
print("  - TinyLlama-1.1B model: ~1.1 GB")
print("  - PyTorch + dependencies: ~2-3 GB")
print("  - Total: ~4-5 GB")

print("\nMemory Requirements:")
print("  - Whisper base: ~500 MB RAM")
print("  - TinyLlama: ~1.5 GB RAM")
print("  - Recommended: 2GB+ RAM")

print("\nRender Plan Recommendations:")
print("  - Free tier (512MB RAM): ✗ Too small")
print("  - Starter $7/mo (512MB RAM): ✗ Too small")
print("  - Standard $25/mo (2GB RAM): ✓ Should work")
print("  - Pro $85/mo (4GB RAM): ✓ Comfortable")
