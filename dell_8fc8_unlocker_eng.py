import os
import re
import sys
import shutil
import subprocess
import tempfile

def replace_dell_patterns(hex_line):
    """Replaces target password vectors: fdaa -> fd00 and fcaa -> fc00."""
    line = hex_line.lower()
    line = line.replace("fdaa", "fd00")
    line = line.replace("fcaa", "fc00")
    return line

def parse_xxd_line(hex_line):
    """
    Simulates 'xxd -r'. Extracts the offset prior to the colon 
    and converts the subsequent hex characters back into binary bytes.
    """
    cleaned = hex_line.strip()
    if not cleaned:
        return None, None
    
    parts = cleaned.split(":")
    if len(parts) < 2:
        return None, None
        
    try:
        offset = int(parts[0], 16)
    except ValueError:
        return None, None
        
    # Korrektur: .strip() auf den String anwenden, nicht auf die Liste
    hex_data_part = parts[1].strip().split()
    # Read the first 8 columns of hex bytes (ignoring ASCII string on the right)
    pure_hex = "".join(hex_data_part[:8])
    
    try:
        new_bytes = bytes.fromhex(pure_hex)
        return offset, new_bytes
    except ValueError:
        return None, None

def scan_file_for_patterns(file_path, search_limit):
    """
    Scans the binary dump up to the specified limit.
    Generates xxd-formatted hex lines matching '00fcaa' or '00fdaa',
    handling compressed structures seamlessly regardless of spacing.
    """
    lines = []
    if not os.path.exists(file_path):
        return lines

    with open(file_path, "rb") as f:
        data = f.read(search_limit)

    # Walk through the dump in 16-byte chunks (xxd structure)
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset+16]
        
        # Build a continuous hex sequence for resilient string comparison
        full_hex = "".join(f"{b:02x}" for b in chunk)
        
        # Pattern match implementation (corresponds to egrep)
        if "00fcaa" in full_hex or "00fdaa" in full_hex:
            hex_string = " ".join(f"{b:02x}" for b in chunk)
            raw_parts = hex_string.split()
            
            # Format the output bytes into standard 2-byte pairs
            formatted_groups = []
            for i in range(0, len(raw_parts), 2):
                if i+1 < len(raw_parts):
                    formatted_groups.append(raw_parts[i] + raw_parts[i+1])
                else:
                    formatted_groups.append(raw_parts[i])
            
            # Apply the targeted hex modifications
            xxd_line = f"{offset:08x}: {' '.join(formatted_groups)}"
            modified_line = replace_dell_patterns(xxd_line)
            lines.append(modified_line)
            
    return lines

def main():
    # Handle single file parsing via terminal argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        current_dir = os.getcwd()
        bins = [f for f in os.listdir(current_dir) if f.lower().endswith(('_locked.bin', '.bin'))]
        if not bins:
            print("[-] Error: No matching .bin file found in the current directory.")
            return
        file_path = os.path.join(current_dir, bins[0])

    if not os.path.exists(file_path):
        print(f"[-] Error: Target file '{file_path}' does not exist.")
        return

    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name_without_ext, _ = os.path.splitext(base_name)
    unlocked_file_path = os.path.join(dir_name, f"{name_without_ext}_UNLOCKED.bin")
    
    # Create working clone of the target binary
    shutil.copyfile(file_path, unlocked_file_path)

    print(f"\n[+] Selected file: {base_name}")
    model_input = input("-> Please enter the Dell model number (e.g., 5400): ").strip()
    
    # Dynamic size scan limits
    search_limit = 2400000 if model_input.startswith("5") else 9000000

    # Start automated sequence extraction
    matching_lines = scan_file_for_patterns(file_path, search_limit)

    # Plattformunabhängiger Temp-Pfad (Windows nutzt AppData, Linux nutzt /tmp)
    tmp_txt_path = os.path.join(tempfile.gettempdir(), "AA_00.txt")
    with open(tmp_txt_path, "w", encoding="utf-8") as tmp_f:
        tmp_f.write("\n".join(matching_lines) + "\n")

    print("[*] Opening text editor for verification step...")
    # Erkennt das Betriebssystem und öffnet den passenden Editor
    if os.name == 'nt':
        subprocess.run(["notepad.exe", tmp_txt_path])
    elif shutil.which("gedit"):
        subprocess.run(["gedit", tmp_txt_path])
    else:
        subprocess.run(["nano", tmp_txt_path])

    input("\n[!] Are the extracted offset lines correct? Press ENTER to proceed with patch, or CTRL+C to abort...")

    # Load changes made by the operator
    with open(tmp_txt_path, "r", encoding="utf-8") as tmp_f:
        edited_lines = [l.strip() for l in tmp_f.readlines() if l.strip()]

    # Inject changes into clone file
    with open(unlocked_file_path, "rb") as f_in:
        unlocked_data = bytearray(f_in.read())

    patched_count = 0
    for line in edited_lines:
        offset, new_bytes = parse_xxd_line(line)
        if offset is not None and new_bytes is not None:
            unlocked_data[offset:offset+len(new_bytes)] = new_bytes
            patched_count += 1

    with open(unlocked_file_path, "wb") as f_out:
        f_out.write(unlocked_data)

    # Perform hex check (simulates 'cmp -l | gawk')
    with open(file_path, "rb") as f_orig:
        original_data = f_orig.read()

    diff_report = []
    for i in range(min(len(original_data), len(unlocked_data))):
        if original_data[i] != unlocked_data[i]:
            diff_report.append(f"{i:08X} {original_data[i]:02X} {unlocked_data[i]:02X}")

    print("\n" + "="*50 + "\n COMPARISON VERIFICATION REPORT \n" + "="*50)
    if diff_report:
        print("\n".join(diff_report))
    else:
        print("[-] No changes were made (File content remains identical).")
    
    file_size_mb = len(original_data) / (1024 * 1024)
    print(f"\n[+] Successfully patched {patched_count} line(s) from {file_size_mb:.1f} MB binary.")
    print(f"[+] Output saved to: {unlocked_file_path}\n")

if __name__ == "__main__":
    main()
