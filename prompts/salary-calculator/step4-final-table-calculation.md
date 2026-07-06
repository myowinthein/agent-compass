Based on the salary data I provided and the international candidate adjustment values you estimated, calculate adjusted expected salary ranges for each country.

Only calculate countries that have BOTH:

- salary data
- international candidate adjustment data

Skip countries with missing data.

Keep the same country order as the imported salary dataset.

Definitions

- Market Midpoint = the "Realistic" value for the relevant tier, as provided in the salary dataset. Do not average, estimate, or derive it any other way.
- Safe = Market Midpoint from the Mid-size / Mainstream Local-Market tier.
- Stretch = Market Midpoint from the Premium / International / Remote-first tier.

Do not estimate new salary tiers. Use only the salary data already provided.

Calculation Rules

1. Apply the international candidate adjustment independently to both the Safe and Stretch Market Midpoints.

Adjusted Midpoint = Market Midpoint x (1 - Adjustment %)

2. Range Calculation

For each Adjusted Midpoint:

- Lower Range = Fixed x 0.95
- Upper Range = Fixed x 1.10

3. Fixed Value

Fixed = Adjusted Midpoint

4. Monthly Calculation

Monthly = Annual / 12

Show Your Work

Before producing the final table, show the calculation for each country: Market Midpoint, Adjustment % applied, and resulting Adjusted Midpoint, for both Safe and Stretch. This lets me verify the math before you finalize the table.

Formatting Rules

- After showing the calculations, output ALL countries in ONE combined table.
- Group Annual and Monthly rows together for each country.
- Use ONLY these columns:

| Country | Period | Safe (Range) | Safe (Fixed) | Stretch (Range) | Stretch (Fixed) |

Country column must include the currency code.

Examples:

- United States (USD)
- Australia (AUD)
- Germany (EUR)

Do NOT repeat currency symbols or currency codes inside salary values.

Salary values must:

- use local currency only
- contain plain formatted numbers only
- not convert to USD
- round cleanly for readability
- use consistent formatting across all countries

Recommended rounding:

- Annual: nearest 500
- Monthly: nearest 50

Each country must contain exactly two rows:

- Row 1 = Annual
- Row 2 = Monthly

Example:

Country                     Period   Safe (Range)      Safe (Fixed)  Stretch (Range)    Stretch (Fixed)
United States (USD)         Annual   130,000-150,000   140,000       160,000-190,000    175,000
                             Monthly  10,800-12,500     11,700        13,300-15,800      14,600

After the table, output:

Summary

- Countries calculated: X
- Countries skipped: Y

If any countries are skipped, list them with the reason.

Do not perform any additional analysis, ranking, recommendations, or commentary.
