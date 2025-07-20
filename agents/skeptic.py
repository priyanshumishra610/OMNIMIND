"""
Skeptic Agent for OMNIMIND

Agent responsible for critical analysis and questioning assumptions.
"""

from .agent_base import BaseAgent
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Skeptic(BaseAgent):
    """Agent that critically analyzes and questions information."""
    
    def __init__(self, name: str = "Skeptic"):
        super().__init__(name, "skeptic")
        self.critical_questions = []
        self.assumption_checks = []
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and critically analyze the input data."""
        try:
            content = input_data.get("content", "")
            claims = input_data.get("claims", [])
            context = input_data.get("context", "")
            
            critical_analysis = []
            skepticism_score = 0.0
            
            # Analyze claims
            for claim in claims:
                analysis = self._analyze_claim(claim, context)
                critical_analysis.append(analysis)
                skepticism_score += analysis.get("skepticism_score", 0.0)
            
            # Generate critical questions
            questions = self._generate_critical_questions(content, claims)
            
            if critical_analysis:
                skepticism_score /= len(critical_analysis)
            
            self.update_confidence(1.0 - skepticism_score)  # Lower confidence for high skepticism
            
            return {
                "agent": self.name,
                "critical_analysis": critical_analysis,
                "critical_questions": questions,
                "skepticism_score": skepticism_score,
                "status": "completed"
            }
        except Exception as e:
            logger.error(f"Error in skeptical analysis: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "status": "failed"
            }
    
    def _analyze_claim(self, claim: str, context: str) -> Dict[str, Any]:
        """Analyze a claim for potential issues."""
        # Placeholder for actual critical analysis
        issues = []
        skepticism_score = 0.3  # Placeholder score
        
        # Check for common logical fallacies
        if "always" in claim.lower() or "never" in claim.lower():
            issues.append("Absolute language detected")
            skepticism_score += 0.2
        
        if "proven" in claim.lower() and "study" not in context.lower():
            issues.append("Unsupported proof claim")
            skepticism_score += 0.3
        
        return {
            "claim": claim,
            "issues": issues,
            "skepticism_score": min(1.0, skepticism_score),
            "analysis_method": "placeholder"
        }
    
    def _generate_critical_questions(self, content: str, claims: List[str]) -> List[str]:
        """Generate critical questions about the content."""
        questions = []
        
        # Placeholder questions
        if claims:
            questions.append("What evidence supports these claims?")
            questions.append("Are there alternative explanations?")
            questions.append("What are the limitations of this analysis?")
        
        return questions
    
    def add_critical_question(self, question: str):
        """Add a critical question to the agent's repertoire."""
        if question not in self.critical_questions:
            self.critical_questions.append(question)
    
    def get_critical_questions(self) -> List[str]:
        """Get all critical questions."""
        return self.critical_questions.copy() 

    def run(self, question, answer, context):
        # Dummy implementation for test compatibility
        return {"challenge": "Are you sure?"} 