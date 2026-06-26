"""
Pemini Girl 9.5.2 - LLM Integration Engine
"""

import os
import torch
from typing import Dict, List, Optional, Generator
from dataclasses import dataclass
from enum import Enum
import time

class LLMProvider(Enum):
    CODE_LLAMA = "codellama"
    DEEPSEEK_CODER = "deepseek-coder"
    QWEN_CODER = "qwen-coder"
    STARCODER = "starcoder"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

@dataclass
class GenerationConfig:
    max_new_tokens: int = 512
    temperature: float = 0.2
    top_p: float = 0.95
    top_k: int = 50
    repetition_penalty: float = 1.1
    do_sample: bool = True
    stream: bool = False

@dataclass
class GenerationResult:
    text: str
    tokens_generated: int
    generation_time_ms: float
    tokens_per_second: float
    model_used: str
    finish_reason: str

class LLMIntegrationEngine:
    PROMPT_TEMPLATES = {
        "ar": {
            "generate": "اكتب كود {language} للقيام بما يلي: {prompt}\n\nالكود:",
            "analyze": "حلل الكود التالي واكتشف الأخطاء:\n\n```{language}\n{code}\n```\n\nالتحليل:",
            "explain": "اشرح الكود التالي بالعربية:\n\n```{language}\n{code}\n```\n\nالشرح:",
            "optimize": "حسن الكود التالي:\n\n```{language}\n{code}\n```\n\nالكود المحسن:",
            "complete": "أكمل الكود التالي:\n\n```{language}\n{code}\n```\n\nالإكمال:"
        },
        "zh": {
            "generate": "编写{language}代码来实现以下功能：{prompt}\n\n代码：",
            "analyze": "分析以下代码并找出错误：\n\n```{language}\n{code}\n```\n\n分析：",
            "explain": "用中文解释以下代码：\n\n```{language}\n{code}\n```\n\n解释：",
            "optimize": "优化以下代码：\n\n```{language}\n{code}\n```\n\n优化后的代码：",
            "complete": "补全以下代码：\n\n```{language}\n{code}\n```\n\n补全："
        },
        "en": {
            "generate": "Write {language} code to: {prompt}\n\nCode:",
            "analyze": "Analyze the following code and find errors:\n\n```{language}\n{code}\n```\n\nAnalysis:",
            "explain": "Explain the following code in English:\n\n```{language}\n{code}\n```\n\nExplanation:",
            "optimize": "Optimize the following code:\n\n```{language}\n{code}\n```\n\nOptimized code:",
            "complete": "Complete the following code:\n\n```{language}\n{code}\n```\n\nCompletion:"
        }
    }

    def __init__(self, model_name: str = "codellama/CodeLlama-7b-hf",
                 device: str = "auto", use_4bit: bool = True):
        self.model_name = model_name
        self.device = device
        self.use_4bit = use_4bit
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.is_loaded = False
        self.stats = {"total_generations": 0, "total_tokens": 0,
                     "avg_latency_ms": 0, "errors": 0}

    def load_model(self):
        try:
            from transformers import (AutoModelForCausalLM, AutoTokenizer,
                                    BitsAndBytesConfig, pipeline)
            print(f"Loading model: {self.model_name}")
            kwargs = {}
            if self.use_4bit:
                kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4"
                )
            if self.device == "auto":
                kwargs["device_map"] = "auto"
            else:
                kwargs["device_map"] = self.device

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, torch_dtype=torch.float16,
                trust_remote_code=True, **kwargs
            )

            self.pipeline = pipeline("text-generation", model=self.model,
                                    tokenizer=self.tokenizer, return_full_text=False)
            self.is_loaded = True
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.stats["errors"] += 1
            return False

    def generate(self, task: str, language: str = "python",
                 natural_language: str = "en", prompt: str = "",
                 code: str = "", config: Optional[GenerationConfig] = None):
        if not self.is_loaded:
            if not self.load_model():
                return GenerationResult(text="Error: Model not loaded",
                    tokens_generated=0, generation_time_ms=0,
                    tokens_per_second=0, model_used=self.model_name, finish_reason="error")

        config = config or GenerationConfig()
        template = self.PROMPT_TEMPLATES.get(natural_language,
                self.PROMPT_TEMPLATES["en"]).get(task, "{prompt}")
        formatted_prompt = template.format(language=language, prompt=prompt, code=code)

        start_time = time.time()
        try:
            outputs = self.pipeline(formatted_prompt,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature, top_p=config.top_p,
                top_k=config.top_k, repetition_penalty=config.repetition_penalty,
                do_sample=config.do_sample, return_full_text=False)

            generated_text = outputs[0]["generated_text"]
            generated_text = self._clean_output(generated_text, task)

            generation_time = (time.time() - start_time) * 1000
            tokens = len(self.tokenizer.encode(generated_text))
            tps = tokens / (generation_time / 1000) if generation_time > 0 else 0

            self.stats["total_generations"] += 1
            self.stats["total_tokens"] += tokens
            n = self.stats["total_generations"]
            self.stats["avg_latency_ms"] = (self.stats["avg_latency_ms"] * (n-1) + generation_time) / n

            return GenerationResult(text=generated_text, tokens_generated=tokens,
                generation_time_ms=generation_time, tokens_per_second=tps,
                model_used=self.model_name, finish_reason="stop")
        except Exception as e:
            self.stats["errors"] += 1
            return GenerationResult(text=f"Error: {str(e)}",
                tokens_generated=0, generation_time_ms=(time.time() - start_time) * 1000,
                tokens_per_second=0, model_used=self.model_name, finish_reason="error")

    def _clean_output(self, text: str, task: str) -> str:
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)
        stop_phrases = ["Explanation:", "Analysis:", "Notes:", "##", "---"]
        for phrase in stop_phrases:
            if phrase in text:
                text = text.split(phrase)[0]
        return text.strip()

    def get_stats(self):
        return self.stats.copy()

    def unload_model(self):
        if self.model:
            del self.model
            self.model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        self.is_loaded = False
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("Model unloaded")

class OpenAICompatibleClient:
    def __init__(self, api_key: str = None, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url
        self.client = None

    def initialize(self):
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
            return True
        except ImportError:
            print("Please install openai: pip install openai")
            return False

    def generate(self, prompt: str, model: str = "gpt-4", **kwargs):
        if not self.client:
            if not self.initialize():
                return "Error: OpenAI client not initialized"
        try:
            response = self.client.chat.completions.create(
                model=model, messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.2),
                max_tokens=kwargs.get("max_tokens", 512)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    engine = LLMIntegrationEngine()
    print("LLM Integration Engine initialized")
    print(f"Model: {engine.model_name}")
    print(f"Device: {engine.device}")
    print(f"4-bit quantization: {engine.use_4bit}")
