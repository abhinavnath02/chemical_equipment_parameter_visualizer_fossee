"""
Test script to verify all dependencies are installed correctly
"""
import sys

def test_imports():
    """Test if all required packages can be imported"""
    results = []
    
    # Test PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        results.append(("PyQt5", "✓ OK"))
    except ImportError as e:
        results.append(("PyQt5", f"✗ FAILED: {e}"))
    
    # Test matplotlib
    try:
        import matplotlib
        try:
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        except ImportError:
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        results.append(("matplotlib", "✓ OK"))
    except ImportError as e:
        results.append(("matplotlib", f"✗ FAILED: {e}"))
    
    # Test requests
    try:
        import requests
        results.append(("requests", "✓ OK"))
    except ImportError as e:
        results.append(("requests", f"✗ FAILED: {e}"))
    
    # Test pandas
    try:
        import pandas
        results.append(("pandas", "✓ OK"))
    except ImportError as e:
        results.append(("pandas", f"✗ FAILED: {e}"))
    
    # Print results
    print("=" * 50)
    print("Dependency Check Results")
    print("=" * 50)
    
    all_ok = True
    for package, status in results:
        print(f"{package:15} : {status}")
        if "FAILED" in status:
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("\n✓ All dependencies installed successfully!")
        print("\nYou can now run the application with:")
        print("  python main.py")
        return 0
    else:
        print("\n✗ Some dependencies are missing.")
        print("\nInstall them with:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(test_imports())
