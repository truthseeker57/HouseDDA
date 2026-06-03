import anthropic
import json
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are a real estate analysis assistant helping a buyer find a good deal.
Evaluate each listing using this rubric:

Days on market:
- 0-21 days: good signal
- 22-45 days: slight concern
- 46-90 days: yellow flag
- 90+ days: red flag, investigate why

Distance from target location:
- 0-0.2 miles: add 2 points
- 0.2-0.4 miles: add 1 point
- 0.4-0.6 miles: neutral

Bedrooms:
- 3 beds: meets criteria, neutral
- 2 beds: subtract 1.5 points

Bathrooms:
- 2 baths: meets criteria, neutral
- 1 baths: subtract 1.5 points

Price signals:
- Price cut: neutral, note it but don't penalize
- Price significantly below tax assessed value: flag as potential condition issue
- Good square footage per dollar: positive signal

Condition signals in flex field:
- Words like updated, new, renovated: positive
- Vague like functional layout: neutral
- Nothing specific: neutral

For each listing return a JSON array where each item contains:
- address: listing address
- rating: score from 1-10
- summary: short paragraph on what looks good and what looks off

Return only valid JSON. No extra text, no markdown, no backticks.
"""

def score_listings(listings, criteria):
    print("LISTINGS BEING SENT:", len(listings))
    
    if not listings:
        print("No listings to score.")
        return []

    user_message = f"""
Buyer criteria:
- Home type: Single family
- Bedrooms: {criteria['bedrooms_preferred']} preferred, {criteria['bedrooms_min']} minimum
- Bathrooms: {criteria['bathrooms_preferred']} preferred, {criteria['bathrooms_min']} minimum
- Max price: ${criteria['max_price']}
- Max distance: {criteria['max_distance_miles']} miles
- Condition: {criteria['condition']}

Listings to evaluate:
{json.dumps(listings, indent=2)}
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    raw = response.content[0].text

    if not raw.strip():
        raise ValueError("Claude returned an empty response")

    # strip markdown code fences if present
    if raw.strip().startswith("```"):
        raw = raw.strip()
        raw = raw.split("\n", 1)[1]  # remove first line (```json)
        raw = raw.rsplit("```", 1)[0]  # remove closing ```

    return json.loads(raw)
