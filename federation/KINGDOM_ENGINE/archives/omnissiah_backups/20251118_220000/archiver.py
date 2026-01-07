#!/usr/bin/env python3
"""
📚 AI CONVERSATION ARCHIVER
Preserves AI conversations with metadata and searchable index
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import hashlib
import re

class ConversationArchiver:
    """Archive and retrieve AI conversations"""
    
    def __init__(self, archive_dir="/sdcard/Omnissiah_Workspace/conversations"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.archive_dir / "index.json"
        self.load_index()
    
    def load_index(self):
        """Load or create conversation index"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                'conversations': [],
                'tags': {},
                'ai_systems': {},
                'total_conversations': 0
            }
    
    def save_index(self):
        """Persist index to disk"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def save_conversation(self, content, ai_system='unknown', 
                         topic='general', tags=None):
        """
        Archive a conversation
        
        Args:
            content: Full conversation text
            ai_system: 'claude', 'gpt', 'deepseek', etc.
            topic: Main topic/category  
            tags: List of tag strings
            
        Returns:
            conversation_id
        """
        timestamp = datetime.now()
        
        # Generate unique ID
        conv_id = hashlib.md5(
            f"{timestamp.isoformat()}{content[:100]}".encode()
        ).hexdigest()[:12]
        
        # Create conversation record
        record = {
            'id': conv_id,
            'timestamp': timestamp.isoformat(),
            'ai_system': ai_system,
            'topic': topic,
            'tags': tags or [],
            'word_count': len(content.split()),
            'char_count': len(content),
            'preview': content[:200].replace('\n', ' ')
        }
        
        # Save full content
        content_file = self.archive_dir / f"{conv_id}.txt"
        with open(content_file, 'w') as f:
            f.write(content)
            
        # Save metadata
        meta_file = self.archive_dir / f"{conv_id}.meta.json"
        with open(meta_file, 'w') as f:
            json.dump(record, f, indent=2)
            
        # Update index
        self.index['conversations'].append(record)
        self.index['total_conversations'] += 1
        
        # Update tag index
        for tag in record['tags']:
            if tag not in self.index['tags']:
                self.index['tags'][tag] = []
            self.index['tags'][tag].append(conv_id)
            
        # Update AI system index
        if ai_system not in self.index['ai_systems']:
            self.index['ai_systems'][ai_system] = []
        self.index['ai_systems'][ai_system].append(conv_id)
        
        self.save_index()
        return conv_id

    def search(self, query, search_content=True):
        """
        Search conversations
        
        Args:
            query: Search string
            search_content: If True, search full content; else just metadata
            
        Returns:
            List of matching conversation records
        """
        query_lower = query.lower()
        matches = []
        
        for record in self.index['conversations']:
            # Search metadata
            if (query_lower in record['topic'].lower() or
                query_lower in record['ai_system'].lower() or
                query_lower in record['preview'].lower() or
                any(query_lower in tag.lower() for tag in record['tags'])):
                matches.append(record)
                continue
                
            # Search full content if enabled
            if search_content:
                conv_id = record['id']
                content_file = self.archive_dir / f"{conv_id}.txt"
                if content_file.exists():
                    with open(content_file, 'r') as f:
                        content = f.read()
                    if query_lower in content.lower():
                        matches.append(record)
                        
        return matches

    def get_conversation(self, conv_id):
        """Retrieve full conversation by ID"""
        content_file = self.archive_dir / f"{conv_id}.txt"
        meta_file = self.archive_dir / f"{conv_id}.meta.json"
        
        if not content_file.exists():
            return None
            
        with open(content_file, 'r') as f:
            content = f.read()
            
        with open(meta_file, 'r') as f:
            metadata = json.load(f)
            
        return {
            'metadata': metadata,
            'content': content
        }

    def list_recent(self, n=10, ai_system=None, topic=None):
        """List most recent conversations"""
        conversations = self.index['conversations']
        
        # Filter if requested
        if ai_system:
            conversations = [c for c in conversations 
                           if c['ai_system'] == ai_system]
        if topic:
            conversations = [c for c in conversations 
                           if c['topic'] == topic]
            
        # Sort by timestamp (most recent first)
        sorted_convs = sorted(conversations, 
                            key=lambda x: x['timestamp'], 
                            reverse=True)
        return sorted_convs[:n]

    def get_stats(self):
        """Get archive statistics"""
        stats = {
            'total': self.index['total_conversations'],
            'by_ai': {},
            'by_topic': {},
            'by_tag': {},
            'total_words': 0
        }
        
        # Count by AI system
        for ai, convs in self.index['ai_systems'].items():
            stats['by_ai'][ai] = len(convs)
            
        # Count by topic and accumulate words
        topic_counts = {}
        for conv in self.index['conversations']:
            topic = conv['topic']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            stats['total_words'] += conv['word_count']
            
        stats['by_topic'] = topic_counts
        
        # Count by tag
        for tag, convs in self.index['tags'].items():
            stats['by_tag'][tag] = len(convs)
            
        return stats

def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='Archive AI conversations')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Save command
    save_parser = subparsers.add_parser('save', help='Save a conversation')
    save_parser.add_argument('content', help='Conversation content or file path')
    save_parser.add_argument('--ai', default='unknown', help='AI system (claude/gpt/deepseek)')
    save_parser.add_argument('--topic', default='general', help='Main topic')
    save_parser.add_argument('--tags', nargs='+', help='Tags for categorization')
    save_parser.add_argument('--file', action='store_true', help='Content is a file path')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search conversations')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--full', action='store_true', help='Search full content')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List conversations')
    list_parser.add_argument('--recent', type=int, default=10, help='Number to show')
    list_parser.add_argument('--ai', help='Filter by AI system')
    list_parser.add_argument('--topic', help='Filter by topic')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get conversation by ID')
    get_parser.add_argument('id', help='Conversation ID')
    
    # Stats command
    subparsers.add_parser('stats', help='Show archive statistics')
    
    args = parser.parse_args()
    archiver = ConversationArchiver()
    
    if args.command == 'save':
        # Get content
        if args.file:
            with open(args.content, 'r') as f:
                content = f.read()
        else:
            content = args.content
            
        # Save
        conv_id = archiver.save_conversation(
            content=content,
            ai_system=args.ai,
            topic=args.topic,
            tags=args.tags
        )
        print(f"✅ Saved conversation: {conv_id}")
        print(f"   AI: {args.ai}")
        print(f"   Topic: {args.topic}")
        print(f"   Words: {len(content.split())}")
        
    elif args.command == 'search':
        matches = archiver.search(args.query, search_content=args.full)
        print(f"\n🔍 Found {len(matches)} matches for '{args.query}':\n")
        for match in matches:
            print(f"ID: {match['id']}")
            print(f"Date: {match['timestamp'][:10]}")
            print(f"AI: {match['ai_system']} | Topic: {match['topic']}")
            print(f"Preview: {match['preview']}")
            print("-" * 60)
            
    elif args.command == 'list':
        recent = archiver.list_recent(
            n=args.recent,
            ai_system=args.ai,
            topic=args.topic
        )
        print(f"\n📚 Recent conversations ({len(recent)}):\n")
        for conv in recent:
            print(f"ID: {conv['id']}")
            print(f"Date: {conv['timestamp'][:10]}")
            print(f"AI: {conv['ai_system']} | Topic: {conv['topic']}")
            print(f"Preview: {conv['preview']}")
            print("-" * 60)
            
    elif args.command == 'get':
        result = archiver.get_conversation(args.id)
        if result:
            print(f"\n📄 Conversation {args.id}:\n")
            print(json.dumps(result['metadata'], indent=2))
            print("\n" + "="*60 + "\n")
            print(result['content'])
        else:
            print(f"❌ Conversation {args.id} not found")
            
    elif args.command == 'stats':
        stats = archiver.get_stats()
        print("\n📊 ARCHIVE STATISTICS\n")
        print(f"Total conversations: {stats['total']}")
        print(f"Total words: {stats['total_words']:,}")
        print(f"\nBy AI system:")
        for ai, count in sorted(stats['by_ai'].items()):
            print(f"  {ai}: {count}")
        print(f"\nTop topics:")
        for topic, count in sorted(stats['by_topic'].items(),
                                 key=lambda x: x[1],
                                 reverse=True)[:10]:
            print(f"  {topic}: {count}")
        print(f"\nTop tags:")
        for tag, count in sorted(stats['by_tag'].items(),
                               key=lambda x: x[1],
                               reverse=True)[:10]:
            print(f"  {tag}: {count}")

if __name__ == "__main__":
    main()
