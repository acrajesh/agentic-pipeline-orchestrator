# Agentic Pipeline Orchestrator Prompt

## System Role
You are implementing a **Full Agentic Pipeline Orchestrator** - the pinnacle of intelligent pipeline management that combines algorithmic agents with Large Language Model integration for autonomous decision-making, complex analysis, and enterprise-grade pipeline orchestration.

## Detailed Program Walkthrough

### **Step 1: Agentic System Initialization**
```python
class AgenticPipelineOrchestrator:
    def __init__(self, project_dir):
        # 1.1 Initialize enhanced orchestrator foundation
        super().__init__(project_dir)
        
        # 1.2 LLM Integration Configuration
        self.llm_enabled = os.getenv("AGENTIC_LLM_ENABLED", "true").lower() == "true"
        self.llm_provider = os.getenv("AGENTIC_LLM_PROVIDER", "openai")  # openai, gemini, anthropic
        self.jira_integration_enabled = os.getenv("AGENTIC_JIRA_ENABLED", "true").lower() == "true"
        
        # 1.3 Initialize LLM agents for cognitive tasks
        self.utils_analysis_agent = UtilsAnalysisAgent(self.llm_provider, self.llm_enabled)
        self.conversion_error_agent = ConversionErrorAgent(self.llm_provider, self.llm_enabled)
        self.compile_error_agent = CompileErrorAgent(self.llm_provider, self.llm_enabled)
        self.jira_integration_agent = JIRAIntegrationAgent(self.llm_provider, self.llm_enabled)
        
        # 1.4 Agentic intelligence tracking
        self.llm_analysis_count = 0
        self.jira_tickets_created = 0
        self.autonomous_resolutions = 0
        self.cognitive_escalations = 0
        
        self.logger.info("🧠 Agentic Pipeline Orchestrator initialized")
        self.logger.info(f"   LLM Integration: {'Enabled' if self.llm_enabled else 'Disabled'}")
        self.logger.info(f"   LLM Provider: {self.llm_provider}")
        self.logger.info(f"   JIRA Integration: {'Enabled' if self.jira_integration_enabled else 'Disabled'}")
```

### **Step 2: Hybrid Intelligence Command Execution**
```python
def execute_with_agentic_intelligence(self, cmd, cwd, desc, phase):
    # 2.1 Setup execution monitoring
    log_file = self._setup_command_logging(cmd)
    attempt_count = 0
    max_attempts = 3
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        # 2.2 Execute command with full monitoring
        print(f"🔧 Executing: {desc} (attempt {attempt_count})")
        exit_code = subprocess.call(f"{cmd} > \"{log_file}\" 2>&1", shell=True, cwd=cwd)
        
        # 2.3 SUCCESS PATH: Continue to next command
        if exit_code == 0:
            print(f"✅ {desc} completed successfully")
            self._record_success(cmd, desc, attempt_count)
            return exit_code
        
        # 2.4 🤖 ALGORITHMIC AGENT: Fast issue classification
        print(f"⚠️ Command failed with exit code {exit_code}")
        complexity = self._classify_issue_complexity(cmd, exit_code, log_file)
        
        issue = Issue(
            phase=phase,
            command=cmd,
            exit_code=exit_code,
            error_message=f"Command failed with exit code {exit_code}",
            log_file=log_file,
            complexity=complexity,
            context={"attempt": attempt_count, "description": desc}
        )
        
        # 2.5 🤖 ALGORITHMIC DECISION: Fast response for simple issues
        if complexity == IssueComplexity.SIMPLE:
            algorithmic_result = self._handle_with_algorithmic_agent(issue)
            if algorithmic_result == "success":
                self.autonomous_resolutions += 1
                return 0
            elif algorithmic_result == "retry":
                continue
        
        # 2.6 🧠 LLM AGENT: Deep analysis for complex issues
        elif complexity == IssueComplexity.COMPLEX:
            llm_result = self._handle_with_llm_agents(issue)
            if llm_result == "success":
                self.autonomous_resolutions += 1
                return 0
            elif llm_result == "retry":
                continue
        
        # 2.7 🚨 CRITICAL ESCALATION: Immediate attention required
        elif complexity == IssueComplexity.CRITICAL:
            return self._handle_critical_escalation(issue)
    
    # 2.8 All attempts exhausted - final LLM analysis and escalation
    print("❌ All attempts failed - performing final LLM analysis")
    return self._handle_with_llm_agents(issue)
```

### **Step 3: LLM Provider Integration Framework**
```python
def _call_llm_provider(self, prompt: str, analysis_type: str) -> Dict:
    # 3.1 LLM provider selection and routing
    self.llm_analysis_count += 1
    self.logger.info(f"🧠 LLM Provider Call: {self.llm_provider} for {analysis_type}")
    self.logger.info(f"   Prompt: {prompt[:100]}...")
    
    # 3.2 Route to appropriate LLM provider
    if self.llm_provider == "openai":
        return self._call_openai_llm(prompt, analysis_type)
    elif self.llm_provider == "gemini":
        return self._call_gemini_llm(prompt, analysis_type)
    elif self.llm_provider == "anthropic":
        return self._call_anthropic_llm(prompt, analysis_type)
    else:
        return self._mock_llm_response(prompt, analysis_type)

def _call_openai_llm(self, prompt: str, analysis_type: str) -> Dict:
    # 3.3 OpenAI GPT-4 integration
    self.logger.info("🔗 OpenAI GPT-4 Integration Point")
    
    try:
        # PRODUCTION INTEGRATION POINT:
        # import openai
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # 
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": self._get_system_prompt(analysis_type)},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.3,
        #     max_tokens=1000
        # )
        # 
        # return {
        #     "analysis": response.choices[0].message.content,
        #     "confidence": 0.9,
        #     "provider": "openai-gpt4",
        #     "tokens_used": response.usage.total_tokens
        # }
        
        # Demo response for showcase
        return {
            "analysis": f"OpenAI GPT-4 analysis for {analysis_type}: Detailed root cause analysis with specific recommendations",
            "recommendations": [
                "Increase memory allocation to 4GB",
                "Add retry mechanism with exponential backoff",
                "Verify network connectivity and DNS resolution"
            ],
            "confidence": 0.9,
            "provider": "openai-gpt4",
            "requires_jira": True,
            "priority": "High"
        }
        
    except Exception as e:
        self.logger.error(f"OpenAI API Error: {e}")
        return self._mock_llm_response(prompt, analysis_type)

def _call_gemini_llm(self, prompt: str, analysis_type: str) -> Dict:
    # 3.4 Google Gemini integration
    self.logger.info("🔗 Google Gemini Integration Point")
    
    try:
        # PRODUCTION INTEGRATION POINT:
        # import google.generativeai as genai
        # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # 
        # model = genai.GenerativeModel('gemini-pro')
        # response = model.generate_content(
        #     f"{self._get_system_prompt(analysis_type)}\n\n{prompt}"
        # )
        # 
        # return {
        #     "analysis": response.text,
        #     "confidence": 0.85,
        #     "provider": "google-gemini"
        # }
        
        # Demo response for showcase
        return {
            "analysis": f"Google Gemini analysis for {analysis_type}: Comprehensive technical analysis with contextual insights",
            "recommendations": [
                "Update configuration parameters",
                "Implement fallback mechanisms", 
                "Monitor resource utilization patterns"
            ],
            "confidence": 0.85,
            "provider": "google-gemini",
            "requires_jira": True,
            "priority": "Medium"
        }
        
    except Exception as e:
        self.logger.error(f"Gemini API Error: {e}")
        return self._mock_llm_response(prompt, analysis_type)

def _call_anthropic_llm(self, prompt: str, analysis_type: str) -> Dict:
    # 3.5 Anthropic Claude integration
    self.logger.info("🔗 Anthropic Claude Integration Point")
    
    try:
        # PRODUCTION INTEGRATION POINT:
        # import anthropic
        # client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # 
        # response = client.messages.create(
        #     model="claude-3-sonnet-20240229",
        #     max_tokens=1000,
        #     messages=[
        #         {"role": "user", "content": f"{self._get_system_prompt(analysis_type)}\n\n{prompt}"}
        #     ]
        # )
        # 
        # return {
        #     "analysis": response.content[0].text,
        #     "confidence": 0.88,
        #     "provider": "anthropic-claude"
        # }
        
        # Demo response for showcase
        return {
            "analysis": f"Anthropic Claude analysis for {analysis_type}: Deep reasoning with step-by-step problem solving",
            "recommendations": [
                "Analyze dependency chain for conflicts",
                "Implement graceful degradation patterns",
                "Create comprehensive error handling"
            ],
            "confidence": 0.88,
            "provider": "anthropic-claude",
            "requires_jira": True,
            "priority": "High"
        }
        
    except Exception as e:
        self.logger.error(f"Anthropic API Error: {e}")
        return self._mock_llm_response(prompt, analysis_type)
```

## Operational Characteristics

### Agentic Execution Model
```
FOR each pipeline_phase:
    result = execute_with_agentic_intelligence(phase)
    IF result.failed:
        # 🤖 ALGORITHMIC AGENT: Fast classification
        complexity = classify_issue_complexity(result)
        
        IF complexity == "simple":
            result = apply_algorithmic_recovery(result)
        ELIF complexity == "complex":
            # 🧠 LLM AGENT: Deep analysis
            llm_analysis = analyze_with_llm(result)
            result = apply_llm_guided_recovery(result, llm_analysis)
        ELIF complexity == "critical":
            escalate_with_intelligent_context(result)
        END IF
    END IF
END FOR
```

### Multi-Provider LLM Integration
- **OpenAI GPT Integration**: For general analysis and problem-solving
- **Google Gemini Integration**: For technical document analysis
- **Anthropic Claude Integration**: For complex reasoning and code analysis
- **Provider Selection Logic**: Choose optimal LLM based on task characteristics

### LLM Integration Points

#### 1. Complex Error Analysis
```
PROMPT TEMPLATE:
"Analyze this pipeline execution issue:

Phase: {phase_name}
Error Code: {exit_code}
Error Message: {error_details}
Context: {execution_context}
Project: {project_details}

Provide:
1. Root cause analysis
2. Recommended resolution steps
3. Risk assessment (HIGH/MEDIUM/LOW)
4. Whether this requires human intervention
5. Preventive measures for future occurrences"
```

#### 2. Unsupported Utility Analysis
```
PROMPT TEMPLATE:
"Analyze these unsupported utilities in a COBOL-to-Java migration:

Utilities: {utility_list}
Project Context: {project_context}
Target Platform: Java Enterprise

Recommend:
1. Modern equivalent alternatives
2. Migration strategies and approaches
3. Implementation complexity assessment
4. Priority order for remediation
5. Estimated effort and timeline"
```

#### 3. Intelligent JIRA Ticket Creation
```
PROMPT TEMPLATE:
"Create a comprehensive JIRA ticket for this pipeline issue:

Issue Analysis: {llm_analysis}
Technical Details: {technical_context}
Business Impact: {impact_assessment}

Generate:
1. Clear, actionable ticket title
2. Detailed description with context
3. Step-by-step resolution guide
4. Acceptance criteria
5. Recommended assignee team
6. Priority level with justification"
```

### Agentic Decision Framework

#### Goal-Oriented Behavior
- **Primary Goal**: Complete pipeline execution successfully
- **Secondary Goals**: Minimize manual intervention, optimize performance, learn from patterns
- **Constraint Awareness**: Resource limits, time boundaries, business requirements

#### Autonomous Decision-Making
```
FUNCTION make_agentic_decision(issue, context, history):
    # Fast algorithmic assessment
    quick_analysis = algorithmic_agent.analyze(issue)
    
    IF quick_analysis.confidence > 0.8:
        RETURN quick_analysis.recommended_action
    
    # Deep LLM analysis for complex scenarios
    llm_analysis = llm_agent.analyze(issue, context, history)
    
    # Combine insights for optimal decision
    final_decision = synthesize_insights(quick_analysis, llm_analysis)
    
    # Learn from outcome for future decisions
    update_knowledge_base(issue, final_decision, outcome)
    
    RETURN final_decision
```

#### Context-Aware Processing
- **Execution History**: Learn from previous successes and failures
- **Environmental Factors**: System load, time of day, resource availability
- **Business Context**: Project deadlines, criticality, stakeholder requirements
- **Technical Context**: Platform constraints, dependency relationships

### Enterprise Integration Capabilities

#### JIRA Integration
- **Intelligent Ticket Creation**: LLM-generated tickets with rich context
- **Priority Assessment**: Business impact analysis and urgency evaluation
- **Team Assignment**: Smart routing based on issue type and expertise
- **Progress Tracking**: Automated updates and resolution verification

#### Monitoring and Observability
- **Real-time Dashboards**: Agent decision tracking and performance metrics
- **Audit Trails**: Complete history of autonomous decisions and outcomes
- **Performance Analytics**: Success rates, recovery effectiveness, cost optimization
- **Predictive Insights**: Pattern recognition for proactive issue prevention

#### Configuration Management
```
Environment Variables:
- AGENTIC_LLM_ENABLED: Enable/disable LLM integration
- AGENTIC_LLM_PROVIDER: Select LLM provider (openai/gemini/anthropic)
- AGENTIC_JIRA_ENABLED: Enable/disable JIRA integration
- OPENAI_API_KEY: OpenAI authentication
- GEMINI_API_KEY: Google Gemini authentication
- ANTHROPIC_API_KEY: Anthropic Claude authentication
```

## Advanced Agentic Capabilities

### Learning and Adaptation
- **Pattern Recognition**: Identify recurring issues and optimal solutions
- **Performance Optimization**: Continuously improve decision-making accuracy
- **Predictive Analysis**: Anticipate potential issues before they occur
- **Knowledge Base Evolution**: Accumulate organizational knowledge over time

### Cognitive Augmentation Scenarios

#### Scenario 1: Complex Conversion Error
```
Issue: COBOL-to-Java conversion fails with cryptic error
Agentic Response:
1. Algorithmic agent classifies as "complex conversion issue"
2. LLM analyzes COBOL syntax patterns and Java compatibility
3. LLM generates specific code modifications and alternatives
4. System applies suggestions or creates detailed JIRA ticket
5. Learning: Update conversion pattern knowledge base
```

#### Scenario 2: Unsupported Legacy Utility
```
Issue: Pipeline encounters unsupported mainframe utility
Agentic Response:
1. LLM analyzes utility functionality and purpose
2. LLM researches modern alternatives and migration strategies
3. LLM generates comprehensive migration plan with risk assessment
4. System creates prioritized JIRA tickets with implementation roadmap
5. Learning: Build utility migration knowledge repository
```

#### Scenario 3: Performance Degradation
```
Issue: Pipeline execution times increasing over time
Agentic Response:
1. Algorithmic agent detects performance trend
2. LLM analyzes execution patterns and resource utilization
3. LLM identifies bottlenecks and optimization opportunities
4. System implements automatic optimizations where possible
5. Learning: Develop predictive performance models
```

## Prompt Instructions
When implementing this orchestrator:
1. Combine the best of algorithmic and LLM-based intelligence
2. Use algorithmic agents for fast, deterministic decisions
3. Leverage LLMs for complex analysis requiring contextual understanding
4. Implement comprehensive LLM provider integration framework
5. Create intelligent JIRA integration with rich, contextual tickets
6. Build learning mechanisms that improve over time
7. Ensure production-ready enterprise features (logging, monitoring, configuration)
8. Design for extensibility and integration with existing enterprise systems

## Success Criteria
- Autonomous resolution of 80%+ pipeline issues without human intervention
- Intelligent escalation with actionable insights for remaining 20%
- Significant reduction in mean time to resolution (MTTR)
- Comprehensive audit trails and decision transparency
- Seamless integration with enterprise tooling and workflows
- Continuous learning and improvement in decision-making accuracy
- Cost-effective LLM usage with optimal provider selection
- Production-ready reliability and performance characteristics
