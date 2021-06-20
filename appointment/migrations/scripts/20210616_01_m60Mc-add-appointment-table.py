"""
Add appointment table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
		CREATE TABLE appointment(
			id UUID PRIMARY KEY,
			start_date TIMESTAMP NOT NULL,
			end_date TIMESTAMP,
			physician_id UUID NOT NULL,
			patient_id UUID NOT NULL,
			price NUMERIC NOT NULL
		)
	""")
]
