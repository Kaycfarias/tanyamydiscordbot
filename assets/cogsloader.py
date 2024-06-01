import os
import traceback


async def cogsLoader(bot):
    # Diretorio contendo os componentes(comandos e eventos) do BOT
    dir = os.listdir("./components/")
    print("└─» Components/")
    for d in dir:
        if dir.index(d) < len(dir) - 1:
            print(f"    │ » {d}/")
        else:
            print(f"    └─» {d}/")
        # Loop responsavel por iterar cada componente
        subdir = os.listdir(f"./components/{d}")
        for component in subdir:
            if component.endswith(".py"):
                try:
                    # carrega o atual componente
                    await bot.load_extension(
                        f"components.{d}.{component[:-3]}"
                    )
                    if subdir.index(component) < len(subdir) - 2:
                        if dir.index(d) < len(dir) - 1:
                            print(f"    │   │ » {component}")
                        else:
                            print(f"        │ » {component}")

                    else:

                        if dir.index(d) < len(dir) - 1:
                            print(f"    │   └─» {component}")
                        else:
                            print(f"        └─» {component}")

                except Exception:
                    print(f"Falha ao carregar: {component}")
                    traceback.print_exc()

    return True
