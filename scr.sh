# 1. Crée le .gitignore d'abord pour ne pas commiter le .venv
cat > .gitignore << 'EOF'
backend/.venv/
backend/__pycache__/
backend/app/__pycache__/
backend/app/tools/__pycache__/
backend/app/schemas/__pycache__/
backend/app/core/__pycache__/
*.pyc
.env
EOF

# 2. Ajoute tout
git add .

# 3. Commit
git commit -m "feat: backend MCP server with 5 tools — Groq LLM"

# 4. Connecte au repo existant — remplace TON_USERNAME
git remote add origin https://github.com/LANDRYJACQUES237/egov-mcp.git
git branch -M main
git push -u origin main