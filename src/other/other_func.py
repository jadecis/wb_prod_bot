from loader import db

def filter_cat(rm_cat):
    catalog=[]
    res= db.get_catalog_ids()
    for i in res:
        if i["wb_id"] not in rm_cat:
            catalog.append(i["wb_id"])
            
    return catalog