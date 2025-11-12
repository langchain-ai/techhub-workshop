# TechHub Document Corpus

**Location:** `data/documents/`  
**Purpose:** Unstructured content for RAG agent queries  
**Total:** 30 documents (25 product specs + 5 policies)  
**Format:** Markdown

## Overview

Product specifications, setup guides, troubleshooting, and store policies that complement the structured database. Designed for natural language retrieval.

**Key features:**
- Product names and IDs match database exactly
- Consistent structure across all documents
- Real specifications from manufacturer sources
- Policy references consistent across all documents

---

## Structure

```
data/documents/
├── products/           # 25 product documents
│   ├── TECH-LAP-001.md to TECH-LAP-005.md  (5 laptops)
│   ├── TECH-MON-006.md to TECH-MON-009.md  (4 monitors)
│   ├── TECH-KEY-010.md to TECH-KEY-015.md  (6 keyboards/mice)
│   ├── TECH-AUD-016.md to TECH-AUD-020.md  (5 audio)
│   └── TECH-ACC-021.md to TECH-ACC-025.md  (5 accessories)
│
└── policies/          # 5 policy documents
    ├── return_policy.md
    ├── warranty_guide.md
    ├── shipping_guide.md
    ├── compatibility_guide.md
    └── support_faq.md
```

---

## Product Documents (25 files)

**Naming:** `{product_id}.md` (e.g., `TECH-LAP-001.md`)

**Standard structure** (7 sections):
1. Product Overview - target audience, value proposition
2. Key Specifications - technical specs
3. Compatibility - OS, connections, works with
4. What's Included - box contents
5. Setup & Getting Started - 5-step setup
6. Common Questions - upgradability, compatibility, warranty
7. Troubleshooting - 3 common issues with solutions

**Categories:**
- **Laptops** (5): MacBook Air/Pro, Dell XPS, Lenovo ThinkPad, HP Pavilion
- **Monitors** (4): Dell UltraSharp, LG, Samsung Gaming, BenQ Designer
- **Keyboards/Mice** (6): Apple Magic, Logitech MX, Gaming, Combos
- **Audio** (5): Sony/Apple headphones, Blue Yeti mic, speakers, JBL
- **Accessories** (5): USB-C hub, laptop stand, webcam, sleeve, cables

---

## Policy Documents (5 files)

### return_policy.md
Return eligibility, windows, and process.
- Unopened: 30-day window
- Opened: 14-day window
- 15% restocking fee for opened items over $500
- Refunds in 5-7 business days

### warranty_guide.md
Warranty coverage and claims.
- 1-year manufacturer warranty on all products
- Covers defects, excludes damage
- Claims through manufacturers

### shipping_guide.md
Shipping options and timing.
- Standard (5-7 days): FREE on $50+
- Express (2-3 days): $14.99
- UPS/FedEx/USPS

### compatibility_guide.md ⭐
**Critical for multi-agent queries** - cross-product compatibility.
- Mac/PC compatibility matrix
- Monitor connections by laptop model
- USB-C vs Thunderbolt explained
- Common setup recommendations
- Adapter requirements

### support_faq.md
General support questions.
- Order tracking
- Account management
- Contact: 1-800-555-TECH, support@techhub.com
- Payment and security

---

## Usage Patterns

### Product Queries
```
"What ports does the MacBook have?" 
→ Retrieve TECH-LAP-001.md, return Key Specifications section
```

### Policy Queries
```
"What's the return policy?"
→ Retrieve return_policy.md
```

### Multi-Agent Queries
```
"Will this monitor work with my Dell laptop?"
→ DB Agent: identify customer's Dell model
→ RAG Agent: retrieve compatibility_guide.md
```

```
"Can I return the monitor I bought last month?"
→ DB Agent: find purchase date
→ RAG Agent: check return_policy.md rules
```

---

## Data Quality

**Consistency checks:**
- ✅ All 25 products have documents
- ✅ Product names/IDs match database
- ✅ Prices match database
- ✅ Policy references consistent (return windows, fees, warranty terms)
- ✅ Contact info consistent across all documents

**Key policy values** (standardized):
- 14-day return window for opened electronics
- 30-day return window for unopened items
- 15% restocking fee for opened items over $500
- 1-year manufacturer warranty
- Free shipping on orders $50+

---

## RAG Tips

1. **Document selection:** Use product_id for products, keywords ("return", "warranty") for policies
2. **Section targeting:** Product docs have predictable structure
3. **Multi-document:** Some queries need multiple sources (return eligibility = purchase date + policy rules)
4. **Compatibility guide:** Essential for setup and multi-product questions

---

## Additional Resources

**Database schema:** `../structured/SCHEMA.md`  
**Generation process:** `../data_generation/README.md`
