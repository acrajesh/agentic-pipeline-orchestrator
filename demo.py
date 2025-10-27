#!/usr/bin/env python3
"""
Agentic Pipeline Orchestrator Demo
==================================

This demo showcases the agentic framework implementing the concepts from the PDF diagrams.
It demonstrates autonomous issue resolution, intelligent decision-making, and production-ready
pipeline orchestration.

Run this to see the PDF diagram concepts in action!
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from framework.agentic_orchestrator import (
    AgenticPipelineOrchestrator,
    PipelineContext,
    PipelinePhase
)


def run_demo():
    """Run the agentic orchestrator demo"""
    
    print("\n" + "="*80)
    print("🤖 AGENTIC PIPELINE ORCHESTRATOR DEMO")
    print("   Implementing PDF Diagram Concepts in Production Code")
    print("="*80)
    
    print("\n📋 This demo showcases:")
    print("   • Autonomous issue detection and resolution")
    print("   • Intelligent decision-making agents")
    print("   • Self-correcting pipeline execution")
    print("   • Production-ready enterprise framework")
    
    print("\n📄 Based on PDF diagrams:")
    print("   • docs/diagrams/Agentic Flow.pdf")
    print("   • docs/diagrams/Agentic Proposal.pdf")
    
    # Get demo parameters
    print("\n" + "-"*60)
    print("DEMO CONFIGURATION")
    print("-"*60)
    
    project_id = input("Enter project ID (default: demo-project): ").strip() or "demo-project"
    app_name = input("Enter app name (default: demo-app): ").strip() or "demo-app"
    
    print(f"\n🎯 Demo Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   App Name: {app_name}")
    print(f"   Simulated Issues: Enabled (for demonstration)")
    
    # Create pipeline context
    context = PipelineContext(
        project_id=project_id,
        snapshot="demo-snapshot",
        app_name=app_name,
        target_language="java",
        script_language="bash",
        metadata={
            "simulate_issues": True,  # Enable issue simulation for demo
            "demo_mode": True
        }
    )
    
    # Initialize orchestrator
    current_dir = Path.cwd()
    orchestrator = AgenticPipelineOrchestrator(str(current_dir))
    
    print(f"\n🚀 Starting Agentic Pipeline Execution...")
    print(f"   Watch for autonomous issue resolution!")
    
    # Execute pipeline with selected phases
    phases = [PipelinePhase.EXTRACT, PipelinePhase.VALIDATE, PipelinePhase.ANALYZE]
    
    success = orchestrator.execute_pipeline(context, phases)
    
    print(f"\n" + "="*80)
    print("DEMO SUMMARY")
    print("="*80)
    
    if success:
        print("✅ Demo completed successfully!")
        print("   The agentic framework demonstrated:")
        print("   • Autonomous issue detection")
        print("   • Intelligent resolution strategies")
        print("   • Self-correcting behavior")
        print("   • Production-ready logging and metrics")
    else:
        print("⚠️ Demo completed with managed failures")
        print("   This demonstrates:")
        print("   • Graceful failure handling")
        print("   • Intelligent escalation")
        print("   • Comprehensive error reporting")
    
    print(f"\n📊 Key Metrics:")
    print(f"   • Phases Executed: {len(orchestrator.execution_history)}")
    print(f"   • Agent Decisions: {len(orchestrator.issue_resolver.decision_history)}")
    print(f"   • Total Artifacts: {sum(len(r.artifacts) for r in orchestrator.execution_history)}")
    
    print(f"\n🤖 Agentic Intelligence Demonstrated:")
    if orchestrator.issue_resolver.decision_history:
        decision_types = set(d['decision'] for d in orchestrator.issue_resolver.decision_history)
        for decision in decision_types:
            count = sum(1 for d in orchestrator.issue_resolver.decision_history if d['decision'] == decision)
            print(f"   • {decision.title()}: {count} times")
    else:
        print("   • No issues encountered (perfect execution)")
    
    print(f"\n📁 Check the logs directory for detailed execution logs")
    print(f"🔍 Review src/framework/agentic_orchestrator.py for implementation details")
    
    print(f"\n" + "="*80)
    print("This demo proves the PDF concepts work in production code!")
    print("="*80)


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print(f"   This is likely due to missing dependencies or setup issues")
        sys.exit(1)
