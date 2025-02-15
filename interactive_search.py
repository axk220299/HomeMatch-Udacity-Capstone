def get_user_preferences():
    print("\n=== Welcome to HomeMatch! ===")
    print("Please tell us about your dream home:")
    
    preferences = {}
    
    preferences["budget"] = input("\nWhat's your budget? (e.g., $500,000): ")
    preferences["bedrooms"] = input("How many bedrooms do you need? (e.g., 3): ")
    preferences["location"] = input("Preferred location/neighborhood type? (e.g., suburban, urban): ")
    preferences["style"] = input("What style of home do you prefer? (e.g., modern, traditional): ")
    preferences["must_have"] = input("Any must-have features? (e.g., garage, pool): ")
    preferences["additional"] = input("Any additional preferences? (e.g., quiet neighborhood, near schools): ")
    
    # Combine all preferences into a natural language description
    pref_text = f"""
    I'm looking for a {preferences['style']} home with {preferences['bedrooms']} bedrooms.
    My budget is around {preferences['budget']}.
    I prefer a {preferences['location']} location.
    Must have: {preferences['must_have']}.
    Additional preferences: {preferences['additional']}.
    """
    
    return pref_text