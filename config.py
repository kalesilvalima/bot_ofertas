"""
Módulo de gerenciamento de configuração.
Gerencia termos de busca, grupos monitorados e outras configurações.
"""
import json
import os
from typing import List, Set, Optional


CONFIG_FILE = "config.json"


def load_config() -> dict:
    """Carrega a configuração do arquivo JSON."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return get_default_config()
    return get_default_config()


def get_default_config() -> dict:
    """Retorna configuração padrão."""
    return {
        "search_terms": [],
        "monitored_groups": [],
        "user_id": None
    }


def save_config(config: dict) -> None:
    """Salva a configuração no arquivo JSON."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def add_search_term(term: str) -> bool:
    """Adiciona um termo de busca à lista."""
    config = load_config()
    terms = [t.lower() for t in config.get("search_terms", [])]
    term_lower = term.lower().strip()
    
    if term_lower and term_lower not in terms:
        config.setdefault("search_terms", []).append(term_lower)
        save_config(config)
        return True
    return False


def remove_search_term(term: str) -> bool:
    """Remove um termo de busca da lista."""
    config = load_config()
    terms = config.get("search_terms", [])
    term_lower = term.lower().strip()
    
    if term_lower in terms:
        terms.remove(term_lower)
        config["search_terms"] = terms
        save_config(config)
        return True
    return False


def get_search_terms() -> List[str]:
    """Retorna lista de termos de busca."""
    config = load_config()
    return config.get("search_terms", [])


def add_monitored_group(group_id: int, group_title: str = "") -> bool:
    """Adiciona um grupo à lista de monitorados."""
    config = load_config()
    groups = config.get("monitored_groups", [])
    
    # Verifica se o grupo já está na lista
    group_ids = [g["id"] for g in groups]
    if group_id not in group_ids:
        groups.append({
            "id": group_id,
            "title": group_title
        })
        config["monitored_groups"] = groups
        save_config(config)
        return True
    return False


def remove_monitored_group(group_id: int) -> bool:
    """Remove um grupo da lista de monitorados."""
    config = load_config()
    groups = config.get("monitored_groups", [])
    
    original_count = len(groups)
    config["monitored_groups"] = [g for g in groups if g["id"] != group_id]
    
    if len(config["monitored_groups"]) < original_count:
        save_config(config)
        return True
    return False


def get_monitored_groups() -> List[dict]:
    """Retorna lista de grupos monitorados."""
    config = load_config()
    return config.get("monitored_groups", [])


def get_monitored_group_ids() -> Set[int]:
    """Retorna set de IDs dos grupos monitorados."""
    groups = get_monitored_groups()
    return {g["id"] for g in groups}


def set_user_id(user_id: int) -> None:
    """Define o ID do usuário (destino das notificações)."""
    config = load_config()
    config["user_id"] = user_id
    save_config(config)


def get_user_id() -> Optional[int]:
    """Retorna o ID do usuário."""
    config = load_config()
    return config.get("user_id")

