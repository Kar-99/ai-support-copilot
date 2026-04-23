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
        "worst",
        "angry",
        "fraud"
    ]

    medium_words = [
        "track",
        "delivery",
        "delay",
        "payment",
        "when"
    ]

    for word in high_words:
        if word in q:
            return "High"
        
    
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
        "missing",
        "late",
        "angry",
        "worst",
        "bad",
        "problem",
        "issue",
        "refund not received",
        "damaged"
    ]

    positive_words = [
        "thanks",
        "good","great"
    ]


    for word in negative_words:
        if word in q:
            return "Negative"

    for words in positive_words:
        if word in q:
            return "Positive"
            
        return "Neutral"
    
def escalation_needed(priority, sentiment):
    if priority == "High" and sentiment == "Negative":
        return "Yes"
    
    return "No"
                