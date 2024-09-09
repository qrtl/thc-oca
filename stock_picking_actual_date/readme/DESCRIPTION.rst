This module adds an actual date in both stock pickings and stock moves.
The actual date from the picking is propagated to its corresponding stock move.
If a picking doesn't specify an actual date, the stock move's actual date
will be set to the 'Effective Date'. This value is then passed to the SVL's journal entry
accounting date.
