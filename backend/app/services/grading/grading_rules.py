class ProcurementGradingRules:
    """
    Configurable Procurement Center Grading Rules.
    """
    # Threshold percentages for procurement batch recommendation
    ACCEPTANCE_GRADE_A_MIN = 80.0
    CONDITIONAL_GRADE_A_MIN = 60.0

    @classmethod
    def get_recommendation(cls, grade_a_percentage: float) -> str:
        if grade_a_percentage >= cls.ACCEPTANCE_GRADE_A_MIN:
            return "ACCEPT (Grade A Batch)"
        elif grade_a_percentage >= cls.CONDITIONAL_GRADE_A_MIN:
            return "RE-INSPECT / CONDITIONAL ACCEPTANCE"
        else:
            return "REJECT (High URS Defect Ratio)"
