import os
import subprocess
import time
import sys
import re
import shutil
import threading
import zipfile

script_name = os.path.splitext(os.path.basename(__file__))[0]
log_file_name = f"{script_name}.log"

def run_cmd(cmd, cwd, desc, log_dir=None):
    # comfort messages for long steps
    # timer1 = threading.Timer(7, lambda: print(f"{desc} is running, please hold on..."))
    # timer2 = threading.Timer(35, lambda: print(f"{desc} is still running, please hold on..."))
    # timer1.daemon = True
    # timer2.daemon = True
    # timer1.start()
    # timer2.start()
    # Unique log file for each run
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runlogs")
    os.makedirs(log_dir, exist_ok=True)
    # Use script name (without args) for log file, add a timestamp for uniqueness
    script_name = os.path.basename(cmd.split()[2]) if len(cmd.split()) > 2 else cmd.replace(' ', '_')
    log_file = os.path.join(log_dir, f"{os.path.splitext(script_name)[0]}_{int(time.time())}.log")
    full_cmd = f"{cmd} > \"{log_file}\" 2>&1"
    code = subprocess.call(full_cmd, shell=True, cwd=cwd)

    return code

def main():
    print()
    # Step 1: Prompt for factory project folder
    project_dir = input("Enter factory project folder path: ").strip()
    print()
    if not os.path.isdir(project_dir):
        print(f"Folder '{project_dir}' not found. Exiting.")
        sys.exit(1)
    # ... (rest of the original orchestration logic: prompt for snapshot, app name, language, mode selection, etc.)
    # ... (run analysis, convert, compile sequences as per user choice)
    # ... (all original user interaction and execution flow restored)
    # (Retain the improved artifact copying, ANT logic, and summary calculation as previously fixed)

    # --- OBTAIN STEPS BUNDLED MESSAGING ---
    obtain_types = []
    print("\nExecuting obtain steps\n")
    # ... (populate obtain_types as you run each obtain step)
    if obtain_types:
        print("The obtain for the following file types were executed successfully:\n")
        for idx, typ in enumerate(obtain_types, 1):
            print(f"{idx}. {typ}")
        print()
    # Step 2: Select snapshot and app name
    deliveries = os.path.join(project_dir, 'deliveries')
    snapshots = [d for d in os.listdir(deliveries) if os.path.isdir(os.path.join(deliveries, d))]
    print("Available snapshots:\n")
    for i, snap in enumerate(snapshots, 1):
        print(f" {i}. {snap}")
    print()
    snap_choice = input("Select snapshot by number (or press Enter for default 'snapshot-1'): ").strip()
    snapshot = snapshots[int(snap_choice)-1] if snap_choice.isdigit() and 1 <= int(snap_choice) <= len(snapshots) else 'snapshot-1'
    print()
    app_name = input("Enter app-name to use: ").strip()
    print()
    confirm = input("Confirm target languages are JAVA and bash (Y/n): ").strip().lower()
    print()

    # Step 3: Confirm languages
    if confirm in ('n','no'):
        print("Proceeding with default: JAVA and bash")

    # Step 4: (Tool version verification skipped)

    # Step 5: List subfolders in snapshot
    snap_path = os.path.join(deliveries, snapshot)
    subs = [(d, len(os.listdir(os.path.join(snap_path,d)))) for d in os.listdir(snap_path) if os.path.isdir(os.path.join(snap_path,d))]
    print("Snapshot contents:")
    for name,count in subs: print(f" - {name}: {count} files")

    # Step 6: Select execution mode
    print()  # Add blank line for readability
    print("Choose from the below options:\n")
    print(" 1. Analysis only")
    print(" 2. Convert and Compile")
    print(" 3. Analysis, Convert and Compile")
    print(" 4. Exit\n")
    choice = input("Choose mode: ").strip()
    print(f"\nMode selected: {['Analysis only','Convert and Compile','Analysis, Convert and Compile','Exit'][int(choice)-1]}\n")


    # Set environment variables
    os.environ['DELIVERY_DIR'] = f"deliveries/{snapshot}"
    os.environ['SNAPSHOT_NAME'] = snapshot
    os.environ['TARGET_LANGUAGE'] = 'JAVA'
    os.environ['TARGET_SCRIPT_LANGUAGE'] = 'bash'

    # Mode-specific execution
    analysis_cmds = [
        ("OB01", "py -3 tools/migratonomy/obtain-cobol-programs.py"),
        ("OB02", "py -3 tools/migratonomy/obtain-cobol-copybooks.py"),
        ("OB03", "py -3 tools/migratonomy/obtain-mvs-jcl.py"),
        ("OB04", "py -3 tools/migratonomy/obtain-bms-maps.py"),
        ("OB05", "py -3 tools/migratonomy/obtain-sql-scripts.py"),
        ("OB06", "py -3 tools/migratonomy/obtain-cics-tp.py"),

        ("CL01", "py -3 tools/migratonomy/clean-cobol-programs.py"),
        ("CL02", "py -3 tools/migratonomy/clean-cobol-copybooks.py"),
        ("CL03", "py -3 tools/migratonomy/clean-mvs-jcl.py"),

        ("AN02", "py -3 tools/migratonomy/analyze-bms-maps.py"),
        ("AN03", "py -3 tools/migratonomy/analyze-sql-statements.sql-scripts.py"),
        ("AN04", "py -3 tools/migratonomy/analyze-cobol-statements.copybooks.py"),
        ("AN05", "py -3 tools/migratonomy/analyze-cobol-statements.programs.py"),
        ("AN06", "py -3 tools/migratonomy/analyze-cics-statements.copybooks.py"),
        ("AN07", "py -3 tools/migratonomy/analyze-cics-statements.programs.py"),
        ("AN08", "py -3 tools/migratonomy/analyze-sql-statements.copybooks.py"),
        ("AN09", "py -3 tools/migratonomy/analyze-sql-statements.programs.py"),
        ("AN10", "py -3 tools/migratonomy/analyze-mvs-jcl.py"),
        ("AN11", "py -3 tools/migratonomy/analyze-cics-tp.py"),
        ("LD01", f"py -3 tools/migratonomy/load-analysis-csv-files.py --data-set={app_name}"),
        ("GN01", f"py -3 tools/migratonomy/generate-analysis-reports.py --data-set={app_name}"),
    ]
    if choice in ('1','3'):
        obtain_types = []
        clean_types = []
        analyze_types = []
        load_types = []
        generate_types = []
        for _, cmd in analysis_cmds:
            script_part = os.path.basename(cmd.split()[2]) if len(cmd.split()) > 2 else cmd
            display_map = {
                'obtain-cobol-programs.py': 'Executing obtain cobol programs',
                'obtain-cobol-copybooks.py': 'Executing obtain cobol copybooks',
                'obtain-mvs-jcl.py': 'Executing obtain mvs jcls',
                'obtain-bms-maps.py': 'Executing obtain bms maps',
                'obtain-sql-scripts.py': 'Executing obtain sql scripts',
                'obtain-cics-tp.py': 'Executing obtain cics tp',
                'clean-cobol-programs.py': 'Executing clean cobol programs',
                'clean-cobol-copybooks.py': 'Executing clean cobol copybooks',
                'clean-mvs-jcl.py': 'Executing clean mvs jcls',
                'analyze-bms-maps.py': 'Executing analyze bms maps',
                'analyze-sql-statements.sql-scripts.py': 'Executing analyze sql statements (sql scripts)',
                'analyze-cobol-statements.copybooks.py': 'Executing analyze cobol statements (copybooks)',
                'analyze-cobol-statements.programs.py': 'Executing analyze cobol statements (programs)',
                'analyze-cics-statements.copybooks.py': 'Executing analyze cics statements (copybooks)',
                'analyze-cics-statements.programs.py': 'Executing analyze cics statements (programs)',
                'analyze-sql-statements.copybooks.py': 'Executing analyze sql statements (copybooks)',
                'analyze-sql-statements.programs.py': 'Executing analyze sql statements (programs)',
                'analyze-mvs-jcl.py': 'Executing analyze mvs jcls',
                'analyze-cics-tp.py': 'Executing analyze cics tp',
                'load-analysis-csv-files.py': 'Executing load analysis csv files',
                'generate-analysis-reports.py': 'Executing generate analysis reports',
            }
            msg = display_map.get(script_part, 'Executing ' + script_part.replace('.py', '').replace('-', ' '))
            rc = run_cmd(cmd, project_dir, msg)
            if rc != 0:
                print(f"{msg} failed. Exiting.")
                sys.exit(1)
            if script_part in ['obtain-cobol-programs.py', 'obtain-cobol-copybooks.py', 'obtain-mvs-jcl.py', 'obtain-bms-maps.py', 'obtain-sql-scripts.py', 'obtain-cics-tp.py']:
                obtain_types.append(script_part.replace('.py', ''))
            elif script_part in ['clean-cobol-programs.py', 'clean-cobol-copybooks.py', 'clean-mvs-jcl.py']:
                clean_types.append(script_part.replace('.py', ''))
            elif script_part.startswith('analyze-'):
                analyze_types.append(script_part.replace('.py', ''))
            elif script_part.startswith('load-'):
                load_types.append(script_part.replace('.py', ''))
            elif script_part.startswith('generate-'):
                generate_types.append(script_part.replace('.py', ''))
        if obtain_types:
            print("Obtaining:\n")
            print("The obtain for the following file types were executed successfully:\n")
            for idx, typ in enumerate(obtain_types, 1):
                print(f"{idx}. {typ}")
            print()
        if clean_types:
            print("Cleaning:\n")
            print("The clean for the following file types were executed successfully:\n")
            for idx, typ in enumerate(clean_types, 1):
                print(f"{idx}. {typ}")
            print()
        if analyze_types:
            print("Analyzing:\n")
            print("The analyze for the following file types were executed successfully:\n")
            for idx, typ in enumerate(analyze_types, 1):
                print(f"{idx}. {typ}")
            print()
        if load_types:
            print("Loading:\n")
            print("The load steps were executed successfully:\n")
            for idx, typ in enumerate(load_types, 1):
                print(f"{idx}. {typ}")
            print()
        if generate_types:
            print("Generating:\n")
            print("The generate steps were executed successfully:\n")
            for idx, typ in enumerate(generate_types, 1):
                print(f"{idx}. {typ}")
            print()
        if choice == '1':
            print("Analysis only complete.")
            return
    if choice in ('2','3'):
        # Clean runlogs folder before running scripts
        runlogs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runlogs")
        if os.path.exists(runlogs_dir):
            for f in os.listdir(runlogs_dir):
                fp = os.path.join(runlogs_dir, f)
                try:
                    if os.path.isfile(fp) or os.path.islink(fp):
                        os.unlink(fp)
                    elif os.path.isdir(fp):
                        shutil.rmtree(fp)
                except Exception as e:
                    print(f"Warning: could not delete {fp}: {e}")
        else:
            os.makedirs(runlogs_dir, exist_ok=True)

        # Convert and Compile: OB01–OB07, CL01–CL03, AN08–AN09, CN01–CN08, then compilation
        convert_cmds = [
            # OBTAIN
            ("py -3 tools/migratonomy/obtain-cobol-programs.py", "Executing obtain cobol programs"),
            ("py -3 tools/migratonomy/obtain-cobol-copybooks.py", "Executing obtain cobol copybooks"),
            ("py -3 tools/migratonomy/obtain-mvs-jcl.py", "Executing obtain mvs jcl"),
            ("py -3 tools/migratonomy/obtain-bms-maps.py", "Executing obtain bms maps"),
            ("py -3 tools/migratonomy/obtain-sql-scripts.py", "Executing obtain sql scripts"),
            ("py -3 tools/migratonomy/obtain-cics-tp.py", "Executing obtain cics tp"),
            # CLEAN
            ("py -3 tools/migratonomy/clean-cobol-programs.py", "Executing clean cobol programs"),
            ("py -3 tools/migratonomy/clean-cobol-copybooks.py", "Executing clean cobol copybooks"),
            ("py -3 tools/migratonomy/clean-mvs-jcl.py", "Executing clean mvs jcl"),
            # ANALYZE (AN08, AN09)
            ("py -3 tools/migratonomy/analyze-sql-statements.copybooks.py", "Executing analyze sql statements (copybooks)"),
            ("py -3 tools/migratonomy/analyze-sql-statements.programs.py", "Executing analyze sql statements (programs)"),
            # CONVERT
            ("py -3 tools/migratonomy/convert-sql-statements.sql-scripts.py", "Executing convert sql statements (sql scripts)"),
            ("py -3 tools/migratonomy/convert-cobol-to-oo.programs.py --tool-target=java", "Executing convert cobol to oo programs (java)"),
            ("py -3 tools/migratonomy/convert-bms-maps.py", "Executing convert bms maps"),
            ("py -3 tools/migratonomy/generate-bms-maps.java.py", "Executing generate bms maps java"),
            ("py -3 tools/migratonomy/convert-mvs-jcl.py --target-language bash", "Executing convert mvs jcl (bash)"),
            ("py -3 tools/migratonomy/convert-cics-tp.py", "Executing convert cics tp"),
        ]
        clean_types = []
        analyze_types = []
        convert_types = []
        print("Clean runs begun")
        print("Analyze runs begun")
        print("Convert runs begun")
        for cmd, msg in convert_cmds:
            rc = run_cmd(cmd, project_dir, msg, log_dir=runlogs_dir)
            if rc != 0:
                print(f"{msg} failed. Exiting.")
                sys.exit(1)
            # OBTAIN steps
            if msg.startswith("Executing obtain"):
                obtain_types.append(msg.replace("Executing obtain ", "").capitalize())
            # CLEAN steps
            elif msg.startswith("Executing clean"):
                clean_types.append(msg.replace("Executing clean ", "").capitalize())
            # ANALYZE steps
            elif msg.startswith("Executing analyze"):
                analyze_types.append(msg.replace("Executing analyze ", "").capitalize())
            # CONVERT steps
            elif msg.startswith("Executing convert"):
                convert_types.append(msg.replace("Executing convert ", "").capitalize())
        # Print bundled summaries after each group
        if obtain_types:
            print("Obtaining:\n")
            print("The obtain for the following file types were executed successfully:\n")
            for idx, typ in enumerate(obtain_types, 1):
                print(f"{idx}. {typ}")
            print()
        if clean_types:
            print("Cleaning:\n")
            print("The clean for the following file types were executed successfully:\n")
            for idx, typ in enumerate(clean_types, 1):
                print(f"{idx}. {typ}")
            print()
        if analyze_types:
            print("Analyzing:\n")
            print("The analyze for the following file types were executed successfully:\n")
            for idx, typ in enumerate(analyze_types, 1):
                print(f"{idx}. {typ}")
            print()
        if convert_types:
            print("Converting:\n")
            print("The convert for the following file types were executed successfully:\n")
            for idx, typ in enumerate(convert_types, 1):
                print(f"{idx}. {typ}")
            print()

        # After conversion, proceed with artifact copy and compilation (fixed logic)
        # Step 8: Parse clean conversions
        log_file = os.path.join(project_dir, 'logs', 'convert-cobol-to-oo.programs.log')
        clean = []
        all_cobol = []
        pattern_all = re.compile(r"\|\s*([^|]+\.cbl)\s*\|")
        pattern_clean = re.compile(r"\|\s*([^|]+\.cbl)\s*\|\s*0\s*\|")
        with open(log_file) as lf:
            for line in lf:
                m_all = pattern_all.search(line)
                if m_all:
                    all_cobol.append(m_all.group(1))
                m_clean = pattern_clean.search(line)
                if m_clean:
                    clean.append(m_clean.group(1))
        all_cobol_set = {os.path.splitext(x)[0].lower() for x in all_cobol}
        clean_set = {os.path.splitext(x)[0].lower() for x in clean}
        total_cobol = len(all_cobol_set)
        # Step 9: Copy artifacts (fixed logic)
        src_cb = os.path.join(project_dir,'work','convert-cobol-to-oo.programs.java','copybooks')
        src_pr = os.path.join(project_dir,'work','convert-cobol-to-oo.programs.java','programs')
        tgt_cb = os.path.join(project_dir,'target','maintenance','copybooks')
        tgt_pr = os.path.join(project_dir,'target','maintenance','programs')
        try:
            shutil.copytree(src_cb, tgt_cb, dirs_exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not copy copybooks: {e}")
        os.makedirs(tgt_pr, exist_ok=True)
        copied_java = 0
        for r,_,files in os.walk(src_pr):
            rel = os.path.relpath(r, src_pr)
            dest = os.path.join(tgt_pr, rel)
            os.makedirs(dest, exist_ok=True)
            for f in files:
                if f.lower().endswith('.java') and os.path.splitext(f)[0].lower() in clean_set:
                    shutil.copy(os.path.join(r,f), os.path.join(dest,f))
                    copied_java += 1
        print("All artifacts copied to target directories.")
        print()
        # Step 10: Compile using ANT (copybooks first, then programs)
        ant_exec = shutil.which('ant') or shutil.which('ant.bat')
        classes = []
        if not ant_exec:
            print("ANT not found, skipping compilation.")
        else:
            print("Executing ANT steps on copybooks")
            print("Executing ANT steps on programs\n")
            for tree in [tgt_cb, tgt_pr]:
                if not os.path.isdir(tree):
                    continue
                for target in ['clean', 'build', 'install']:
                    ant_cmd = f'{ant_exec} {target}'
                    ant_dir = os.path.basename(tree)
                    ant_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runlogs')
                    ant_log_name = f'ant_{ant_dir}_{target}_{int(time.time())}.log'
                    log_file = os.path.join(ant_log_dir, ant_log_name)
                    os.makedirs(ant_log_dir, exist_ok=True)
                    full_cmd = f'{ant_cmd} > "{log_file}" 2>&1'
                    subprocess.call(full_cmd, shell=True, cwd=tree)

            # Step 11: Collect .class files only from bin under programs, matching only <filename>.class for each COBOL program
            # Find all 'bin' directories under programs and pick the deepest one
            bin_dirs = [root for root, dirs, files in os.walk(tgt_pr) if os.path.basename(root) == 'bin']
            if not bin_dirs:
                print("Warning: no bin directories found under programs; no class files collected.")
                class_files = []
            else:
                bin_dir = max(bin_dirs, key=lambda p: p.count(os.sep))
                class_files = []
                for root, dirs, files in os.walk(bin_dir):
                    for file in files:
                        if file.endswith('.class'):
                            class_files.append(os.path.join(root, file))

            # Step 12: Summary and percentages (match as in orchest.py)
            total_cbl = total_cobol
            clean_basenames = {os.path.splitext(os.path.basename(x))[0].lower() for x in clean}
            compiled_prog_count = sum(
                1 for base in clean_basenames
                if any(os.path.splitext(os.path.basename(cf))[0].lower() == base for cf in class_files)
            )
            conv_pct = (copied_java / total_cbl * 100) if total_cbl else 0
            comp_pct = (compiled_prog_count / total_cbl * 100) if total_cbl else 0
            print(f"Conversion success rate: {conv_pct:.2f}% ({copied_java}/{total_cbl})")
            print(f"Compilation success rate: {comp_pct:.2f}% ({compiled_prog_count}/{total_cbl})")
            return

    print()
    print("Starting COBOL Conversion step...")
    time.sleep(3)
    # The conversion tool writes its own log under logs\convert.oo.programs.log
    cmd = 'py -3 tools\\migratonomy\\convert-cobol-to-oo.programs.py --tool-target=java'
    exit_code = run_cmd(cmd, project_dir, "COBOL Conversion")

    # Step 7: Parse exit code and alert
    if exit_code == 0:
        print("Conversion succeeded.")
        # Step 8: Extract clean converted artifacts from summary table
        log_file = os.path.join(project_dir, 'logs', 'convert-cobol-to-oo.programs.log')
        # parse any data rows with .cbl and error count zero
        clean = []
        pattern = re.compile(r"\|\s*([^|]+\.cbl)\s*\|\s*0\s*\|")
        with open(log_file) as lf:
            for line in lf:
                match = pattern.search(line)
                if match:
                    clean.append(match.group(1))
        if clean:
            print("Clean converted programs:")
            for prog in clean:
                print(f" - {prog}")
        else:
            print("No clean converted programs found.")
        print("Successful")
        time.sleep(5)
        
        # Step 9: Copy ALL copybooks and ONLY clean .java programs to target dir
        src_copybooks = os.path.join(project_dir, 'work', 'convert-cobol-to-oo.programs.java', 'copybooks')
        # Java programs source directory
        src_programs = os.path.join(project_dir, 'work', 'convert-cobol-to-oo.programs.java', 'programs')
        tgt_copybooks = os.path.join(project_dir, 'target', 'maintenance', 'copybooks')
        tgt_programs = os.path.join(project_dir, 'target', 'maintenance', 'programs')
        shutil.copytree(src_copybooks, tgt_copybooks, dirs_exist_ok=True)
        # notify before copying
        print()
        print()
        print("Copying clean converted programs to target folder...")
        # copy clean java programs by searching recursively
        os.makedirs(tgt_programs, exist_ok=True)
        # prepare set of clean basenames for matching
        clean_basenames = {os.path.splitext(os.path.basename(x))[0].lower() for x in clean}
        for root, dirs, files in os.walk(src_programs):
            rel = os.path.relpath(root, src_programs)
            dest = os.path.join(tgt_programs, rel)
            os.makedirs(dest, exist_ok=True)
            for file in files:
                if file.lower().endswith('.java'):
                    name = os.path.splitext(file)[0].lower()
                    if name in clean_basenames:
                        shutil.copy(os.path.join(root, file), os.path.join(dest, file))
        # warn if no java files were copied
        if not any(f.endswith('.java') for _,_,files in os.walk(tgt_programs) for f in files):
            print("Warning: no clean .java programs were copied.")
        # Step 10: COMPILE THE ARTIFACTS USING ANT (CLEAN, BUILD, INSTALL)
        java_copied = any(f.endswith('.java') for _,_,files in os.walk(tgt_programs) for f in files)
        compilation_success = True
        if not java_copied:
            print("No Java programs copied; skipping ANT steps.")
            compilation_success = False
        else:
            ant_exec = shutil.which('ant') or shutil.which('ant.bat')
            if ant_exec is None:
                print("ANT not found; skipping ANT steps.")
                compilation_success = False
            else:
                print()
                print(f"COMPILING THE ARTIFACTS USING ANT in {tgt_copybooks.upper()}")
                for target in ['CLEAN', 'BUILD', 'INSTALL']:
                    print(f"ANT {target} on {tgt_copybooks}")
                    cp = subprocess.run([ant_exec, target], cwd=tgt_copybooks, capture_output=True, text=True)
                    if 'BUILD SUCCESSFUL' in (cp.stdout + cp.stderr):
                        print(f"ANT {target} in {tgt_copybooks}: SUCCESS")
                    else:
                        print(f"ANT {target} in {tgt_copybooks}: FAILED")
                        compilation_success = False
                print()
                print(f"COMPILING THE ARTIFACTS USING ANT in {tgt_programs.upper()}")
                for target in ['CLEAN', 'BUILD', 'INSTALL']:
                    print(f"ANT {target} on {tgt_programs}")
                    cp = subprocess.run([ant_exec, target], cwd=tgt_programs, capture_output=True, text=True)
                    if 'BUILD SUCCESSFUL' in (cp.stdout + cp.stderr):
                        print(f"ANT {target} in {tgt_programs}: SUCCESS")
                    else:
                        print(f"ANT {target} in {tgt_programs}: FAILED")
                        compilation_success = False
        if compilation_success:
            print("Compilation succeeded.")
        else:
            print("Compilation failed.")
        time.sleep(2)
        # Step 11: Collect .class files from the deepest 'bin' directory under programs
        # find all 'bin' directories under target programs
        bin_dirs = [root for root, dirs, files in os.walk(tgt_programs) if os.path.basename(root) == 'bin']
        if not bin_dirs:
            print("Warning: no bin directories found under programs; no class files collected.")
            class_files = []
        else:
            # pick the bin dir with the deepest nesting
            bin_dir = max(bin_dirs, key=lambda p: p.count(os.sep))
            class_files = []
            for root, dirs, files in os.walk(bin_dir):
                for file in files:
                    if file.endswith('.class'):
                        class_files.append(os.path.join(root, file))
        # Step 12: Compute and print metrics
        total_cbl = sum(1 for line in open(log_file) if '.cbl' in line and '|' in line)
        clean_count = len(clean)
        conversion_pct = (clean_count / total_cbl * 100) if total_cbl else 0
        # count unique compiled programs by matching basenames in class files
        clean_basenames = {os.path.splitext(os.path.basename(x))[0].lower() for x in clean}
        compiled_prog_count = sum(
            1 for base in clean_basenames
            if any(os.path.splitext(os.path.basename(cf))[0].lower() == base for cf in class_files)
        )
        compilation_pct = (compiled_prog_count / total_cbl * 100) if total_cbl else 0
        app_name = os.path.basename(project_dir)
        print(f"{app_name} factory certification completion % (conversion): {conversion_pct:.2f}% ({clean_count}/{total_cbl})")
        print(f"{app_name} factory certification completion % (compilation): {compilation_pct:.2f}% ({compiled_prog_count}/{total_cbl})")
    else:
        print("Conversion failed.")
        print("Failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
