import json
from contextlib import asynccontextmanager

from groq import AsyncGroq
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.auth import verify_api_key
from app.core.logging import setup_logging, get_logger, new_request_id
from app.schemas.models import (
    MCPResponse,
    SearchCompaniesInput, TaxCalendarInput,
    ValidateCNPSInput, SocialContributionsInput, PublicDatasetsInput,
    Employee,
)
from app.tools import (
    search_companies, get_tax_calendar,
    validate_cnps_number, calculate_social_contributions,
    get_public_datasets,
)

settings = get_settings()
setup_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("eGov MCP Server démarré avec Groq")
    yield
    logger.info("eGov MCP Server arrêté")


app = FastAPI(
    title="eGov MCP Server — Cameroun",
    description="Serveur MCP exposant des services gouvernementaux camerounais.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des tools au format OpenAI (compatible Groq)
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_companies",
            "description": "Recherche des entreprises enregistrées au Cameroun via Open Data Cameroun.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Nom ou secteur à rechercher"},
                    "region": {"type": "string", "description": "Région ex: Centre, Littoral"},
                    "limit": {"type": "integer", "description": "Nombre de résultats"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tax_calendar",
            "description": "Retourne les échéances fiscales DGI Cameroun pour une année et mois donné.",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {"type": "integer", "description": "Année ex: 2025"},
                    "month": {"type": "integer", "description": "Mois 1-12 optionnel"},
                },
                "required": ["year"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate_cnps_number",
            "description": "Vérifie le format et la région d'un matricule CNPS camerounais.",
            "parameters": {
                "type": "object",
                "properties": {
                    "matricule": {"type": "string", "description": "Ex: C1234567A"},
                },
                "required": ["matricule"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_social_contributions",
            "description": "Calcule les cotisations CNPS et IRPP pour une liste d'employés.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employees_json": {
                        "type": "string",
                        "description": "JSON string des employés ex: [{\"name\":\"Alice\",\"gross_salary\":300000}]",
                    },
                    "month": {"type": "string", "description": "Mois ex: 2025-03"},
                },
                "required": ["employees_json", "month"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_public_datasets",
            "description": "Récupère les datasets publics depuis data.gouv.cm.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "finance, education, santé..."},
                    "limit": {"type": "integer", "description": "Nombre de résultats"},
                },
            },
        },
    },
]


async def dispatch_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "search_companies":
        result = await search_companies(SearchCompaniesInput(**tool_input))

    elif tool_name == "get_tax_calendar":
        result = await get_tax_calendar(TaxCalendarInput(**tool_input))

    elif tool_name == "validate_cnps_number":
        result = await validate_cnps_number(ValidateCNPSInput(**tool_input))

    elif tool_name == "calculate_social_contributions":
        employees_raw = json.loads(tool_input.get("employees_json", "[]"))
        employees = [Employee(**e) for e in employees_raw]
        result = await calculate_social_contributions(
            SocialContributionsInput(
                employees=employees,
                month=tool_input.get("month", "2025-01"),
            )
        )

    elif tool_name == "get_public_datasets":
        result = await get_public_datasets(PublicDatasetsInput(**tool_input))

    else:
        raise ValueError(f"Tool inconnu : {tool_name}")

    return result.model_dump()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "egov-mcp-server", "llm": "groq/llama-3.3-70b-versatile"}


@app.post("/mcp/chat", dependencies=[Depends(verify_api_key)])
async def mcp_chat(body: dict):
    request_id = new_request_id()
    user_message = body.get("message", "")
    conversation_history = body.get("history", [])

    if not user_message:
        raise HTTPException(status_code=400, detail="Le champ 'message' est requis.")

    logger.info(f"mcp_chat — message: {user_message[:80]}")

    client = AsyncGroq(api_key=settings.groq_api_key)

    system_prompt = (
        "Tu es un assistant spécialisé dans les services gouvernementaux du Cameroun. "
        "Tu aides les entreprises et citoyens avec leurs obligations fiscales, sociales et administratives. "
        "Réponds en français ou en anglais selon la langue de l'utilisateur. "
        "IMPORTANT: Tu DOIS utiliser les tools disponibles pour répondre. "
        "Ne réponds JAMAIS sans appeler au moins un tool. "
        "Pour les questions fiscales, utilise get_tax_calendar. "
        "Pour les entreprises, utilise search_companies. "
        "Pour le CNPS, utilise validate_cnps_number ou calculate_social_contributions. "
        "Pour les données publiques, utilise get_public_datasets."
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Ajoute l'historique
    for msg in conversation_history:
        if isinstance(msg.get("content"), str):
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Ajoute le message actuel
    messages.append({"role": "user", "content": user_message})

    tool_calls_made = []

    # Boucle d'orchestration
    while True:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=GROQ_TOOLS,
            tool_choice="auto",
            max_tokens=2048,
        )

        msg = response.choices[0].message

        # Pas de tool call — réponse finale
        if not msg.tool_calls:
            final_text = msg.content or ""
            break

        # Ajoute la réponse assistant avec tool calls
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ],
        })

        # Exécute chaque tool
        for tc in msg.tool_calls:
            tool_name = tc.function.name
            tool_input = json.loads(tc.function.arguments)
            logger.info(f"Tool appelé : {tool_name}")

            try:
                result = await dispatch_tool(tool_name, tool_input)
                tool_calls_made.append({"tool": tool_name, "input": tool_input, "status": "success"})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
            except Exception as e:
                logger.error(f"Erreur tool {tool_name}: {e}")
                tool_calls_made.append({"tool": tool_name, "status": "error", "error": str(e)})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": f"Erreur : {str(e)}",
                })

    return {
        "request_id": request_id,
        "response": final_text,
        "tool_calls": tool_calls_made,
        "history": conversation_history + [{"role": "user", "content": user_message}],
    }


@app.post("/mcp/tool/{tool_name}", dependencies=[Depends(verify_api_key)])
async def call_tool_directly(tool_name: str, body: dict):
    request_id = new_request_id()
    logger.info(f"Appel direct tool={tool_name}")
    try:
        result = await dispatch_tool(tool_name, body)
        return MCPResponse(tool=tool_name, result=result, request_id=request_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur tool direct {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
