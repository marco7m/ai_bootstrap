from __future__ import annotations

from collections.abc import Mapping

SUPPORTED_LANGUAGES = ("en", "pt-BR")

_TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "app_intro": "This tool prepares a repository to work better with AI assistants.",
        "spec_driven_help": (
            "Spec-driven means the assistant first understands the request, writes a spec, waits for approval, "
            "creates a plan and tasks, and only then implements."
        ),
        "living_docs_help": (
            "Living docs are compact project memory: current evidence, approved targets, decisions, roadmap, and terms."
        ),
        "skills_help": "Agent Skills are reusable instructions for compatible AI coding agents.",
        "dry_run_help": "Dry run shows what would happen, but writes nothing.",
        "status_help": (
            "managed/seeded/project/composed/migrated identifies ownership; preserved protects project knowledge; "
            "conflict/migration_required blocks all writes; reset is destructive and separately confirmed."
        ),
        "project_path_placeholder": "Project path",
        "language_label": "Language",
        "project_select_label": "Recent / detected projects",
        "current_directory_button": "Use current directory",
        "home_button": "Home",
        "parent_button": "Parent",
        "refresh_projects_button": "Refresh projects",
        "preview_button": "Preview",
        "dry_run_button": "Dry Run",
        "apply_button": "Apply",
        "cancel_button": "Cancel",
        "confirm_placeholder": "Type APPLY to write",
        "preview_ready": "Preview ready. Type APPLY and press Apply to write changes.",
        "dry_run_done": "Dry run completed. No files were written.",
        "type_apply": "Type APPLY to write files.",
        "type_reset_confirmation": "Type RESET PROJECT KNOWLEDGE to confirm the seeded-knowledge reset.",
        "applied_done": (
            "Applied changes and wrote .ai-bootstrap/state.json.\n"
            "Next steps:\n"
            "1. Open your preferred AI assistant.\n"
            "2. Follow generated entry points when present: AGENTS.md, docs/INDEX.md, and .agents/skills/.\n"
            "3. For non-trivial work, respect the generated approval workflow."
        ),
        "no_projects_found": "No recent or detected projects found yet.",
        "include_skills_label": "Include .agents/skills",
        "overwrite_existing_label": "Update bootstrap-managed files / retire unchanged obsolete scaffolds",
        "reset_project_knowledge_label": "Reset seeded project knowledge (destructive)",
        "reset_confirm_placeholder": "Type RESET PROJECT KNOWLEDGE",
    },
    "pt-BR": {
        "app_intro": "Esta ferramenta prepara um repositório para trabalhar melhor com assistentes de IA.",
        "spec_driven_help": (
            "Spec-driven significa que o assistente primeiro entende o pedido, escreve uma spec, espera aprovação, "
            "cria plano e tarefas, e só depois implementa."
        ),
        "living_docs_help": "Living docs são memória compacta: evidência atual, alvos aprovados, decisões, roadmap e termos.",
        "skills_help": "Agent Skills são instruções reutilizáveis para agentes de IA compatíveis.",
        "dry_run_help": "Dry run mostra o que aconteceria, mas não escreve nada.",
        "status_help": (
            "managed/seeded/project/composed/migrated identifica ownership; preserved protege conhecimento; "
            "conflict/migration_required bloqueia toda escrita; reset é destrutivo e exige confirmação própria."
        ),
        "project_path_placeholder": "Caminho do projeto",
        "language_label": "Idioma",
        "project_select_label": "Projetos recentes / detectados",
        "current_directory_button": "Usar diretório atual",
        "home_button": "Home",
        "parent_button": "Diretório pai",
        "refresh_projects_button": "Atualizar projetos",
        "preview_button": "Prévia",
        "dry_run_button": "Simulação",
        "apply_button": "Aplicar",
        "cancel_button": "Cancelar",
        "confirm_placeholder": "Digite APPLY para escrever",
        "preview_ready": "Prévia pronta. Digite APPLY e clique em Aplicar para escrever as alterações.",
        "dry_run_done": "Dry run concluído. Nenhum arquivo foi escrito.",
        "type_apply": "Digite APPLY para escrever arquivos.",
        "type_reset_confirmation": "Digite RESET PROJECT KNOWLEDGE para confirmar o reset dos documentos seeded.",
        "applied_done": (
            "Alterações aplicadas e .ai-bootstrap/state.json escrito.\n"
            "Próximos passos:\n"
            "1. Abra seu assistente de IA preferido.\n"
            "2. Siga as entradas geradas quando existirem: AGENTS.md, docs/INDEX.md e .agents/skills/.\n"
            "3. Em trabalho não trivial, respeite o workflow de aprovação gerado."
        ),
        "no_projects_found": "Nenhum projeto recente ou detectado encontrado ainda.",
        "include_skills_label": "Incluir .agents/skills",
        "overwrite_existing_label": "Atualizar gerenciados / retirar scaffolds obsoletos intactos",
        "reset_project_knowledge_label": "Resetar conhecimento seeded do projeto (destrutivo)",
        "reset_confirm_placeholder": "Digite RESET PROJECT KNOWLEDGE",
    },
}


def detect_default_language(env: Mapping[str, str] | None = None) -> str:
    source = env or {}
    for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = source.get(key, "")
        if not value:
            continue
        normalized = value.replace("-", "_").lower()
        if normalized.startswith("pt_br") or normalized.startswith("pt"):
            return "pt-BR"
    return "en"


def t(lang: str, key: str) -> str:
    language = lang if lang in SUPPORTED_LANGUAGES else "en"
    value = _TEXTS.get(language, {}).get(key)
    if value is not None:
        return value
    fallback = _TEXTS["en"].get(key)
    if fallback is not None:
        return fallback
    return f"[missing:{key}]"
