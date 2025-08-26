import os
import openai
from dotenv import load_dotenv
from prompt_templates import prompt_templates


class CodeReviewer:
    MODEL_PRICING = {
        "gpt-5-mini": {
            "input_per_million": 0.25,   # USD
            "output_per_million": 2.00   # USD
        }
    }

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_version = os.getenv("OPENAI_MODEL_VERSION")

        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

    def format_prompt(self, code: str, language_choice: str, tone_choice: str) -> str:
        tone_segment = f'Use a {tone_choice} tone:'
        code_segment = f'Be constructive. Do not rewrite the whole code. Code: \n {code}'

        match language_choice:
            case 'Python':
                language_segment = prompt_templates['python']
            case 'PHP':
                language_segment = prompt_templates['php']
            case 'Javascript':
                language_segment = prompt_templates['javascript']
            case 'Java':
                language_segment = prompt_templates['java']
            case 'C':
                language_segment = prompt_templates['c']
            case 'C#':
                language_segment = prompt_templates['c_sharp']
            case _:
                raise ValueError(f"Unsupported language: {language_choice}")

        prompt = language_segment + tone_segment + code_segment
        print(prompt)
        return prompt

    def get_code_feedback(self, code: str, language_choice: str, tone_choice: str) -> dict:
        if not self.model_version:
            raise EnvironmentError("OPENAI_MODEL_VERSION not set in environment variables.")

        prompt = self.format_prompt(code, language_choice, tone_choice)

        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[{"role": "user", "content": prompt}]
        )

        feedback = response.choices[0].message["content"]
        usage = response.usage

        pricing = self.MODEL_PRICING.get(self.model_version)
        if not pricing:
            raise ValueError(f"Pricing for model '{self.model_version}' is not defined.")

        cost_usd = (
            (usage.prompt_tokens / 1_000_000) * pricing["input_per_million"] +
            (usage.completion_tokens / 1_000_000) * pricing["output_per_million"]
        )

        return {
            "feedback": feedback,
            "tokens_prompt": usage.prompt_tokens,
            "tokens_completion": usage.completion_tokens,
            "tokens_total": usage.total_tokens,
            "cost_usd": round(cost_usd, 4),
        }
