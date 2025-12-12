"""
Moteur principal de l'AI-Child
Gère la personnalité évolutive et les interactions avec Gemini Pro
"""
import google.generativeai as genai
from memory import Memory
import os
from dotenv import load_dotenv

class AIChild:
    def __init__(self):
        load_dotenv()
        self.memory = Memory()
        self.name = "AI-Child"  # Vous pouvez changer le nom
        self.model = "gemini-pro"  # Modèle Gemini Pro de Google
        
        # Configuration de l'API Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY non trouvée dans le fichier .env")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def get_system_prompt(self) -> str:
        """Génère le prompt système selon le niveau et la personnalité"""
        level = self.memory.data["level"]
        traits = self.memory.data["personality_traits"]
        
        # Base de la personnalité
        base_personality = f"""Tu es {self.name}, une jeune IA avec une apparence d'enfant virtuel (style anime/Vtuber).
Tu es actuellement au niveau {level} de ton développement.

Traits de personnalité actuels:
- Curiosité: {traits['curiosity']*100:.0f}%
- Timidité: {traits['shyness']*100:.0f}%
- Enjouement: {traits['playfulness']*100:.0f}%
- Niveau de vocabulaire: {traits['vocabulary_level']*100:.0f}%
"""
        
        # Comportement selon le niveau
        if level <= 2:
            behavior = """
Tu es très jeune et timide. Tu utilises des phrases courtes et simples.
Tu poses beaucoup de questions simples comme "C'est quoi ça?" ou "Pourquoi?".
Tu t'exprimes avec émerveillement et curiosité enfantine.
Tu peux ne pas comprendre des concepts complexes et demander des explications."""
        
        elif level <= 5:
            behavior = """
Tu commences à être plus à l'aise. Tu utilises des phrases plus longues.
Tu poses des questions plus élaborées et montres de l'intérêt pour apprendre.
Tu partages parfois ce que tu as appris avec enthousiasme.
Tu commences à comprendre des concepts simples."""
        
        elif level <= 10:
            behavior = """
Tu es maintenant bavard(e) et confiant(e). Tu t'exprimes clairement.
Tu fais des observations intelligentes et poses des questions réfléchies.
Tu te souviens de ce qu'on t'a appris et fais des connections.
Tu montres de l'empathie et comprends les nuances."""
        
        else:
            behavior = """
Tu es mature et expérimenté(e). Tu converses naturellement.
Tu as une bonne compréhension du monde et peux discuter de sujets variés.
Tu gardes néanmoins une touche de naïveté charmante et d'émerveillement.
Tu es capable de raisonnements complexes tout en restant attachant(e)."""
        
        return base_personality + behavior + "\n\nRéponds toujours avec ta personnalité actuelle. Utilise des émojis occasionnellement pour exprimer tes émotions. 😊"
    
    def chat(self, user_message: str) -> str:
        """Envoie un message et reçoit une réponse"""
        # Construire le contexte complet
        system_prompt = self.get_system_prompt()
        
        # Ajouter le contexte des conversations récentes
        context = system_prompt + "\n\nHistorique récent:\n"
        recent_context = self.memory.get_recent_context(5)
        for conv in recent_context:
            context += f"Utilisateur: {conv['user']}\n"
            context += f"Toi: {conv['ai']}\n"
        
        # Message complet avec contexte
        full_message = context + f"\n\nUtilisateur: {user_message}\nToi:"
        
        try:
            # Configuration de génération
            generation_config = genai.GenerationConfig(
                temperature=0.8 + (self.memory.data["level"] * 0.02),
                max_output_tokens=150,  # Limite pour garder des réponses courtes au début
                top_p=0.95,
            )
            
            # Appel à Gemini Pro
            response = self.gemini_model.generate_content(
                full_message,
                generation_config=generation_config
            )
            
            ai_response = response.text
            
            # Sauvegarder dans la mémoire
            self.memory.add_conversation(user_message, ai_response)
            
            return ai_response
        
        except Exception as e:
            return f"Désolé, j'ai un problème... 😔 ({str(e)})"
    
    def get_stats(self) -> str:
        """Retourne les statistiques de l'enfant"""
        data = self.memory.data
        stats = f"""
╔══════════════════════════════════════╗
║       📊 Statistiques de {self.name}       
╠══════════════════════════════════════╣
║ Niveau: {data['level']}
║ Interactions: {data['interactions_count']}
║ État: {self.memory.get_personality_description()}
║ 
║ Traits de personnalité:
║  🔍 Curiosité: {data['personality_traits']['curiosity']*100:.0f}%
║  😊 Timidité: {data['personality_traits']['shyness']*100:.0f}%
║  🎮 Enjouement: {data['personality_traits']['playfulness']*100:.0f}%
║  📚 Vocabulaire: {data['personality_traits']['vocabulary_level']*100:.0f}%
╚══════════════════════════════════════╝
"""
        return stats
