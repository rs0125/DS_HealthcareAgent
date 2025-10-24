"""
Main healthcare workflow
"""

from typing import Dict, Any
from .config import HealthcareConfig
from .chains import (
    GuardrailChain,
    IntentClassifierChain,
    SymptomCheckerChain,
    GovernmentSchemeChain,
    MentalWellnessChain,
    YogaChain,
    AyushChain,
    HospitalLocatorChain
)


class HealthcareWorkflow:
    """Main workflow orchestrator"""
    
    def __init__(self, config: HealthcareConfig):
        self.config = config
        
        # Initialize all chains
        self.guardrail = GuardrailChain(config.llm)
        self.classifier = IntentClassifierChain(config.llm)
        self.symptom_chain = SymptomCheckerChain(config.llm)
        self.gov_scheme_chain = GovernmentSchemeChain(config.llm, config.search_tool)
        self.mental_wellness_chain = MentalWellnessChain(config.llm, config.search_tool)
        self.yoga_chain = YogaChain(config.llm, config.search_tool)
        self.ayush_chain = AyushChain(config.llm, config.search_tool)
        self.hospital_chain = HospitalLocatorChain(config.llm, config.search_tool)
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """Execute the workflow"""
        
        # Step 1: Safety check
        print("🛡️  [STEP 1/3] Running Safety Guardrail Check...")
        safety_check = self.guardrail.check(user_input)
        if not safety_check.get("is_safe", True):
            print(f"   ⚠️  Content blocked: {safety_check.get('reason')}")
            return {
                "status": "blocked",
                "reason": safety_check.get("reason"),
                "category": safety_check.get("category")
            }
        print("   ✓ Content is safe\n")
        
        # Step 2: Classify intent
        print("🎯 [STEP 2/3] Classifying Intent...")
        classification = self.classifier.run(user_input)
        intent = classification.get("classification")
        print(f"   → Intent: {intent}")
        print(f"   → Reasoning: {classification.get('reasoning')}\n")
        
        # Step 3: Route to appropriate chain
        print(f"🔗 [STEP 3/3] Executing Chain for '{intent}'...")
        result = {
            "intent": intent,
            "reasoning": classification.get("reasoning"),
            "output": None
        }
        
        if intent == "government_scheme_support":
            print("   → Running Government Scheme Search Chain")
            result["output"] = self.gov_scheme_chain.run(user_input)
            
        elif intent == "mental_wellness_support":
            print("   → Running Mental Wellness Chain")
            result["output"] = self.mental_wellness_chain.run(user_input)
            
            print("   → Running Yoga Suggestion Chain")
            result["yoga_recommendations"] = self.yoga_chain.run(user_input)
            
        elif intent == "ayush_support":
            print("   → Running AYUSH Support Chain")
            result["output"] = self.ayush_chain.run(user_input)
            
        elif intent == "symptom_checker":
            result.update(self._handle_symptoms(user_input))
            
        elif intent == "facility_locator_support":
            print("   → Running Hospital Locator Chain")
            result["output"] = self.hospital_chain.run(user_input)
            
        else:
            print(f"   ⚠️  Unknown intent: {intent}")
            result["output"] = "I couldn't understand your request. Please try rephrasing."
        
        print("   ✓ Chain execution complete\n")
        return result
    
    def _handle_symptoms(self, user_input: str) -> Dict[str, Any]:
        """Handle symptom checking with multi-agent follow-up"""
        print("   → Running Symptom Extraction Chain")
        symptom_data = self.symptom_chain.run(user_input)
        
        result = {
            "symptom_assessment": symptom_data.model_dump()
        }
        
        print(f"   → Extracted {len(symptom_data.symptoms)} symptoms")
        print(f"   → Emergency flag: {symptom_data.is_emergency}")
        
        if symptom_data.is_emergency:
            print("   ⚠️  EMERGENCY DETECTED!")
            print("   → Routing to Hospital Locator Agent")
            
            hospital_query = f"Find nearest emergency hospitals for: {', '.join(symptom_data.symptoms)}"
            if "location" not in user_input.lower() and "near" not in user_input.lower():
                hospital_query += ". User location not specified - provide general emergency guidance."
            
            result["output"] = {
                "emergency": True,
                "message": "⚠️ URGENT: Seek immediate medical attention. "
                          "Call emergency services (112 in India) or go to nearest hospital.",
                "symptoms": symptom_data.symptoms,
                "severity": symptom_data.severity
            }
            result["hospital_locator"] = self.hospital_chain.run(hospital_query)
            result["emergency_number"] = "112 (India Emergency Services)"
        else:
            # Non-emergency: Multi-agent recommendations
            result["output"] = {
                "emergency": False,
                "message": "Based on your symptoms, here are some recommendations:"
            }
            
            symptom_text = f"Patient has {', '.join(symptom_data.symptoms)} with severity {symptom_data.severity}/10"
            if symptom_data.duration:
                symptom_text += f" for {symptom_data.duration}"
            
            # Ayurveda recommendations
            print("   → Running Ayurvedic Recommendation Agent")
            result["ayurveda_recommendations"] = self.ayush_chain.run(
                f"Provide ayurvedic remedies for: {symptom_text}"
            )
            
            # Yoga recommendations
            print("   → Running Yoga Recommendation Agent")
            result["yoga_recommendations"] = self.yoga_chain.run(
                f"Suggest yoga poses and breathing exercises for: {symptom_text}"
            )
            
            # General wellness guidance
            print("   → Running Wellness Guidance Agent")
            result["general_guidance"] = self.mental_wellness_chain.run(
                f"Provide wellness advice and when to see a doctor for: {symptom_text}"
            )
        
        return result
