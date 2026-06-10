# AI & LLM Strategy

## Current Choice: Groq / Llama 3.3 70B

Chosen for this assessment due to zero-cost free tier.
Strong tool-calling capabilities with explicit prompting.

## Model Comparison for this Product

| Model | Quality | Cost | Latency | Tool Use | Privacy | Verdict |
|-------|---------|------|---------|----------|---------|---------|
| Claude Sonnet 4.6 | ⭐⭐⭐⭐⭐ | $$ | Fast | Native MCP | Good | Best fit |
| Claude Opus 4 | ⭐⭐⭐⭐⭐ | $$$$ | Slow | Native MCP | Good | Overkill |
| GPT-4o | ⭐⭐⭐⭐ | $$$ | Fast | Function calling | Moderate | Good alt |
| GPT-4.1 | ⭐⭐⭐⭐ | $$ | Fast | Function calling | Moderate | Good alt |
| Gemini 2.5 Flash | ⭐⭐⭐ | Free | Fast | Function calling | Google | Dev only |
| Llama 3.3 70B | ⭐⭐⭐ | Free | Very fast | Partial | Self-hostable | Current |
| Mistral Large | ⭐⭐⭐⭐ | $$ | Fast | Function calling | EU-based | GDPR fit |

## Recommended Production Strategy

### Primary: Claude Sonnet 4.6
MCP is an Anthropic protocol — Claude has native, first-class MCP support.
No adapter layer needed. Most reliable tool orchestration.
Cost: ~$0.003/request. At 10,000 requests/day = ~$30/month.

### Fallback: GPT-4.1
If Anthropic has outages, GPT-4.1 is the best alternative.
Requires a thin adapter layer to translate OpenAI function calls to MCP format.

### Cost Optimization
For simple queries (tax deadlines, CNPS validation), route to Llama 3.3 via Groq.
For complex multi-tool queries, route to Claude Sonnet.
Estimated 60% cost reduction with smart routing.

## Privacy & GDPR Considerations

This product handles sensitive financial and employment data.

**Key risks:**
- Salary data sent to LLM API (Groq/Anthropic servers)
- Conversation history stored in memory

**Mitigations:**
- Do not send raw employee names to the LLM — anonymize before tool call
- Use Mistral (EU-based) or self-hosted Llama for maximum GDPR compliance
- Implement data retention policy: conversations deleted after session
- Add privacy notice to frontend

## Self-Hosting Opportunity

For a government contract, self-hosting is likely required.
Llama 3.3 70B can run on 2x A100 GPUs (~$3/hour on cloud).
At 10,000 requests/day, self-hosting breaks even vs API at ~50,000 requests/day.
Below that threshold, managed APIs are more cost-effective.

## Compliance Notes

- Cameroonian data sovereignty: prefer servers in Africa or EU
- OHADA compliance: financial calculations must be auditable
- All tool outputs include data source attribution
