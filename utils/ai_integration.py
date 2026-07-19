"""
utils/ai_integration.py — Single AI Integration Point

This module contains the sole function through which AI recommendations
are surfaced throughout Stadium Coordinator. All RecommendationCard
components source their content from get_ai_recommendations().

To integrate Google Gemini 2.5 Flash in a future release:
  1. Add your Gemini API key to st.secrets["GEMINI_API_KEY"]
  2. Replace the return statement inside get_ai_recommendations() with
     a call to the Gemini API using the provided context dict.
  The function signature must remain unchanged.
"""

from __future__ import annotations

_PLACEHOLDER_RECOMMENDATIONS = [
    "🚨 IMMEDIATE: Deploy 4 additional security stewards to Gate C — queue occupancy at 94%, exceeding the 85% safe threshold. Estimated crowd clearance time: 8 minutes.",
    "🚌 TRANSPORT: Coordinate with metro operations to increase Line 2 frequency from 8-min to 4-min intervals. Current delay: 12 minutes affecting ~2,400 fans en route.",
    "🏥 MEDICAL: Pre-position a second paramedic team at the North Stand first-aid station. Crowd density in that section has reached 88% — heat exhaustion risk elevated.",
    "🛒 VENDOR: Alert vendor managers at Sections D & E to initiate emergency restocking. Beverage stock below 15% — estimated depletion in 22 minutes at current sales rate.",
    "🅿️ PARKING: Open overflow parking Zone F immediately. Main approach road congestion will worsen in 18 minutes as the wave of late arrivals reaches the perimeter.",
    "📢 COMMUNICATION: Issue PA announcement to distribute arriving fans across Gates A, B, and H. Gate C is at capacity — redirecting 800+ queued fans will reduce crush risk.",
    "🙋 VOLUNTEERS: Redeploy 6 volunteers from the low-density West Stand concourse to Gate C queue management and North Stand crowd guidance positions.",
]


# AI INTEGRATION POINT
def get_ai_recommendations(context: dict) -> list[str]:
    """Return a list of operational recommendation strings for the current stadium context.

    Args:
        context: Stadium context dictionary produced by build_stadium_context().
                 Contains one key per active dataset category.

    Returns:
        A non-empty list of recommendation strings. In the current release these
        are static placeholders. When Gemini is integrated, this function will
        call the Gemini API and return dynamically generated recommendations.
    """
    # Replace the return statement below with a Gemini API call when integrating AI.
    return list(_PLACEHOLDER_RECOMMENDATIONS)
