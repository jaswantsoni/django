hooks={}

def register_hook(name):
    def wrapper(name):
        name=name.capitalize()   #Parnika, string.capwords -> Parnika
        return name
    hooks[name]=wrapper
    