import unittest
import os
import sys
import shutil

# Add the parent directory to Python path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.site_manager import SiteManager

class TestSiteManager(unittest.TestCase):
    def setUp(self):
        os.environ['LOCAL_PASSCODE_FOR_SITE_DATA'] = 'test_passcode_123'
        self.site_manager = SiteManager()
        
        # Clean up any existing test data
        if os.path.exists('site/data'):
            shutil.rmtree('site/data')

    def test_build_and_load_site_data(self):
        # Build site data
        self.site_manager.build_site_data()
        
        # Load and verify
        data = self.site_manager.load_site_data()
        
        self.assertIsNotNone(data)
        self.assertIn('site_config', data)
        self.assertIn('content_data', data)  # Changed from 'content' to 'content_data'
        self.assertIn('secrets', data)
        
        # Verify structure
        self.assertEqual(data['site_config']['name'], 'Encrypted Site')
        self.assertEqual(data['content_data']['home']['title'], 'Welcome to Our Secure Site')  # Fixed key

    def tearDown(self):
        # Clean up
        if os.path.exists('site/data'):
            shutil.rmtree('site/data')
        if 'LOCAL_PASSCODE_FOR_SITE_DATA' in os.environ:
            del os.environ['LOCAL_PASSCODE_FOR_SITE_DATA']

if __name__ == '__main__':
    unittest.main()
