import pytest
from engagement_engine import EngagementEngine

class TestEngagementEngine:

    # --- Initialization ---
    def test_initialization(self):
        e = EngagementEngine("user1")
        assert e.user_handle == "user1"
        assert e.score == 0.0
        assert e.verified is False

        e2 = EngagementEngine("user2", verified=True)
        assert e2.verified is True

    # --- process_interaction ---
    def test_valid_interactions(self):
        e = EngagementEngine("user")

        assert e.process_interaction("like", 2)
        assert e.score == 2

        assert e.process_interaction("comment", 1)
        assert e.score == 7  # +5

        assert e.process_interaction("share", 3)
        assert e.score == 37  # +30

    def test_verified_multiplier(self):
        e = EngagementEngine("user", verified=True)
        e.process_interaction("like", 2)
        assert e.score == 3.0

    def test_invalid_interaction(self):
        e = EngagementEngine("user")
        assert not e.process_interaction("view", 1)
        assert e.score == 0.0

    def test_negative_interaction_count(self):
        e = EngagementEngine("user")
        with pytest.raises(ValueError):
            e.process_interaction("like", -1)

    def test_zero_count(self):
        e = EngagementEngine("user")
        assert e.process_interaction("like", 0)
        assert e.score == 0.0

    # --- get_tier ---
    @pytest.mark.parametrize("score,expected", [
        (0, "Newbie"),
        (99.9, "Newbie"),
        (100, "Influencer"),
        (1000, "Influencer"),
        (1000.1, "Icon"),
    ])
    def test_get_tier(self, score, expected):
        e = EngagementEngine("user")
        e.score = score
        assert e.get_tier() == expected

    # --- apply_penalty ---
    def test_apply_penalty_basic(self):
        e = EngagementEngine("user")
        e.score = 100
        e.apply_penalty(1)
        assert e.score == 80

    def test_apply_penalty_multiple(self):
        e = EngagementEngine("user")
        e.score = 100
        e.apply_penalty(2)
        assert e.score == 60

    def test_penalty_caps_at_zero(self):
        e = EngagementEngine("user")
        e.score = 50
        e.apply_penalty(10)
        assert e.score == 0.0

    def test_verified_removed_on_high_reports(self):
        e = EngagementEngine("user", verified=True)
        e.score = 100
        e.apply_penalty(11)
        assert e.verified is False

    def test_verified_not_removed(self):
        e = EngagementEngine("user", verified=True)
        e.apply_penalty(10)
        assert e.verified is True

    def test_negative_report_count(self):
        e = EngagementEngine("user")
        with pytest.raises(ValueError):
            e.apply_penalty(-1)

    # --- integration ---
    def test_full_flow(self):
        e = EngagementEngine("user", verified=True)

        e.process_interaction("like", 10)    # 15
        e.process_interaction("share", 5)    # 75
        assert e.score == 90
        assert e.get_tier() == "Newbie"

        e.process_interaction("comment", 2)  # +15
        assert e.score == 105
        assert e.get_tier() == "Influencer"

        e.apply_penalty(1)  # -20%
        assert e.score == 84