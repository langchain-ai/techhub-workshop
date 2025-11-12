# TechHub Dataset Generation

Scripts for generating the synthetic TechHub e-commerce dataset. The dataset is already generated and ready to use - you only need these scripts if you want to regenerate or modify the data.

## Dataset Overview

**What's included:**
- 50 customers (diverse profiles across Consumer, Corporate, Home Office segments)
- 25 products (laptops, monitors, keyboards, audio, accessories)
- 250 orders (2-year span with realistic patterns)
- ~440 order items (product affinity patterns)
- SQLite database (156 KB, optimized)
- 30 documents for RAG (product specs + policies)

## Quick Regeneration

To regenerate the complete dataset:

```bash
# 1. Generate customers (requires: pip install faker)
python data/data_generation/generate_customers.py

# 2. Generate orders
python data/data_generation/generate_orders.py

# 3. Generate order items
python data/data_generation/generate_order_items.py

# 4. Create SQLite database
python data/data_generation/create_database.py

# 5. Validate
python data/data_generation/validate_database.py

# 6. Build vectorstore (requires: pip install langchain-huggingface sentence-transformers)
python data/data_generation/build_vectorstore.py
```

**Total time:** ~5 minutes

**Note:** Products are manually defined in `data/structured/products.json` (edit directly to modify).

## Generation Scripts

| Script | Output | Purpose |
|--------|--------|---------|
| `generate_customers.py` | `customers.json` | 50 customer profiles with Faker |
| `generate_orders.py` | `orders.json` | 250 orders with temporal patterns |
| `generate_order_items.py` | `order_items.json` | ~440 items with product affinity |
| `create_database.py` | `techhub.db` | SQLite database with schema |
| `validate_database.py` | Validation report | Data quality checks |
| `build_vectorstore.py` | `techhub_vectorstore.pkl` | RAG embeddings |

## Key Features

**Realistic patterns:**
- Seasonal order variations (Q4 spike)
- Power law customer distribution (20% = 60% of orders)
- Product affinity (laptops with accessories, monitors with keyboards)
- Status distribution: 80% Delivered, 12% Shipped, 7% Processing, 1% Cancelled

**Reproducible:**
- Fixed random seeds (42) for consistent regeneration
- Change seeds in scripts for different variations

## Customization

Edit constants in each script:
- `NUM_CUSTOMERS`, `NUM_ORDERS` - adjust counts
- `CURRENT_DATE` - change date anchor
- `random.seed(42)` - change for different patterns

See script comments for detailed customization options.

## Data Quality

Validation checks ensure:
- Zero foreign key violations
- Correct date logic (shipped_date >= order_date)
- Order totals match line items
- Price variations within ±5%
- All queries execute in <1ms

## Additional Documentation

- **Database schema:** `../structured/SCHEMA.md`
- **Document corpus:** `../documents/DOCUMENTS_OVERVIEW.md`
- **Sample queries:** `sample_queries.sql`
