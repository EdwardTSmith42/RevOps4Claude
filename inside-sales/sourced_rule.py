"""Single source of truth for how the tightened "sourced" rule is WORDED.

The rule itself lives in two places on purpose: extract.py computes it from dated
engagements (the real definition), and build.py re-derives it from the per-contact
counters in a leads.json that predates the change, so the VP can review the current
window without re-running the extract. Both of them document it with the strings
below, so the data dictionary on the page cannot say one thing while the numbers
say another.

VP decision, 2026-09-13: "yes, let's drop the 10 and explain why on the dashboard
in the data dictionary."
"""

# The four things that count as the team reaching out. Everything else is either
# something the prospect did or something we wrote to each other.
REAL_OUTREACH = ("an outbound call, an outbound email, a meeting, or an inbound "
                 "call somebody answered")

ENROLLED_PREDICATE = (
    "Enrollment date on the practice falls inside the window (minus 1 day) AND, on or before that "
    "date, someone on the team made a REAL OUTREACH TOUCH to an associated contact: " + REAL_OUTREACH
    + ". A note, a task, an inbound email we never replied to, and an inbound call nobody picked up "
      "do NOT qualify."
)

# Why the definition moved, with the counts and the one example that makes it obvious.
ENROLLED_WHY = (
    "WHY THE RULE TIGHTENED (VP decision, 2026-09-13). It used to be enough that the team had ANY "
    "activity on the record first. Fifteen contacts cleared that bar on activity that was not "
    "outreach at all: 10 on an internal staff-to-staff note ('Enrollment Spreadsheet', '@Tia Bel "
    "This is for 4 locations'), 3 on an inbound email from the prospect with no outbound email ever "
    "sent, and 2 on an inbound call nobody answered. The clearest case: Colesville Dental Center "
    "rang Gabrielle Nurod's line FIVE times, every ring 0 seconds with no call outcome logged, and "
    "we were claiming we had sourced them. Ten practices dropped out, 144 to 134; at contact grain, "
    "157 to 142. To check one by hand, open the practice in HubSpot and look at the activity on its "
    "contacts before the enrollment date: you need at least one call with Direction = Outbound, or "
    "an email with Direction = Sent, or a meeting, or an inbound call with a Call outcome set. "
    "First touch date in the lead table is UNCHANGED and still means the first activity of any "
    "kind, so a row can show a first touch that does not qualify here. "
)
