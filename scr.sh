cat > PROMPTS.md << 'EOF'
# AI Tools & Prompts Used

## Tools Used
- Claude (claude.ai) — Architecture design, code generation, debugging
- GitHub Copilot — Inline code completion

## Claude Prompts Used

### Architecture
"Quelle est la meilleure approche pour faire ce genre d'évaluation [assessment PDF]"
"Pour quoi choisir Vercel pour le frontend et Render pour le backend ?"
"Pourquoi Claude au lieu d'un autre LLM ?"

### Backend
"Commence avec la première phase — architecture et choix technologiques"
"Donne-moi le code du MCP Server FastAPI avec les 5 tools"

### Debugging
"Voici les erreurs [logs] — comment corriger ?"
"On bascule sur Groq — adapte le main.py"

## What Was AI-Generated
- Initial file structure and boilerplate
- Pydantic schema definitions
- Tool implementation templates
- Test structure

## What Was Manually Written / Verified
- CNPS rates and region prefixes (verified against cnps.cm)
- DGI tax calendar (verified against impots.cm circulaire 2024)
- IRPP tax brackets (verified against CGI Cameroun art. 69)
- SMIG value (verified against Code du Travail Cameroun 2024)
- All business logic corrections and debugging
- Deployment configuration
- This document
EOF

git add .
git commit -m "docs: add PROMPTS.md — AI usage disclosure"
git push