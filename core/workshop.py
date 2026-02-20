import os

def parse_info(path):

    mod_id=None
    name=None

    with open(path,encoding="utf8",errors="ignore") as f:
        for line in f:
            line=line.strip()

            if line.startswith("id="):
                mod_id=line.split("=",1)[1].lower()

            elif line.startswith("name="):
                name=line.split("=",1)[1]

    if not mod_id:
        return None

    return mod_id,name or mod_id


# ---------------------------------------------------------

def scan_mods(workshop):

    mods={}
    
    for wid in os.listdir(workshop):

        base=os.path.join(workshop,wid)

        for root,dirs,files in os.walk(base):

            if "mod.info" not in files:
                continue

            info=os.path.join(root,"mod.info")
            data=parse_info(info)

            if not data:
                continue

            mod_id,name=data

            # si ya existe no lo duplicamos
            if mod_id not in mods:
                mods[mod_id]={
                    "name":name,
                    "id":mod_id,
                    "wid":wid
                }

    return list(mods.values())