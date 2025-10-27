# Baseline Pipeline Orchestrator Prompt

## System Role
You are implementing a **Traditional Pipeline Orchestrator** based on the original `orchest.py` - a deterministic script that manages COBOL-to-Java migration pipelines through sequential command execution.

## Detailed Program Walkthrough

### **Step 1: User Interaction and Setup**
```python
def main():
    # 1.1 Prompt for project directory
    project_dir = input("Enter factory project folder path: ").strip()
    validate_directory_exists(project_dir)
    
    # 1.2 Discover and display available snapshots
    deliveries_path = os.path.join(project_dir, 'deliveries')
    snapshots = list_subdirectories(deliveries_path)
    display_numbered_list(snapshots)
    
    # 1.3 Get user snapshot selection
    snap_choice = input("Select snapshot by number (or press Enter for default): ")
    snapshot = resolve_snapshot_choice(snap_choice, snapshots, default='snapshot-1')
    
    # 1.4 Get application name
    app_name = input("Enter app-name to use: ").strip()
    
    # 1.5 Confirm target languages
    confirm = input("Confirm target languages are JAVA and bash (Y/n): ")
    
    # 1.6 Display snapshot contents with file counts
    display_snapshot_contents(project_dir, snapshot)
```

### **Step 2: Execution Mode Selection**
```python
    # 2.1 Present execution options
    print("Choose from the below options:\n")
    print(" 1. Analysis only")
    print(" 2. Convert and Compile") 
    print(" 3. Analysis, Convert and Compile")
    print(" 4. Exit\n")
    
    # 2.2 Get user choice
    choice = input("Choose mode: ").strip()
    mode_name = get_mode_name(choice)
    print(f"\nMode selected: {mode_name}\n")
```

### **Step 3: Environment Configuration**
```python
    # 3.1 Set required environment variables
    os.environ['DELIVERY_DIR'] = f"deliveries/{snapshot}"
    os.environ['SNAPSHOT_NAME'] = snapshot
    os.environ['TARGET_LANGUAGE'] = 'JAVA'
    os.environ['TARGET_SCRIPT_LANGUAGE'] = 'bash'
    
    # 3.2 Create necessary directories
    ensure_directory_exists('runlogs')
    ensure_directory_exists('work/transformed')
    ensure_directory_exists('target/artifacts')
```

### **Step 4: Command Execution Engine**
```python
def run_cmd(cmd, cwd, desc, log_dir=None):
    # 4.1 Setup logging infrastructure
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(__file__), "runlogs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 4.2 Generate unique timestamped log file
    script_name = extract_script_name(cmd)
    timestamp = int(time.time())
    log_file = os.path.join(log_dir, f"{script_name}_{timestamp}.log")
    
    # 4.3 Execute command with output redirection
    full_cmd = f"{cmd} > \"{log_file}\" 2>&1"
    print(f"🔧 Executing: {desc}")
    exit_code = subprocess.call(full_cmd, shell=True, cwd=cwd)
    
    # 4.4 CRITICAL: Binary failure handling
    if exit_code != 0:
        print(f"{desc} failed. Exiting.")
        sys.exit(1)  # ❌ IMMEDIATE TERMINATION - NO RECOVERY
    
    return exit_code
```

### **Step 5: Pipeline Phase Execution**

#### **Analysis Phase (Mode 1 & 3)**
```python
def execute_analysis_phase(project_dir):
    print("\n" + "="*60)
    print("PHASE 1: ANALYSIS")
    print("="*60 + "\n")
    
    analysis_commands = [
        ("py -3 tools/migratonomy/obtain-cobol-programs.py", "Obtaining COBOL programs"),
        ("py -3 tools/migratonomy/obtain-cobol-copybooks.py", "Obtaining COBOL copybooks"),
        ("py -3 tools/migratonomy/obtain-mvs-jcl.py", "Obtaining MVS JCL"),
        ("py -3 tools/migratonomy/obtain-bms-maps.py", "Obtaining BMS maps"),
        ("py -3 tools/migratonomy/analyze-dependencies.py", "Analyzing dependencies"),
        ("py -3 tools/migratonomy/generate-analysis-report.py", "Generating analysis report")
    ]
    
    for cmd, desc in analysis_commands:
        run_cmd(cmd, project_dir, desc)  # Fails immediately on any error
        print(f"✅ {desc} completed")
```

#### **Conversion Phase (Mode 2 & 3)**
```python
def execute_conversion_phase(project_dir, app_name):
    print("\n" + "="*60)
    print("PHASE 2: CONVERSION")
    print("="*60 + "\n")
    
    conversion_commands = [
        (f"py -3 tools/conversion/convert-cobol-to-java.py {app_name}", "Converting COBOL to Java"),
        (f"py -3 tools/conversion/convert-jcl-to-bash.py {app_name}", "Converting JCL to Bash"),
        (f"py -3 tools/conversion/convert-bms-to-jsp.py {app_name}", "Converting BMS to JSP"),
        ("py -3 tools/conversion/generate-build-files.py", "Generating build files")
    ]
    
    for cmd, desc in conversion_commands:
        run_cmd(cmd, project_dir, desc)  # Fails immediately on any error
        print(f"✅ {desc} completed")
```

#### **Compilation Phase (Mode 2 & 3)**
```python
def execute_compilation_phase(project_dir):
    print("\n" + "="*60)
    print("PHASE 3: COMPILATION")
    print("="*60 + "\n")
    
    # 5.1 Parse transformation logs for successful artifacts
    successful_artifacts = parse_transformation_logs()
    
    # 5.2 Copy only zero-error artifacts to target directory
    copy_successful_artifacts(successful_artifacts)
    
    # 5.3 Execute compilation commands
    compile_commands = [
        ("javac -cp . *.java", "Compiling Java files"),
        ("ant build", "Building with ANT"),
        ("jar cf application.jar *.class", "Creating JAR file")
    ]
    
    for cmd, desc in compile_commands:
        run_cmd(cmd, "target/artifacts", desc)  # Fails immediately on any error
        print(f"✅ {desc} completed")
```

### **Step 6: Artifact Quality Control**
```python
def parse_transformation_logs():
    # 6.1 Read transformation log file
    log_file = "logs/transformation.log"
    
    # 6.2 Parse for zero-error artifacts using regex
    pattern = re.compile(r"\|\s*([^|]+\.\w+)\s*\|\s*0\s*\|")
    successful_artifacts = []
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                artifact_name = match.group(1).strip()
                successful_artifacts.append(artifact_name)
    
    return successful_artifacts

def copy_successful_artifacts(artifacts):
    # 6.3 Copy only validated artifacts to target directory
    source_dir = "work/transformed"
    target_dir = "target/artifacts"
    
    for artifact in artifacts:
        source_path = os.path.join(source_dir, artifact)
        target_path = os.path.join(target_dir, artifact)
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
```

### **Step 7: Metrics and Reporting**
```python
def generate_execution_summary():
    # 7.1 Calculate transformation success rate
    total_artifacts = count_total_artifacts()
    successful_transformations = count_successful_transformations()
    transformation_rate = (successful_transformations / total_artifacts) * 100
    
    # 7.2 Calculate build success rate  
    built_artifacts = count_built_artifacts()
    build_rate = (built_artifacts / successful_transformations) * 100
    
    # 7.3 Display summary report
    print("\n" + "="*60)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*60)
    print(f"Total Artifacts Processed:    {total_artifacts}")
    print(f"Successful Transformations:   {successful_transformations}")
    print(f"Artifacts Built:              {built_artifacts}")
    print(f"Transformation Success Rate:  {transformation_rate:.2f}%")
    print(f"Build Success Rate:           {build_rate:.2f}%")
    print("="*60)
```

### **Step 8: Error Handling and Termination**
```python
def handle_failure(command, exit_code, description):
    # 8.1 Log the failure details
    print(f"❌ FAILURE: {description}")
    print(f"   Command: {command}")
    print(f"   Exit Code: {exit_code}")
    print(f"   Check log files in runlogs/ for details")
    
    # 8.2 CRITICAL LIMITATION: Immediate termination
    print(f"\n🛑 Pipeline execution terminated due to failure.")
    print(f"   Manual investigation required.")
    print(f"   No automatic recovery attempted.")
    
    # 8.3 Hard exit - no recovery, no analysis, no alternatives
    sys.exit(1)
```

## **Key Program Characteristics**

### **1. Sequential Execution Model**
- Each command must complete successfully before the next begins
- No parallel execution or asynchronous operations
- Strict dependency chain: Analysis → Conversion → Compilation

### **2. Binary Success/Failure Logic**
```python
# The core limitation - no intelligence
if subprocess_exit_code != 0:
    sys.exit(1)  # Game over - no questions asked
```

### **3. User-Driven Configuration**
- Manual input for all configuration parameters
- No automatic discovery or intelligent defaults
- Human decision-making for all execution modes

### **4. Basic Logging Infrastructure**
- Timestamped log files for audit trails
- Stdout/stderr redirection for debugging
- No log analysis or pattern recognition

### **5. Artifact Quality Control**
- Regex parsing of transformation logs
- Selective copying of zero-error artifacts
- Basic success rate calculations

## **Critical Limitations Demonstrated**

### **No Failure Analysis**
```python
# What the program CANNOT do:
def analyze_why_command_failed(exit_code, log_content):
    pass  # Not implemented - no intelligence

def determine_if_retryable(error_type):
    pass  # Not implemented - no decision-making

def suggest_recovery_actions(failure_context):
    pass  # Not implemented - no adaptive behavior
```

### **No Recovery Mechanisms**
- Cannot retry failed operations
- Cannot adapt parameters based on failure types
- Cannot find alternative execution paths
- Cannot escalate intelligently to human operators

### **No Learning Capabilities**
- Cannot remember previous execution patterns
- Cannot improve performance over time
- Cannot predict potential issues
- Cannot optimize based on historical data

## **Typical Execution Flow**
```
1. User starts program
2. User provides: project_dir, snapshot, app_name, execution_mode
3. Program sets environment variables
4. Program executes commands sequentially:
   - IF mode includes analysis: run analysis commands
   - IF mode includes conversion: run conversion commands  
   - IF mode includes compilation: run compilation commands
5. Program generates summary report
6. Program exits successfully OR fails immediately on first error
```

## **When This Program Fails**
```
❌ COBOL conversion fails with syntax error
❌ Java compilation fails due to missing dependency
❌ Network timeout during file transfer
❌ Disk space exhaustion during build
❌ Permission denied on target directory
❌ Missing configuration file

RESULT: Immediate termination, manual debugging required
```

## **Implementation Requirements**

### **Core Functions to Implement**
1. `main()` - User interaction and orchestration
2. `run_cmd()` - Command execution with logging
3. `execute_analysis_phase()` - Analysis command sequence
4. `execute_conversion_phase()` - Conversion command sequence  
5. `execute_compilation_phase()` - Compilation command sequence
6. `parse_transformation_logs()` - Artifact quality parsing
7. `generate_execution_summary()` - Metrics calculation

### **Key Data Structures**
```python
# Command definitions
analysis_commands = [
    ("py -3 tools/migratonomy/obtain-cobol-programs.py", "Obtaining COBOL programs"),
    # ... more commands
]

conversion_commands = [
    ("py -3 tools/conversion/convert-cobol-to-java.py {app_name}", "Converting COBOL to Java"),
    # ... more commands
]

# Environment variables
required_env_vars = {
    'DELIVERY_DIR': f"deliveries/{snapshot}",
    'SNAPSHOT_NAME': snapshot,
    'TARGET_LANGUAGE': 'JAVA',
    'TARGET_SCRIPT_LANGUAGE': 'bash'
}
```

### **Success Criteria**
- ✅ Executes all commands in correct sequence when no failures occur
- ✅ Provides clear user interface for mode selection
- ✅ Generates comprehensive logs for debugging
- ✅ Calculates accurate success rate metrics
- ✅ Terminates immediately on any command failure
- ✅ Demonstrates the limitations of non-agentic approaches
