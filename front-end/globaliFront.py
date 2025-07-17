
SVILUPPO=True
logato = { }
if SVILUPPO:
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    target_module_dir = os.path.join(project_root, 'utilita')
    if target_module_dir not in os.sys.path:
        os.sys.path.append(target_module_dir)
    target_module_dir = os.path.join(project_root, 'img')
    if target_module_dir not in os.sys.path:
        os.sys.path.append(target_module_dir)

