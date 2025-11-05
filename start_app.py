#!/usr/bin/env python3
"""
Startup script that ensures everything is set up correctly before starting the app
"""
import os
import sys

def setup_and_start():
    """Set up directories and start the app"""

    print("🚀 CalorieApp Startup")
    print("=" * 50)

    # 1. Ensure instance directory exists
    print("📁 Creating instance directory...")
    os.makedirs('instance', exist_ok=True)
    print("   ✅ Instance directory ready")

    # 2. Check if database exists
    db_path = 'instance/calorie_tracker.db'
    if os.path.exists(db_path):
        print(f"✅ Database found at {db_path} ({os.path.getsize(db_path)} bytes)")
    else:
        print(f"📝 Database will be created at {db_path}")

    # 3. Start the Flask app
    print("\n🌟 Starting Flask app...")
    print("=" * 50)

    # Import and run the app
    from app import app
    app.run(host='0.0.0.0', port=5151, debug=True)

if __name__ == "__main__":
    try:
        setup_and_start()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
