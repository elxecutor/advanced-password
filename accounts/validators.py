from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .advanced_password_checker import evaluate_password_strength

class AdvancedPasswordValidator:
    """
    A custom password validator that uses an advanced password checker.
    """
    def __init__(self, min_entropy=60):
        self.min_entropy = min_entropy

    def validate(self, password, user=None):
        result = evaluate_password_strength(password)
        effective_entropy = result.get("effective_entropy", 0)
        if effective_entropy < self.min_entropy:
            feedback_text = " ".join(result.get("feedback", []))
            raise ValidationError(
                _("This password is too weak. %s" % feedback_text),
                code="password_too_weak",
            )

    def get_help_text(self):
        return _(
            "Your password must have at least %(min_entropy)d bits of effective entropy."
            % {"min_entropy": self.min_entropy}
        )
