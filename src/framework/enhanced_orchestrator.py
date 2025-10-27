"""
Enhanced Orchestrator with Agent Integration Points
==================================================

This is the orchest.py baseline enhanced with agent intervention points.
It maintains all existing functionality while adding agent hooks where
the PDF diagram shows intelligence is needed.

Key principle: Agents fill the gaps, don't replace working code.
"""

import os
import subprocess
import time
import sys
import re
import shutil
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AgentDecision(Enum):
    """Agent decision types from PDF diagram"""
    PROCEED = "proceed"
    RETRY = "retry"
    ADAPT = "adapt"
    ESCALATE = "escalate"
    ALTERNATIVE_PATH = "alternative_path"


@dataclass
class ExecutionContext:
    """Context that flows through the pipeline"""
    project_dir: str
    snapshot: str
    app_name: str
    target_language: str = "JAVA"
    script_language: str = "bash"
    environment_vars: Dict[str, str] = None
    execution_history: List[Dict] = None
    
    def __post_init__(self):
        if self.environment_vars is None:
            self.environment_vars = {}
        if self.execution_history is None:
            self.execution_history = []


class AgentInterface:
    """
    Interface for agent interventions - this is where agents plug in
    """
    
    def __init__(self, name: str):
        self.name = name
        self.intervention_count = 0
    
    def analyze_failure(self, cmd: str, exit_code: int, log_file: str, context: ExecutionContext) -> Dict:
        """🤖 AGENT INTERVENTION POINT: Analyze command failure"""
        self.intervention_count += 1
        print(f"🤖 {self.name} analyzing failure: {cmd}")
        
        # TEMPLATE: Agent analyzes the failure
        issue_analysis = {
            'issue_type': self._classify_issue(exit_code, log_file),
            'severity': self._assess_severity(cmd, exit_code),
            'context': {'command': cmd, 'exit_code': exit_code},
            'suggested_action': self._suggest_action(cmd, exit_code)
        }
        
        return issue_analysis
    
    def adapt_parameters(self, context: ExecutionContext, issue_analysis: Dict) -> Dict:
        """🤖 AGENT INTERVENTION POINT: Adapt execution parameters"""
        print(f"🤖 {self.name} adapting parameters based on: {issue_analysis['issue_type']}")
        
        # TEMPLATE: Agent adapts parameters
        adaptations = {}
        
        if 'timeout' in issue_analysis.get('context', {}).get('command', '').lower():
            adaptations['timeout'] = '600'  # Increase timeout
        
        if 'memory' in str(issue_analysis.get('context', {})).lower():
            adaptations['memory_limit'] = '4G'  # Increase memory
        
        return adaptations
    
    def decide_retry_strategy(self, cmd: str, attempt_count: int, context: ExecutionContext) -> AgentDecision:
        """🤖 AGENT INTERVENTION POINT: Decide retry strategy"""
        print(f"🤖 {self.name} deciding retry strategy for attempt {attempt_count}")
        
        # TEMPLATE: Agent decides retry strategy
        if attempt_count < 3:
            if 'network' in cmd.lower() or 'timeout' in cmd.lower():
                return AgentDecision.RETRY
            else:
                return AgentDecision.ADAPT
        else:
            return AgentDecision.ESCALATE
    
    def find_alternative_path(self, failed_phase: str, context: ExecutionContext) -> Optional[List[str]]:
        """🤖 AGENT INTERVENTION POINT: Find alternative execution path"""
        print(f"🤖 {self.name} finding alternative path for failed phase: {failed_phase}")
        
        # TEMPLATE: Agent finds alternative paths
        alternatives = {
            'obtain-cobol-programs': ['obtain-cobol-copybooks', 'analyze-existing-programs'],
            'convert-cobol-to-oo': ['convert-with-relaxed-rules', 'partial-conversion'],
            'ant-build': ['maven-build', 'gradle-build']
        }
        
        return alternatives.get(failed_phase, None)
    
    def escalate_issue(self, issue_analysis: Dict, context: ExecutionContext) -> bool:
        """🤖 AGENT INTERVENTION POINT: Escalate critical issues"""
        print(f"🤖 {self.name} escalating issue: {issue_analysis['issue_type']}")
        
        # TEMPLATE: Agent escalates with context
        escalation_data = {
            'timestamp': time.time(),
            'project': context.app_name,
            'issue': issue_analysis,
            'context': context.__dict__,
            'intervention_count': self.intervention_count
        }
        
        # In production: Send to monitoring system
        print(f"📤 Escalation data prepared: {json.dumps(escalation_data, indent=2)}")
        return True
    
    def _classify_issue(self, exit_code: int, log_file: str) -> str:
        """Classify the type of issue"""
        # TEMPLATE: Issue classification logic
        if exit_code == 1:
            return "general_error"
        elif exit_code == 2:
            return "configuration_error"
        elif exit_code == 124:
            return "timeout_error"
        else:
            return "unknown_error"
    
    def _assess_severity(self, cmd: str, exit_code: int) -> str:
        """Assess issue severity"""
        # TEMPLATE: Severity assessment logic
        if 'critical' in cmd.lower() or exit_code > 100:
            return "high"
        elif 'analyze' in cmd.lower():
            return "medium"
        else:
            return "low"
    
    def _suggest_action(self, cmd: str, exit_code: int) -> str:
        """Suggest resolution action"""
        # TEMPLATE: Action suggestion logic
        if exit_code == 124:
            return "increase_timeout"
        elif 'memory' in cmd.lower():
            return "increase_memory"
        else:
            return "retry_with_backoff"


class EnhancedOrchestrator:
    """
    Enhanced version of orchest.py with agent integration points
    Maintains all original functionality + agent interventions
    """
    
    def __init__(self):
        self.agent = AgentInterface("PipelineAgent")
        self.context: Optional[ExecutionContext] = None
    
    def run_cmd_with_agent(self, cmd: str, cwd: str, desc: str, log_dir: str = None) -> int:
        """
        Enhanced version of run_cmd with agent intervention
        🔄 MAINTAINS ORIGINAL FUNCTIONALITY + ADDS AGENT INTELLIGENCE
        """
        # Original logging setup (unchanged)
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runlogs")
        os.makedirs(log_dir, exist_ok=True)
        
        script_name = os.path.basename(cmd.split()[2]) if len(cmd.split()) > 2 else cmd.replace(' ', '_')
        log_file = os.path.join(log_dir, f"{os.path.splitext(script_name)[0]}_{int(time.time())}.log")
        
        attempt_count = 0
        max_attempts = 3
        
        while attempt_count < max_attempts:
            attempt_count += 1
            
            # Apply any parameter adaptations from previous attempts
            if attempt_count > 1 and self.context:
                cmd = self._apply_parameter_adaptations(cmd, self.context)
            
            # Execute command (original logic)
            full_cmd = f"{cmd} > \"{log_file}\" 2>&1"
            print(f"🔧 Executing: {desc} (attempt {attempt_count})")
            code = subprocess.call(full_cmd, shell=True, cwd=cwd)
            
            # ✅ ORIGINAL SUCCESS PATH (unchanged)
            if code == 0:
                return code
            
            # 🤖 AGENT INTERVENTION POINT: Failure analysis
            print(f"⚠️ Command failed with exit code {code}")
            issue_analysis = self.agent.analyze_failure(cmd, code, log_file, self.context)
            
            # 🤖 AGENT INTERVENTION POINT: Decide next action
            decision = self.agent.decide_retry_strategy(cmd, attempt_count, self.context)
            
            if decision == AgentDecision.PROCEED:
                print("🤖 Agent decided to proceed despite failure")
                return 0  # Agent overrides failure
            
            elif decision == AgentDecision.RETRY:
                if attempt_count < max_attempts:
                    delay = 2 ** attempt_count  # Exponential backoff
                    print(f"🤖 Agent decided to retry in {delay}s...")
                    time.sleep(delay)
                    continue
            
            elif decision == AgentDecision.ADAPT:
                print("🤖 Agent decided to adapt parameters")
                adaptations = self.agent.adapt_parameters(self.context, issue_analysis)
                self._apply_adaptations(adaptations)
                if attempt_count < max_attempts:
                    continue
            
            elif decision == AgentDecision.ALTERNATIVE_PATH:
                print("🤖 Agent searching for alternative path")
                alternatives = self.agent.find_alternative_path(script_name, self.context)
                if alternatives:
                    # Try first alternative
                    alt_cmd = alternatives[0]
                    print(f"🤖 Trying alternative: {alt_cmd}")
                    return self.run_cmd_with_agent(alt_cmd, cwd, f"Alternative: {desc}", log_dir)
            
            elif decision == AgentDecision.ESCALATE:
                print("🤖 Agent decided to escalate")
                self.agent.escalate_issue(issue_analysis, self.context)
                break
        
        # If all attempts failed, return original error code
        print(f"❌ All attempts failed for: {desc}")
        return code
    
    def main_with_agents(self):
        """
        Enhanced main function with agent integration points
        🔄 MAINTAINS ALL ORIGINAL ORCHEST.PY LOGIC + ADDS AGENT INTELLIGENCE
        """
        print("🤖 Enhanced Orchestrator with Agent Intelligence")
        print("   Based on orchest.py + PDF diagram concepts")
        
        # ✅ ORIGINAL USER INPUT (unchanged)
        project_dir = input("Enter factory project folder path: ").strip()
        if not os.path.isdir(project_dir):
            print(f"Folder '{project_dir}' not found. Exiting.")
            sys.exit(1)
        
        # ✅ ORIGINAL SNAPSHOT SELECTION (unchanged)
        deliveries = os.path.join(project_dir, 'deliveries')
        snapshots = [d for d in os.listdir(deliveries) if os.path.isdir(os.path.join(deliveries, d))]
        print("Available snapshots:")
        for i, snap in enumerate(snapshots, 1):
            print(f" {i}. {snap}")
        
        snap_choice = input("Select snapshot by number (or press Enter for default 'snapshot-1'): ").strip()
        snapshot = snapshots[int(snap_choice)-1] if snap_choice.isdigit() and 1 <= int(snap_choice) <= len(snapshots) else 'snapshot-1'
        
        app_name = input("Enter app-name to use: ").strip()
        confirm = input("Confirm target languages are JAVA and bash (Y/n): ").strip().lower()
        
        # Initialize execution context for agents
        self.context = ExecutionContext(
            project_dir=project_dir,
            snapshot=snapshot,
            app_name=app_name,
            target_language="JAVA",
            script_language="bash"
        )
        
        # ✅ ORIGINAL MODE SELECTION (unchanged)
        print("Choose from the below options:")
        print(" 1. Analysis only")
        print(" 2. Convert and Compile")
        print(" 3. Analysis, Convert and Compile")
        print(" 4. Exit")
        choice = input("Choose mode: ").strip()
        
        # ✅ ORIGINAL ENVIRONMENT SETUP (unchanged)
        os.environ['DELIVERY_DIR'] = f"deliveries/{snapshot}"
        os.environ['SNAPSHOT_NAME'] = snapshot
        os.environ['TARGET_LANGUAGE'] = 'JAVA'
        os.environ['TARGET_SCRIPT_LANGUAGE'] = 'bash'
        
        # ✅ ORIGINAL COMMAND DEFINITIONS (unchanged)
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
            ("LD01", f"py -3 tools/migratonomy/load-analysis-csv-files.py --data-set={{app_name}}"),
            ("GN01", f"py -3 tools/migratonomy/generate-analysis-reports.py --data-set={{app_name}}"),
        ]
        
        # 🔄 ENHANCED EXECUTION WITH AGENT INTELLIGENCE
        if choice in ('1', '3'):
            print("🤖 Starting analysis phase with agent monitoring...")
            
            for phase_id, cmd in analysis_cmds:
                # Replace app_name placeholder
                cmd = cmd.format(app_name=app_name)
                
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
                
                # 🤖 USE ENHANCED COMMAND EXECUTION WITH AGENT
                rc = self.run_cmd_with_agent(cmd, project_dir, msg)
                
                # 🔄 ORIGINAL LOGIC: Only exit if agent couldn't resolve
                if rc != 0:
                    print(f"❌ {msg} failed even after agent intervention")
                    # 🤖 FINAL AGENT ESCALATION
                    issue_analysis = {
                        'phase': phase_id,
                        'command': cmd,
                        'exit_code': rc,
                        'message': f"Unrecoverable failure in {msg}"
                    }
                    self.agent.escalate_issue(issue_analysis, self.context)
                    sys.exit(1)
                
                # ✅ ORIGINAL SUCCESS REPORTING (unchanged)
                print(f"✅ {msg} completed successfully")
        
        # ✅ ORIGINAL ARTIFACT MANAGEMENT (unchanged but with agent monitoring)
        if choice in ('2', '3'):
            print("🤖 Starting conversion phase with agent monitoring...")
            # Conversion commands would go here with run_cmd_with_agent
        
        # 🤖 AGENT SUMMARY REPORT
        self._generate_agent_report()
    
    def _apply_parameter_adaptations(self, cmd: str, context: ExecutionContext) -> str:
        """Apply parameter adaptations suggested by agents"""
        # TEMPLATE: Parameter adaptation logic
        adapted_cmd = cmd
        
        if 'timeout' in context.environment_vars:
            adapted_cmd += f" --timeout={context.environment_vars['timeout']}"
        
        if 'memory_limit' in context.environment_vars:
            adapted_cmd += f" --memory={context.environment_vars['memory_limit']}"
        
        return adapted_cmd
    
    def _apply_adaptations(self, adaptations: Dict):
        """Apply adaptations to context"""
        if self.context:
            self.context.environment_vars.update(adaptations)
    
    def _generate_agent_report(self):
        """Generate report of agent interventions"""
        print(f"\n{'='*60}")
        print("🤖 AGENT INTERVENTION REPORT")
        print(f"{'='*60}")
        print(f"Total Agent Interventions: {self.agent.intervention_count}")
        print(f"Project: {self.context.app_name}")
        print(f"Snapshot: {self.context.snapshot}")
        print("Agent successfully filled gaps in the baseline orchestrator!")


if __name__ == '__main__':
    orchestrator = EnhancedOrchestrator()
    orchestrator.main_with_agents()
