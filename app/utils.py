import os

from config import BASE_SYS


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None
    
def get_all_sys():
    return os.listdir(BASE_SYS)

import os


def get_sys_structure(dir, max_depth=2):
    visited = set()

    def walk(path, depth):
        if depth > max_depth:
            return "..."

        try:
            real_path = os.path.realpath(path)
        except:
            real_path = path

        # 🔥 evita loop
        if real_path in visited:
            return "<loop>"

        visited.add(real_path)

        structure = {}

        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)

                # 🔗 symlink
                if os.path.islink(full_path):
                    target = os.path.realpath(full_path)
                    structure[entry] = f"-> {target}"

                    # opcional: seguir symlink como dir
                    if os.path.isdir(full_path):
                        structure[entry + " (resolved)"] = walk(full_path, depth + 1)

                # 📂 diretório normal
                elif os.path.isdir(full_path):
                    structure[entry] = walk(full_path, depth + 1)

                # 📄 arquivo
                else:
                    try:
                        with open(full_path) as f:
                            value = f.read().strip()

                        if len(value) > 100:
                            value = value[:100] + "..."

                        structure[entry] = value

                    except:
                        structure[entry] = "<unreadable>"

        except Exception as e:
            return f"<error: {e}>"

        return structure

    path = os.path.join(BASE_SYS, dir)
    return walk(path, 0)

def print_structure(data, prefix=""):
    if isinstance(data, dict):
        for i, (key, value) in enumerate(data.items()):
            is_last = i == len(data) - 1
            branch = "└── " if is_last else "├── "

            if isinstance(value, dict):
                print(prefix + branch + key)
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_structure(value, new_prefix)
            else:
                print(prefix + branch + f"{key}: {value}")
    else:
        print(prefix + str(data))