#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#modules
import modules.internal as internal
from databases.ammolist import all_ammo_list
from databases.itemslist import items_list


#print("[+] Updating Database")
try:
    internal.updatedb_items(items_list)
    internal.updatedb_ammo(all_ammo_list)
    #print("   [+] Update Successfull")
except Exception as e:
    print("[-] Database Update Failed:",e)
    #print("   [-] Update Failed")