import tkinter as tk
from tkinter import messagebox, font


BG        = "#1C1C2E"   
PANEL     = "#252540"   
ACCENT    = "#7C5CBF"   
ACCENT2   = "#A07EE6"   
DELETE_C  = "#E05C7A"   
DELETE_H  = "#F07090"
DONE_C    = "#4CAF8A"   
TEXT_W    = "#EDECF4"   
TEXT_MUT  = "#8A8AAA"   
ENTRY_BG  = "#1A1A30"
BORDER    = "#3A3A60"



class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Todo List")
        self.geometry("520x640")
        self.configure(bg=BG)

        # Fonts
        self.f_title   = font.Font(family="Georgia",      size=22, weight="bold")
        self.f_sub     = font.Font(family="Georgia",      size=10, slant="italic")
        self.f_btn     = font.Font(family="Trebuchet MS", size=10, weight="bold")
        self.f_item    = font.Font(family="Trebuchet MS", size=11)
        self.f_item_st = font.Font(family="Trebuchet MS", size=11, overstrike=True)
        self.f_label   = font.Font(family="Trebuchet MS", size=9,  weight="bold")

        self.tasks         = []   # list of {"text": str, "done": bool}
        self.selected_idx  = None

        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(28, 0))

        tk.Label(header, text="To-Do List", font=self.f_title,
                 bg=BG, fg=TEXT_W).pack(anchor="w")
        tk.Label(header, text=" -- Organize your works --",
                 font=self.f_sub, bg=BG, fg=TEXT_MUT).pack(anchor="w")

        # Thin separator
        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x", padx=30, pady=(14, 0))

        # Input area
        input_frame = tk.Frame(self, bg=PANEL, bd=0, highlightthickness=1,
                               highlightbackground=BORDER)
        input_frame.pack(fill="x", padx=30, pady=(16, 0))

        tk.Label(input_frame, text="TASK", font=self.f_label,
                 bg=PANEL, fg=TEXT_MUT).pack(anchor="w", padx=14, pady=(10, 2))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(input_frame, textvariable=self.entry_var,
                              bg=ENTRY_BG, fg=TEXT_W, insertbackground=TEXT_W,
                              relief="flat", bd=0, font=self.f_item,
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=ACCENT)
        self.entry.pack(fill="x", padx=14, pady=(0, 12), ipady=7)
        self.entry.bind("<Return>", lambda e: self._add_task())

        # Button row
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=30, pady=(10, 0))

        self.btn_add    = self._make_btn(btn_row, "＋  Add",    ACCENT,  ACCENT2,  self._add_task)
        self.btn_update = self._make_btn(btn_row, "✎  Update",  "#5566CC","#6677DD",self._update_task)
        self.btn_done   = self._make_btn(btn_row, "✔  Done",    DONE_C,  "#5DC89A", self._toggle_done)
        self.btn_delete = self._make_btn(btn_row, "✕  Delete",  DELETE_C, DELETE_H, self._delete_task)

        for b in (self.btn_add, self.btn_update, self.btn_done, self.btn_delete):
            b.pack(side="left", expand=True, fill="x", padx=3)

        # List label
        tk.Label(self, text="YOUR LIST", font=self.f_label,
                 bg=BG, fg=TEXT_MUT).pack(anchor="w", padx=30, pady=(18, 4))

        # Scrollable task list
        list_frame = tk.Frame(self, bg=PANEL, bd=0, highlightthickness=1,
                              highlightbackground=BORDER)
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 26))

        scrollbar = tk.Scrollbar(list_frame, bg=PANEL, troughcolor=PANEL,
                                 activebackground=ACCENT, relief="flat", width=6)
        scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=4)

        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=PANEL, fg=TEXT_W,
            selectbackground=ACCENT, selectforeground=TEXT_W,
            activestyle="none",
            relief="flat", bd=0,
            font=self.f_item,
            highlightthickness=0,
            cursor="hand2",
        )
        self.listbox.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Status bar
        self.status_var = tk.StringVar(value="Add your first task ✦")
        tk.Label(self, textvariable=self.status_var, font=self.f_label,
                 bg=BG, fg=TEXT_MUT).pack(anchor="w", padx=32, pady=(0, 10))

    def _make_btn(self, parent, text, color, hover_color, cmd):
        b = tk.Button(parent,
                      text=text,
                      command=cmd,
                      bg=color,
                      fg=TEXT_W,
                      activebackground=hover_color,
                      activeforeground=TEXT_W,
                      relief="flat",
                      bd=0,
                      font=self.f_btn,
                      cursor="hand2",
                      padx=4,
                      pady=7
                      )
        b.bind("<Enter>", lambda e, h=hover_color: b.config(bg=h))
        b.bind("<Leave>", lambda e, c=color:       b.config(bg=c))
        return b

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for t in self.tasks:
            prefix = "✔ " if t["done"] else "  "
            self.listbox.insert(tk.END, f"{prefix}{t['text']}")
            idx = self.listbox.size() - 1
            color = TEXT_MUT if t["done"] else TEXT_W
            self.listbox.itemconfig(idx, fg=color)

        done  = sum(1 for t in self.tasks if t["done"])
        total = len(self.tasks)
        self.status_var.set(
            f"{total} task{'s' if total != 1 else ''}  ·  {done} completed"
            if total else "Add your first task ✦"
        )

    def _on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected_idx = sel[0]
        task_text = self.tasks[self.selected_idx]["text"]
        self.entry_var.set(task_text)
        self.entry.icursor(tk.END)

    def _add_task(self):
        text = self.entry_var.get().strip()
        if not text:
            messagebox.showwarning("Empty", "Please type a task first.")
            return
        self.tasks.append({"text": text, "done": False})
        self.entry_var.set("")
        self.selected_idx = None
        self._refresh_list()

    def _update_task(self):
        if self.selected_idx is None:
            messagebox.showinfo("Select a task", "Click a task to select it, then edit.")
            return
        text = self.entry_var.get().strip()
        if not text:
            messagebox.showwarning("Empty", "Task text cannot be empty.")
            return
        self.tasks[self.selected_idx]["text"] = text
        self.entry_var.set("")
        self.selected_idx = None
        self._refresh_list()

    def _toggle_done(self):
        if self.selected_idx is None:
            messagebox.showinfo("Select a task", "Click a task to mark it done/undone.")
            return
        t = self.tasks[self.selected_idx]
        t["done"] = not t["done"]
        self._refresh_list()

    def _delete_task(self):
        if self.selected_idx is None:
            messagebox.showinfo("Select a task", "Click a task to select it for deletion.")
            return
        task_text = self.tasks[self.selected_idx]["text"]
        if messagebox.askyesno("Delete", f'Delete "{task_text}"?'):
            self.tasks.pop(self.selected_idx)
            self.entry_var.set("")
            self.selected_idx = None
            self._refresh_list()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()