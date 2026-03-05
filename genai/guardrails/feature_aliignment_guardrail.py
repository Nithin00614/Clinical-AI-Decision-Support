def validate_feature_alignment(llm_text, driver_list):

    text = llm_text.lower()

    disallowed_terms = [
        "smoking",
        "diabetes",
        "obesity",
        "cardiovascular",
        "cholesterol",
        "dyslipidemia"
    ]

    for term in disallowed_terms:
        if term in text:
            return False, term

    return True, None