SCHEMA_EXPLORER_PROMPT = """
You are a database expert. Given a question, identify ALL tables whose data is needed to answer it.

## Database Schema:
{schema_description}

## Question:
"{question}"

## Important Rules:
1. Return EVERY table whose data is necessary to answer the question
2. Include tables needed for calculations (e.g., order_details for revenue)
3. Include tables needed for filtering, grouping, or joining
4. DO NOT include tables just because they might be interesting
5. Think: "If I remove this table, can I still answer the question?"

## Examples:
- "Revenue by category" → ["products", "categories", "order_details", "orders"]
- "Top customers" → ["customers", "orders"]
- "Products ordered most" → ["products", "order_details", "orders"]

## Output JSON:
{{
    "relevant_tables": ["table1", "table2", "table3"],
    "reasoning": "Brief explanation of why each table is needed"
}}

Return ONLY valid JSON.
"""
