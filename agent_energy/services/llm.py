from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()

_orig_model_dump = LiteLlm.model_dump

def _safe_model_dump(self, **kwargs):
    result = _orig_model_dump(self, **kwargs)
    result.pop("llm_client", None)
    return result

LiteLlm.model_dump = _safe_model_dump

MODEL = LiteLlm(model="deepseek/deepseek-chat")
