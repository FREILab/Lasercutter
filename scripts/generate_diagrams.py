import os
import subprocess
from os import listdir
from os.path import join, isdir

Import("env")

# Pfad relativ zur platformio.ini
DIAG_DIR = join("Elektronik", "Wiring_Plan")

def build_d2_diagrams(source, target, env):
    project_dir = env.get("PROJECT_DIR")
    abs_diag_dir = join(project_dir, DIAG_DIR)
    
    if not isdir(abs_diag_dir):
        print(f"\n[D2-INFO] Verzeichnis nicht gefunden: {abs_diag_dir}")
        return

    print(f"\n[D2-INFO] Starte Export-Vorgang (SVG, PNG, PNG-Trans)...")
    
    files_processed = 0
    for file in listdir(abs_diag_dir):
        if file.endswith(".d2"):
            base_name = file.replace(".d2", "")
            input_file = join(abs_diag_dir, file)
            
            # Export-Pfade
            out_svg = join(abs_diag_dir, f"{base_name}.svg")
            out_png = join(abs_diag_dir, f"{base_name}.png")
            out_png_trans = join(abs_diag_dir, f"{base_name}_transparent.png")
            
            try:
                # 1. SVG (Standard)
                subprocess.run(["d2", input_file, out_svg], check=True)
                
                # 2. PNG (Solid - nutzt Standard-Hintergrund des Themes, meist weiß)
                # Wir erzwingen Theme 0 (Neutral), damit es sicher hell ist
                subprocess.run(["d2", "--theme", "0", input_file, out_png], check=True)
                
                # 3. PNG (Transparent)
                subprocess.run(["d2", "--transparent", input_file, out_png_trans], check=True)
                
                print(f"  >> ERFOLG: {file} -> [SVG, PNG, PNG-Trans]")
                files_processed += 1
            except Exception as e:
                print(f"  >> FEHLER beim Export von {file}: {e}")

    if files_processed > 0:
        print(f"[D2-INFO] Fertig. {files_processed} Datei(en) verarbeitet.\n")
    else:
        print("[D2-INFO] Keine Dateien erfolgreich verarbeitet.\n")

env.AddCustomTarget(
    name="generate_docs",
    dependencies=None,
    actions=[build_d2_diagrams],
    title="D2: Diagramme rendern",
    description="Erzeugt SVG und zwei PNG-Varianten"
)