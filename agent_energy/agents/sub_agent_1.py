from google.adk.agents import LlmAgent

from .services.llm import MODEL
from .prompts.estrattore_prompt import prompt

estrattore = LlmAgent(
    name="estrattore",
    model=MODEL,
    description="Analizza e classifica la richiesta del cliente.",
    instruction=prompt,
    output_key="analisi_richiesta",
)

