"""
Add billing table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
		CREATE TABLE billing(
			id UUID PRIMARY KEY,
			appointment_id UUID NOT NULL,
			total_price NUMERIC NOT NULL
		)
	""")
]
