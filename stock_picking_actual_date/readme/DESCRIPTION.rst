This module adds an actual date in both stock pickings and stock moves.
The actual date from the picking is propagated to its corresponding stock move.
If a picking doesn't specify an actual date, the stock move's actual date
will be set to the 'Effective Date'. This value is then passed to the SVL's journal entry
accounting date.

The partner_tz module(https://github.com/OCA/partner-contact/tree/16.0/partner_tz) should be installed, if necessary, to adjust the timezone for each partner.
