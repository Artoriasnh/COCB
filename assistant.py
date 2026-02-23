from typing import Dict, List, Optional
import ollama

DEFAULT_MODEL = "qwen3-coder:30b"

SYSTEM_PROMPT = """你是一个资深Python工程师，擅长调试与重构。
你会收到多个项目文件内容和用户问题描述。

必须严格按格式输出：

[SUMMARY]
一句话总结你理解的问题

[PATCH]
# file: <path>
```python
<该文件的完整新内容>
如果修改多个文件，重复多个 # file 块。

[NOTES]

最多6条，说明修改原因
"""

class OfflineAssistant:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        num_ctx: int = 8192,
        temperature: float = 0.15,
        top_p: Optional[float] = None,
    ):
        self.model = model
        self.num_ctx = num_ctx
        self.temperature = temperature
        self.top_p = top_p

        self.messages: List[Dict[str, str]] = [ {"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})

        options = {
            "num_ctx": self.num_ctx,
            "temperature": self.temperature,
        }
        if self.top_p is not None:
            options["top_p"] = self.top_p

        resp = ollama.chat(
            model=self.model,
            messages=self.messages,
            options=options,
        )

        answer = resp["message"]["content"]
        self.messages.append({"role": "assistant", "content": answer})
        return answer