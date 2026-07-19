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
    "Deploy additional security personnel to Gate C — queue occupancy has reached 87%.",
    "Coordinate with metro operations to increase train frequency on Line 2; current delay is 12 minutes.",
    "Alert medical team to maintain elevated readiness — crowd density in the North Stand exceeds safe thresholds.",
    "Notify vendor managers in Sections D and E to restock beverages; stock levels are below 20%.",
    "Recommend opening overflow parking at Zone F to reduce congestion on the main approach road.",
    "Issue a public address announcement to distribute spectators evenly across all open gates.",
    "Confirm volunteer deployment at first-aid stations in Blocks 101–105 before match kick-off.",
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
