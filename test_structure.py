#!/usr/bin/env python3
"""
Simple test script to verify Jarvis structure without heavy dependencies
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_structure():
    """Test that all files and directories are in place"""
    
    expected_files = [
        'main.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'jarvis/__init__.py',
        'jarvis/core/__init__.py',
        'jarvis/core/bot.py',
        'jarvis/apis/__init__.py',
        'jarvis/apis/voice_handler.py',
        'jarvis/apis/calling_service.py',
        'jarvis/apis/weather_api.py',
        'jarvis/apis/news_api.py',
        'jarvis/utils/__init__.py',
        'jarvis/utils/config.py',
        'jarvis/utils/logger.py',
        'jarvis/plugins/__init__.py',
        'jarvis/plugins/sample_plugin.py',
    ]
    
    print("🔍 Checking project structure...")
    
    all_good = True
    for file_path in expected_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def test_imports():
    """Test basic imports without heavy dependencies"""
    print("\n🔍 Testing basic imports...")
    
    try:
        # Test utils imports
        from jarvis.utils.config import Config
        print("✅ Config import successful")
        
        # Test config functionality
        config = Config()
        bot_name = config.get('bot_name', 'Jarvis')
        print(f"✅ Config test successful - Bot name: {bot_name}")
        
        from jarvis.utils.logger import setup_logger
        print("✅ Logger import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_cli_help():
    """Test that main.py CLI works"""
    print("\n🔍 Testing CLI help...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'main.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'Local Jarvis' in result.stdout:
            print("✅ CLI help works")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Local Jarvis - Project Structure Test\n")
    
    tests = [
        ("Project Structure", test_structure),
        ("Basic Imports", test_imports),
        ("CLI Help", test_cli_help),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Jarvis structure is ready!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Setup configuration: python main.py setup")
        print("3. Test voice: python main.py test-voice")
        print("4. Start Jarvis: python main.py start")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())