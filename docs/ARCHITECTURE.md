# Architecture Decision Document

## System Overview

eGov MCP is an AI-native platform that allows Cameroonian citizens and businesses
to interact with government services through natural language.

## Architecture Diagram

┌─────────────────────────────────────────────────────┐
│                    User (FR / EN)                    │
└─────────────────────┬───────────────────────────────┘
│ Natural language
┌─────────────────────▼───────────────────────────────┐
│           React Frontend — Vercel                    │
│         (MCP Client / Chat Interface)                │
└─────────────────────┬───────────────────────────────┘
│ HTTP POST /mcp/chat
┌─────────────────────▼───────────────────────────────┐
│         FastAPI MCP Server — Render                  │
│  ┌─────────────────────────────────────────────┐    │
│  │           Groq / Llama 3.3 70B              │    │
│  │         (Tool orchestration)                │    │
│  └──────────────────┬──────────────────────────┘    │
│                     │ Tool calls                     │
│  ┌──────────────────▼──────────────────────────┐    │
│  │            5 MCP Tools                      │    │
│  │  • get_tax_calendar                         │    │
│  │  • validate_cnps_number                     │    │
│  │  • calculate_social_contributions           │    │
│  │  • search_companies                         │    │
│  │  • get_public_datasets                      │    │
│  └──────────────────┬──────────────────────────┘    │
└─────────────────────┼───────────────────────────────┘
│ HTTP
┌─────────────────────▼───────────────────────────────┐
│            Government APIs                           │
│   • data.gouv.cm (Open Data Cameroun — CKAN)        │
│   • DGI logic (CGI Cameroun)                        │
│   • CNPS logic (official rates)                     │
└─────────────────────────────────────────────────────┘

## Key Decisions

### 1. Monorepo

**Decision:** Single repository with backend/ and frontend/ directories.

**Why:** For a 12-hour assessment with one developer, a monorepo reduces
friction — one repo to submit, one CI/CD pipeline, consistent versioning.

**Tradeoffs:**
- ✅ Simple to manage and submit
- ✅ Shared CI/CD
- ❌ Would not scale well with multiple teams
- ❌ Build times increase as project grows

**At scale:** Would migrate to Turborepo or Nx for monorepo tooling,
or split into separate repos with a shared package registry.

### 2. FastAPI over Django/Flask

**Decision:** FastAPI for the MCP server.

**Why:** FastAPI is async-native (required for concurrent tool execution),
has automatic OpenAPI documentation (required by the assessment), and
Pydantic v2 integration is first-class. Django would add unnecessary
overhead for an API-only service.

### 3. Groq / Llama 3.3 over Claude / GPT-4o

**Decision:** Groq with Llama 3.3 70B as the LLM orchestrator.

**Why:** Groq offers a genuinely free tier with no credit card required,
making it accessible for this assessment. Llama 3.3 70B has strong
tool-calling capabilities.

**Tradeoffs:**
- ✅ Free, no credit card
- ✅ Fast inference (Groq LPU)
- ❌ Less reliable tool-calling than Claude Sonnet
- ❌ Requires more explicit system prompting

**Ideal choice:** Claude Sonnet 4.6 — MCP is an Anthropic protocol,
native integration, more reliable tool use. Would be the production choice.

### 4. Vercel + Render over Railway/Fly.io

**Decision:** Vercel for frontend, Render for backend.

**Why:**
- Vercel has zero-config Vite/React deployment
- Render has native Python support with free tier
- Both connect directly to GitHub for auto-deploy
- No credit card required for either

**Tradeoffs:**
- ✅ Free, fast setup
- ❌ Render free tier has cold starts (~30s)
- ❌ Not suitable for production SLAs

## Scalability Plan

### 100 users (current)
- Single Render instance (free tier)
- No caching needed
- SQLite or in-memory state

### 10,000 users
- Upgrade Render to paid tier (always-on)
- Add Redis for API response caching (TTL: 1h for tax calendar)
- Add rate limiting per user
- PostgreSQL for conversation history

### 100,000 users
- Horizontal scaling with load balancer
- Background job queue (Celery + Redis) for heavy tool calls
- CDN for frontend (already on Vercel)
- Dedicated LLM API contract with guaranteed rate limits
- Observability: Sentry + Datadog
- Database: PostgreSQL with read replicas
- Consider self-hosting Llama on dedicated GPU for cost control

## Security Considerations

- API key authentication on all MCP endpoints
- CORS restricted to known frontend domains in production
- Environment variables never committed to git
- Input validation via Pydantic on all tool parameters
- No PII stored — conversations are stateless
