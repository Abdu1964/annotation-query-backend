import os
from dotenv import load_dotenv
from app.services.llm_models import OpenAIModel, GeminiModel
from app.services.graph_handler import Graph_Summarizer
import logging

load_dotenv()

class LLMHandler:
    def __init__(self):
        model_type = os.getenv('LLM_MODEL')

        if model_type == 'openai':
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                self.model = None
            else:
                self.model = OpenAIModel(openai_api_key)
        elif model_type == 'gemini':
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                self.model = None
            else:
                self.model = GeminiModel(gemini_api_key)
        else:
            raise ValueError("Invalid model type in configuration")

    def generate_title(self, query, request=None, node_map=None):
        try:
            print(request)
            print(node_map)
            if self.model is None:
                if request is None or node_map is None:
                    return "Untitled"
                else:
                    title = self.generate_title_no_llm(request, node_map)
                    return title
            prompt = f'''From this query generate approperiate title. Only give the title sentence don't add any prefix.
                         Query: {query}'''
            title = self.model.generate(prompt)
            return title
        except Exception as e:
            logging.error("Error generating title: ", {e})
            if request is None or node_map is None:
                return "Untitled"
            else:
                title = self.generate_title_no_llm(request, node_map)
                return title

    def generate_title_no_llm(self, req, node_map):
        predicates = req.get('predicates', [])
    
        def describe_node(node):
            """Describe node with its properties."""
            node_type_clean = node['type'].replace('_', ' ').lower()
            props = node.get('properties', {})
    
            if not props:
                return node_type_clean
    
            props_str = ", ".join(
                f"{k.replace('_',' ')} '{str(v).replace('_',' ')}'" for k,v in props.items()
            )
    
            return f"{node_type_clean} with {props_str}"
    
        # Generic verb for linking
        link_verb = "linked to"
    
        if not predicates:
            parts = [describe_node(node) for node in node_map.values()]
            return "Explore " + ", ".join(parts)
    
        # Build chain with "linked to" + optional relationship label
        relations = []
        for p in predicates:
            source_desc = describe_node(node_map[p['source']])
            target_desc = describe_node(node_map[p['target']])
            rel_desc = p['type'].replace('_',' ').lower()  # use the predicate name as relationship
    
            # e.g., "linked to protein with relationship gene product"
            relations.append(f"{source_desc} {link_verb} {target_desc} with relationship {rel_desc}")
    
        return "Explore " + ", ".join(relations)

    def generate_summary(self, graph, request, user_query=None,graph_id=None, summary=None):
        try:
            if self.model is None:
                return "No summary available"
            summarizer = Graph_Summarizer(self.model)
            summary = summarizer.summary(graph, request, user_query, graph_id, summary)
            return summary
        except Exception as e:
            logging.error("Error generating summary: ", e)
            return "No summary available"
