# Data Enrichment Log

**Project:** Forecasting Financial Inclusion in Ethiopia  
**Submission:** Week 11 Interim - Task 1 and Task 2  
**Collected by:** Mariamawit Alemu  
**Collection date:** 2026-07-19

## Summary

Eight records were added to the 57-record starter dataset, producing 65 total records:

- 5 observations that complete required Access and Usage analyses
- 1 policy event that was not in the starter event catalog
- 2 impact links connecting the new event to Access and Usage indicators

The additions preserve the unified-schema rule: observations and impact links have a `pillar`, while the event remains pillar-neutral.

## Added Records

### REC_0034 - Account ownership, 2011

- **record_type:** observation
- **pillar:** ACCESS
- **source_url:** https://www.worldbank.org/en/publication/globalfindex
- **original_text:** Ethiopia account ownership in 2011: 14%.
- **confidence:** high
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Completes the official 2011, 2014, 2017, 2021, and 2024 trajectory required for growth-rate and slowdown analysis.

### REC_0035 - Made or received a digital payment, 2024

- **record_type:** observation
- **pillar:** USAGE
- **source_url:** https://www.worldbank.org/en/publication/globalfindex
- **original_text:** Made or received a digital payment: approximately 35% in 2024.
- **confidence:** medium
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Adds the primary Global Findex Usage outcome. The value is approximate in the challenge brief, so confidence is set to medium.

### REC_0036 - Used an account to receive wages, 2024

- **record_type:** observation
- **pillar:** USAGE
- **source_url:** https://www.worldbank.org/en/publication/globalfindex
- **original_text:** Used an account to receive wages: approximately 15% in 2024.
- **confidence:** medium
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Adds a specific payment use case and helps distinguish account ownership from meaningful account use.

### REC_0037 - Registered mobile money accounts, 2024

- **record_type:** observation
- **pillar:** ACCESS
- **source_url:** https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/
- **original_text:** Mobile money accounts exceeded 128.5 million by December 31, 2024.
- **confidence:** high
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Adds a supply-side access measure that helps explain why account registrations can grow much faster than unique-adult ownership measured by Findex.

### REC_0038 - Active mobile money account share

- **record_type:** observation
- **pillar:** USAGE
- **source_url:** https://nbe.gov.et/ndps/
- **original_text:** Only 15% of accounts and 25% of agents are active.
- **confidence:** medium
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Supports registered-versus-active analysis. This is a system-wide strategy estimate and is not directly comparable with M-Pesa's provider-specific 90-day active-user rate.

### EVT_0011 - National Digital Payments Strategy Phase Two launch

- **record_type:** event
- **category:** policy
- **pillar:** intentionally blank
- **source_url:** https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/
- **original_text:** The National Bank of Ethiopia announced Phase Two on March 28, 2025.
- **confidence:** high
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** Adds a major policy intervention focused on deeper usage, interoperability, digital ID integration, merchant acceptance, women, and rural populations.

### IMP_0015 - NDPS Phase Two to digital-payment adoption

- **record_type:** impact_link
- **parent_id:** EVT_0011
- **pillar:** USAGE
- **related_indicator:** USG_DIGITAL_PAYMENT
- **source_url:** https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/
- **original_text:** Phase Two focuses on deepening digital-payment usage and merchant acceptance.
- **confidence:** medium
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** An explicit modeling hypothesis: enabling relationship, increase direction, medium magnitude, 10% assumed effect, and 12-month lag. It is not treated as an observed causal estimate.

### IMP_0016 - NDPS Phase Two to account ownership

- **record_type:** impact_link
- **parent_id:** EVT_0011
- **pillar:** ACCESS
- **related_indicator:** ACC_OWNERSHIP
- **source_url:** https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/
- **original_text:** Phase Two aims to expand inclusive digital financial services nationwide.
- **confidence:** medium
- **collected_by:** Mariamawit_Alemu
- **collection_date:** 2026-07-19
- **notes:** A conservative enabling hypothesis with a 5% assumed effect and 18-month lag. The longer lag reflects onboarding, identity, trust, and behavior-change requirements.

## Reproducibility

Rebuild the enriched file from raw data and the code-defined additions:

```bash
python scripts/build_enriched_data.py
```

This creates:

- `data/processed/enrichment_records.csv`
- `data/processed/ethiopia_fi_enriched.csv`
