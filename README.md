# eGov MCP — Cameroun

AI-native eGovernment platform for Cameroonian public services, built with MCP (Model Context Protocol).

## Live Demo

| Service | URL |
|---------|-----|
| Frontend | https://egov-mcp.vercel.app |
| Backend API | https://egov-mcp-backend.onrender.com |
| API Docs | https://egov-mcp-backend.onrender.com/docs |

## Architecture
React Frontend (MCP Client)
↓ HTTP
FastAPI MCP Server
↓ Tool Execution
Government APIs (Open Data Cameroun, DGI, CNPS logic)
↑ Orchestration
Groq / Llama 3.3 70B

## MCP Tools

| Tool | Description | Data Source |
|------|-------------|-------------|
| `get_tax_calendar` | Tax deadlines DGI Cameroun | Business logic (CGI) |
| `validate_cnps_number` | CNPS registration validation | Format + region logic |
| `calculate_social_contributions` | CNPS + IRPP calculation | Official rates |
| `search_companies` | Company search | Open Data Cameroun |
| `get_public_datasets` | Public datasets | data.gouv.cm |

## Setup Local

### Prerequisites
- Python 3.11
- Node.js 18+
- Groq API key (free at console.groq.com)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY in .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
echo "VITE_API_URL=http://127.0.0.1:8000" > .env
npm run dev
```

### Docker

```bash
docker-compose up
```

## Deployment

| Service | Platform | Config |
|---------|----------|--------|
| Backend | Render (free tier) | render.yaml |
| Frontend | Vercel (free tier) | Auto-detected Vite |

## Testing

```bash
cd backend
python -m pytest tests/ -v
# 14/14 tests passing
```

## Tech Stack

**Backend:** Python 3.11 · FastAPI · Pydantic v2 · Groq SDK · httpx
**Frontend:** React 18 · TypeScript · Tailwind CSS · Vite
**LLM:** Llama 3.3 70B via Groq
**DevOps:** Docker · GitHub Actions · Render · Vercel

## Repository Structure

egov-mcp/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI + MCP orchestration
│   │   ├── config.py        # Settings
│   │   ├── tools/           # 5 MCP tools
│   │   ├── schemas/         # Pydantic models
│   │   └── core/            # Auth + logging
│   └── tests/               # 14 unit tests
├── frontend/
│   └── src/
│       ├── components/      # React components
│       ├── hooks/           # useChat hook
│       └── types/           # TypeScript types
├── docker-compose.yml
└── .github/workflows/ci.yml
## Assumptions & Tradeoffs

**Groq instead of Anthropic/OpenAI:** Groq offers a truly free tier with no credit card required, which is practical for this assessment. The tradeoff is that Llama 3.3 has slightly less reliable tool-calling than Claude Sonnet, requiring a more explicit system prompt.

**CNPS/DGI without official API:** Neither CNPS nor DGI Cameroun expose public APIs. The tools implement real business logic (official CNPS rates, real DGI tax calendar from CGI) rather than mock data. This is disclosed transparently.

**Monorepo:** Single repository simplifies CI/CD and submission. For a production system with multiple teams, a multi-repo or Turborepo setup would be preferable.

## Future Improvements

- Add Redis caching for Open Data API responses
- Implement user authentication (JWT)
- Add support for document upload (DSF, liasse fiscale)
- Migrate to Claude Sonnet for more reliable tool orchestration
- Add WebSocket support for streaming responses
- Integrate real CNPS and DGI APIs when they become available

## AI Tools Used

- **Claude (Anthropic):** Architecture design, code generation, debugging,docs
- **Prompts used:** Available in PROMPTS.md

## License

MIT
