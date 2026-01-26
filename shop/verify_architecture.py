"""
Architecture Verification Script
Tests to ensure the project follows Model-DAO-View-Template architecture
"""
import os
import sys
import re
from pathlib import Path

# Add shop directory to path
sys.path.insert(0, '/home/quocdai/Software-Analysis-Design/shop')

def check_architecture():
    """Verify the architecture is correctly implemented"""
    
    results = {
        'passed': [],
        'failed': []
    }
    
    print("=" * 60)
    print("ARCHITECTURE VERIFICATION")
    print("=" * 60)
    
    # Test 1: Check models exist and are separate
    print("\n[1] Checking Model Layer...")
    models_dir = Path('/home/quocdai/Software-Analysis-Design/shop/core/models')
    required_models = ['customer.py', 'book.py', 'cart.py', 'cart_item.py']
    
    for model in required_models:
        model_path = models_dir / model
        if model_path.exists():
            results['passed'].append(f"✓ Model file exists: {model}")
            print(f"  ✓ {model} exists")
        else:
            results['failed'].append(f"✗ Model file missing: {model}")
            print(f"  ✗ {model} MISSING")
    
    # Test 2: Check DAO layer exists
    print("\n[2] Checking DAO Layer...")
    dao_dir = Path('/home/quocdai/Software-Analysis-Design/shop/core/dao')
    required_daos = ['book_dao.py', 'customer_dao.py', 'cart_dao.py']
    
    for dao in required_daos:
        dao_path = dao_dir / dao
        if dao_path.exists():
            results['passed'].append(f"✓ DAO file exists: {dao}")
            print(f"  ✓ {dao} exists")
        else:
            results['failed'].append(f"✗ DAO file missing: {dao}")
            print(f"  ✗ {dao} MISSING")
    
    # Test 3: Check views don't use ORM directly
    print("\n[3] Checking Views Layer (No direct ORM calls)...")
    views_path = Path('/home/quocdai/Software-Analysis-Design/shop/core/views.py')
    
    if views_path.exists():
        with open(views_path, 'r') as f:
            views_content = f.read()
        
        # Check for direct ORM usage patterns
        orm_patterns = [
            r'Book\.objects\.',
            r'Customer\.objects\.',
            r'Cart\.objects\.',
            r'CartItem\.objects\.'
        ]
        
        found_orm_in_views = False
        for pattern in orm_patterns:
            # Allow imports and DAO usage
            if re.search(pattern, views_content):
                # Check if it's not in an import or DAO
                matches = re.finditer(pattern, views_content)
                for match in matches:
                    # Get line context
                    line_start = views_content.rfind('\n', 0, match.start()) + 1
                    line_end = views_content.find('\n', match.start())
                    line = views_content[line_start:line_end]
                    
                    # Skip if it's in a DAO or import
                    if 'from' not in line and 'import' not in line:
                        found_orm_in_views = True
        
        if not found_orm_in_views:
            results['passed'].append("✓ Views don't use ORM directly")
            print("  ✓ No direct ORM calls in views.py")
        else:
            results['failed'].append("✗ Views use ORM directly")
            print("  ✗ Views contain direct ORM calls")
    
    # Test 4: Check DAO methods are static
    print("\n[4] Checking DAO Methods are Static...")
    for dao_file in required_daos:
        dao_path = dao_dir / dao_file
        if dao_path.exists():
            with open(dao_path, 'r') as f:
                dao_content = f.read()
            
            # Check for @staticmethod
            if '@staticmethod' in dao_content:
                results['passed'].append(f"✓ {dao_file} uses @staticmethod")
                print(f"  ✓ {dao_file} uses @staticmethod")
            else:
                results['failed'].append(f"✗ {dao_file} missing @staticmethod")
                print(f"  ✗ {dao_file} missing @staticmethod")
    
    # Test 5: Check templates exist
    print("\n[5] Checking Template Layer...")
    templates_dir = Path('/home/quocdai/Software-Analysis-Design/shop/core/templates/core')
    required_templates = ['books.html', 'cart.html', 'login.html', 'register.html']
    
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            results['passed'].append(f"✓ Template exists: {template}")
            print(f"  ✓ {template} exists")
        else:
            results['failed'].append(f"✗ Template missing: {template}")
            print(f"  ✗ {template} MISSING")
    
    # Test 6: Check URLs are properly configured
    print("\n[6] Checking URL Routing...")
    urls_path = Path('/home/quocdai/Software-Analysis-Design/shop/core/urls.py')
    
    if urls_path.exists():
        with open(urls_path, 'r') as f:
            urls_content = f.read()
        
        required_urls = [
            'register',
            'login',
            'book_list',
            'cart_view',
            'add_to_cart'
        ]
        
        for url in required_urls:
            if f"name='{url}'" in urls_content:
                results['passed'].append(f"✓ URL route exists: {url}")
                print(f"  ✓ {url} route exists")
            else:
                results['failed'].append(f"✗ URL route missing: {url}")
                print(f"  ✗ {url} route MISSING")
    
    # Test 7: Check migrations exist
    print("\n[7] Checking Database Migrations...")
    migrations_dir = Path('/home/quocdai/Software-Analysis-Design/shop/core/migrations')
    
    if migrations_dir.exists() and (migrations_dir / '0001_initial.py').exists():
        results['passed'].append("✓ Migrations created")
        print("  ✓ Migrations created")
    else:
        results['failed'].append("✗ Migrations missing")
        print("  ✗ Migrations MISSING")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Passed: {len(results['passed'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\nFailed Tests:")
        for fail in results['failed']:
            print(f"  {fail}")
    
    print("\n" + "=" * 60)
    
    return len(results['failed']) == 0


if __name__ == '__main__':
    success = check_architecture()
    sys.exit(0 if success else 1)
