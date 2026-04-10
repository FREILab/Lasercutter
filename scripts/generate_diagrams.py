import os
import subprocess
from os import listdir
from os.path import join, isdir

Import("env")

DIAG_DIR = join("Elektronik", "Wiring_Plan")

def build_d2_diagrams(source, target, env):
    project_dir = env.get("PROJECT_DIR")
    abs_diag_dir = join(project_dir, DIAG_DIR)
    
    if not isdir(abs_diag_dir):
        print(f"\n[D2-INFO] Verzeichnis nicht gefunden: {abs_diag_dir}")
        return

    print(f"\n[D2-INFO] Starte Export-Vorgang...")
    
    files_processed = 0
    for file in listdir(abs_diag_dir):
        if file.endswith(".d2"):
            input_file = join(abs_diag_dir, file)
            base_name = file.replace(".d2", "")
            
            # Export-Formate
            formats = [
                {"ext": "svg", "args": []},
                {"ext": "png", "args": ["--theme", "200"]}, # Theme 200 ist meist neutral/hell
                {"ext": "transparent.png", "args": ["--transparent"]}
            ]
            
            for fmt in formats:
                output_file = join(abs_diag_dir, f"{base_name}.{fmt['ext']}")
                cmd = ["d2"] + fmt["args"] + [input_file, output_file]
                
                try:
                    # Capture_output=True erlaubt uns, die Fehlermeldung von D2 zu lesen
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"  >> FEHLER bei {file} ({fmt['ext']}):")
                    print(f"     Status: {e.returncode}")
                    print(f"     Meldung: {e.stderr.strip()}")
                    continue

            print(f"  >> ERFOLG: {file} verarbeitet.")
            files_processed += 1

    print(f"[D2-INFO] Fertig. {files_processed} Datei(en) verarbeitet.\n")

env.AddCustomTarget(
    name="generate_docs",
    dependencies=None,
    actions=[build_d2_diagrams],
    title="D2: Diagramme rendern",
    description="Erzeugt SVG und PNG-Varianten"
)
