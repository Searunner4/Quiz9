class EngagementEngine:
    WEIGHTS = {
        "like": 1,
        "comment": 5,
        "share": 10,
    }

    def __init__(self, user_handle: str, verified: bool = False) -> None:
        self.user_handle = user_handle
        self.score = 0.0
        self.verified = verified

    def process_interaction(self, interaction_type: str, count: int = 1) -> bool:
        if count < 0:
            raise ValueError("Count cannot be negative")

        if interaction_type not in self.WEIGHTS:
            return False

        points = self.WEIGHTS[interaction_type] * count

        if self.verified:
            points *= 1.5

        self.score += points
        return True

    def get_tier(self) -> str:
        if self.score < 100:
            return "Newbie"
        elif self.score <= 1000:
            return "Influencer"
        else:
            return "Icon"

    def apply_penalty(self, report_count: int) -> None:
        if report_count < 0:
            raise ValueError("Report count cannot be negative")

        if report_count > 10:
            self.verified = False

        reduction = self.score * (0.20 * report_count)
        self.score = max(0.0, self.score - reduction)