# src/ai_token_crusher/core/techniques/remove_pass.py
def remove_pass(text: str) -> str:
    # Remove lone 'pass' statements
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped != "pass":
            new_lines.append(line)
        # اگر خط خالی بعد از pass باشه، حذف نکن (ممکنه ساختار باشه)
        elif new_lines and new_lines[-1].strip() == "":
            new_lines.pop()  # حذف خط خالی قبلش
    return "\n".join(new_lines)