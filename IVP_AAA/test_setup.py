#!/usr/bin/env python3
"""
Test script to verify IVP AI Photographer Analyzer setup
"""

import os
import sys
import json
import importlib.util

def test_python_dependencies():
    """Test if all required Python packages are installed"""
    print("Testing Python dependencies...")
    
    required_packages = [
        'cv2', 'numpy', 'PIL', 'google.generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'numpy':
                import numpy
            elif package == 'PIL':
                from PIL import Image
            elif package == 'google.generativeai':
                import google.generativeai as genai
            print(f"OK {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"X {package} - Missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_ivp_modules():
    """Test if IVP modules can be loaded"""
    print("\nTesting IVP modules...")
    
    ivp_modules_path = "IVP_Modules"
    if not os.path.exists(ivp_modules_path):
        print("X IVP_Modules directory not found")
        return False
    
    module_files = [f for f in os.listdir(ivp_modules_path) if f.endswith('.py')]
    print(f"Found {len(module_files)} IVP modules")
    
    # Test loading a few modules
    test_modules = module_files[:3]  # Test first 3 modules
    
    for module_file in test_modules:
        try:
            module_path = os.path.join(ivp_modules_path, module_file)
            spec = importlib.util.spec_from_file_location(module_file[:-3], module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"OK {module_file}")
        except Exception as e:
            print(f"X {module_file} - Error: {str(e)}")
    
    return True

def test_config_files():
    """Test if configuration files exist and are valid"""
    print("\nTesting configuration files...")
    
    # Test Topic.json
    try:
        with open('Topic.json', 'r') as f:
            topics = json.load(f)
        if 'Image_Topics' in topics and 'Video_Topics' in topics:
            print("OK Topic.json - Valid")
        else:
            print("X Topic.json - Invalid structure")
            return False
    except Exception as e:
        print(f"X Topic.json - Error: {str(e)}")
        return False
    
    # Test Analyser.json
    try:
        with open('Analyser.json', 'r') as f:
            analyser = json.load(f)
        if isinstance(analyser, list):
            print("OK Analyser.json - Valid")
        else:
            print("X Analyser.json - Invalid structure")
            return False
    except Exception as e:
        print(f"X Analyser.json - Error: {str(e)}")
        return False
    
    return True

def test_gemini_api():
    """Test Gemini API configuration"""
    print("\nTesting Gemini API configuration...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
        print("X GEMINI_API_KEY not set")
        print("Set it with: export GEMINI_API_KEY=your_api_key_here")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        print("OK Gemini API configured")
        return True
    except Exception as e:
        print(f"X Gemini API error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("IVP AI Photographer Analyzer - Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_dependencies,
        test_ivp_modules,
        test_config_files,
        test_gemini_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("OK All tests passed! Setup is complete.")
        print("\nTo start the application:")
        print("  Windows: start.bat")
        print("  Linux/Mac: ./start.sh")
        print("  Manual: npm start")
    else:
        print("X Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
