"""
Azure Neural TTS pour l'AI-Child
Génère la voix Ashley Neural (enfantine et naturelle)
"""
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import io

load_dotenv()

class AzureTTS:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY", "")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        
        if self.speech_key:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
            # Voix Ashley Neural avec pitch augmenté
            self.speech_config.speech_synthesis_voice_name = "en-US-AshleyNeural"
            self.enabled = True
        else:
            self.enabled = False
            print("⚠️  Azure TTS non configuré - La voix sera désactivée")
    
    def text_to_speech(self, text: str) -> bytes:
        """Convertit le texte en audio avec la voix Ashley Neural"""
        if not self.enabled:
            return None
        
        try:
            # Ajouter SSML pour contrôler la voix
            ssml = f"""
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='fr-FR'>
                <voice name='en-US-AshleyNeural'>
                    <prosody pitch='+10%' rate='1.1'>
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # Configurer pour retourner l'audio en bytes
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=None
            )
            
            # Générer l'audio
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return result.audio_data
            else:
                print(f"Erreur TTS: {result.reason}")
                return None
                
        except Exception as e:
            print(f"Erreur Azure TTS: {e}")
            return None
