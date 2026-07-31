import os
import json
import httpx
from groq import Groq
import gradio as gr

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

CATEGORIES = ["ALL", "CODING", "WRITING", "DESIGN", "VIDEO", "AUDIO", "BUSINESS", "RESEARCH"]

# Domains that never contain an official product page — mirrors the
# excludeDomains filter used by AI-TOOL-HUNTER's /api/hunt deep search route.
EXCLUDED_DOMAINS = ["linkedin.com", "instagram.com", "facebook.com"]


async def hunt_ai_tool(query: str, category: str = "ALL") -> str:
    """
    Find the best AI tools for any task or use case.

    Args:
        query: What you want to do (e.g. 'generate images from text')
        category: Filter by category - ALL, CODING, WRITING,
                  DESIGN, VIDEO, AUDIO, BUSINESS, RESEARCH
    Returns:
        JSON list of matching AI tools with name, description,
        url, pricing, category, and why_it_fits
    """
    # Build search query — same "official site / pricing / features" framing
    # as the main app's deep search route, so Tavily favors product landing
    # pages over "Top 10" listicles.
    search_query = f"best {query} ai tool software pricing features official site"
    if category and category != "ALL":
        search_query += f" {category}"

    # Step 1 — Tavily Search
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            tavily_response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": search_query,
                    "search_depth": "advanced",
                    "max_results": 7,
                    "exclude_domains": EXCLUDED_DOMAINS,
                }
            )
            search_data = tavily_response.json()
            search_results = search_data.get("results", [])
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})

    # Format results for Groq
    results_text = "\n".join([
        f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nContent: {r.get('content', '')}"
        for r in search_results
    ])

    # Step 2 — Groq structures the output
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert AI tool curator.
From the search results, extract AI tools and return a JSON array.
IGNORE "Top 10" lists, blogs, or newsletters. Prefer official product
landing pages. Each item must have exactly:
{
  "name": "Tool name",
  "description": "One clear sentence",
  "url": "Official URL only",
  "pricing": "FREE | FREEMIUM | PAID",
  "category": "CODING | WRITING | DESIGN | VIDEO | AUDIO | BUSINESS | RESEARCH",
  "why_it_fits": "Why this matches the query"
}
Return ONLY valid JSON array. No markdown, no explanation."""
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\nCategory filter: {category}\n\nResults:\n{results_text}"
                }
            ],
            temperature=0.1,
            max_tokens=2000
        )
        result = completion.choices[0].message.content.strip()
        # Clean markdown if present
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        parsed = json.loads(result.strip())
        return json.dumps(parsed, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Processing failed: {str(e)}"})


def list_categories() -> str:
    """
    List all available tool categories that hunt_ai_tool accepts
    as its `category` filter.

    Returns:
        JSON array of category names.
    """
    return json.dumps(CATEGORIES)


# Gradio UI
with gr.Blocks(
    title="AI Tool Hunter MCP",
    theme=gr.themes.Base(),
    css="""
    .gradio-container { max-width: 800px; margin: auto; }
    """
) as demo:
    gr.Markdown("""
    # 🔍 AI Tool Hunter MCP
    **Find the perfect AI tool for any task — powered by live web search**
    Connect this to Cursor, VS Code, or Claude Desktop via MCP.
    """)

    with gr.Row():
        query_input = gr.Textbox(
            placeholder="e.g. generate images from text, transcribe podcasts...",
            label="What do you want to do?",
            scale=3
        )
        category_input = gr.Dropdown(
            choices=CATEGORIES,
            value="ALL",
            label="Category",
            scale=1
        )

    search_btn = gr.Button("🔍 Hunt Tools", variant="primary")
    output = gr.JSON(label="Discovered Tools")

    search_btn.click(
        fn=hunt_ai_tool,
        inputs=[query_input, category_input],
        outputs=output,
        api_name="hunt_ai_tool"
    )

    with gr.Row(visible=False):
        categories_btn = gr.Button()
        categories_output = gr.JSON()
        categories_btn.click(
            fn=list_categories,
            inputs=[],
            outputs=categories_output,
            api_name="list_categories"
        )

    gr.Markdown("""
    ---
    ### 🔌 Connect via MCP
    Add to your MCP client config:
```json
    {
      "mcpServers": {
        "ai-tool-hunter": {
          "url": "https://ai-tool-hunter-mcp.onrender.com/gradio_api/mcp/sse"
        }
      }
    }
```
    Built by **Vishal Singh** | [AI Tool Hunter](https://ai-tool-hunter-eight.vercel.app)
    """)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(mcp_server=True, server_name="0.0.0.0", server_port=port, share=False)
