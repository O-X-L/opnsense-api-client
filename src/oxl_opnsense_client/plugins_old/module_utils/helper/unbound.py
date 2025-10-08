
from .validate import is_valid_domain


def validate_domain(m, domain: str) -> None:
    test_domain = domain

    if domain.find('.') == -1:
        # TLD-only will fail the domain validation
        test_domain = f'dummy.{domain}'

    if not is_valid_domain(test_domain):
        m.fail(f"Value '{domain}' is an invalid domain!")
