# Changelog

## [1.1.0] - 2026-01-22

### Fixed
- Replaced `{self.amount}` with `{self.total_amount}` in the eSewa status check request.
- Fixes incorrect verification when tax, service charge, or delivery charge are non-zero.
- Previously passed silently because all extra charges were tested as zero, making `amount == total_amount`.
- `get_status()` method of EsewaPayment now has a default value of `False` for the dev flag.

### Notes
- This change ensures payment status validation matches the actual charged total sent to eSewa.
