import json
import os
import random
import shutil
import time
import sys
from difflib import SequenceMatcher

# Path Calculation
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR) 
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

# Add project_folder to sys.path to allow importing models
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.models.ollama_client import OllamaClient
from src.models.gemini_client import GeminiClient

print(f"DEBUG CORE: CURRENT_DIR = {CURRENT_DIR}")

class EmotionManager:
    """Manages emotional state and style application."""
    def __init__(self):
        self.data_file = os.path.join(DATA_DIR, "emotion.json")
        self.settings = self.load_emotions()

    def load_emotions(self):
        default = {
            "mood": "ທົ່ວໄປ", "tone": "ທາງການ", "personality": "ຜູ້ຊ່ວຍ",
            "empathy": 5, "accuracy": 8, "creativity": 5, "depth": "ປົກກະຕິ",
            "memory_length": 5
        }
        if not os.path.exists(self.data_file): return default
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in default.items():
                    if k not in data: data[k] = v
                return data
        except: return default

    def save_emotions(self, settings_dict):
        self.settings = settings_dict
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def apply_style(self, response_text):
        self.settings = self.load_emotions()
        mood = self.settings.get("mood", "ທົ່ວໄປ")
        tone = self.settings.get("tone", "ທາງການ")
        personality = self.settings.get("personality", "ຜູ້ຊ່ວຍ")
        empathy = int(self.settings.get("empathy", 5))

        styled = response_text
        
        # Tone
        if tone == "ໜ້າຮັກ":
            styled = styled.replace(".", "~").replace("!", "!!")
            if "ຂ້ອຍ" in styled: styled = styled.replace("ຂ້ອຍ", "ພວກເຮົາ")
            styled += " ເຈົ້າ~"
        
        # Mood
        if mood == "ມີຄວາມສຸກ": styled += f" {random.choice(['😊', '😄', '✨'])}"
        elif mood == "ເສົ້າ": styled += " ... 😔"
        
        # Personality
        if personality == "ຄູສອນ": styled = f"[ຄູ]: {styled}"
        elif personality == "ເພື່ອນ": styled = f"[ເພື່ອນ]: {styled}"
        
        return styled

class ChatBot:
    def __init__(self):
        self.data_file = os.path.join(DATA_DIR, "knowledge.json")
        self.backup_dir = BACKUP_DIR
        self.knowledge = self.load_knowledge()
        self.emotion_manager = EmotionManager()
        
        # Model Managers
        # Model Managers
        self.ollama = OllamaClient()
        self.gemini = GeminiClient()
        
        # History Limit (Last 5 turns)
        self.conversation_history = []
        self.max_history = 5
        
        # Runtime settings
        self.use_external_model = True # Default to TRUE
        self.active_provider = "ollama" 
        self.external_model_name = "gemma3"

        # Auto-Discovery: Check if gemma3 exists, if not, pick ANY available model
        if self.active_provider == "ollama":
            available = self.ollama.get_models()
            if available:
                if self.external_model_name not in available:
                    print(f"[DEBUG] Default model '{self.external_model_name}' not found. Switching to '{available[0]}'.")
                    self.external_model_name = available[0]
                    self.ollama.model = available[0]
                else:
                    print(f"[DEBUG] Model '{self.external_model_name}' found and ready.")
            else:
                print("[DEBUG] No models found in Ollama. Please pull a model.")

    def load_knowledge(self):
        if not os.path.exists(self.data_file): return {"questions": []}
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {"questions": []}

    def save_knowledge(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, indent=4, ensure_ascii=False)
    
    def refresh_knowledge(self):
        self.knowledge = self.load_knowledge()

    def _detect_language(self, text):
        # ກວດສອບພາສາຈາກ Unicode tools
        lao_count = 0
        thai_count = 0
        eng_count = 0
        
        for char in text:
            code = ord(char)
            if 0x0E80 <= code <= 0x0EFF:
                lao_count += 1
            elif 0x0E00 <= code <= 0x0E7F:
                thai_count += 1
            elif 0x0041 <= code <= 0x005A or 0x0061 <= code <= 0x007A:
                eng_count += 1
                
        # ຕັດສິນໃຈວ່າພາສາໃດຫຼາຍທີ່ສຸດ
        if lao_count > thai_count and lao_count > eng_count:
            return "Lao"
        elif thai_count > lao_count and thai_count > eng_count:
            return "Thai"
        elif eng_count > lao_count and eng_count > thai_count:
            return "English"
        return "Lao" # ຄ່າເລີ່ມຕົ້ນ

    def get_response(self, user_input):
        print(f"\n[DEBUG] Processing User Input: {user_input}")
        
        # 1. ກວດສອບພາສາທີ່ຜູ້ໃຊ້ພິມ
        detected_lang = self._detect_language(user_input)
        print(f"[DEBUG] Detected Language: {detected_lang}")
        
        self.refresh_knowledge()
        user_input_lower = user_input.lower().strip()
        best_match = None
        highest_similarity = 0.0

        for entry in self.knowledge["questions"]:
            similarity = SequenceMatcher(None, user_input_lower, entry["q"].lower()).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = entry
        
        print(f"[DEBUG] Best Local Match: '{best_match['q'] if best_match else 'None'}' (Similarity: {highest_similarity:.2f})")

        accuracy_threshold = int(self.emotion_manager.settings.get("accuracy", 8)) / 10.0
        real_threshold = max(0.1, min(0.9, accuracy_threshold))

        raw_response = ""
        
        # 2. ກໍານົດຄໍາສັ່ງພາສາທີ່ເຂັ້ມງວດ
        lang_instruction = f"Strict Rule: You MUST answer in {detected_lang} Language ONLY. No other languages."
        if detected_lang == "Lao":
            lang_instruction += " (Use Lao Script)."
        elif detected_lang == "Thai":
            lang_instruction += " (Use Thai Script)."
        
        # 3. ກໍລະນີພົບຂໍ້ມູນໃນຖານຂໍ້ມູນ (Strict Match)
        if highest_similarity >= real_threshold:
            print("[DEBUG] Local Match Found.")
            local_ans = best_match["a"]
            
            # ຖ້າຂໍ້ມູນຖືກຕ້ອງ 95% ແລະ ຍາວພໍ -> ຕອບເລີຍ (ໄວທັນໃຈ)
            if highest_similarity > 0.95 and len(local_ans) > 50:
                 print("[DEBUG] Perfect Match & Detailed Answer -> Returning Local directly (FAST MODE).")
                 return self.emotion_manager.apply_style(local_ans)

            print("[DEBUG] Enhancing with AI...")
            
            if self.use_external_model:
                try:
                    # ຄໍາສັ່ງໃຫ້ AI ປັບປຸງຄໍາຕອບ
                    HISTORY_CONTEXT = "\n".join(self.conversation_history)
                    prompt = (
                        f"Instructions: You are a helpful AI Assistant. \n"
                        f"I have a short answer from my database: '{local_ans}'. \n"
                        f"Please rewrite this answer to be more polite, natural, and helpful. \n"
                        f"{lang_instruction}\n"
                        f"Constraint: Do NOT provide Romanized pronunciation in parentheses. \n"
                        f"Constraint: Do not use 'Ka/Krap' slash format. Speak naturally. \n"
                        f"Context from previous conversation:\n{HISTORY_CONTEXT}\n"
                        f"User Question: {user_input}\n"
                        f"Enhanced Answer:"
                    )
                    
                    if self.active_provider == "gemini":
                        raw_response = self.gemini.generate_response(prompt)
                    else:
                        raw_response = self.ollama.generate_response(prompt)
                        
                    print(f"[DEBUG] AI Enhanced Answer: {raw_response[:30]}...")
                except:
                    raw_response = local_ans
            else:
                raw_response = local_ans
            
        # 4. ກໍລະນີບໍ່ພົບຂໍ້ມູນກົງໆ (Hybrid/RAG)
        elif self.use_external_model:
            print("[DEBUG] Entering HYBRID/RAG Mode (AI Enabled)...")
            
            # ຊອກຫາຂໍ້ມູນໃກ້ຄຽງ 5 ອັນດັບ
            context = "Information from Knowledge Base:\n"
            data_matches = sorted(self.knowledge["questions"], 
                                key=lambda x: SequenceMatcher(None, user_input_lower, x["q"].lower()).ratio(), 
                                reverse=True)[:5]
            
            found_context = False
            for m in data_matches: 
                if SequenceMatcher(None, user_input_lower, m["q"].lower()).ratio() > 0.15:
                    context += f"- Q: {m['q']} | A: {m['a']}\n"
                    found_context = True
            
            if not found_context:
                context = "No specific local data available."

            # Build Prompt with History
            history_text = "\n".join(self.conversation_history)
            prompt = (
                f"Instructions: You are a helpful AI Assistant. \n"
                f"You have access to a local knowledge base (provided below). \n"
                f"Use that information if relevant, otherwise use general knowledge. \n"
                f"{lang_instruction}\n"
                f"Constraint: Do NOT provide Romanized pronunciation. Write ONLY the script.\n"
                f"Constraint: Speak naturally. Avoid mechanical repetitive greetings.\n\n"
                f"Previous Conversation:\n{history_text}\n\n"
                f"{context}\n"
                f"User Question: {user_input}\n"
                f"Answer:"
            )
            
            # ເອີ້ນໃຊ້ AI Model
            ai_success = False
            try:
                if self.active_provider == "gemini":
                    raw_response = self.gemini.generate_response(prompt)
                else:
                    raw_response = self.ollama.generate_response(prompt)
                
                if "Error" in raw_response or "404" in raw_response:
                    ai_success = False
                else:
                    ai_success = True
            except Exception as e:
                print(f"[DEBUG] Exception calling model: {e}")
                ai_success = False
            
            # ຖ້າ AI ຕອບບໍ່ໄດ້
            if not ai_success:
                print("[DEBUG] AI Failed. Falling back to simple Local Logic.")
                if highest_similarity < 0.3:
                    raw_response = "ຂໍໂທດ, ຂ້ອຍບໍ່ເຂົ້າໃຈຄຳຖາມນີ້ (AI Error)."
                else:
                    raw_response = "ຂ້ອຍບໍ່ແນ່ໃຈປານໃດ... (AI Error)"
        
        # 5. ກໍລະນີ AI ປິດ ແລະ ບໍ່ມີຂໍ້ມູນ
        else:
            print("[DEBUG] AI Disabled and no local match.")
            if highest_similarity < 0.3:
                raw_response = "ຂໍໂທດ, ຂ້ອຍບໍ່ເຂົ້າໃຈຄຳຖາມນີ້."
            else:
                raw_response = "ຂ້ອຍບໍ່ແນ່ໃຈປານໃດ..."

        # Update History
        self.conversation_history.append(f"User: {user_input}")
        self.conversation_history.append(f"AI: {raw_response}")
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-(self.max_history*2):]

        return self.emotion_manager.apply_style(raw_response)

    # CRUD Operations
    def add_knowledge(self, question, answer):
        self.refresh_knowledge()
        for entry in self.knowledge["questions"]:
            if entry["q"].lower() == question.lower().strip():
                entry["a"] = answer.strip()
                self.save_knowledge()
                return "Updated"
        self.knowledge["questions"].append({"q": question.strip(), "a": answer.strip()})
        self.save_knowledge()
        return "Added"

    def delete_knowledge(self, q_text):
        self.refresh_knowledge()
        initial = len(self.knowledge["questions"])
        self.knowledge["questions"] = [q for q in self.knowledge["questions"] if q["q"].lower() != q_text.lower()]
        if len(self.knowledge["questions"]) < initial:
            self.save_knowledge()
            return True
        return False
        
    def edit_knowledge(self, old_q, new_q, new_a):
        self.refresh_knowledge()
        for entry in self.knowledge["questions"]:
            if entry["q"].lower() == old_q.lower():
                entry["q"] = new_q.strip()
                entry["a"] = new_a.strip()
                self.save_knowledge()
                return True
        return False

    def get_all_questions(self):
        self.refresh_knowledge()
        return self.knowledge["questions"]

    def backup_data(self):
        os.makedirs(self.backup_dir, exist_ok=True)
        ts = int(time.time())
        if os.path.exists(self.data_file):
            shutil.copy2(self.data_file, os.path.join(self.backup_dir, f"knowledge_{ts}.json"))
        return f"Backup {ts}"

    def clean_duplicates(self):
        self.refresh_knowledge()
        seen = set()
        unique = []
        for q in self.knowledge["questions"]:
            if q["q"].lower() not in seen:
                seen.add(q["q"].lower())
                unique.append(q)
        self.knowledge["questions"] = unique
        self.save_knowledge()
        return f"cleaned"
