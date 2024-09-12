This module adds an actual date to both stock pickings and stock moves. The actual date from the picking is propagated to its corresponding stock move. If a picking doesn't specify an actual date, the stock move's actual date (which is a date field) will be computed based on the 'Effective Date' (a datetime field) and adjusted according to the active company’s partner timezone. If no company's partner timezone is defined, the current user's timezone will be used.

To ensure accurate timezone conversions, the partner_tz module (https://github.com/OCA/partner-contact/tree/16.0/partner_tz) should be installed, allowing timezones to be set for each partner. This ensures that the actual_date is correctly adjusted based on the company's partner timezone.

Once the actual_date is set, it is passed to the SVL's journal entry accounting date. The inventory manager can also change the actual date of a completed picking, and the change will propagate to the related journal entry.
