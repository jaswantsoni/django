HOOKS = {}

def register_hook(name):
    def wrapper(func):
        HOOKS.setdefault(name, []).append(func)
        return func
    return wrapper

def call_hooks(name, *args, **kwargs):
    for func in HOOKS.get(name, []):
        func(*args, **kwargs)
def hook_update_streak(user):
    print(f"[HOOK] {user.username}'s new streak is {user.streak_count}")
