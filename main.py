import os
from typing import List

from assistant import OfflineAssistant, DEFAULT_MODEL
from file_context import build_context_text, load_files
from patch_parser import extract_patch_files, extract_summary, PatchFile


def print_help():
    print("命令：")
    print("  load <path1> <path2> ...   加载文件或文件夹（只读 .py/.html/.txt/.md）")
    print("  ask <你的问题>             提问，例如 ask 修复函数bug并重构")
    print("  show                       预览上一次解析到的补丁（每个文件前40行）")
    print("  apply                      把上一次补丁写回本地文件（会覆盖原文件）")
    print("  clear                      清空上下文与补丁缓存")
    print("  help                       显示帮助")
    print("  exit                       退出")


def safe_write_file(path: str, content: str):
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(content)


def main():
    model = os.environ.get("OFFLINE_MODEL", DEFAULT_MODEL)
    num_ctx = int(os.environ.get("OFFLINE_NUM_CTX", "8192"))
    temperature = float(os.environ.get("OFFLINE_TEMPERATURE", "0.15"))

    bot = OfflineAssistant(model=model, num_ctx=num_ctx, temperature=temperature)

    loaded_context = ""
    last_patch_files: List[PatchFile] = []

    print("离线代码助手启动")
    print(f"模型: {model}")
    print(f"num_ctx: {num_ctx}")
    print(f"temperature: {temperature}")
    print_help()

    while True:
        raw = input("\n>>> ").strip()
        if not raw:
            continue

        if raw == "exit":
            break

        if raw == "help":
            print_help()
            continue

        if raw == "clear":
            loaded_context = ""
            last_patch_files = []
            print("已清空上下文与补丁缓存")
            continue

        if raw.startswith("load "):
            args = raw.split()[1:]
            if not args:
                print("请提供路径")
                continue

            loaded_files, _ = load_files(args)
            loaded_context = build_context_text(loaded_files)

            print(f"已加载: {len(loaded_files)} 个文件，上下文字符数约: {len(loaded_context)}")
            truncated_count = sum(1 for f in loaded_files if f.truncated)
            if truncated_count:
                print(f"注意: 有 {truncated_count} 个文件被截断。建议只 load 关键文件。")
            continue

        if raw.startswith("ask "):
            question = raw[4:].strip()
            if not question:
                print("请提供问题描述")
                continue

            prompt = f"""项目上下文如下（可能包含 TRUNCATED 截断标记）：
{loaded_context}

用户问题：
{question}

请严格按指定格式输出。"""

            answer = bot.ask(prompt)

            summary = extract_summary(answer)
            patch_files = extract_patch_files(answer)
            last_patch_files = patch_files

            print("\n===== SUMMARY =====")
            print(summary if summary else "(未解析到 SUMMARY)")

            print("\n===== PATCH FILES =====")
            if patch_files:
                for pf in patch_files:
                    print(f"- {pf.path} ({len(pf.code)} chars)")
            else:
                print("未解析到补丁。请在问题里明确要求输出 [PATCH] 并给出 # file 块。")

            print("\n===== RAW OUTPUT =====")
            print(answer)
            continue

        if raw == "show":
            if not last_patch_files:
                print("没有补丁缓存，请先 ask")
                continue
            for pf in last_patch_files:
                print("\n------------------------")
                print(f"FILE: {pf.path}")
                lines = pf.code.splitlines()
                print("\n".join(lines[:40]))
            continue

        if raw == "apply":
            if not last_patch_files:
                print("没有补丁缓存，请先 ask")
                continue

            print("将覆盖写回以下文件：")
            for pf in last_patch_files:
                print(f"- {pf.path}")

            confirm = input("输入 YES 确认写回：").strip()
            if confirm != "YES":
                print("已取消")
                continue

            for pf in last_patch_files:
                safe_write_file(pf.path, pf.code)

            print("已写回完成")
            continue

        print("未知命令，输入 help 查看")


if __name__ == "__main__":
    main()