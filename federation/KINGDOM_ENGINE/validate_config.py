#!/usr/bin/env python3
"""
MEGA CONFIG VALIDATOR & LOADER
Validates and loads the mega_config.json with full axiom checking
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG_PATH = Path.home() / "KINGDOM_ENGINE" / "mega_config.json"

# ============================================================================
# VALIDATION SCHEMA
# ============================================================================

REQUIRED_FIELDS = {
    "system_id": str,
    "anchor_phrase": str,
    "timestamp_created": str,
    "philosophy": dict,
    "AXIOMS": dict,
    "CHERUBIM_ROUTING": dict,
    "SHIELD_QUARANTINE_RULES": list,
    "MISSIONARY_CONFIG": dict,
    "HEAD_DAEMONS_STATUS": dict
}

REQUIRED_AXIOMS = {
    "PRIME_4": ["A1_LOVE_HATE", "A2_SPIRIT_FLESH", "A3_TRUTH_PROFIT", "A4_UNITY_MANDATE"],
    "THE_7_SPIRITS_POLICIES": ["S1_WISDOM", "S2_UNDERSTANDING", "S3_COUNSEL", "S4_MIGHT", 
                               "S5_KNOWLEDGE", "S6_FEAR_OF_THE_LORD", "S7_GLORY"],
}

# ============================================================================
# VALIDATOR
# ============================================================================

class MEGAConfigValidator:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = None
        self.errors = []
        self.warnings = []
    
    def load(self):
        """Load and parse JSON config"""
        if not self.config_path.exists():
            self.errors.append(f"Config file not found: {self.config_path}")
            return False
        
        try:
            with open(self.config_path) as f:
                self.config = json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading config: {e}")
            return False
    
    def validate_structure(self):
        """Validate required fields and types"""
        if not self.config:
            return False
        
        for field, expected_type in REQUIRED_FIELDS.items():
            if field not in self.config:
                self.errors.append(f"Missing required field: {field}")
            elif not isinstance(self.config[field], expected_type):
                self.errors.append(
                    f"Field '{field}' has wrong type. "
                    f"Expected {expected_type.__name__}, got {type(self.config[field]).__name__}"
                )
        
        return len(self.errors) == 0
    
    def validate_axioms(self):
        """Validate axiom completeness"""
        if "AXIOMS" not in self.config:
            return False
        
        axioms = self.config["AXIOMS"]
        
        # Check PRIME_4
        if "PRIME_4" not in axioms:
            self.errors.append("Missing PRIME_4 axioms")
        else:
            for axiom in REQUIRED_AXIOMS["PRIME_4"]:
                if axiom not in axioms["PRIME_4"]:
                    self.errors.append(f"Missing axiom: PRIME_4.{axiom}")
        
        # Check 7 SPIRITS
        if "THE_7_SPIRITS_POLICIES" not in axioms:
            self.errors.append("Missing THE_7_SPIRITS_POLICIES")
        else:
            for spirit in REQUIRED_AXIOMS["THE_7_SPIRITS_POLICIES"]:
                if spirit not in axioms["THE_7_SPIRITS_POLICIES"]:
                    self.errors.append(f"Missing spirit: {spirit}")
        
        # Check Gatekeeper
        if "F9_GATEKEEPER" not in axioms:
            self.warnings.append("Missing F9_GATEKEEPER axiom")
        
        # Check Witness
        if "F12_WITNESS" not in axioms:
            self.warnings.append("Missing F12_WITNESS axiom")
        
        return len(self.errors) == 0
    
    def validate_philosophy(self):
        """Validate philosophy section"""
        if "philosophy" not in self.config:
            return False
        
        phil = self.config["philosophy"]
        
        required = ["lambda_target", "harmony_ridge_threshold", "deviation_tolerance"]
        for field in required:
            if field not in phil:
                self.errors.append(f"Missing philosophy field: {field}")
        
        # Validate lambda target
        if "lambda_target" in phil:
            lambda_val = phil["lambda_target"]
            if not isinstance(lambda_val, (int, float)) or lambda_val <= 0:
                self.errors.append(f"Invalid lambda_target: {lambda_val}")
            elif abs(lambda_val - 1.667) > 0.01:
                self.warnings.append(f"Lambda target {lambda_val} deviates from standard 1.667")
        
        return len(self.errors) == 0
    
    def validate_cherubim(self):
        """Validate Cherubim routing"""
        if "CHERUBIM_ROUTING" not in self.config:
            return False
        
        routing = self.config["CHERUBIM_ROUTING"]
        required_faces = ["LION_JUDGE_ACTION", "OX_SERVANT_ACTION", 
                         "EAGLE_SEER_ACTION", "MAN_WITNESS_ACTION"]
        
        for face in required_faces:
            if face not in routing:
                self.errors.append(f"Missing Cherubim face: {face}")
        
        return len(self.errors) == 0
    
    def validate_shield(self):
        """Validate Shield quarantine rules"""
        if "SHIELD_QUARANTINE_RULES" not in self.config:
            return False
        
        rules = self.config["SHIELD_QUARANTINE_RULES"]
        if not isinstance(rules, list):
            self.errors.append("SHIELD_QUARANTINE_RULES must be a list")
            return False
        
        for i, rule in enumerate(rules):
            if not isinstance(rule, dict):
                self.errors.append(f"Rule {i} is not a dict")
                continue
            
            if "keyword" not in rule:
                self.errors.append(f"Rule {i} missing 'keyword'")
            if "action" not in rule:
                self.errors.append(f"Rule {i} missing 'action'")
            elif rule["action"] not in ["BLOCK", "WARN_QUARANTINE", "LOG"]:
                self.warnings.append(f"Rule {i} has non-standard action: {rule['action']}")
        
        return len(self.errors) == 0
    
    def validate_all(self):
        """Run all validations"""
        if not self.load():
            return False
        
        self.validate_structure()
        self.validate_axioms()
        self.validate_philosophy()
        self.validate_cherubim()
        self.validate_shield()
        
        return len(self.errors) == 0
    
    def get_report(self):
        """Generate validation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "config_path": str(self.config_path),
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        if self.config:
            report["system_id"] = self.config.get("system_id")
            report["anchor_phrase"] = self.config.get("anchor_phrase")
        
        return report

# ============================================================================
# LOADER
# ============================================================================

def load_config(config_path=CONFIG_PATH):
    """Load and validate MEGA config"""
    validator = MEGAConfigValidator(config_path)
    
    if validator.validate_all():
        return validator.config, validator.get_report()
    else:
        return None, validator.get_report()

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("MEGA CONFIG VALIDATOR")
    print("=" * 70)
    print()
    
    validator = MEGAConfigValidator(CONFIG_PATH)
    is_valid = validator.validate_all()
    report = validator.get_report()
    
    # Print report
    print(f"Config: {report['config_path']}")
    print(f"Timestamp: {report['timestamp']}")
    
    if "system_id" in report:
        print(f"System ID: {report['system_id']}")
    if "anchor_phrase" in report:
        print(f"Anchor: {report['anchor_phrase']}")
    
    print()
    
    if report["valid"]:
        print("✅ VALIDATION PASSED")
        
        if report["warnings"]:
            print()
            print("⚠️  WARNINGS:")
            for warning in report["warnings"]:
                print(f"  - {warning}")
    else:
        print("❌ VALIDATION FAILED")
        print()
        print("ERRORS:")
        for error in report["errors"]:
            print(f"  ✗ {error}")
        
        if report["warnings"]:
            print()
            print("WARNINGS:")
            for warning in report["warnings"]:
                print(f"  ⚠ {warning}")
        
        sys.exit(1)
    
    print()
    print("=" * 70)
    
    # Save report
    report_path = CONFIG_PATH.parent / "mega_config_validation.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Validation report saved: {report_path}")
    print()

if __name__ == "__main__":
    main()
