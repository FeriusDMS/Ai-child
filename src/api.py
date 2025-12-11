"""
API Flask pour l'AI-Child
Permet d'accéder à l'IA depuis un téléphone mobile
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ai_child import AIChild
import os

app = Flask(__name__, 
            static_folder='../web/static',
            template_folder='../web/templates')
CORS(app)

# Instance globale de l'AI-Child
ai_child = AIChild()

@app.route('/')
def home():
    """Page principale de l'application mobile"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint pour envoyer un message à l'AI-Child"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Obtenir la réponse de l'IA
        ai_response = ai_child.chat(user_message)
        
        return jsonify({
            'response': ai_response,
            'level': ai_child.memory.data['level'],
            'interactions': ai_child.memory.data['interactions_count']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Endpoint pour obtenir les statistiques de l'AI-Child"""
    try:
        data = ai_child.memory.data
        return jsonify({
            'name': ai_child.name,
            'level': data['level'],
            'interactions_count': data['interactions_count'],
            'personality_traits': data['personality_traits'],
            'description': ai_child.memory.get_personality_description()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """Endpoint pour obtenir l'historique des conversations"""
    try:
        conversations = ai_child.memory.load_conversations()
        # Retourner les 20 dernières conversations
        return jsonify({
            'conversations': conversations[-20:] if conversations else []
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_local_ip():
    """Obtient l'adresse IP locale pour accès depuis mobile"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*50)
    print("🌟 AI-CHILD - Serveur Mobile Démarré")
    print("="*50)
    print(f"\n📱 Accès depuis votre téléphone:")
    print(f"   http://{local_ip}:{port}")
    print(f"\n💻 Accès depuis ce PC:")
    print(f"   http://localhost:{port}")
    print(f"\nℹ️  Assurez-vous que votre téléphone et PC sont sur le même WiFi")
    print("="*50 + "\n")
    
    # Démarrer le serveur accessible depuis le réseau local
    app.run(host='0.0.0.0', port=port, debug=True)
