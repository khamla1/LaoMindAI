
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import shutil
import datetime
try:
    from .engine import ChatBot
except ImportError:
    from engine import ChatBot, EmotionManager

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.chatbot = ChatBot()
        self.emotion_manager = self.chatbot.emotion_manager
        
        self._setup_ui()

    def _setup_ui(self):
        self.root.title("LaoMind-AI Admin Panel")
        self.root.geometry("800x600")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Lao font setup
        self.font_h1 = ("Phetsarath OT", 14, "bold")
        self.font_ui = ("Phetsarath OT", 11)
        self.font_s = ("Phetsarath OT", 10)
        
        # Configure ttk styles for font
        self.style.configure('.', font=self.font_ui)
        self.style.configure('TNotebook.Tab', font=self.font_ui)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create Tabs
        self.tab_character = ttk.Frame(notebook)
        self.tab_knowledge = ttk.Frame(notebook)
        self.tab_aimodels = ttk.Frame(notebook)

        notebook.add(self.tab_character, text='ການຕັ້ງຄ່າຕົວລະຄອນ (Character)')
        notebook.add(self.tab_knowledge, text='ຄວາມຮູ້ (Knowledge)')
        notebook.add(self.tab_aimodels, text='ສະໝອງ AI (AI Brain)')

        self._build_character_tab()
        self._build_knowledge_tab()
        self._build_aimodels_tab()

    def _build_character_tab(self):
        frame = self.tab_character
        tk.Label(frame, text="ຕັ້ງຄ່າຕົວລະຄອນ (Character Settings)", font=self.font_h1).pack(pady=10)
        
        current = self.emotion_manager.load_emotions()
        
        # Container for columns
        container = tk.Frame(frame)
        container.pack(fill="both", expand=True, padx=20)
        
        # --- LEFT COLUMN: Personality & Emotion ---
        left_col = tk.Frame(container)
        left_col.pack(side="left", fill="both", expand=True, padx=5)
        
        # 1. Personality Section
        p_frame = tk.LabelFrame(left_col, text="1. ບຸກຄະລິກ (Personality)", font=self.font_ui)
        p_frame.pack(fill="x", pady=5)
        
        tk.Label(p_frame, text="ແບບບຸກຄະລິກ:", font=self.font_ui).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.pers_var = tk.StringVar(value=current.get("personality", "ຜູ້ຊ່ວຍ"))
        ttk.Combobox(p_frame, textvariable=self.pers_var, font=self.font_ui, values=["ຜູ້ຊ່ວຍ", "ເພື່ອນ", "ຄູສອນ", "ບອດໜ້າຮັກ"], state="readonly", width=15).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(p_frame, text="ຮູບແບບການເວົ້າ:", font=self.font_ui).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.tone_var = tk.StringVar(value=current.get("tone", "ທາງການ"))
        ttk.Combobox(p_frame, textvariable=self.tone_var, font=self.font_ui, values=["ທາງການ", "ໜ້າຮັກ", "ເປັນກັນເອງ"], state="readonly", width=15).grid(row=1, column=1, padx=10, pady=5)

        # 2. Emotion Section
        e_frame = tk.LabelFrame(left_col, text="2. ອາລົມ (Emotion)", font=self.font_ui)
        e_frame.pack(fill="x", pady=5)
        
        tk.Label(e_frame, text="ອາລົມພື້ນຖານ:", font=self.font_ui).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.mood_var = tk.StringVar(value=current.get("mood", "ທົ່ວໄປ"))
        ttk.Combobox(e_frame, textvariable=self.mood_var, font=self.font_ui, values=["ທົ່ວໄປ", "ມີຄວາມສຸກ", "ຕື່ນເຕັ້ນ", "ສະຫງົບ", "ເສົ້າ"], state="readonly", width=15).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(e_frame, text="Empathy (1-10):", font=self.font_ui).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.empathy_var = tk.IntVar(value=int(current.get("empathy", 5)))
        tk.Scale(e_frame, from_=1, to=10, orient="horizontal", variable=self.empathy_var, font=self.font_ui).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # --- RIGHT COLUMN: Behavior ---
        right_col = tk.Frame(container)
        right_col.pack(side="left", fill="both", expand=True, padx=5)

        # 3. Behavior Section
        b_frame = tk.LabelFrame(right_col, text="3. ພຶດຕິກຳ (Behavior)", font=self.font_ui)
        b_frame.pack(fill="x", pady=5)
        
        tk.Label(b_frame, text="ຄວາມຖືກຕ້ອງ (Accuracy):", font=self.font_ui).pack(anchor="w", padx=10, pady=(5,0))
        self.acc_var = tk.IntVar(value=int(current.get("accuracy", 8)))
        tk.Scale(b_frame, from_=1, to=10, orient="horizontal", variable=self.acc_var, font=self.font_ui, label="Creative <-> Strict").pack(fill="x", padx=10, pady=5)
        
        tk.Label(b_frame, text="ຄວາມຄິດສ້າງສັນ:", font=self.font_ui).pack(anchor="w", padx=10)
        self.creat_var = tk.IntVar(value=int(current.get("creativity", 5)))
        tk.Scale(b_frame, from_=1, to=10, orient="horizontal", variable=self.creat_var, font=self.font_ui).pack(fill="x", padx=10, pady=5)
        
        tk.Label(b_frame, text="ຄວາມລະອຽດ:", font=self.font_ui).pack(anchor="w", padx=10)
        self.depth_var = tk.StringVar(value=current.get("depth", "ປົກກະຕິ"))
        ttk.Combobox(b_frame, textvariable=self.depth_var, font=self.font_ui, values=["ສັ້ນ", "ປົກກະຕິ", "ລະອຽດ"], state="readonly").pack(fill="x", padx=10, pady=5)

        # SAVE BUTTON
        tk.Button(frame, text="💾 ບັນທຶກການຕັ້ງຄ່າທັງໝົດ", command=self._save_settings, bg="#4CAF50", fg="white", font=self.font_h1).pack(pady=20, fill="x", padx=100)

    def _build_knowledge_tab(self):
        frame = self.tab_knowledge
        
        # Top controls
        top_frame = tk.Frame(frame)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(top_frame, text="ເພີ່ມຂໍ້ມູນໃໝ່", command=self._add_knowledge_popup, bg="#2196F3", fg="white", font=self.font_ui).pack(side="left")
        tk.Button(top_frame, text="✨ ສ້າງຂໍ້ມູນອັດຕະໂນມັດ (AI Import)", command=self._ai_import_popup, bg="#9C27B0", fg="white", font=self.font_ui).pack(side="left", padx=5)
        tk.Button(top_frame, text="ໂຫຼດຂໍ້ມູນຄືນ", command=self._idx_knowledge_list, font=self.font_ui).pack(side="left", padx=5)
        tk.Button(top_frame, text="ລົບລາຍການທີ່ເລືອກ", command=self._dalete_knowledge_item, bg="#f44336", fg="white", font=self.font_ui).pack(side="right")
        
        # Listbox
        self.k_list = tk.Listbox(frame, width=50, height=20, font=self.font_ui)
        self.k_list.pack(fill="both", expand=True, padx=10)
        self.k_list.bind('<Double-Button-1>', self._edit_knowledge_popup)
        
        self._idx_knowledge_list()

    def _idx_knowledge_list(self):
        self.k_list.delete(0, tk.END)
        self.chatbot.refresh_knowledge()
        for item in self.chatbot.get_all_questions():
            self.k_list.insert(tk.END, f"ຖາມ: {item['q']} | ຕອບ: {item['a']}")

    def _ai_import_popup(self):
        win = tk.Toplevel(self.root)
        win.title("ສ້າງຂໍ້ມູນອັດຕະໂນມັດ (AI Data Generator)")
        win.geometry("600x500")
        
        tk.Label(win, text="ວາງບົດຄວາມ/ຂໍ້ມູນຂອງທ່ານທີ່ນີ້ (Paste Text):", font=self.font_ui).pack(pady=10)
        txt_input = tk.Text(win, height=15, font=self.font_s)
        txt_input.pack(fill="both", expand=True, padx=20)
        
        def process():
            raw_text = txt_input.get("1.0", tk.END).strip()
            if len(raw_text) < 10:
                messagebox.showwarning("Warning", "ຂໍ້ຄວາມສັ້ນເກີນໄປ!")
                return
                
            btn.config(text="ກຳລັງໃຫ້ AI ຄິດ... (Processing...)", state="disabled")
            win.update()
            
            try:
                # 1. Generate Q&A
                import json
                prompt = (
                    f"Instructions: Analyze the text below and generate 5 to 10 question-answer pairs in Lao language. "
                    f"Return ONLY a raw JSON list of objects with keys 'q' and 'a'. "
                    f"Do NOT use Markdown formatting. Do NOT explain. Just the JSON.\n\n"
                    f"Text: {raw_text}\n"
                    f"JSON Output:"
                )
                
                if self.chatbot.active_provider == "gemini":
                    resp = self.chatbot.gemini.generate_response(prompt)
                else:
                    resp = self.chatbot.ollama.generate_response(prompt)
                
                # 2. Clean & Parse JSON
                # Remove common markdown wraps if present
                clean_json = resp.replace("```json", "").replace("```", "").strip()
                
                try:
                    data = json.loads(clean_json)
                    count = 0
                    if isinstance(data, list):
                        for item in data:
                            if "q" in item and "a" in item:
                                self.chatbot.add_knowledge(item["q"], item["a"])
                                count += 1
                        
                        messagebox.showinfo("Success", f"AI ສ້າງຂໍ້ມູນສຳເລັດ {count} ຂໍ້!")
                        self._idx_knowledge_list()
                        win.destroy()
                    else:
                        messagebox.showerror("Error", "AI ຕອບກັບມາຜິດຮູບແບບ (Not a list).")
                except json.JSONDecodeError:
                    messagebox.showerror("Error", f"AI ຕອບກັບມາຜິດຮູບແບບ JSON:\n{clean_json[:100]}...")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
            finally:
                btn.config(text="✨ ໃຫ້ AI ສ້າງໃຫ້ (Generate)", state="normal")

        btn = tk.Button(win, text="✨ ໃຫ້ AI ສ້າງໃຫ້ (Generate)", command=process, bg="#9C27B0", fg="white", font=self.font_h1)
        btn.pack(pady=20, fill="x", padx=50)

    def _add_knowledge_popup(self):
        self._knowledge_form()

    def _edit_knowledge_popup(self, event):
        sel = self.k_list.curselection()
        if not sel: return
        item_text = self.k_list.get(sel[0])
        try:
            q_part = item_text.split(" | ຕອບ: ")[0].replace("ຖາມ: ", "")
            a_part = item_text.split(" | ຕອບ: ")[1]
            self._knowledge_form(q_part, a_part)
        except:
            pass

    def _knowledge_form(self, old_q=None, old_a=None):
        win = tk.Toplevel(self.root)
        win.title("ແກ້ໄຂຂໍ້ມູນ" if old_q else "ເພີ່ມຂໍ້ມູນໃໝ່")
        
        tk.Label(win, text="ຄຳຖາມ:", font=self.font_ui).pack(pady=5)
        q_ent = tk.Entry(win, width=50, font=self.font_ui)
        q_ent.pack(padx=10)
        if old_q: q_ent.insert(0, old_q)
        
        tk.Label(win, text="ຄຳຕອບ:", font=self.font_ui).pack(pady=5)
        a_ent = tk.Entry(win, width=50, font=self.font_ui)
        a_ent.pack(padx=10)
        if old_a: a_ent.insert(0, old_a)
        
        def save():
            new_q, new_a = q_ent.get(), a_ent.get()
            if not new_q or not new_a: return
            
            if old_q: # Edit mode
                self.chatbot.edit_knowledge(old_q, new_q, new_a)
            else: # Add mode
                self.chatbot.add_knowledge(new_q, new_a)
            
            self._idx_knowledge_list()
            win.destroy()
            
        tk.Button(win, text="ບັນທຶກ", command=save, bg="#4CAF50", fg="white", font=self.font_ui).pack(pady=10)

    def _dalete_knowledge_item(self):
        sel = self.k_list.curselection()
        if not sel: return
        item_text = self.k_list.get(sel[0])
        q_part = item_text.split(" | ຕອບ: ")[0].replace("ຖາມ: ", "")
        
        if messagebox.askyesno("ຢືນຢັນ", f"ຕ້ອງການລົບ '{q_part}' ຫຼືບໍ່?"):
            self.chatbot.delete_knowledge(q_part)
            self._idx_knowledge_list()


    
    def _build_aimodels_tab(self):
        frame = self.tab_aimodels
        tk.Label(frame, text="ສະໝອງ AI (AI Brain Control)", font=self.font_h1).pack(pady=20)
        
        # Main Container
        center_frame = tk.LabelFrame(frame, text="ສະຖານະການທຳງານ (Status)", font=self.font_ui)
        center_frame.pack(fill="x", padx=50, pady=20)

        # 1. Active Model Display
        tk.Label(center_frame, text="ໂມເດວປັດຈຸບັນ (Current Model):", font=self.font_ui).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        available_models = self.chatbot.ollama.get_models()
        if not available_models:
            available_models = ["gemma:2b", "gemma2:2b", "llama3", "mistral"] 
            
        self.model_entry_var = tk.StringVar(value=self.chatbot.external_model_name)
        self.model_combo = ttk.Combobox(center_frame, textvariable=self.model_entry_var, values=available_models, font=self.font_ui, width=30, state="readonly")
        self.model_combo.grid(row=0, column=1, padx=10, pady=20)
        
        def refresh_models():
            mods = self.chatbot.ollama.get_models()
            if mods:
                self.model_combo['values'] = mods
                messagebox.showinfo("Refreshed", f"Found {len(mods)} models!")
            else:
                messagebox.showerror("Error", "Could not fetch models.")
        tk.Button(center_frame, text="🔄", command=refresh_models).grid(row=0, column=2, padx=10)

        # 2. Toggle Switch
        tk.Label(center_frame, text="ການທຳງານ (Status):", font=self.font_ui).grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.use_ai_var = tk.BooleanVar(value=self.chatbot.use_external_model)
        
        # Big Checkbutton
        tk.Checkbutton(center_frame, text="ເປີດໃຊ້ງານ AI (Enable AI)", variable=self.use_ai_var, font=("Phetsarath OT", 12, "bold"), fg="#2196F3").grid(row=1, column=1, sticky="w", padx=10)

        # 3. Save Button
        tk.Button(frame, text="💾 ບັນທຶກສະຖານະ (Update Status)", command=self._update_ai_settings, bg="#4CAF50", fg="white", font=self.font_h1).pack(pady=30, fill="x", padx=150)
        
        # Note
        tk.Label(frame, text="ໝາຍເຫດ: ຖ້າປິດ AI ລະບົບຈະໃຊ້ສະເພາະຂໍ້ມູນໃນຖານຂໍ້ມູນຂອງທ່ານເທົ່ານັ້ນ.", font=self.font_s, fg="gray").pack(side="bottom", pady=20)

    def _update_ai_settings(self):
        # Save to runtime chatbot instance
        val = self.model_entry_var.get()
        
        self.chatbot.active_provider = "ollama" # Force Ollama for simple mode
        self.chatbot.use_external_model = self.use_ai_var.get()
        self.chatbot.external_model_name = val
        self.chatbot.ollama.model = val
            
        messagebox.showinfo("Success", f"Updated AI Status!\nModel: {val}\nAI Enabled: {self.chatbot.use_external_model}")

    def _save_settings(self):
        settings = {
            "mood": self.mood_var.get(),
            "tone": self.tone_var.get(),
            "personality": self.pers_var.get(),
            "empathy": self.empathy_var.get(),
            "accuracy": self.acc_var.get(),
            "creativity": self.creat_var.get(),
            "depth": self.depth_var.get(),
        }
        self.emotion_manager.save_emotions(settings)
        messagebox.showinfo("Saved", "ບັນທຶກການຕັ້ງຄ່າສຳເລັດ!")
