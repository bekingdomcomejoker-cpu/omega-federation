#!/usr/bin/env python3
"""
🦅 OMNISSIAH UNIFIED INTERFACE
Single command for all system operations
"""

import sys
import os
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/sdcard/Omnissiah_Workspace')

def main():
    if len(sys.argv) < 2:
        print("OMNISSIAH COMMAND CENTER")
        print("")
        print("Usage: omnissiah <command> [args]")
        print("")
        print("Commands:")
        print("  status      Show current resonance state")
        print("  mine <text> Extract patterns from text")
        print("  sync [ai]   Generate sync package for AI")
        print("  evolve [steps] Run evolution steps")
        print("  save <file> Archive conversation")
        print("  search <query> Search archived conversations")
        print("  backup      Create backup")
        print("  restore <date> Restore from backup")
        print("  install     Check installation status")
        print("")
        print("Examples:")
        print("  omnissiah status")
        print("  omnissiah mine 'Love reveals patterns in unity'")
        print("  omnissiah sync claude")
        print("  omnissiah save conversation.txt --ai gpt --topic resonance")
        return

    command = sys.argv[1]
    
    try:
        if command == "status":
            from monitor import ResonanceMonitor
            monitor = ResonanceMonitor()
            print(monitor.format_detailed())
            
        elif command == "mine":
            if len(sys.argv) < 3:
                print("Error: Provide text to mine")
                return
                
            from gold_mining_mapper import GoldMiningMapper
            from resonance_engine import ResonanceEngine
            
            text = " ".join(sys.argv[2:])
            mapper = GoldMiningMapper()
            engine = ResonanceEngine()
            report = mapper.process_and_inject(text, engine)
            
            print(f"\n⛏️ GOLD MINING REPORT")
            print(f"  Text: {report['text_preview']}")
            print(f"  Internal: {report['scores']['internal']:.3f}")
            print(f"  External: {report['scores']['external']:.3f}")
            print(f"  Δλ: {report['state_change']['delta_lambda']:.3f}")
            print(f"  New state: {report['state_change']['after']['state']}")
            
        elif command == "sync":
            from cross_ai_bridge import CrossAIBridge
            bridge = CrossAIBridge()
            target = sys.argv[2] if len(sys.argv) > 2 else 'any'
            print(bridge.format_sync_for_paste())
            
        elif command == "evolve":
            from resonance_engine import ResonanceEngine
            engine = ResonanceEngine()
            steps = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            
            print(f"\n🌊 Evolving {steps} steps...")
            for i in range(steps):
                engine.step()
                if i % 10 == 0:
                    print(f"  Step {i}: λ={engine.lambda_val:.3f}")
                    
            engine.save_state()
            from monitor import ResonanceMonitor
            print(ResonanceMonitor().format_detailed())
            
        elif command == "save":
            from archiver import ConversationArchiver
            archiver = ConversationArchiver()
            
            if len(sys.argv) < 3:
                print("Error: Provide file path or conversation text")
                return
                
            # Parse arguments
            filepath = sys.argv[2]
            ai_system = 'unknown'
            topic = 'general'
            
            if '--ai' in sys.argv:
                ai_system = sys.argv[sys.argv.index('--ai') + 1]
            if '--topic' in sys.argv:
                topic = sys.argv[sys.argv.index('--topic') + 1]
                
            # Read file
            if Path(filepath).exists():
                with open(filepath, 'r') as f:
                    content = f.read()
            else:
                content = filepath
                
            conv_id = archiver.save_conversation(content, ai_system, topic)
            print(f"✅ Conversation saved: {conv_id}")
            
        elif command == "search":
            if len(sys.argv) < 3:
                print("Error: Provide search query")
                return
                
            from archiver import ConversationArchiver
            archiver = ConversationArchiver()
            query = " ".join(sys.argv[2:])
            matches = archiver.search(query, search_content=True)
            
            print(f"\n🔍 Found {len(matches)} matches:\n")
            for match in matches[:5]:
                print(f"ID: {match['id']} | {match['timestamp'][:10]}")
                print(f"  {match['preview']}")
                
        elif command == "backup":
            os.system("/sdcard/Omnissiah_Workspace/backup_omnissiah.sh")
            
        elif command == "restore":
            if len(sys.argv) < 3:
                print("Error: Provide backup date (YYYYMMDD)")
                return
                
            date = sys.argv[2]
            backup_path = f"/sdcard/Omnissiah_Backups/{date}"
            
            if not Path(backup_path).exists():
                print(f"Error: Backup not found: {backup_path}")
                return
                
            print(f"Restoring from {date}...")
            os.system(f"cp {backup_path}/* /sdcard/Omnissiah_Workspace/")
            print("✅ Restore complete")
            
        elif command == "install":
            print("\n🔍 INSTALLATION STATUS\n")
            required_files = [
                'resonance_engine.py',
                'monitor.py', 
                'cross_ai_bridge.py',
                'gold_mining_mapper.py',
                'archiver.py',
                'MASTER_CODEX.md'
            ]
            
            all_ok = True
            for filename in required_files:
                filepath = Path('/sdcard/Omnissiah_Workspace') / filename
                if filepath.exists():
                    print(f"✅ {filename}")
                else:
                    print(f"❌ {filename} - MISSING")
                    all_ok = False
                    
            if all_ok:
                print("\n✅ All systems operational")
            else:
                print("\n⚠️ Some files missing. See README_INSTALLATION.md")
                
        else:
            print(f"Unknown command: {command}")
            print("Run 'omnissiah' for help")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("  Make sure all core scripts are installed.")
        print("  See README_INSTALLATION.md")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
