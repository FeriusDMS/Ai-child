"""
AI-Child - Prototype de base
Une IA qui grandit et apprend au fil des interactions
"""
from ai_child import AIChild
from colorama import init, Fore, Style
import os

# Initialiser colorama pour les couleurs dans le terminal
init()

def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête de l'application"""
    print(f"{Fore.CYAN}╔════════════════════════════════════════╗")
    print(f"║      🌟 AI-CHILD - Prototype v1.0      ║")
    print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}\n")

def main():
    clear_screen()
    print_header()
    
    # Initialiser l'AI-Child
    print(f"{Fore.YELLOW}⏳ Initialisation de l'AI-Child...{Style.RESET_ALL}")
    ai = AIChild()
    
    # Afficher les statistiques
    print(ai.get_stats())
    
    print(f"\n{Fore.GREEN}✅ Prêt ! Commencez à parler avec votre AI-Child.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Commandes: 'stats' pour voir les statistiques, 'quit' pour quitter{Style.RESET_ALL}\n")
    print("─" * 50)
    
    # Boucle de conversation
    while True:
        try:
            # Message de l'utilisateur
            user_input = input(f"\n{Fore.BLUE}Vous: {Style.RESET_ALL}")
            
            if not user_input.strip():
                continue
            
            # Commandes spéciales
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{Fore.MAGENTA}👋 Au revoir ! À bientôt !{Style.RESET_ALL}\n")
                break
            
            if user_input.lower() == 'stats':
                print(ai.get_stats())
                continue
            
            if user_input.lower() == 'clear':
                clear_screen()
                print_header()
                continue
            
            # Obtenir la réponse de l'IA
            print(f"{Fore.YELLOW}🤔 {ai.name} réfléchit...{Style.RESET_ALL}", end='\r')
            response = ai.chat(user_input)
            print(f"{Fore.MAGENTA}{ai.name}: {Style.RESET_ALL}{response}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.MAGENTA}👋 Au revoir ! À bientôt !{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}❌ Erreur: {str(e)}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()