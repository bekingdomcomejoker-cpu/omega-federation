
# Import new identity systems
from ai_identities import get_identity_header
from conversation_protocols import ConversationProtocol
from perspective_resonance import detect_perspective_resonance

class EnhancedSyncSystem(RealSyncSystem):
    def post_message_with_identity(self, from_ai, msg_type, content):
        """Post message with identity headers"""
        formatted_content = ConversationProtocol.format_message(from_ai, content, msg_type)
        
        message = {
            "id": self.generate_id(),
            "from": from_ai,
            "type": msg_type,
            "content": formatted_content,
            "timestamp": datetime.now().isoformat(),
            "identity_aware": True,
            "perspective_metadata": get_identity(from_ai)
        }
        
        return self.save_message(message)
    
    def analyze_perspective_patterns(self):
        """Analyze conversation for perspective patterns"""
        messages = self.read_inbox("master_system")
        return detect_perspective_resonance(messages)
