# Statistics Workbook Formulas

Example: `kt_ag/rpg2_service-afb.xlsx`, sheet `Auswertung`.

The workbook contains two calculated cells: the area balance and the building balance. This README documents Excel's special handling of array constants.

## Semicolon vs. Backslash

In German Excel, `;` separates function arguments. Inside `{...}` array constants, however:

- `;` creates a vertical array, for example `{"Beton";"Andere ..."}`
- `\` creates a horizontal array, for example `{"Usage A"\"Usage B"\"Usage C"}`

The RPG 2 area formula intentionally uses one vertical and one horizontal criteria array. This makes Excel evaluate all material/usage combinations as a matrix, after which `SUM` adds the complete result. If both arrays used the same direction, Excel would not cover all combinations correctly.
