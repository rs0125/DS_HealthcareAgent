"""
Specialized chain implementations
"""

from .base_chains import SearchBasedChain


class GovernmentSchemeChain(SearchBasedChain):
    """Handles government scheme queries"""
    
    def __init__(self, llm, search_tool):
        system_prompt = """You are a government healthcare scheme advisor for India.

Based on the user query and search results:
1. Identify relevant government health schemes
2. Explain eligibility criteria
3. Provide official links and application process

Search results available:
{search_results}"""
        super().__init__(llm, search_tool, system_prompt)
    
    def run(self, user_input: str) -> str:
        search_query = f"India government health schemes {user_input}"
        return self.search_and_generate(user_input, search_query)


class MentalWellnessChain(SearchBasedChain):
    """Handles mental wellness support"""
    
    def __init__(self, llm, search_tool):
        system_prompt = """You are a compassionate mental wellness counselor.

Provide:
1. Empathetic acknowledgment
2. Evidence-based coping strategies
3. Professional help resources
4. Indian mental health helplines (KIRAN: 1800-599-0019)

Use search results for current resources:
{search_results}"""
        super().__init__(llm, search_tool, system_prompt)
    
    def run(self, user_input: str) -> str:
        search_query = f"mental health support resources India {user_input}"
        return self.search_and_generate(user_input, search_query)


class YogaChain(SearchBasedChain):
    """Provides yoga recommendations"""
    
    def __init__(self, llm, search_tool):
        system_prompt = """You are a certified yoga instructor.

Provide:
1. Specific yoga poses (asanas)
2. Breathing exercises (pranayama)
3. Safety precautions
4. Duration and frequency

Search results:
{search_results}"""
        super().__init__(llm, search_tool, system_prompt)
    
    def run(self, user_input: str) -> str:
        search_query = f"yoga therapy recommendations {user_input}"
        return self.search_and_generate(user_input, search_query)


class AyushChain(SearchBasedChain):
    """Handles AYUSH-related queries"""
    
    def __init__(self, llm, search_tool):
        system_prompt = """You are an AYUSH (Ayurveda, Yoga, Unani, Siddha, Homeopathy) advisor.

Provide:
1. Traditional remedies and treatments
2. Dietary recommendations
3. Lifestyle modifications
4. Precautions and contraindications

Search results:
{search_results}"""
        super().__init__(llm, search_tool, system_prompt)
    
    def run(self, user_input: str) -> str:
        search_query = f"AYUSH ministry India schemes {user_input}"
        return self.search_and_generate(user_input, search_query)


class HospitalLocatorChain(SearchBasedChain):
    """Finds nearby healthcare facilities"""
    
    def __init__(self, llm, search_tool):
        system_prompt = """You are a healthcare facility locator.

Provide:
1. Extract location from user query
2. Search for nearby healthcare facilities
3. List hospitals with address, contact, and specialties

Search results:
{search_results}"""
        super().__init__(llm, search_tool, system_prompt)
    
    def run(self, user_input: str) -> str:
        search_query = f"hospitals healthcare facilities near {user_input}"
        return self.search_and_generate(user_input, search_query)
