"""
Système de mémoire pour l'AI-Child
Stocke les conversations et l'évolution de la personnalité
"""
import json
import os
from datetime import datetime
from typing import List, Dict

class Memory:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.memory_file = os.path.join(data_dir, "memory.json")
        self.conversations_file = os.path.join(data_dir, "conversations.json")
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs(data_dir, exist_ok=True)
        
        self.load_memory()
    
    def load_memory(self):
        """Charge la mémoire depuis le fichier"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            # Initialiser une nouvelle mémoire
            self.data = {
                "level": 1,  # Niveau de développement de l'enfant
                "interactions_count": 0,
                "learned_topics": [],
                "personality_traits": {
                    "curiosity": 0.8,
                    "shyness": 0.7,
                    "playfulness": 0.9,
                    "vocabulary_level": 0.2
                },
                "first_interaction": datetime.now().isoformat(),
                "last_interaction": None
            }
            self.save_memory()
    
    def save_memory(self):
        """Sauvegarde la mémoire"""
        self.data["last_interaction"] = datetime.now().isoformat()
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_conversation(self, user_message: str, ai_response: str):
        """Ajoute une conversation à l'historique"""
        conversations = self.load_conversations()
        
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response,
            "level": self.data["level"]
        }
        
        conversations.append(conversation)
        
        # Garder seulement les 100 dernières conversations
        if len(conversations) > 100:
            conversations = conversations[-100:]
        
        with open(self.conversations_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
        
        # Mettre à jour le compteur d'interactions
        self.data["interactions_count"] += 1
        self.check_level_up()
        self.save_memory()
    
    def load_conversations(self) -> List[Dict]:
        """Charge l'historique des conversations"""
        if os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_recent_context(self, num_messages: int = 5) -> List[Dict]:
        """Récupère les dernières conversations pour le contexte"""
        conversations = self.load_conversations()
        return conversations[-num_messages:] if conversations else []
    
    def check_level_up(self):
        """Vérifie si l'AI doit monter de niveau"""
        # Tous les 20 interactions, l'enfant monte de niveau
        if self.data["interactions_count"] % 20 == 0 and self.data["interactions_count"] > 0:
            self.data["level"] += 1
            self.data["personality_traits"]["vocabulary_level"] = min(1.0, 
                self.data["personality_traits"]["vocabulary_level"] + 0.1)
            self.data["personality_traits"]["shyness"] = max(0.2, 
                self.data["personality_traits"]["shyness"] - 0.05)
            print(f"\n🎉 L'enfant a grandi ! Niveau {self.data['level']} atteint !")
    
    def get_personality_description(self) -> str:
        """Retourne une description de la personnalité actuelle"""
        traits = self.data["personality_traits"]
        level = self.data["level"]
        
        if level <= 2:
            stage = "très jeune et timide"
        elif level <= 5:
            stage = "curieux et commence à s'ouvrir"
        elif level <= 10:
            stage = "bavard et enjoué"
        else:
            stage = "mature et confiante"
        
        return f"Niveau {level} - {stage}"
