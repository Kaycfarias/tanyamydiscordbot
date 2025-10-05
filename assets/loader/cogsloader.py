import os
import traceback
from pathlib import Path
from typing import Dict, List


class CogsLoader:
    """Carregador simples e eficiente de componentes do bot."""
    
    def __init__(self, components_dir: str = "./components"):
        self.components_dir = Path(components_dir)
        self.results: Dict[str, List[Dict]] = {}

    def _should_load_component(self, component_file: str) -> bool:
        """Verifica se o arquivo deve ser carregado."""
        return (
            component_file.endswith('.py') and
            component_file not in ['__init__.py'] and
            not component_file.startswith('_')
        )

    async def _load_single_component(self, bot, category: str, component_file: str) -> Dict:
        """Carrega um único componente."""
        component_name = component_file[:-3]  # Remove .py
        component_path = f"components.{category}.{component_name}"
        
        try:
            await bot.load_extension(component_path)
            return {"name": component_name, "status": "success"}
        except Exception as e:
            print(f"Falha ao carregar: {component_name} - {str(e)}")
            return {"name": component_name, "status": "failed", "error": str(e)}

    def _print_tree_structure(self) -> None:
        """Imprime estrutura em árvore simples e bonita."""
        print("\n🗂️  Componentes carregados:")
        
        categories = list(self.results.keys())
        for i, category in enumerate(categories):
            is_last_category = i == len(categories) - 1
            
            # Ícone da categoria
            category_icon = "📁" if category == "commands" else "⚡" if category == "events" else "📦"
            
            # Prefixo da categoria
            if is_last_category:
                print(f"   └── {category_icon} {category}")
                category_indent = "       "
            else:
                print(f"   ├── {category_icon} {category}")
                category_indent = "   │   "
            
            # Componentes da categoria
            components = self.results[category]
            for j, result in enumerate(components):
                is_last_component = j == len(components) - 1
                
                # Status emoji
                status_emoji = "✅" if result["status"] == "success" else "❌"
                
                # Conectores
                if is_last_component:
                    print(f"{category_indent}└── {status_emoji} {result['name']}.py")
                else:
                    print(f"{category_indent}├── {status_emoji} {result['name']}.py")

    async def load_components(self, bot) -> bool:
        """Carrega todos os componentes disponíveis."""
        if not self.components_dir.exists():
            print(f"❌ Diretório não encontrado: {self.components_dir}")
            return False
        
        self.results.clear()
        success_count = 0
        total_count = 0
        
        # Descobrir e carregar categorias
        try:
            categories = [
                d for d in os.listdir(self.components_dir)
                if (self.components_dir / d).is_dir() and not d.startswith(('__', '.'))
            ]
        except Exception as e:
            print(f"❌ Erro ao listar categorias: {e}")
            return False
        
        # Carregar componentes por categoria
        for category in sorted(categories):
            category_path = self.components_dir / category
            self.results[category] = []
            
            try:
                component_files = [
                    f for f in os.listdir(category_path)
                    if self._should_load_component(f)
                ]
                
                for component_file in sorted(component_files):
                    result = await self._load_single_component(bot, category, component_file)
                    self.results[category].append(result)
                    total_count += 1
                    if result["status"] == "success":
                        success_count += 1
                        
            except Exception as e:
                print(f"❌ Erro na categoria '{category}': {e}")
        
        # Exibir estrutura
        self._print_tree_structure()
        
        # Resumo simples e bonito
        if total_count > 0:
            success_rate = (success_count / total_count) * 100
            
            # Escolher emoji baseado na taxa de sucesso
            if success_rate == 100:
                summary_emoji = "🎉"
            elif success_rate >= 80:
                summary_emoji = "✅"
            elif success_rate >= 50:
                summary_emoji = "⚠️"
            else:
                summary_emoji = "❌"
                
            print(f"\n{summary_emoji} {success_count}/{total_count} componentes carregados ({success_rate:.0f}%)")
        
        return success_count > 0


# Função principal - interface simples
async def cogsLoader(bot) -> bool:
    """
    Carrega todos os componentes do bot.
    Mantém compatibilidade com versão anterior.
    """
    loader = CogsLoader()
    return await loader.load_components(bot)
