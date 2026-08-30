# Dell 8FC8 BIOS Password Unlocker (Python Edition)
**Entwickelt von: Markus1741 (Badcaps) / Linux User (@Linux-User925)**

Dieses Werkzeug ist ein plattformunabhängiges Python-Skript, das automatisiert die vier redundanten Passwort-Sicherheitsflags in Dell NVRAM-Dumps sucht und modifiziert. Es basiert auf dem originalen Shell-Skript-Ablauf aus meinem YouTube-Video.

Das Tool bereitet die Datei so vor, dass das Mainboard nach dem Flashen direkt im **Manufacturing Mode (Herstellungsmodus)** startet, in dem das alte BIOS-Passwort ignoriert wird.

### 🛠️ Besondere Sicherheitsfunktionen (Human-in-the-Loop)
Das Skript folgt der Philosophie: **Die Maschine sucht und bereitet vor, aber der Mensch behält die Kontrolle.**
* Es bricht die Suche nicht ab, wenn Leerzeichen im Hex-Dump verschoben sind (resistent gegen Formatierungsfehler).
* Es öffnet vor dem Patchen automatisch einen Texteditor (`gedit` unter Linux / `Notepad` unter Windows).
* **Wichtig:** Der Techniker muss manuell überprüfen, ob genau die typischen 4 Zeilen gefunden wurden, bevor das Skript die Datei patcht. Das schützt das BIOS zuverlässig vor Datenkorruption.

### 🚀 Voraussetzungen & Nutzung
Das Skript läuft unter Linux (Ubuntu), Windows und macOS. Es benötigt keine manuellen Installationen.

1. Lege deinen gesperrten Dump (z.B. `backup_locked.bin`) in denselben Ordner wie das Skript.
2. Starte das Skript im Terminal:
   ```bash
   python3 dell_8fc8_unlocker.py
   ```
3. Gib die Modellnummer ein (z.B. `5520`).
4. Kontrolliere die Zeilen im Editor, schließe ihn und drücke **ENTER** im Terminal.

### 📜 Lizenz & Gemeinnützigkeit
Dieses Projekt ist gemeinnützig und steht unter der MIT-Lizenz. Es darf frei geteilt, genutzt und modifiziert werden, solange der Urheber genannt wird. Es wird ohne jegliche Gewährleistung oder Haftung bereitgestellt.

# Dell 8FC8 BIOS Password Unlocker (Python Edition)
**Developed by: Markus1741 (Badcaps) / Linux User (@Linux-User925)**

This utility is a platform-independent Python script designed to automatically locate and modify the four redundant password verification flags inside Dell NVRAM storage blocks. It is based on the original shell script workflow featured on my YouTube channel.

The tool prepares the binary dump so that upon flashing, the motherboard is forced into **Manufacturing Mode**, bypassing the locked BIOS administrator password.

### 🛠️ Human-in-the-Loop Safety Features
This tool strictly follows a safe repair philosophy: **The machine scans and prepares, but the human remains in control.**
* **Resilient Parsing:** The search algorithm handles compressed structures and spacing anomalies smoothly, mitigating layout formatting shifts.
* **Mandatory Verification Step:** Before any data is modified, the script automatically opens a text editor (`gedit` on Linux / `Notepad` on Windows) displaying the extracted lines.
* **Brick Prevention:** The operator must manually review the file to ensure exactly the expected 4 lines are modified. Pressing ENTER in the terminal only commits the changes after this human approval, keeping the rest of the 32MB image entirely safe from corruption.

### 🚀 Requirements & Usage
Since this is pure Python, it runs natively on Linux (Ubuntu), Windows, and macOS without requiring heavy dependencies or external compilers.

1. Place your locked BIOS dump (e.g., `backup_locked.bin`) into the same directory as the script.
2. Launch the utility from your terminal or command prompt:
   ```bash
   python3 dell_8fc8_unlocker.py
   ```
3. Enter the Dell model number when prompted (e.g., `5520`).
4. Review the extracted lines in the editor, close the editor window, and press **ENTER** in the terminal to patch the file.
5. Review the final `COMPARISON VERIFICATION REPORT` printed in your terminal to ensure precise byte modifications.

### 📜 Open Source & Community Policy
This project is strictly non-commercial and published under the MIT License. It may be freely used, shared, and modified by technicians worldwide, provided that original authorship credits are preserved. The software is provided "as is", without warranty of any kind.


