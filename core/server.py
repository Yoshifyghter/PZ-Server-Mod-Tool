import os

def list_servers():
    path=os.path.join(os.environ["USERPROFILE"],"Zomboid","Server")
    if not os.path.exists(path):
        return []

    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".ini")]


def read_mods(path):

    with open(path,encoding="utf8",errors="ignore") as f:
        for line in f:

            if line.startswith("Mods="):

                raw=line.split("=",1)[1].strip()

                mods=[]

                for m in raw.split(";"):
                    m=m.strip().lower()

                    # limpiar slash inicial
                    if m.startswith("\\"):
                        m=m[1:]

                    if m:
                        mods.append(m)

                return mods

    return []


def write_workshop(ini,ids):

    lines=open(ini,encoding="utf8",errors="ignore").readlines()

    for i,l in enumerate(lines):
        if l.startswith("WorkshopItems="):
            lines[i]="WorkshopItems="+(";".join(ids))+"\n"
            break
    else:
        lines.append("\nWorkshopItems="+(";".join(ids))+"\n")

    open(ini,"w",encoding="utf8").writelines(lines)