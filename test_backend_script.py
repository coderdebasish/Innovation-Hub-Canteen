from canteen_backend import ItemManager, InvoiceGenerator
import os

def test_backend():
    print("Testing Backend...")
    
    # 1. Item Manager
    im = ItemManager()
    print("Saving test item 999...")
    im.save_item("999", "Test Item", 100, 50)
    
    item = im.get_item("999")
    if item and item['name'] == "Test Item":
        print("Item saved and retrieved successfully.")
    else:
        print("Item save/retrieve FAILED.")
        
    # 2. Invoice Gen
    ig = InvoiceGenerator()
    items = [{
        'code': '999',
        'name': 'Test Item',
        'price': 100,
        'qty': 2,
        'total': 200
    }]
    
    print("Generating test invoice...")
    try:
        # We need to ensure templates exist or this will fail. 
        # The user has Templetes/1.docx etc.
        # If they don't exist, this will raise FileNotFoundError.
        # We'll try with a mock template if real ones aren't there, but we expect them to be there.
        path = ig.generate_invoice(items, 0, "Cash")
        print(f"Invoice generated at: {path}")
    except Exception as e:
        print(f"Invoice generation failed: {e}")

    # Cleanup
    # os.remove("Items/999.txt")

if __name__ == "__main__":
    test_backend()
