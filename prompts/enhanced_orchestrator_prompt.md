# Enhanced Pipeline Orchestrator Prompt

## System Role
You are implementing an **Enhanced Pipeline Orchestrator** that builds upon the baseline orchestrator by adding algorithmic agent intelligence and recovery mechanisms. This system demonstrates the first step toward agentic behavior through rule-based decision-making and adaptive responses.

## Detailed Program Walkthrough

### **Step 1: Enhanced Initialization with Agent Setup**
```python
class EnhancedPipelineOrchestrator:
    def __init__(self, project_dir):
        # 1.1 Initialize baseline orchestrator capabilities
        self.project_dir = project_dir
        self.logger = self._setup_logging()
        
        # 1.2 NEW: Initialize agentic components
        self.issue_resolver = IssueResolutionAgent()
        self.execution_history = []
        self.context = ExecutionContext()
        
        # 1.3 NEW: Agent intervention tracking
        self.agent_interventions = 0
        self.successful_recoveries = 0
        self.escalated_issues = 0
        
        self.logger.info("🤖 Enhanced Orchestrator initialized with agent capabilities")
```

### **Step 2: Intelligent Command Execution with Agent Monitoring**
```python
def run_cmd_with_agent(self, cmd, cwd, desc, log_dir=None):
    # 2.1 Setup logging (same as baseline)
    log_file = self._setup_command_logging(cmd, log_dir)
    
    # 2.2 Execute command with monitoring
    attempt_count = 0
    max_attempts = 3
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        # 2.3 Execute the command
        print(f"🔧 Executing: {desc} (attempt {attempt_count})")
        full_cmd = f"{cmd} > \"{log_file}\" 2>&1"
        exit_code = subprocess.call(full_cmd, shell=True, cwd=cwd)
        
        # 2.4 SUCCESS PATH: Command completed successfully
        if exit_code == 0:
            print(f"✅ {desc} completed successfully")
            self._record_success(cmd, desc, attempt_count)
            return exit_code
        
        # 2.5 🤖 AGENT INTERVENTION POINT: Failure detected
        print(f"⚠️ Command failed with exit code {exit_code}")
        self.agent_interventions += 1
        
        # 2.6 🤖 AGENT ANALYSIS: Classify and analyze the failure
        issue_analysis = self.issue_resolver.analyze_failure(
            cmd, exit_code, log_file, self.context
        )
        
        # 2.7 🤖 AGENT DECISION: Determine recovery strategy
        decision = self.issue_resolver.decide_retry_strategy(
            cmd, attempt_count, issue_analysis, self.context
        )
        
        # 2.8 🤖 AGENT ACTION: Execute recovery strategy
        recovery_result = self._execute_agent_decision(
            decision, cmd, cwd, desc, issue_analysis, attempt_count
        )
        
        if recovery_result == "success":
            self.successful_recoveries += 1
            return 0
        elif recovery_result == "retry":
            continue  # Try again with next attempt
        elif recovery_result == "escalate":
            self.escalated_issues += 1
            return self._escalate_to_human(issue_analysis, cmd, desc)
    
    # 2.9 All attempts exhausted
    print(f"❌ All {max_attempts} attempts failed for: {desc}")
    return self._escalate_to_human(issue_analysis, cmd, desc)
```

### **Step 3: Issue Analysis Agent**
```python
class IssueResolutionAgent:
    def analyze_failure(self, cmd, exit_code, log_file, context):
        # 3.1 Classify issue type based on exit code patterns
        issue_type = self._classify_issue_type(exit_code, cmd)
        
        # 3.2 Analyze log content for additional context
        log_analysis = self._analyze_log_content(log_file)
        
        # 3.3 Check execution history for patterns
        historical_context = self._check_execution_history(cmd, context)
        
        # 3.4 Assess severity and recoverability
        severity = self._assess_severity(issue_type, log_analysis, historical_context)
        
        return IssueAnalysis(
            issue_type=issue_type,
            severity=severity,
            log_analysis=log_analysis,
            historical_context=historical_context,
            timestamp=time.time()
        )
    
    def _classify_issue_type(self, exit_code, cmd):
        # 3.5 Rule-based issue classification
        if exit_code == 124:  # Timeout
            return IssueType.TIMEOUT
        elif exit_code == 137:  # Memory/Resource exhaustion
            return IssueType.RESOURCE_EXHAUSTION
        elif exit_code in [1, 2]:  # General errors
            if "network" in cmd.lower() or "download" in cmd.lower():
                return IssueType.NETWORK_ERROR
            elif "java" in cmd.lower() or "compile" in cmd.lower():
                return IssueType.COMPILATION_ERROR
            else:
                return IssueType.GENERAL_ERROR
        elif exit_code == 126:  # Permission denied
            return IssueType.PERMISSION_ERROR
        else:
            return IssueType.UNKNOWN_ERROR
    
    def _analyze_log_content(self, log_file):
        # 3.6 Parse log file for error patterns
        error_patterns = {
            'timeout': ['timeout', 'timed out', 'connection timeout'],
            'memory': ['out of memory', 'heap space', 'memory exhausted'],
            'network': ['connection refused', 'network unreachable', 'dns'],
            'permission': ['permission denied', 'access denied', 'unauthorized'],
            'missing_file': ['file not found', 'no such file', 'missing'],
            'syntax_error': ['syntax error', 'parse error', 'invalid syntax']
        }
        
        detected_patterns = []
        try:
            with open(log_file, 'r') as f:
                log_content = f.read().lower()
                for pattern_type, patterns in error_patterns.items():
                    if any(pattern in log_content for pattern in patterns):
                        detected_patterns.append(pattern_type)
        except Exception:
            pass
        
        return detected_patterns
```

### **Step 4: Agent Decision-Making Framework**
```python
    def decide_retry_strategy(self, cmd, attempt_count, issue_analysis, context):
        # 4.1 Quick exit for critical issues
        if issue_analysis.severity == "critical":
            return AgentDecision.ESCALATE
        
        # 4.2 Timeout handling - usually retryable
        if issue_analysis.issue_type == IssueType.TIMEOUT:
            if attempt_count < 3:
                return AgentDecision.RETRY_WITH_BACKOFF
            else:
                return AgentDecision.ADAPT_PARAMETERS
        
        # 4.3 Resource exhaustion - try parameter adaptation
        if issue_analysis.issue_type == IssueType.RESOURCE_EXHAUSTION:
            if self._can_adapt_resources(context):
                return AgentDecision.ADAPT_PARAMETERS
            else:
                return AgentDecision.ESCALATE
        
        # 4.4 Network errors - retry with exponential backoff
        if issue_analysis.issue_type == IssueType.NETWORK_ERROR:
            if attempt_count < 3:
                return AgentDecision.RETRY_WITH_BACKOFF
            else:
                return AgentDecision.ALTERNATIVE_PATH
        
        # 4.5 Permission errors - try alternative approach
        if issue_analysis.issue_type == IssueType.PERMISSION_ERROR:
            return AgentDecision.ALTERNATIVE_PATH
        
        # 4.6 Compilation errors - analyze and adapt
        if issue_analysis.issue_type == IssueType.COMPILATION_ERROR:
            return AgentDecision.ADAPT_PARAMETERS
        
        # 4.7 Default: retry once, then escalate
        if attempt_count == 1:
            return AgentDecision.RETRY_WITH_BACKOFF
        else:
            return AgentDecision.ESCALATE
```

### **Step 5: Recovery Strategy Execution**
```python
def _execute_agent_decision(self, decision, cmd, cwd, desc, issue_analysis, attempt_count):
    # 5.1 RETRY WITH EXPONENTIAL BACKOFF
    if decision == AgentDecision.RETRY_WITH_BACKOFF:
        delay = min(2 ** attempt_count, 30)  # Cap at 30 seconds
        print(f"🤖 Agent decision: Retry with {delay}s backoff")
        time.sleep(delay)
        return "retry"
    
    # 5.2 ADAPT PARAMETERS
    elif decision == AgentDecision.ADAPT_PARAMETERS:
        print(f"🤖 Agent decision: Adapt parameters and retry")
        adaptations = self._generate_parameter_adaptations(issue_analysis)
        self._apply_adaptations(adaptations)
        return "retry"
    
    # 5.3 ALTERNATIVE PATH
    elif decision == AgentDecision.ALTERNATIVE_PATH:
        print(f"🤖 Agent decision: Try alternative approach")
        alternative_cmd = self._find_alternative_command(cmd, issue_analysis)
        if alternative_cmd:
            print(f"🔄 Trying alternative: {alternative_cmd}")
            # Execute alternative command
            result = self.run_cmd_with_agent(alternative_cmd, cwd, f"Alternative: {desc}")
            return "success" if result == 0 else "escalate"
        else:
            return "escalate"
    
    # 5.4 ESCALATE TO HUMAN
    elif decision == AgentDecision.ESCALATE:
        print(f"🤖 Agent decision: Escalate to human operator")
        return "escalate"
    
    return "escalate"

def _generate_parameter_adaptations(self, issue_analysis):
    # 5.5 Generate specific parameter changes based on issue type
    adaptations = {}
    
    if issue_analysis.issue_type == IssueType.TIMEOUT:
        adaptations['timeout'] = '600'  # Increase timeout to 10 minutes
        adaptations['retry_delay'] = '5'
    
    elif issue_analysis.issue_type == IssueType.RESOURCE_EXHAUSTION:
        adaptations['memory_limit'] = '4G'  # Increase memory
        adaptations['max_heap'] = '3G'
    
    elif issue_analysis.issue_type == IssueType.NETWORK_ERROR:
        adaptations['connection_timeout'] = '120'
        adaptations['read_timeout'] = '300'
    
    return adaptations

def _apply_adaptations(self, adaptations):
    # 5.6 Apply parameter adaptations to environment
    for param, value in adaptations.items():
        os.environ[param.upper()] = value
        print(f"   📝 Set {param} = {value}")
```

### **Step 6: Enhanced Pipeline Execution**
```python
def execute_pipeline_with_agents(self, context, phases=None):
    # 6.1 Initialize execution context
    if phases is None:
        phases = [PipelinePhase.EXTRACT, PipelinePhase.VALIDATE, 
                 PipelinePhase.ANALYZE, PipelinePhase.TRANSFORM, PipelinePhase.BUILD]
    
    self.context = context
    overall_success = True
    
    print(f"🚀 Starting enhanced pipeline execution with agent monitoring")
    
    # 6.2 Execute each phase with agent intervention
    for phase in phases:
        print(f"\n{'='*60}")
        print(f"PHASE: {phase.value.upper()}")
        print(f"{'='*60}")
        
        # 6.3 Execute phase with agentic monitoring
        result = self._execute_phase_with_agent(phase, context)
        self.execution_history.append(result)
        
        # 6.4 Check phase success
        if not result.success:
            print(f"⚠️ Phase {phase.value} completed with issues")
            overall_success = False
            
            # 6.5 🤖 AGENT DECISION: Continue or abort pipeline
            continue_decision = self._should_continue_pipeline(result, phase)
            if not continue_decision:
                print(f"🛑 Agent decided to abort pipeline execution")
                break
        else:
            print(f"✅ Phase {phase.value} completed successfully")
    
    # 6.6 Generate enhanced execution report
    self._generate_agent_execution_report()
    
    return overall_success
```

### **Step 7: Agent Execution Reporting**
```python
def _generate_agent_execution_report(self):
    # 7.1 Calculate agent intervention metrics
    total_commands = len([h for h in self.execution_history if h.commands_executed > 0])
    intervention_rate = (self.agent_interventions / total_commands) * 100 if total_commands > 0 else 0
    recovery_rate = (self.successful_recoveries / self.agent_interventions) * 100 if self.agent_interventions > 0 else 0
    
    # 7.2 Display enhanced execution summary
    print(f"\n{'='*60}")
    print("ENHANCED ORCHESTRATOR EXECUTION REPORT")
    print(f"{'='*60}")
    print(f"Total Commands Executed:      {total_commands}")
    print(f"Agent Interventions:          {self.agent_interventions}")
    print(f"Successful Recoveries:        {self.successful_recoveries}")
    print(f"Escalated Issues:             {self.escalated_issues}")
    print(f"Intervention Rate:            {intervention_rate:.1f}%")
    print(f"Recovery Success Rate:        {recovery_rate:.1f}%")
    print(f"{'='*60}")
    
    # 7.3 Display agent decision breakdown
    if self.agent_interventions > 0:
        print(f"\n🤖 AGENT PERFORMANCE SUMMARY:")
        print(f"   • Autonomous Recovery: {self.successful_recoveries} issues resolved")
        print(f"   • Human Escalation: {self.escalated_issues} issues required manual intervention")
        print(f"   • Overall Effectiveness: {recovery_rate:.1f}% autonomous resolution rate")
```

### **Step 8: Key Data Structures and Enums**
```python
class IssueType(Enum):
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    NETWORK_ERROR = "network_error"
    COMPILATION_ERROR = "compilation_error"
    PERMISSION_ERROR = "permission_error"
    GENERAL_ERROR = "general_error"
    UNKNOWN_ERROR = "unknown_error"

class AgentDecision(Enum):
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    ADAPT_PARAMETERS = "adapt_parameters"
    ALTERNATIVE_PATH = "alternative_path"
    ESCALATE = "escalate"

@dataclass
class IssueAnalysis:
    issue_type: IssueType
    severity: str  # "low", "medium", "high", "critical"
    log_analysis: List[str]
    historical_context: Dict
    timestamp: float
    
@dataclass
class ExecutionContext:
    project_dir: str
    snapshot: str
    app_name: str
    environment_vars: Dict[str, str]
    execution_history: List[Dict]
```

## **Key Program Characteristics**

### **1. Algorithmic Intelligence**
- Rule-based decision making using exit codes and log patterns
- No LLM integration - pure algorithmic analysis
- Deterministic responses based on predefined logic
- Fast decision-making with minimal latency

### **2. Agent Intervention Points**
```python
# Critical intervention moments in the program:
1. Command failure detection (exit_code != 0)
2. Issue classification and analysis
3. Recovery strategy selection
4. Parameter adaptation
5. Alternative path exploration
6. Human escalation decision
```

### **3. Recovery Mechanisms**
- **Exponential Backoff Retry**: For transient issues like network timeouts
- **Parameter Adaptation**: Increase memory, timeouts, or other resource limits
- **Alternative Commands**: Try different tools or approaches for same goal
- **Intelligent Escalation**: Provide rich context when human intervention needed

### **4. Context Awareness**
- Track execution history and patterns
- Consider environmental factors and resource availability
- Maintain success/failure statistics per operation type
- Learn from previous recovery attempts (basic pattern recognition)

## **Typical Enhanced Execution Flow**
```
1. User starts enhanced orchestrator
2. System initializes with agent capabilities
3. User provides configuration (same as baseline)
4. For each pipeline phase:
   a. Execute commands with agent monitoring
   b. On failure: Agent analyzes issue and selects strategy
   c. Agent attempts recovery (retry/adapt/alternative)
   d. If recovery fails: Escalate with rich context
   e. Track intervention metrics
5. Generate enhanced execution report with agent statistics
```

## **Agent Decision Examples**

### **Scenario 1: Network Timeout (Exit Code 124)**
```
🔧 Executing: Download COBOL programs (attempt 1)
⚠️ Command failed with exit code 124
🤖 Agent Analysis: TIMEOUT detected, network operation
🤖 Agent Decision: Retry with 2s backoff
🔧 Executing: Download COBOL programs (attempt 2)
✅ Download COBOL programs completed successfully
📊 Agent Recovery: SUCCESS
```

### **Scenario 2: Memory Exhaustion (Exit Code 137)**
```
🔧 Executing: Compile Java files (attempt 1)
⚠️ Command failed with exit code 137
🤖 Agent Analysis: RESOURCE_EXHAUSTION detected
🤖 Agent Decision: Adapt parameters and retry
   📝 Set memory_limit = 4G
   📝 Set max_heap = 3G
🔧 Executing: Compile Java files (attempt 2)
✅ Compile Java files completed successfully
📊 Agent Recovery: SUCCESS
```

### **Scenario 3: Permission Error (Exit Code 126)**
```
🔧 Executing: Copy artifacts to target (attempt 1)
⚠️ Command failed with exit code 126
🤖 Agent Analysis: PERMISSION_ERROR detected
🤖 Agent Decision: Try alternative approach
🔄 Trying alternative: sudo cp artifacts/* target/
✅ Alternative: Copy artifacts to target completed successfully
📊 Agent Recovery: SUCCESS
```

### **Scenario 4: Complex Compilation Error**
```
🔧 Executing: Compile converted COBOL (attempt 1)
⚠️ Command failed with exit code 1
🤖 Agent Analysis: COMPILATION_ERROR detected, syntax issues in log
🤖 Agent Decision: Adapt parameters and retry
   📝 Set compiler_flags = -Xlint:none
🔧 Executing: Compile converted COBOL (attempt 2)
⚠️ Command failed with exit code 1
🤖 Agent Decision: Escalate to human operator
🎫 Creating escalation ticket with compilation error details
📊 Agent Recovery: ESCALATED
```

## **Implementation Requirements**

### **Core Classes to Implement**
1. `EnhancedPipelineOrchestrator` - Main orchestrator with agent capabilities
2. `IssueResolutionAgent` - Algorithmic intelligence for failure analysis
3. `ExecutionContext` - Rich context tracking throughout execution
4. `IssueAnalysis` - Structured failure analysis results
5. `AgentDecision` - Enumerated recovery strategies

### **Key Methods to Implement**
```python
# Core orchestration
def run_cmd_with_agent(cmd, cwd, desc, log_dir=None)
def execute_pipeline_with_agents(context, phases=None)

# Agent intelligence
def analyze_failure(cmd, exit_code, log_file, context)
def decide_retry_strategy(cmd, attempt_count, issue_analysis, context)
def _execute_agent_decision(decision, cmd, cwd, desc, issue_analysis, attempt_count)

# Recovery mechanisms
def _generate_parameter_adaptations(issue_analysis)
def _find_alternative_command(cmd, issue_analysis)
def _escalate_to_human(issue_analysis, cmd, desc)

# Reporting and metrics
def _generate_agent_execution_report()
def _calculate_intervention_metrics()
```

### **Success Criteria**
- ✅ 60-80% reduction in manual intervention compared to baseline
- ✅ Intelligent recovery from common failure patterns (timeouts, resource issues)
- ✅ Comprehensive agent decision audit trails
- ✅ Adaptive parameter adjustment based on issue types
- ✅ Graceful escalation with rich context when recovery fails
- ✅ Maintains backward compatibility with baseline orchestrator
- ✅ Demonstrates clear progression toward full agentic capabilities
