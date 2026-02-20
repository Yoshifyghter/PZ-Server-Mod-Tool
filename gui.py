import tkinter as tk
import os
from tkinter import messagebox
from core import steam, workshop, server

BG="#1e1f22"
PANEL="#2b2d31"
HEADER="#313338"
LINE="#3f4147"
BTN="#3a3d42"
BTN_HOVER="#4b4f56"
TXT="#e6e6e6"
ASSETS="assets"

FONT=("Segoe UI",10)
FONT_B=("Segoe UI",10,"bold")
MONO=("Consolas",10)

def blend(c1,c2,t):
    c1=[int(c1[i:i+2],16) for i in (1,3,5)]
    c2=[int(c2[i:i+2],16) for i in (1,3,5)]
    mix=[int(a+(b-a)*t) for a,b in zip(c1,c2)]
    return "#"+"".join(f"{v:02x}" for v in mix)

class HoverButton(tk.Button):
    def __init__(self,master,**kw):
        super().__init__(master,**kw)
        self.base=self["bg"]
        self.bind("<Enter>",self.fade_in)
        self.bind("<Leave>",self.fade_out)

    def fade_in(self,e=None):
        self.config(bg=BTN_HOVER)

    def fade_out(self,e=None):
        self.config(bg=self.base)

class App:

    def __init__(self,root):

        self.root=root
        root.title("PZ Server Mod Tool")
        root.geometry("780x780")
        root.configure(bg=BG)
        root.resizable(False,False)

        # ---------- ICONOS ----------
        self.icons={}
        def load(name):
            path=os.path.join(ASSETS,name)
            return tk.PhotoImage(file=path)

        try:
            self.icons["scan"]=load("scan.png")
            self.icons["sync"]=load("sync.png")
        except:
            pass

        try:
            root.iconbitmap(os.path.join(ASSETS,"app.ico"))
        except:
            pass

        self.mods=[]
        self.servers=[]
        self.server_mod_ids=[]

        # TOP
        top=tk.Frame(root,bg=BG)
        top.pack(pady=12)

        HoverButton(
            top,
            text=" Escanear Mods",
            image=self.icons.get("scan"),
            compound="left",
            bg=BTN,fg=TXT,font=FONT,relief="flat",
            padx=14,pady=4,
            command=self.scan
        ).pack(side=tk.LEFT,padx=6)

        HoverButton(
            top,
            text=" Generar WorkshopIDs",
            image=self.icons.get("sync"),
            compound="left",
            bg=BTN,fg=TXT,font=FONT,relief="flat",
            padx=14,pady=4,
            command=self.generate
        ).pack(side=tk.LEFT,padx=6)

        # HEADER
        header_frame=tk.Frame(root,bg=BG)
        header_frame.pack(fill="x",padx=12)

        self.header=tk.Label(header_frame,bg=HEADER,fg=TXT,font=FONT_B,anchor="w")
        self.header.pack(fill="x")

        tk.Frame(root,height=1,bg=LINE).pack(fill="x",padx=12,pady=(0,6))

        # LISTA MODS
        frame=tk.Frame(root,bg=PANEL)
        frame.pack(padx=12)

        scrollbar=tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.modsbox=tk.Listbox(frame,width=110,height=15,
                                yscrollcommand=scrollbar.set,
                                font=MONO,bg=PANEL,fg=TXT,
                                selectbackground="#50545c",
                                bd=0,highlightthickness=0)
        self.modsbox.pack(side=tk.LEFT)
        scrollbar.config(command=self.modsbox.yview)

        # SERVERS
        tk.Label(root,text="Servers",bg=BG,fg=TXT,font=FONT_B).pack(pady=(12,0))

        self.serverbox=tk.Listbox(root,width=40,height=5,font=FONT,
                                  bg=PANEL,fg=TXT,
                                  selectbackground="#50545c",
                                  bd=0)
        self.serverbox.pack()
        self.serverbox.bind("<<ListboxSelect>>",self.load_server_mods)

        # HEADER SERVER
        server_header_frame=tk.Frame(root,bg=BG)
        server_header_frame.pack(fill="x",padx=12,pady=(12,0))

        self.serverheader=tk.Label(server_header_frame,bg=HEADER,fg=TXT,font=FONT_B,anchor="w")
        self.serverheader.pack(fill="x")

        tk.Frame(root,height=1,bg=LINE).pack(fill="x",padx=12,pady=(0,6))

        # SERVER LIST
        self.servermods=tk.Listbox(root,width=110,height=10,font=MONO,
                                   bg=PANEL,fg=TXT,
                                   selectbackground="#50545c",
                                   bd=0)
        self.servermods.pack(padx=12)

        # LOG
        self.log=tk.Text(root,width=110,height=7,font=("Consolas",9),
                         bg=PANEL,fg=TXT,bd=0)
        self.log.pack(padx=12,pady=12)

    # ------------------------------------------------

    def normalize(self,text):
        return text.strip().lower()

    def write(self,msg):
        self.log.insert(tk.END,msg+"\n")
        self.log.see(tk.END)

    # ------------------------------------------------

    def scan(self):

        self.modsbox.delete(0,tk.END)
        self.serverbox.delete(0,tk.END)
        self.servermods.delete(0,tk.END)
        self.log.delete(1.0,tk.END)

        self.write("Buscando Workshop...")

        work=steam.find_workshop()
        if not work:
            self.write("No se encontró workshop")
            return

        self.mods=workshop.scan_mods(work)

        for m in self.mods:
            m["id"]=self.normalize(m["id"])

        self.render_mod_list()

        self.servers=server.list_servers()
        for s in self.servers:
            self.serverbox.insert(tk.END,s.split("\\")[-1])

    # ------------------------------------------------

    def render_mod_list(self):

        if not self.mods:
            return

        id_w=max(len(m["id"]) for m in self.mods)
        wid_w=max(len(m["wid"]) for m in self.mods)
        name_w=40

        header=f"{'Mod Name':<{name_w}} | {'Mod ID':<{id_w}} | {'Workshop ID':<{wid_w}}"
        self.header.config(text=header)

        self.modsbox.delete(0,tk.END)

        for m in sorted(self.mods,key=lambda x:x["name"].lower()):
            name=m["name"][:name_w]
            self.modsbox.insert(tk.END,f"{name:<{name_w}} | {m['id']:<{id_w}} | {m['wid']:<{wid_w}}")

    # ------------------------------------------------

    def load_server_mods(self,event):

        if not self.serverbox.curselection():
            return

        index=self.serverbox.curselection()[0]
        ini=self.servers[index]

        mods_server=server.read_mods(ini)
        self.server_mod_ids=[self.normalize(m) for m in mods_server]

        id_w=max(len(m["id"]) for m in self.mods)
        wid_w=max(len(m["wid"]) for m in self.mods)
        name_w=40

        header=f"{'Mod Name':<{name_w}} | {'Mod ID':<{id_w}} | {'Workshop ID':<{wid_w}}"
        self.serverheader.config(text=header)

        self.servermods.delete(0,tk.END)

        for smod in self.server_mod_ids:

            name="UNKNOWN"
            wid="NO LOCAL"

            for m in self.mods:
                if m["id"]==smod:
                    name=m["name"]
                    wid=m["wid"]
                    break

            self.servermods.insert(tk.END,f"{name:<{name_w}} | {smod:<{id_w}} | {wid:<{wid_w}}")

    # ------------------------------------------------

    def generate(self):

        if not self.serverbox.curselection():
            messagebox.showwarning("Error","Selecciona un server")
            return

        index=self.serverbox.curselection()[0]
        ini=self.servers[index]

        ids=[]
        missing=[]

        for smod in self.server_mod_ids:
            for m in self.mods:
                if m["id"]==smod:
                    ids.append(m["wid"])
                    break
            else:
                missing.append(smod)

        server.write_workshop(ini,ids)

        messagebox.showinfo(
            "Listo",
            f"WorkshopItems actualizado\n\nEncontrados: {len(ids)}\nFaltantes: {len(missing)}"
        )