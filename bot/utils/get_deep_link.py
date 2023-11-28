def get_deep_link(message_text: str):
    m = message_text.split("wl_")
    if len(m) > 1 and m[-1]:
        return m[-1]
    return None
