import sys
import os

sys.path.append(os.getcwd())

try:
    print("Importing backend.fastapi_app...")
    from backend import fastapi_app
    print("Successfully imported backend.fastapi_app")
except Exception as e:
    print(f"Error importing backend: {e}")
    import traceback
    traceback.print_exc()
