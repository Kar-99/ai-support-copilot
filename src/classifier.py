def detect_priority(query):
    q = query.lower()

    high_words = [
        "refund",
        "missing",
        "damaged",
        "late",
        "not delivered",
        "wrong item",
        "cancelled"
    ]

    for word in high_words:
        if word in q:
            return "High"
        
    medium_words = [
        "track",
        "delivery",
        "payment"

    ]   

    for word in medium_words:
        if word in q:
            return "Medium"
        
    return "low"    

def detect_category(query):
    q = query.lower()

    if"refund" in q:
        return "Refund"
    
    elif "cancel" in q:
        return "Cancellation"
    
    elif "delivery" in q or "track" in q:
        return "Delivery"

    elif "payment" in q:
        return "Payment"

    elif "missing" in q:
        return "Missing Item"

    return "General"

def detect_sentiment(query):
    q = query.lower()

    negative_words = [
        "angry",
        "bad",
        "late",
        "missing",
        "worst",
        "refund",
        "issue",
        "problem"
    ]

    for word in negative_words:
        if word in q:
            return "Negative"
        
        return "Neutral"
    
def escalation_needed(priority, sentiment):
    if priority == "High" and sentiment == "Negative":
        return "Yes"
    
    return "No"
                