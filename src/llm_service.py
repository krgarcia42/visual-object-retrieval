import logging

logger = logging.getLogger(__name__)

class LLMService:
    """
    Local LLM Simulation. 
    Provides a generative-style description without external API calls.
    """
    def summarize_scene(self, labels):
        if not labels:
            return "A desolate or empty scene with no visible objects."

        #simulate the 'LLM brain' by constructing a sentence based on the labels provided by InferenceWorker
        formatted_labels = ", ".join(labels[:-1]) + " and " + labels[-1] if len(labels) > 1 else labels[0]
        
        #simulate the "intelligence"
        summary = f"The visual data suggests a scene prominently featuring {formatted_labels}."
        
        logger.info(f"Local LLM Summary Generated: {summary}")
        return summary
