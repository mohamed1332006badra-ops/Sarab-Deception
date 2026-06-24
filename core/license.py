import hashlib
from datetime import datetime

class LicenseManager:
    def __init__(self, license_file='license.lic'):
        self.license_file = license_file
        self.expiry_date = None
        self.is_valid = False
    
    def validate(self):
        try:
            # Simple simulation of license validation
            self.expiry_date = datetime.now().replace(year=datetime.now().year + 1)
            self.is_valid = True
            return True
        except:
            self.is_valid = False
            return False
    
    def get_status(self):
        return {
            'valid': self.is_valid,
            'expires': self.expiry_date.isoformat() if self.expiry_date else None,
            'days_left': (self.expiry_date - datetime.now()).days if self.expiry_date else 0
        }
