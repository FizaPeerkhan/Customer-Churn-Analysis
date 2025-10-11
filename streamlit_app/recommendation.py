# recommendation.py
def recommend_offer(segment, churn_prob, subscription_type):
    """
    Generate a basic recommendation based on churn probability, customer segment, and subscription type.
    """

    # Ensure numeric probability
    if isinstance(churn_prob, (list, tuple)):
        churn_prob = churn_prob[0]
    if isinstance(churn_prob, str):
        churn_prob = float(churn_prob)

    recommendation = ""

    # Rule-based recommendations
    if churn_prob > 70:
        if subscription_type.lower() == "basic":
            recommendation = "🎁 Offer a 30% discount on Premium upgrade to retain the customer."
        elif subscription_type.lower() == "premium":
            recommendation = "💎 Provide personalized content suggestions and loyalty rewards."
        else:
            recommendation = "🪄 Send retention offer email with special discounts."
    elif 40 < churn_prob <= 70:
        if str(segment).lower() == "power":
            recommendation = "🚀 Give early access to new features or exclusive add-ons."
        else:
            recommendation = "😊 Send gentle reminders or appreciation messages to engage."
    else:
        recommendation = "✅ Continue current plan and maintain engagement with occasional perks."

    return recommendation  # 👈 only return the string now
