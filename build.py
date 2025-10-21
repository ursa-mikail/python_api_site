#!/usr/bin/env python3
"""
Build script for encrypted site data
"""
from app.site_manager import SiteManager

def main():
    print("🔐 Building encrypted site data...")
    
    site_manager = SiteManager()
    site_manager.build_site_data()
    
    # Verify the data can be decrypted
    print("\n🔓 Verifying encryption...")
    decrypted_data = site_manager.view_decrypted_data()
    
    if decrypted_data:
        print("\n✅ Build completed successfully!")
    else:
        print("\n❌ Build failed!")

if __name__ == '__main__':
    main()
