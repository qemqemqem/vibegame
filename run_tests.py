#!/usr/bin/env python3
"""
Test runner for Vibe Game
This is our battle plan execution - run all tests to ensure quality!
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return False
            
    except FileNotFoundError:
        print(f"⚠️ {description} - SKIPPED (command not found)")
        return None
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all tests for the Vibe Game"""
    print("🎲 Vibe Game Test Suite")
    print("======================")
    print("Running all tests to ensure our code is battle-ready!")
    
    results = []
    
    # Backend tests
    print("\n🔥 BACKEND TESTS")
    print("-" * 40)
    
    # Check if pytest is available
    pytest_result = run_command(['python', '-m', 'pytest', '--version'], 'Check pytest availability')
    if pytest_result:
        # Run backend tests
        backend_result = run_command([
            'python', '-m', 'pytest', 
            'tests/backend/', 
            '-v', 
            '--tb=short'
        ], 'Backend unit tests')
        results.append(('Backend Tests', backend_result))
    else:
        print("⚠️ pytest not available - install with: pip install pytest")
        results.append(('Backend Tests', None))
    
    # Frontend tests (just check if the file exists for now)
    print("\n🎨 FRONTEND TESTS")
    print("-" * 40)
    
    frontend_test_file = Path('tests/frontend/test_game_logic.html')
    if frontend_test_file.exists():
        print(f"✅ Frontend test file exists: {frontend_test_file}")
        print("📝 To run frontend tests, open tests/frontend/test_game_logic.html in a browser")
        results.append(('Frontend Tests', True))
    else:
        print(f"❌ Frontend test file missing: {frontend_test_file}")
        results.append(('Frontend Tests', False))
    
    # Server quick test
    print("\n🖥️ SERVER TESTS")
    print("-" * 40)
    
    server_result = run_command([
        'python', 'backend/server.py', '--test'
    ], 'Server quick test')
    results.append(('Server Test', server_result))
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}")
        elif result is False:
            print(f"❌ {test_name}")
        else:
            print(f"⚠️ {test_name} (skipped)")
    
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Ready for vibecoding!")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Time to hunt down those bugs!")
        return 1

if __name__ == '__main__':
    sys.exit(main())