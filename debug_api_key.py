#!/usr/bin/env python3
"""
Quick API Key Debug Helper
Compares the working .env key with the key you're trying to use in the browser
"""

import os

def debug_api_key():
    print("🔍 API Key Debug Helper")
    print("=" * 40)
    
    # Get the working key from .env
    env_key = os.getenv('ANTHROPIC_API_KEY')
    
    if env_key:
        print(f"✅ Working .env key found:")
        print(f"   Length: {len(env_key)} characters")
        print(f"   Starts with: {env_key[:15]}...")
        print(f"   Format: {'✅ Valid' if env_key.startswith('sk-ant-api') else '❌ Invalid'}")
        print()
        
        # Ask user to paste their browser key
        print("📋 Paste the key you're trying to use in the browser:")
        browser_key = input().strip()
        
        if browser_key:
            print(f"\n🔍 Browser key analysis:")
            print(f"   Length: {len(browser_key)} characters")
            print(f"   Starts with: {browser_key[:15]}...")
            print(f"   Format: {'✅ Valid' if browser_key.startswith('sk-ant-api') else '❌ Invalid'}")
            
            # Compare
            if env_key == browser_key:
                print(f"\n✅ KEYS MATCH! The browser key should work.")
            else:
                print(f"\n❌ KEYS DON'T MATCH!")
                print(f"   .env key length: {len(env_key)}")
                print(f"   Browser key length: {len(browser_key)}")
                
                # Check for common issues
                if len(browser_key) != len(env_key):
                    print(f"   ⚠️ Length difference: {abs(len(browser_key) - len(env_key))} characters")
                
                if browser_key.startswith(env_key[:20]):
                    print(f"   ⚠️ Browser key seems to start correctly but differs later")
                elif env_key.startswith(browser_key[:20]):
                    print(f"   ⚠️ Browser key seems incomplete")
                else:
                    print(f"   ⚠️ Keys are completely different")
        else:
            print("\n❌ No browser key provided")
    else:
        print("❌ No API key found in .env file")
        print("   Make sure you have ANTHROPIC_API_KEY=... in your .env file")

if __name__ == "__main__":
    debug_api_key()