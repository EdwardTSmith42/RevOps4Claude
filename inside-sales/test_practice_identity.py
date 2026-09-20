"""Regression tests for extract.py's practice-identity resolver.

Run:  python test_practice_identity.py

The resolver decides how many PRACTICES a set of company records represents, which
is one half of the locations-vs-practices pair Mel Matthews asked for on
2026-09-14. Ed Smith added the matching rule on 2026-09-20: "Be sure to check
legalname, practice name and dba when matching."

Getting it wrong is silent and expensive in both directions, so every case below
is a REAL pattern pulled from the live portal, not an invented one:

  * Bayou Orthodontics    - one brand, six locations, all named for the brand.
                            Must collapse to one practice.
  * Amulet Management     - a DSO whose 48 children carry a COPIED Practice Name
                            and include Williams Orthodontics (Gilbert AZ) and
                            Jensen Orthodontics (Las Cruces NM). Must stay apart.
  * NY Family Dentistry   - same copied-Practice-Name pattern, value "Avenue D
                            Dental" on five unrelated Brooklyn practices.
  * Perla Dental          - a parent record and one treating location, same brand
                            in both names. Must collapse to one practice.

The test EXECUTES the resolver's own source out of extract.py rather than copying
it, so it cannot drift from what ships.
"""
import io
import os
import re
import sys
import textwrap
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "extract.py")

_src = io.open(SRC, encoding="utf-8").read()
_start = _src.index("    NAME_SPAN_MAX")
_end = _src.index("    PRACTICE_KEY, PRACTICE_REPORT = build_practice_index")
BLOCK = textwrap.dedent(_src[_start:_end])


def load(records):
    """Execute the shipped resolver source against a stub company table."""
    ns = {"re": re, "defaultdict": defaultdict, "companies": records}
    exec(BLOCK, ns)
    return ns


def resolve(records):
    """Run the shipped resolver over a dict of {company_id: properties}."""
    return load(records)["build_practice_index"](records.keys())


def co(cid, name, pid, parent="0", legal=None, practice=None, dba=None):
    return (cid, {"name": name, "provider_unique_key": pid, "parent_provider": parent,
                  "legal_business_name": legal, "practice_name": practice,
                  "doing_business_as": dba})


CASES = [
    ("Bayou Orthodontics: one brand, 7 records, 6 named for the brand",
     dict([co("1", "Bayou Orthodontics Corporate", "20386", legal="Bayou Orthodontics"),
           co("2", "Bayou Orthodontics - Harvey", "20388", "20386", legal="Bayou Orthodontics"),
           co("3", "Bayou Orthodontics - Baton Rouge", "20389", "20386", legal="Bayou Orthodontics"),
           co("4", "Bayou Orthodontics - Lafayette", "20390", "20386", legal="Bayou Orthodontics"),
           co("5", "Bayou Orthodontics - New Orleans", "20387", "20386", legal="Bayou Orthodontics"),
           co("6", "Bayou Orthodontics - Alexandria", "21085", "20386", legal="Bayou Orthodontics"),
           co("7", "Bayou Braces - New Iberia", "20217", "20386", legal="Bayou Orthodontics")]),
     2, "the six brand-named records are one practice; Bayou Braces is not named "
        "for the brand and stays separate"),

    ("Amulet Management DSO: Practice Name copied across unrelated practices",
     dict([co("1", "Amulet Management LLC - Parent", "30358", practice="Children's Choice Dental Care Stockton"),
           co("2", "Williams Orthodontics", "30366", "30358", practice="Children's Choice Dental Care Stockton"),
           co("3", "Jensen Orthodontics", "30369", "30358", practice="Children's Choice Dental Care Stockton"),
           co("4", "Thunderbird Kids Dentistry", "30367", "30358", practice="Children's Choice Dental Care Stockton"),
           co("5", "Premier Orthodontics - Oxnard", "30364", "30358", practice="Children's Choice Dental Care Stockton")]),
     5, "a copied Practice Name is not identity, and a shared parent is one OWNER "
        "not one practice"),

    ("NY Family Dentistry: 'Avenue D Dental' copied onto five Brooklyn practices",
     dict([co("1", "New York Family Dentistry Corporate", "19793", practice="Avenue D Dental"),
           co("2", "NYFD - Avenue L", "18919", "19793", practice="Avenue D Dental"),
           co("3", "Avenue D Dental", "18921", "19793", practice="Avenue D Dental"),
           co("4", "Canarsie Family and Cosmetic Dentistry", "18922", "19793", practice="Avenue D Dental"),
           co("5", "Lincoln Family Dental", "18924", "19793", practice="Avenue D Dental")]),
     5, "same copied-name pattern; only one record is actually called Avenue D Dental"),

    ("Perla Dental: parent record plus one location, brand in both names",
     dict([co("1", "Perla Dental - Parent - 39731", "39731", legal="Perla Dental PC",
              practice="Perla Dental ", dba="Perla Dental - Parent"),
           co("2", "Perla Dental of Farmers Branch - 39738", "39738", "39731",
              legal="Perla Dental of Farmers Branch PA", practice="Perla Dental ",
              dba="Perla Dental of Farmers Branch")]),
     1, "two locations, one practice - the case Ed asked for"),

    ("Two unrelated practices stay apart",
     dict([co("1", "Perla Dental", "1", legal="Perla Dental PC"),
           co("2", "Lazar Orthodontics", "2", legal="Lazar Ortho PLLC")]),
     2, "no shared name, no join"),

    ("Same practice entered twice, one record has no Provider ID",
     dict([co("1", "Riverbend Dental Care", "500", legal="Riverbend Dental Care LLC"),
           co("2", "Riverbend Dental Care", "", legal="Riverbend Dental Care LLC")]),
     1, "name matching is what catches the pre-Provider-ID duplicate"),

    ("Category-only names are never identity",
     dict([co("1", "Family Dental Care", "10", legal="Family Dental Care"),
           co("2", "Family Dental Care", "11", legal="Family Dental Care"),
           co("3", "Family Dental Care", "12", legal="Family Dental Care")]),
     3, "every token is a category word, so the name describes an industry"),
]


def main():
    ns = load({})
    norm = ns["norm_name"]

    failures = 0
    print("normaliser")
    NORM = [("Perla Dental PC", "perla dental"),
            ("Smith & Jones Dental, LLC", "smith jones dental"),
            ("Parkway Dental Inc", "parkway dental"),
            ("Parent Orthodontics", "parent orthodontics"),
            ("Compassion Dental", "compassion dental"),
            ("Family Dental Care", ""),
            ("The Dental Office", "")]
    for raw, want in NORM:
        got = norm(raw)
        ok = got == want
        failures += not ok
        print("  %-5s %-32r -> %r%s" % ("PASS" if ok else "FAIL", raw, got,
                                        "" if ok else "  (want %r)" % want))

    print("\nresolver")
    for label, records, want, why in CASES:
        _keys, rep = resolve(records)
        ok = rep["practices"] == want
        failures += not ok
        print("  %-5s %-58s %d records -> %d practices (want %d)"
              % ("PASS" if ok else "FAIL", label, len(records), rep["practices"], want))
        print("        %s" % why)

    print("\n%s" % ("ALL CHECKS PASSED" if not failures else "%d CHECK(S) FAILED" % failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
