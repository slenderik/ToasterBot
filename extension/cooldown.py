from time import time

cooldowns = {}


async def cooldown(user_id: int, action: str) -> int | None:
    """"Вернуть время на кулдаун."""
    global cooldowns
    cooldown_ = cooldowns.get(f"{user_id}-{action}", None)
    print(cooldown_)
    if cooldown_ is None:
        return None

    elif cooldown_ <= round(time()):
        cooldowns.pop(f"{user_id}-{action}")
        return None

    elif cooldown_ > round(time()):
        return cooldowns[f"{user_id}-{action}"] - round(time())


async def add_cooldown(user_id: int, action: str, add_time: int = 30):
    """Добавить в кулдауны время когда участник сможет использовать команду снова."""
    global cooldowns
    cooldowns_time = {f"{user_id}-{action}": round(time()) + add_time}
    cooldowns.update(cooldowns_time)

