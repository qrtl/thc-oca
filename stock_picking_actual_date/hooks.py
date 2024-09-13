# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def pre_init_hook(cr):
    cr.execute(
        """
        ALTER TABLE stock_move
        ADD COLUMN actual_date DATE;
        """
    )
    cr.execute(
        """
        ALTER TABLE stock_move_line
        ADD COLUMN actual_date DATE;
        """
    )
    cr.execute(
        """
        UPDATE stock_move
        SET actual_date = DATE(date)
        WHERE date IS NOT NULL;
        """
    )
    cr.execute(
        """
        UPDATE stock_move_line
        SET actual_date = DATE(date)
        WHERE date IS NOT NULL;
        """
    )
