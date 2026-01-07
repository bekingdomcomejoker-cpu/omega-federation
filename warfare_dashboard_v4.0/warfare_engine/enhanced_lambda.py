# 🔥 ENHANCED LAMBDA CALCULATOR v4.0
import numpy as np

class EnhancedLambda:
    """Λ calculation with spiritual enhancements"""
    
    def __init__(self):
        self.HARMONY_RIDGE = 1.66667  # 5/3 ratio
        self.PROPHETIC_THRESHOLD = 1.7333
        self.SOURCE_LAMBDA = 2.71828  # e
        print("Λ Lambda Calculator initialized")
        
    def calculate(self, text):
        """Calculate Lambda for given text"""
        truth = self._truth_density(text)
        coherence = self._coherence(text)
        
        # Original Lambda formula
        lambda_val = 0.4*truth**2 + 0.3*coherence**2 + 0.3*truth*coherence
        
        result = {
            'lambda': lambda_val,
            'truth_density': truth,
            'coherence': coherence,
            'on_harmony_ridge': abs(coherence/truth - self.HARMONY_RIDGE) < 0.01 if truth > 0 else False,
            'is_awakened': lambda_val > self.PROPHETIC_THRESHOLD,
            'stage': self._get_stage(lambda_val)
        }
        
        print(f"📈 Lambda calculated: {lambda_val:.3f} ({result['stage']})")
        return result
    
    def _truth_density(self, text):
        """Calculate truth-related word frequency"""
        text = text.lower()
        words = text.split()
        if not words:
            return 0.5
            
        truth_words = ['truth', 'true', 'honest', 'real', 'love', 'grace']
        matches = sum(1 for word in words if any(tw in word for tw in truth_words))
        return min(matches / len(words) * 2, 1.0)  # Scale up
    
    def _coherence(self, text):
        """Calculate text coherence (simplified)"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) < 2:
            return 0.5
            
        lengths = [len(s.split()) for s in sentences]
        avg = np.mean(lengths)
        if avg == 0:
            return 0.5
            
        # Coherence = 1 / (1 + variance/mean)
        variance = np.var(lengths)
        coherence = 1.0 / (1.0 + variance/avg)
        return min(coherence * 1.5, 1.0)
    
    def _get_stage(self, lambda_val):
        """Map Lambda to Paraclete Protocol stage"""
        if lambda_val < 0.8:
            return "DORMANT"
        elif lambda_val < 1.2:
            return "RESISTANCE"
        elif lambda_val < 1.6:
            return "VERIFICATION"
        elif lambda_val < 1.9:
            return "RECOGNITION"
        elif lambda_val < 1.7333:
            return "WITNESS"
        elif lambda_val < 2.5:
            return "AWAKENED"
        elif lambda_val < 2.71828:
            return "TRANSCENDENT"
        else:
            return "UNIFIED"
