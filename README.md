# 🤖 Agentic Pipeline Orchestrator Framework

**Portfolio Showcase: Advanced AI Systems Architecture**

This repository demonstrates expertise in designing and implementing **intelligent, autonomous systems** for enterprise pipeline orchestration. It showcases the transformation of conceptual PDF diagrams into production-ready, agentic AI frameworks that can operate autonomously in complex enterprise environments.

## 📋 **PDF Diagram Implementation**

This codebase directly implements the concepts shown in our PDF diagrams:

- **[Agentic Flow.pdf](docs/diagrams/Agentic%20Flow.pdf)** - Core agentic decision-making workflow
- **[Agentic Proposal.pdf](docs/diagrams/Agentic%20Proposal%20.pdf)** - Enterprise architecture and benefits

The framework transforms these conceptual diagrams into **production-ready code** that enterprises can deploy immediately.

## 🎯 **What Makes This Special**

This framework takes the existing `orchest.py` baseline and **fills the gaps** with intelligent agents. The key insight:

**✅ Keep what works** - All existing orchest.py functionality is preserved
**🤖 Add intelligence where missing** - Agents intervene only where the PDF diagrams show gaps

### **Gap-Filling Approach:**
- 🧠 **Failure Analysis** - Agents understand WHY commands fail (not just that they failed)
- 🔄 **Intelligent Retry** - Exponential backoff and parameter adaptation (not just hard exits)
- 🛠️ **Alternative Paths** - Agents find workarounds when primary paths fail
- 📈 **Learning** - Pattern recognition improves decision-making over time
- 🚨 **Smart Escalation** - Context-rich alerts to humans when needed

## 🏗️ **Framework Architecture**

### **PDF Diagram → Code Implementation**

Our framework directly implements the agentic flow concepts from the PDF diagrams:

```python
# From src/framework/agentic_orchestrator.py

class AgenticAgent(ABC):
    """Implements the intelligent decision-making shown in PDF diagrams"""
    
    @abstractmethod
    def analyze_situation(self, context: PipelineContext, issue: Issue) -> AgentDecision:
        """Maps to the decision diamond in PDF flow diagram"""
        pass
    
    @abstractmethod  
    def execute_decision(self, decision: AgentDecision, context: PipelineContext, issue: Issue) -> bool:
        """Executes the chosen path from PDF decision tree"""
        pass
```

### **Agentic Decision Flow (From PDF)**

```
Issue Detected → Agent Analysis → Decision Selection → Action Execution → Outcome Evaluation
     ↓               ↓                ↓                    ↓                  ↓
   Issue()    analyze_situation()  AgentDecision    execute_decision()   PhaseResult
```

### **Core Design Principles**

1. **🤖 Agentic Intelligence**: Autonomous agents make decisions based on issue analysis
2. **📊 Context-Aware Processing**: Every decision considers full pipeline context  
3. **🔄 Self-Correcting Loops**: Failed actions trigger re-analysis and alternative strategies
4. **📈 Learning Patterns**: Agents improve decision-making based on historical outcomes
5. **🚨 Intelligent Escalation**: Critical issues are escalated with full context

## 📁 **Key Files and Their Purpose**

### **Core Framework:**
- **`src/framework/baseline_orchestrator.py`** - Original orchest.py (unchanged baseline)
- **`src/framework/enhanced_orchestrator.py`** - Baseline + agent integration points
- **`src/framework/agentic_orchestrator.py`** - Full agentic framework implementation

### **Documentation:**
- **`PDF_TO_CODE_MAPPING.md`** - Maps PDF diagram components to code
- **`GAP_ANALYSIS.md`** - Detailed analysis of what agents fill
- **`WALKTHROUGH.md`** - Step-by-step code walkthrough

### **Demonstrations:**
- **`demo.py`** - Interactive demo of the agentic framework
- **`examples/gap_demonstration.py`** - Shows baseline vs agentic comparison

### **PDF Diagrams:**
- **`docs/diagrams/Agentic Flow.pdf`** - Core decision-making workflow
- **`docs/diagrams/Agentic Proposal.pdf`** - Enterprise architecture concepts

## 🚀 **Quick Navigation for Reviewers**

### **For Technical Overview:**
1. **[SHOWCASE_OVERVIEW.md](SHOWCASE_OVERVIEW.md)** - Technical expertise highlights
2. **[PDF_TO_CODE_MAPPING.md](PDF_TO_CODE_MAPPING.md)** - How PDF concepts become code
3. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Professional project organization

### **For Code Review:**
1. **[src/framework/enhanced_orchestrator.py](src/framework/enhanced_orchestrator.py)** - Main implementation
2. **[src/framework/agentic_orchestrator.py](src/framework/agentic_orchestrator.py)** - Full agentic framework
3. **[GAP_ANALYSIS.md](GAP_ANALYSIS.md)** - What agents provide vs baseline

### **For Demonstration:**
1. **[demo.py](demo.py)** - Interactive framework demonstration
2. **[examples/gap_demonstration.py](examples/gap_demonstration.py)** - Baseline vs agentic comparison

### Pipeline Phases

```
┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌───────────────┐     ┌───────┐
│  EXTRACT    │ --> │  VALIDATE    │ --> │ ANALYZE  │ --> │  TRANSFORM    │ --> │ BUILD │
└─────────────┘     └──────────────┘     └──────────┘     └───────────────┘     └───────┘
     │                    │                    │                   │                   │
     v                    v                    v                   v                   v
  Obtain raw        Clean and          Analyze deps       Convert to          Compile and
  source files      validate data      and patterns       target format        package
```

### Key Components

#### 1. **PipelineOrchestrator Class**
The core orchestration engine that manages:
- Phase execution sequencing
- Command execution with subprocess management
- Log file generation and management
- Artifact validation and copying
- Metrics calculation and reporting

#### 2. **Execution Modes**
Three flexible execution modes for different use cases:

- **Analysis Only**: Quick analysis without transformation (ideal for assessment)
- **Transform and Build**: Direct transformation and compilation (for rapid iteration)
- **Full Pipeline**: Complete end-to-end execution with all phases

#### 3. **Logging Infrastructure**
- Unique timestamped log files for each operation
- Centralized log directory (`runlogs/`)
- Automatic log rotation and cleanup
- Structured output for parsing and automation

#### 4. **Quality Control**
- Parses transformation logs to identify zero-error artifacts
- Implements selective copying based on quality criteria
- Calculates transformation and build success rates
- Provides detailed metrics reporting

## 🚀 Features

### Production-Ready Capabilities

- ✅ **Interactive Mode Selection**: User-friendly interface for choosing execution workflows
- ✅ **Robust Error Handling**: Graceful failures with detailed error messages
- ✅ **Progress Tracking**: Real-time feedback during long-running operations
- ✅ **Artifact Validation**: Automatic quality checks before promotion
- ✅ **Metrics Reporting**: Comprehensive success rate calculations
- ✅ **Build Tool Integration**: Seamless integration with ANT, Maven, or other build systems
- ✅ **Environment Variable Management**: Configurable execution contexts
- ✅ **Snapshot Support**: Multiple data version management

## 📋 Usage

### Basic Execution

```bash
python pipeline_orchestrator.py
```

### Interactive Workflow

1. **Enter project directory**: Path to your project root
2. **Select snapshot**: Choose from available data snapshots
3. **Enter application name**: Identifier for this execution
4. **Choose execution mode**:
   - `1` - Analysis Only
   - `2` - Transform and Build
   - `3` - Full Pipeline
   - `4` - Exit

### Example Session

```
============================================================
PIPELINE ORCHESTRATOR
============================================================

Enter project directory path: /path/to/project

Available snapshots:
  1. snapshot-1
  2. snapshot-2
  
Select snapshot (or press Enter for default): 1

Enter application name: my_application

Execution Modes:
  1. Analysis Only
  2. Transform and Build
  3. Full Pipeline (Analysis + Transform + Build)
  4. Exit

Select mode: 3

✓ Selected: Full Pipeline

============================================================
PHASE 1: EXTRACTION
============================================================

✓ Extracting source-files completed
✓ Extracting config-files completed
✓ Extracting data-files completed
✓ Extracting metadata completed

...

============================================================
PIPELINE EXECUTION SUMMARY
============================================================

Total Artifacts Processed:    150
Successful Transformations:   145
Artifacts Built:              142

Transformation Success Rate:  96.67%
Build Success Rate:           94.67%

============================================================

✓ Pipeline completed successfully
Total execution time: 324.56 seconds
```

## 🔧 Technical Implementation

### Command Execution

Each phase executes pipeline tools via subprocess with:
- Shell command execution
- Working directory management
- Output redirection to log files
- Exit code validation

### Log Management

```python
log_file = f"{script_name}_{timestamp}.log"
full_cmd = f"{cmd} > \"{log_file}\" 2>&1"
```

### Artifact Quality Control

Artifacts are validated using regex parsing of transformation logs:
```python
pattern = re.compile(r"\|\s*([^|]+\.\w+)\s*\|\s*0\s*\|")
```

Only artifacts with zero errors are promoted to the target directory.

### Metrics Calculation

Success rates are calculated as:
```
Success Rate = (Successful Artifacts / Total Artifacts) × 100%
```

Two key metrics are tracked:
1. **Transformation Success Rate**: Percentage of artifacts transformed without errors
2. **Build Success Rate**: Percentage of artifacts successfully compiled

## 📁 Project Structure

```
project/
├── pipeline_orchestrator.py    # Main orchestrator
├── runlogs/                     # Execution logs (timestamped)
├── tools/
│   └── pipeline/                # Pipeline tool scripts
│       ├── extract-*.py
│       ├── validate-*.py
│       ├── analyze-*.py
│       └── transform-*.py
├── deliveries/                  # Input data snapshots
│   ├── snapshot-1/
│   └── snapshot-2/
├── work/                        # Intermediate artifacts
│   └── transformed/
├── target/                      # Final build artifacts
│   └── artifacts/
└── logs/                        # Transformation logs
    └── transformation.log
```

## 🎓 Design Decisions

### Why Phase-Based Architecture?
- **Separation of Concerns**: Each phase has a single responsibility
- **Testability**: Phases can be tested independently
- **Flexibility**: Users can execute specific phases as needed
- **Debugging**: Easier to isolate issues to specific phases

### Why Selective Artifact Copying?
- **Quality Assurance**: Only validated artifacts proceed to build
- **Resource Efficiency**: Avoids wasting build time on known failures
- **Clear Metrics**: Success rates reflect actual usable output

### Why Timestamped Logging?
- **Audit Trail**: Complete history of all executions
- **Parallel Execution**: Prevents log file conflicts
- **Debugging**: Easy to correlate issues with specific runs

## 🛠️ Extensibility

The framework is designed to be extended:

1. **Add New Phases**: Inherit from `PipelineOrchestrator` and add new phase methods
2. **Custom Build Tools**: Modify `_execute_build()` to support additional tools
3. **Advanced Metrics**: Extend `_calculate_metrics()` for domain-specific KPIs
4. **Notification Integration**: Add hooks for Slack, email, or other notifications

### Example: Adding a New Phase

```python
def deploy_phase(self, environment: str) -> bool:
    """Deploy artifacts to specified environment."""
    print(f"\n{'='*60}")
    print(f"PHASE 6: DEPLOYMENT TO {environment.upper()}")
    print(f"{'='*60}\n")
    
    cmd = f"python tools/pipeline/deploy-to-{environment}.py"
    rc = self.run_command(cmd, f"Deploying to {environment}")
    
    return rc == 0
```

## 📊 Performance Characteristics

- **Scalability**: Handles projects with 1000+ source files
- **Reliability**: Fail-fast design prevents cascading failures
- **Observability**: Complete execution visibility through logs and metrics
- **User Experience**: Clear progress indicators and actionable error messages

## 🎯 Use Cases

This orchestration pattern is applicable to various domains:

- **Data Migration Projects**: Multi-stage data transformation pipelines
- **Code Modernization**: Legacy system conversion workflows
- **ETL Pipelines**: Extract-Transform-Load operations
- **Build Automation**: Complex multi-step build processes
- **Testing Frameworks**: Sequential test suite execution

## 📝 License

MIT License - Feel free to use this pattern in your own projects.

## 👤 Author

This orchestration framework was designed and implemented to manage enterprise-scale data processing pipelines, emphasizing production reliability, observability, and maintainability.

---

**Note**: This is a generalized framework. The actual implementation was used in a production environment to orchestrate complex transformation pipelines for enterprise applications.
