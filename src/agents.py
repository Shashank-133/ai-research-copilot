"""
Multi-agent system for AI Research Co-Pilot
"""

from datetime import datetime


class MultiAgentSystem:
    """
    Orchestrates multiple AI agents for comprehensive research
    """
    
    def __init__(self, client, model):
        """
        Initialize multi-agent system
        
        Args:
            client: OpenAI client instance
            model (str): Model name to use
        """
        self.client = client
        self.model = model
        self.current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    
    def researcher_agent(self, query, search_results):
        """
        Agent 1: Research and gather information
        
        Args:
            query (str): User query
            search_results (list): Web search results
            
        Returns:
            str: Research findings
        """
        search_context = ""
        if search_results:
            search_context = "\n\nWEB SEARCH RESULTS:\n"
            for i, result in enumerate(search_results, 1):
                search_context += f"\n{i}. {result['title']}\n"
                search_context += f"   {result['snippet']}\n"
                search_context += f"   Source: {result['url']}\n"
        
        system_prompt = f"""You are a Research Agent specializing in gathering and organizing information.
Current Date/Time: {self.current_time}

Your task:
1. Analyze the query and search results
2. Extract key information and facts
3. Identify important data points
4. List all sources

Provide a comprehensive research summary."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{query}\n{search_context}"}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def analyst_agent(self, query, research_data):
        """
        Agent 2: Analyze and synthesize information
        
        Args:
            query (str): User query
            research_data (str): Research findings from researcher agent
            
        Returns:
            str: Analysis and insights
        """
        system_prompt = """You are an Analysis Agent specializing in critical thinking and synthesis.

Your task:
1. Analyze the research findings
2. Identify patterns and trends
3. Draw meaningful conclusions
4. Highlight key insights
5. Provide expert perspective

Create a detailed analysis with clear insights."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}\n\nResearch Data:\n{research_data}"}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def writer_agent(self, query, research_data, analysis_data):
        """
        Agent 3: Create final polished output
        
        Args:
            query (str): User query
            research_data (str): Research findings
            analysis_data (str): Analysis insights
            
        Returns:
            str: Final comprehensive answer
        """
        system_prompt = """You are a Writing Agent specializing in creating clear, engaging content.

Your task:
1. Synthesize research and analysis
2. Create a well-structured response
3. Use clear, professional language
4. Include specific examples and data
5. Provide actionable insights

Create a comprehensive, well-formatted final answer."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Query: {query}

Research Findings:
{research_data}

Analysis:
{analysis_data}

Create the final comprehensive answer."""}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content