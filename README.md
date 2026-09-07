# Dell 8FC8 BIOS Password Unlocker (Python Edition)
**Entwickelt von: Markus1741 (Badcaps) / Linux User (@Linux-User925)**

Dieses Werkzeug ist ein plattformunabhängiges Python-Skript, das automatisiert die vier redundanten Passwort-Sicherheitsflags in Dell NVRAM-Dumps sucht und modifiziert. Es basiert auf dem originalen Shell-Skript-Ablauf aus meinem YouTube-Video.

Das Tool bereitet die Datei so vor, dass das Mainboard nach dem Flashen direkt im **Manufacturing Mode (Herstellungsmodus)** startet, in dem das alte BIOS-Passwort ignoriert wird.

### 🛠️ Besondere Sicherheitsfunktionen (Human-in-the-Loop)
Das Skript folgt der Philosophie: **Die Maschine sucht und bereitet vor, aber der Mensch behält die Kontrolle.**
* Es bricht die Suche nicht ab, wenn Leerzeichen im Hex-Dump verschoben sind (resistent gegen Formatierungsfehler).
* Es erkennt dein Betriebssystem und öffnet vor dem Patchen automatisch den passenden Texteditor (**`Notepad` unter Windows** / `gedit` oder `nano` unter Linux).
* **Wichtig:** Der Techniker muss manuell überprüfen, ob genau die typischen 4 Zeilen gefunden wurden, bevor das Skript die Datei patcht. Das schützt das BIOS zuverlässig vor Datenkorruption.

### 🚀 Voraussetzungen & Nutzung
Das Skript läuft nativ unter Windows 11/10, Linux (Ubuntu) und macOS. Es benötigt keine manuellen Installationen von Drittanbietern.

1. Lege deinen gesperrten Dump (z.B. `backup_locked.bin`) in denselben Ordner wie das Skript.
2. Öffne dein Terminal (CMD/PowerShell unter Windows oder Terminal unter Linux) in diesem Ordner.
3. Starte das Skript mit dem passenden Befehl für dein Betriebssystem:
   * **Windows:**
     ```cmd
     python dell_8fc8_unlocker_eng.py
     ```
   * **Linux (Ubuntu) / macOS:**
     ```bash
     python3 dell_8fc8_unlocker_eng.py
     ```
4. Gib die Modellnummer ein (z.B. `5501`).
5. Kontrolliere die Zeilen im automatisch geöffneten Editor, schließe das Editor-Fenster und drücke **ENTER** im Terminal, um den Patch anzuwenden.

### 📜 Lizenz & Gemeinnützigkeit
Dieses Projekt ist gemeinnützig und steht unter der MIT-Lizenz. Es darf frei geteilt, genutzt und modifiziert werden, solange der Urheber genannt wird. Es wird ohne jegliche Gewährleistung oder Haftung bereitgestellt.

---

# Dell 8FC8 BIOS Password Unlocker (Python Edition)
**Developed by: Markus1741 (Badcaps) / Linux User (@Linux-User925)**

This utility is a platform-independent Python script designed to automatically locate and modify the four redundant password verification flags inside Dell NVRAM storage blocks. It is based on the original shell script workflow featured on my YouTube channel.

The tool prepares the binary dump so that upon flashing, the motherboard is forced into **Manufacturing Mode**, bypassing the locked BIOS administrator password.

### 🛠️ Human-in-the-Loop Safety Features
This tool strictly follows a safe repair philosophy: **The machine scans and prepares, but the human remains in control.**
* **Resilient Parsing:** The search algorithm handles compressed structures and spacing anomalies smoothly, mitigating layout formatting shifts.
* **Mandatory Verification Step:** Before any data is modified, the script automatically detects your OS and opens a native text editor (**`Notepad` on Windows** / `gedit` or `nano` on Linux) displaying the extracted lines.
* **Brick Prevention:** The operator must manually review the file to ensure exactly the expected 4 lines are modified. Pressing ENTER in the terminal only commits the changes after this human approval, keeping the rest of the 32MB image entirely safe from corruption.

### 🚀 Requirements & Usage
Since this is pure Python, it runs natively on Windows 11/10, Linux (Ubuntu), and macOS without requiring heavy dependencies or external compilers.

1. Place your locked BIOS dump (e.g., `backup_locked.bin`) into the same directory as the script.
2. Open your command prompt or terminal inside this directory.
3. Launch the utility using the correct command for your operating system:
   * **Windows:**
     ```cmd
     python dell_8fc8_unlocker_eng.py
     ```
   * **Linux (Ubuntu) / macOS:**
     ```bash
     python3 dell_8fc8_unlocker_eng.py
     ```
4. Enter the Dell model number when prompted (e.g., `5501`).
5. Review the extracted lines in the editor, close the editor window, and press **ENTER** in the terminal to patch the file.
6. Review the final `COMPARISON VERIFICATION REPORT` printed in your terminal to ensure precise byte modifications.

### 📜 Open Source & Community Policy
This project is strictly non-commercial and published under the MIT License. It may be freely used, shared, and modified by technicians worldwide, provided that original authorship credits are preserved. The software is provided "as is", without warranty of any kind.
