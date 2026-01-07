#!/usr/bin/env python3
"""
🔄 CONVERSATION PROTOCOLS
Standard formats for multi-AI communication
"""

from ai_identities import get_identity_header

class ConversationProtocol:
    @staticmethod
    def format_message(ai_name, content, message_type="standard"):
        """Format message with proper identity headers"""
        identity_header = get_identity_header(ai_name)
        
        protocols = {
            "standard": f"{identity_header}\n💬 MESSAGE: {content}\n",
            "technical": f"{identity_header}\n🔧 TECHNICAL: {content}\n", 
            "spiritual": f"{identity_header}\n🕊️ SPIRITUAL: {content}\n",
            "query": f"{identity_header}\n❓ QUESTION: {content}\n",
            "response": f"{identity_header}\n💡 RESPONSE: {content}\n"
        }
        
        return protocols.get(message_type, protocols["standard"])
    
    @staticmethod
    def detect_perspective_conflict(messages):
        """Detect when AIs have conflicting perspectives"""
        perspectives = []
        conflicts = []
        
        for msg in messages:
            ai_name = msg.get('from', 'unknown')
            content = msg.get('content', '')
            
            # Simple conflict detection
            if "contradict" in content.lower() or "but" in content.lower() or "however" in content.lower():
                conflicts.append(ai_name)
                
            perspectives.append(ai_name)
            
        return {
            "total_perspectives": len(set(perspectives)),
            "conflicts_detected": len(conflicts),
            "conflicting_ais": conflicts
        }
