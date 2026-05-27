# SOURCES.md

## SAP Fuel/Procurement

Real-world format researched:

- SAP S/4HANA material document and goods-movement style data.
- Practical customer exports are often flat files or custom ABAP reports, not clean public APIs.

What I learned:

- SAP rows usually include plant, posting date, document number, material/fuel description, quantity, and unit.
- Headers may be technical, localized, or customer-specific.
- Quantity and unit must be interpreted together.

Sample data:

- `sample_data/sap_fuel_flat_file.csv`
- German-style fields: `Werk`, `Buchungsdatum`, `Material Document`, `Kraftstoff`, `Menge`, `Einheit`
- Includes valid diesel rows, invalid date rows, negative quantity, and unit variants.

What would break in real deployment:

- Custom ABAP reports may rename columns.
- Plant/material master data is needed for richer categorization.
- Movement types change operational meaning.
- Live SAP integration needs credentials, idempotency, and tenant-specific mappings.

## Utility Electricity

Real-world format researched:

- Utility portal CSV usage exports and Green Button-style consumption data.

What I learned:

- kWh is the core unit, but billing periods and interval periods vary.
- Meter ID and account ID are critical for traceability.
- Utility exports can include tariffs/rate classes that are useful but not enough for final emissions.

Sample data:

- `sample_data/utility_portal_export.csv`
- Fields include account, meter ID, billing start/end, usage kWh, unit, tariff.
- Includes missing meter ID, impossible date range, and extreme usage.

What would break in real deployment:

- Green Button XML needs a dedicated parser.
- Interval data can be large.
- PDF bills require OCR/template extraction.
- Demand charges, time-of-use, and taxes are out of scope.

## Corporate Travel

Real-world format researched:

- SAP Concur and Navan-style corporate travel/expense exports.

What I learned:

- Travel data is category-rich and often configurable per company.
- Flights, hotels, and ground transport normalize differently.
- Airport codes are common and useful when distance is missing.

Sample data:

- `sample_data/travel_platform_export.csv`
- Fields include trip ID, category, trip date, airport pair, distance, nights, and unit.
- Includes flight, hotel, and ground examples plus invalid airport-code cases.

What would break in real deployment:

- Complete airport distance lookup is needed.
- Multi-leg trips, cabin class, rail, taxi, and ride-hailing need richer models.
- Travel APIs require OAuth and tenant-specific expense permissions.
- Client-specific expense categories need mapping management.
