# SOURCES.md

## SAP Fuel and Procurement

Researched format:

- SAP S/4HANA material-document style data, represented in the prototype as a CSV flat-file export.

References:

- [SAP Help Portal: Read Material Documents](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/eb2a39dd0c124fed8252f684002d55e1/78f5a8461d554cc38b3af2d07d6f9c8e.html)
- [SAP Help Portal: Material Document API operations](https://help.sap.com/docs/SAP_S4HANA_CLOUD/3f57e7df4a114edabffe8b2d581a59ed/1aef4e402acd4c8b8ec2ea2bfda7715b.html)

What I learned:

- Material document APIs/data commonly involve posting dates, material document identifiers, plants/storage locations, quantities, and units.
- SAP data often uses compact field names or localized/custom report headers.
- Quantity and unit must be treated together.

Sample data shape:

`sample_data/sap_fuel_flat_file.csv` includes:

- German headers: `Werk`, `Buchungsdatum`, `Kraftstoff`, `Menge`, `Einheit`
- plant codes
- material document references
- mixed units: `L`, `ltr`, `therm`
- negative and invalid-date rows

What would break in real deployment:

- Plant codes need a master-data lookup.
- SAP movement types and material master data affect meaning.
- Custom ABAP reports may rename or omit fields.
- Live SAP integration would need credentials, OData/BAPI decisions, and idempotency.

## Utility Electricity

Researched format:

- Utility portal or Green Button-style electricity usage export.

References:

- [Green Button FAQ](https://green-button.github.io/faq/)
- [Green Button Learn](https://green-button.github.io/learn/)
- [U.S. Energy Information Administration: Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php)
- [U.S. Department of Energy: Electric meters](https://www.energy.gov/energysaver/electric-meters)

What I learned:

- Electricity usage is commonly measured in kWh.
- Billing periods are time intervals and may not align to calendar months.
- Utility data may include meter identifiers, usage values, tariff/rate context, and interval or monthly periods.

Sample data shape:

`sample_data/utility_portal_export.csv` includes:

- account number
- meter ID
- billing start and billing end
- kWh
- tariff
- missing meter ID
- impossible billing period
- extreme electricity usage

What would break in real deployment:

- Interval data can be much larger than monthly billing data.
- Tariffs may include demand charges, tiering, taxes, and time-of-use periods.
- Green Button XML requires a dedicated XML parser rather than this CSV parser.
- PDF bills need extraction confidence and manual validation.

## Corporate Travel

Researched format:

- Corporate travel/expense platform export inspired by SAP Concur and Navan-style workflows.

References:

- [SAP Concur Developer Center: Expense Configuration v4](https://preview.developer.concur.com/api-reference/expense/expense-config/v4.expense.config.html)
- [SAP Concur Developer Center: Expense Entry Attendee v3](https://preview.developer.concur.com/api-reference/expense/expense-report/v3.expense-entry-attendee.html)
- [Navan corporate travel platform](https://navan.com/)
- [Navan sustainability announcement](https://navan.com/blog/news/tripactions-introduces-business-travel-sustainability-features?deviceId=5a3fdef3-a401-43da-871a-3582a6287a0e)

What I learned:

- Travel platforms expose expense/travel categories and workflow data, but full APIs are usually enterprise credentialed.
- Flights, hotels, and ground transport should not be normalized identically.
- Flight records may provide airport pairs without reliable distance.

Sample data shape:

`sample_data/travel_platform_export.csv` includes:

- trip ID
- category: flight, hotel, ground
- trip date
- airport pairs
- distance when available
- hotel nights
- invalid airport code

What would break in real deployment:

- Distances need a complete airport and route-distance service.
- Cabin class, trip legs, layovers, rail, and ride-hailing categories change emission-factor selection.
- Travel APIs require OAuth, scopes, tenant setup, and user/expense permissions.
- Expense category names are client configurable.
