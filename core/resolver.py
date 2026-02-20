def resolve_dependencies(active, mods):

    resolved=[]
    seen=set()

    def add(mod):
        if mod in seen:
            return
        seen.add(mod)

        if mod not in mods:
            return

        for dep in mods[mod]["requires"]:
            add(dep)

        resolved.append(mod)

    for m in active:
        add(m)

    return resolved


def sort_load_order(modlist,mods):
    ordered=[]
    temp=set()
    perm=set()

    def visit(n):
        if n in perm:
            return
        if n in temp:
            return
        temp.add(n)

        for d in mods.get(n,{}).get("requires",[]):
            visit(d)

        perm.add(n)
        ordered.append(n)

    for m in modlist:
        visit(m)

    return ordered