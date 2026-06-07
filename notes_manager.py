#!/usr/bin/env python3
"""
Notes Manager for OSCP Cheat Sheet
Supports: Create, Read, Update, Delete, Append operations on notes.json
"""

import json
import base64
import os
import sys
import argparse
from typing import Dict, List, Optional, Any

class NotesManager:
    def __init__(self, json_file: str = "notes.json"):
        self.json_file = json_file
        self.data: List[Dict] = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load existing data from notes.json"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Error: {self.json_file} is corrupted. Starting with empty data.")
                self.data = []
            except Exception as e:
                print(f"❌ Error loading {self.json_file}: {e}")
                self.data = []
        else:
            print(f"⚠️  {self.json_file} not found. Creating new file.")
            self.data = []
    
    def save_data(self) -> None:
        """Save data to notes.json"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"✅ Successfully saved to {self.json_file}")
        except Exception as e:
            print(f"❌ Error saving to {self.json_file}: {e}")
    
    @staticmethod
    def encode_to_base64(text: str) -> str:
        """Encode plain text to base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_from_base64(encoded: str) -> str:
        """Decode base64 to plain text"""
        try:
            return base64.b64decode(encoded).decode('utf-8')
        except Exception:
            return encoded
    
    def find_note_index(self, button_name: str) -> Optional[int]:
        """Find index of note by button_name"""
        for i, note in enumerate(self.data):
            if note.get('button_name') == button_name:
                return i
        return None
    
    def find_content_index(self, note_index: int, sub_header: str) -> Optional[int]:
        """Find content index by sub_header within a note"""
        for i, content in enumerate(self.data[note_index]['contents']):
            if content.get('sub_header') == sub_header:
                return i
        return None
    
    def add_note(self, button_name: str, note_header: str, contents: List[Dict] = None) -> bool:
        """
        Add a new note (button)
        
        Args:
            button_name: Name displayed on the button
            note_header: Header shown when note is selected
            contents: List of content dicts with sub_header and plain text content
        
        Example:
            contents = [
                {
                    "sub_header": "Directory Fuzzing",
                    "content": "ffuf -w wordlist.txt -u https://target/FUZZ"
                }
            ]
        """
        if self.find_note_index(button_name) is not None:
            print(f"❌ Note with button_name '{button_name}' already exists!")
            return False
        
        # Encode contents to base64 if they're plain text
        encoded_contents = []
        if contents:
            for content_item in contents:
                encoded_contents.append({
                    "sub_header": content_item.get("sub_header", ""),
                    "content": self.encode_to_base64(content_item.get("content", ""))
                })
        
        new_note = {
            "button_name": button_name,
            "note_header": note_header,
            "contents": encoded_contents
        }
        
        self.data.append(new_note)
        self.save_data()
        print(f"✅ Added new note: '{button_name}'")
        return True
    
    def add_content(self, button_name: str, sub_header: str, content: str, append: bool = False) -> bool:
        """
        Add new content to an existing note
        
        Args:
            button_name: Target button name
            sub_header: Sub-header for the new content
            content: Plain text content (will be encoded to base64)
            append: If True, append to existing content with same sub_header
                   If False, create new content entry (or error if exists)
        """
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{button_name}' not found!")
            return False
        
        # Check if sub_header already exists
        content_index = self.find_content_index(note_index, sub_header)
        
        if content_index is not None:
            if append:
                # Append to existing content
                existing_content = self.data[note_index]['contents'][content_index]['content']
                existing_decoded = self.decode_from_base64(existing_content)
                
                # Combine existing and new content
                combined = existing_decoded + "\n" + content
                self.data[note_index]['contents'][content_index]['content'] = self.encode_to_base64(combined)
                self.save_data()
                print(f"✅ Appended to existing content '{sub_header}' in '{button_name}'")
                return True
            else:
                print(f"❌ Content with sub_header '{sub_header}' already exists! Use --append to add more commands.")
                return False
        
        # Create new content entry
        new_content = {
            "sub_header": sub_header,
            "content": self.encode_to_base64(content)
        }
        
        self.data[note_index]['contents'].append(new_content)
        self.save_data()
        print(f"✅ Added new content to '{button_name}': '{sub_header}'")
        return True
    
    def update_note(self, old_button_name: str, new_button_name: str = None, new_note_header: str = None) -> bool:
        """Update button_name and/or note_header of an existing note"""
        note_index = self.find_note_index(old_button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{old_button_name}' not found!")
            return False
        
        if new_button_name:
            # Check if new button_name conflicts
            if self.find_note_index(new_button_name) is not None and new_button_name != old_button_name:
                print(f"❌ Note with button_name '{new_button_name}' already exists!")
                return False
            self.data[note_index]['button_name'] = new_button_name
            print(f"✅ Updated button_name from '{old_button_name}' to '{new_button_name}'")
        
        if new_note_header:
            self.data[note_index]['note_header'] = new_note_header
            print(f"✅ Updated note_header to '{new_note_header}'")
        
        self.save_data()
        return True
    
    def update_content(self, button_name: str, sub_header: str, new_sub_header: str = None, new_content: str = None) -> bool:
        """Update sub_header and/or content of an existing content item"""
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{button_name}' not found!")
            return False
        
        content_index = self.find_content_index(note_index, sub_header)
        if content_index is None:
            print(f"❌ Content with sub_header '{sub_header}' not found!")
            return False
        
        if new_sub_header:
            self.data[note_index]['contents'][content_index]['sub_header'] = new_sub_header
            print(f"✅ Updated sub_header from '{sub_header}' to '{new_sub_header}'")
        
        if new_content:
            self.data[note_index]['contents'][content_index]['content'] = self.encode_to_base64(new_content)
            print(f"✅ Updated content for '{new_sub_header or sub_header}'")
        
        self.save_data()
        return True
    
    def delete_note(self, button_name: str) -> bool:
        """Delete an entire note (button)"""
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{button_name}' not found!")
            return False
        
        deleted = self.data.pop(note_index)
        self.save_data()
        print(f"✅ Deleted note: '{deleted['button_name']}'")
        return True
    
    def delete_content(self, button_name: str, sub_header: str) -> bool:
        """Delete specific content from a note"""
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{button_name}' not found!")
            return False
        
        content_index = self.find_content_index(note_index, sub_header)
        if content_index is None:
            print(f"❌ Content with sub_header '{sub_header}' not found!")
            return False
        
        deleted = self.data[note_index]['contents'].pop(content_index)
        self.save_data()
        print(f"✅ Deleted content '{deleted['sub_header']}' from '{button_name}'")
        return True
    
    def overwrite_note(self, button_name: str, note_header: str, contents: List[Dict]) -> bool:
        """
        Completely overwrite an existing note
        
        Args:
            button_name: Button name (must exist)
            note_header: New header
            contents: New contents list (plain text, will be encoded)
        """
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note with button_name '{button_name}' not found! Use 'add-note' to create new.")
            return False
        
        encoded_contents = []
        for content_item in contents:
            encoded_contents.append({
                "sub_header": content_item.get("sub_header", ""),
                "content": self.encode_to_base64(content_item.get("content", ""))
            })
        
        self.data[note_index] = {
            "button_name": button_name,
            "note_header": note_header,
            "contents": encoded_contents
        }
        
        self.save_data()
        print(f"✅ Overwrote note: '{button_name}'")
        return True
    
    def list_notes(self) -> None:
        """Display all notes with their sub_headers"""
        if not self.data:
            print("📭 No notes found.")
            return
        
        print(f"\n📚 Total Notes: {len(self.data)}\n")
        print("=" * 70)
        for i, note in enumerate(self.data, 1):
            print(f"\n{i}. 🔘 {note['button_name']}")
            print(f"   📌 Header: {note['note_header']}")
            print(f"   📄 Contents ({len(note['contents'])} items):")
            for content in note['contents']:
                print(f"      └─ {content['sub_header']}")
        print("\n" + "=" * 70)
    
    def show_note(self, button_name: str, decode_content: bool = False) -> None:
        """Display a specific note's full content"""
        note_index = self.find_note_index(button_name)
        if note_index is None:
            print(f"❌ Note '{button_name}' not found!")
            return
        
        note = self.data[note_index]
        print(f"\n🔘 Button: {note['button_name']}")
        print(f"📌 Header: {note['note_header']}")
        print(f"\n📄 Contents ({len(note['contents'])} items):\n")
        print("-" * 70)
        
        for i, content in enumerate(note['contents'], 1):
            print(f"\n{i}. 📎 {content['sub_header']}")
            if decode_content:
                decoded = self.decode_from_base64(content['content'])
                print(f"   💻 Command:\n   {decoded}")
            else:
                print(f"   💾 Base64: {content['content'][:50]}...")
        print("\n" + "-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="OSCP Notes Manager - Manage your notes.json with CRUD operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a new note
  python3 notes_manager.py add-note "Redis Enum" "Redis Enumeration" --content "Redis Enum" "redis-cli -h <IP> info" --content "Redis Keys" "redis-cli -h <IP> keys *"
  
  # Add content to existing note (creates new or fails if exists)
  python3 notes_manager.py add-content "Info Gathering For All" "SMB Enumeration" "smbclient -L //<IP>/ -N"
  
  # APPEND to existing content (adds more commands to same sub_header)
  python3 notes_manager.py add-content "Info Gathering For All" "SMB Enumeration" "smbmap -H <IP>" --append
  python3 notes_manager.py add-content "Info Gathering For All" "SMB Enumeration" "enum4linux -a <IP>" --append
  
  # Append multiple lines at once
  python3 notes_manager.py add-content "Info Gathering For All" "SMB Enumeration" "nmap --script smb-enum-shares.nse -p445 <IP>
nmap --script smb-os-discovery.nse -p445 <IP>" --append
  
  # Update note header
  python3 notes_manager.py update-note "Info Gathering For All" --new-header "Advanced Information Gathering"
  
  # Update content
  python3 notes_manager.py update-content "Info Gathering For All" "Directory and File Fuzzing with Ffuf" --new-content "ffuf -w /usr/share/wordlists/dirb/common.txt -u https://[ip]/FUZZ -mc 200,301,302"
  
  # Delete content
  python3 notes_manager.py delete-content "Info Gathering For All" "WordPress XML-RPC Password Bruteforce"
  
  # Delete note
  python3 notes_manager.py delete-note "Old Note Name"
  
  # List all notes
  python3 notes_manager.py list
  
  # Show note with decoded content
  python3 notes_manager.py show "Reverse Shell" --decode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add Note command
    add_note_parser = subparsers.add_parser('add-note', help='Add a new note')
    add_note_parser.add_argument('button_name', help='Button name')
    add_note_parser.add_argument('note_header', help='Note header')
    add_note_parser.add_argument('--content', action='append', nargs=2, metavar=('SUB_HEADER', 'CONTENT'),
                                 help='Add content (can be used multiple times)')
    
    # Add Content command (with append option)
    add_content_parser = subparsers.add_parser('add-content', help='Add content to existing note')
    add_content_parser.add_argument('button_name', help='Target button name')
    add_content_parser.add_argument('sub_header', help='Sub-header for new content')
    add_content_parser.add_argument('content', help='Plain text content')
    add_content_parser.add_argument('--append', '-a', action='store_true', 
                                   help='Append to existing content instead of creating new (or failing)')
    
    # Update Note command
    update_note_parser = subparsers.add_parser('update-note', help='Update note metadata')
    update_note_parser.add_argument('button_name', help='Current button name')
    update_note_parser.add_argument('--new-name', help='New button name')
    update_note_parser.add_argument('--new-header', help='New note header')
    
    # Update Content command
    update_content_parser = subparsers.add_parser('update-content', help='Update content')
    update_content_parser.add_argument('button_name', help='Button name')
    update_content_parser.add_argument('sub_header', help='Current sub-header')
    update_content_parser.add_argument('--new-sub', help='New sub-header')
    update_content_parser.add_argument('--new-content', help='New content (plain text)')
    
    # Delete Note command
    delete_note_parser = subparsers.add_parser('delete-note', help='Delete a note')
    delete_note_parser.add_argument('button_name', help='Button name to delete')
    
    # Delete Content command
    delete_content_parser = subparsers.add_parser('delete-content', help='Delete content from note')
    delete_content_parser.add_argument('button_name', help='Button name')
    delete_content_parser.add_argument('sub_header', help='Sub-header to delete')
    
    # Overwrite Note command
    overwrite_parser = subparsers.add_parser('overwrite', help='Completely overwrite a note')
    overwrite_parser.add_argument('button_name', help='Button name (must exist)')
    overwrite_parser.add_argument('note_header', help='New note header')
    overwrite_parser.add_argument('--content', action='append', nargs=2, metavar=('SUB_HEADER', 'CONTENT'),
                                  help='Content items (can be used multiple times)')
    
    # List command
    subparsers.add_parser('list', help='List all notes')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show specific note')
    show_parser.add_argument('button_name', help='Button name to show')
    show_parser.add_argument('--decode', action='store_true', help='Decode base64 content')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = NotesManager()
    
    if args.command == 'add-note':
        contents = []
        if args.content:
            for sub_header, content in args.content:
                contents.append({"sub_header": sub_header, "content": content})
        manager.add_note(args.button_name, args.note_header, contents if contents else None)
    
    elif args.command == 'add-content':
        manager.add_content(args.button_name, args.sub_header, args.content, args.append)
    
    elif args.command == 'update-note':
        manager.update_note(args.button_name, args.new_name, args.new_header)
    
    elif args.command == 'update-content':
        manager.update_content(args.button_name, args.sub_header, args.new_sub, args.new_content)
    
    elif args.command == 'delete-note':
        manager.delete_note(args.button_name)
    
    elif args.command == 'delete-content':
        manager.delete_content(args.button_name, args.sub_header)
    
    elif args.command == 'overwrite':
        contents = []
        if args.content:
            for sub_header, content in args.content:
                contents.append({"sub_header": sub_header, "content": content})
        manager.overwrite_note(args.button_name, args.note_header, contents)
    
    elif args.command == 'list':
        manager.list_notes()
    
    elif args.command == 'show':
        manager.show_note(args.button_name, args.decode)


if __name__ == "__main__":
    main()
