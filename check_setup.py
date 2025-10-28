"""Check if all dependencies for new.py are installed"""
import sys

def check_dependencies():
    print("Checking dependencies for new.py...")
    print("-" * 50)
    
    required_packages = {
        'dotenv': 'python-dotenv',
        'moviepy': 'moviepy',
        'assemblyai': 'assemblyai',
        'reportlab': 'reportlab'
    }
    
    missing = []
    
    for module_name, package_name in required_packages.items():
        try:
            if module_name == 'dotenv':
                import dotenv
            elif module_name == 'moviepy':
                import moviepy
            elif module_name == 'assemblyai':
                import assemblyai
            elif module_name == 'reportlab':
                import reportlab
            print(f"✅ {package_name} - Installed")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing.append(package_name)
    
    print("-" * 50)
    
    if missing:
        print("\n⚠️  Missing packages. Install them with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        print("\nTo run new.py, use:")
        print('   python new.py "path/to/your/audio_or_video_file.mp3"')
        return True

if __name__ == "__main__":
    check_dependencies()
