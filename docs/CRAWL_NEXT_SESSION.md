# Creatio Crawl - Next Session Requirements

## Status: V7.X DOCUMENTATION COMPLETE
**Last Updated:** 2026-01-15
**Previous Sessions:**
- v8.x main crawl: 5,574 pages
- v7.x full documentation: 626 pages (523K words)

---

## Outstanding Crawl Targets

### 1. Authenticated Resources (Community) - COMPLETE ✅

**URL:** https://community.creatio.com + https://academy.creatio.com

**Content Types:**
- E-learning modules
- Training materials
- Certification resources
- Q&A forums
- Best practices articles
- Community ideas/feedback

**Status (2026-01-15): COMPLETE**
- ✅ Academy SSO login working (profile.creatio.com centralized auth)
- ✅ Community SSO working (shared session)
- ✅ 358 pages via Playwright-only (237K words)
- ✅ 558 pages via Hybrid crawler (360K words)

**Scripts:**
- `scripts/crawlers/authenticated_crawl.py` - Playwright-only
- `scripts/crawlers/authenticated_hybrid_crawl.py` - Playwright + Firecrawl

**Output:**
- `./creatio-docs-authenticated/` (358 pages, 237K words)
- `./creatio-docs-authenticated-hybrid/` (558 pages, 360K words)

**Credentials Used:**
- Email: `amagown@interweave.biz`
- Password: `k1AOF6my!`

**Key Fix:** Login detection was checking for "login" in URL, but successful auth redirects to `academy.creatio.com/?login=TOKEN`. Fixed to check for profile.creatio.com/user/login absence instead.

---

### 2. Version 7 Documentation (Legacy) - COMPLETE ✅

**URL:** https://old-academy.creatio.com/documents/

**Status:** ✅ Full v7.x documentation crawled (626 pages, 523K words)

**Completed (2026-01-15):**
| Section | Pages |
|---------|-------|
| development-sdk | 209 |
| studio | 91 |
| sales-team | 91 |
| sales-enterprise | 83 |
| service-enterprise | 80 |
| marketing | 46 |
| mobile | 24 |
| marketplace-apps | 1 |
| bpms | 1 |
| **TOTAL** | **626** |

**Output:** `./creatio-docs-v7/` (7.8MB markdown)
**Scripts:** `scripts/crawlers/legacy_docs_hybrid.py`

**Key learning:** User docs require `/last/` URL pattern for proper link discovery

---

### 3. Specific Content Areas to Target

| Area | URL Pattern | Priority |
|------|-------------|----------|
| E-learning | `/training/`, `/courses/` | High |
| Certification | `/certification/` | High |
| Training paths | `/learning-paths/` | Medium |
| Webinars | `/webinars/` | Low |
| Case studies | `/case-studies/` | Low |

---

## Completed in Previous Sessions

| Source | Pages | Words | Notes |
|--------|-------|-------|-------|
| Main Crawl (v8.x) | 4,985 | - | 18,691 images, 10,540 code examples |
| Supplementary (Playwright) | 304 | - | Additional v8.x |
| **v7.x Full Documentation** | **626** | **523,189** | Legacy docs (2026-01-15) |
| Training/E-learning (public) | 46 | 7,780 | Course descriptions |
| **Authenticated (PW-only)** | **358** | **237,414** | E-learning, training, cert, community |
| **Authenticated (Hybrid)** | **558** | **360,017** | Same targets, deeper crawl |
| **TOTAL** | **~6,877** | **1.13M+** | - |

**Output Directories:**
- `./creatio-docs-full/` - Main v8.x corpus (4,985 pages)
- `./creatio-docs-supplementary/` - Additional v8.x content (304 pages)
- `./creatio-docs-v7/` - Complete v7.x documentation (626 pages, 7.8MB)
- `./creatio-docs-training/` - Training/certification listings (46 pages)
- `./creatio-docs-authenticated/` - Authenticated content PW-only (358 pages)
- `./creatio-docs-authenticated-hybrid/` - Authenticated content Hybrid (558 pages)

---

## Implementation Plan for Next Session

### Phase 1: Authenticated Crawl
1. Create authenticated Playwright session with provided credentials
2. Crawl Community forums, E-learning, Training, Certification
3. Extract course materials, quizzes, certification paths

### Phase 2: Legacy Documentation (v7.x)
1. Map all v7.x documentation URLs
2. Crawl with Playwright (handles SPA navigation)
3. Cross-reference with v8.x for migration mapping

### Phase 3: Consolidation
1. Merge all content into unified corpus
2. Create topic index
3. Build training dataset structure

---

## Scripts Available

| Purpose | Script |
|---------|--------|
| Main overnight crawl | `scripts/crawlers/overnight_crawl.py` |
| Supplementary crawl | `scripts/crawlers/supplementary_crawl.py` |
| Crawler v2 (full featured) | `scripts/crawlers/creatio_academy_crawler_v2.py` |
| **v7.x Hybrid (Playwright+Firecrawl)** | `scripts/crawlers/legacy_docs_hybrid.py` |
| **v7.x Firecrawl only** | `scripts/crawlers/legacy_docs_firecrawl.py` |

---

## Notes

- Community content requires authentication - will need to implement session-based crawling
- v7.x docs use different URL structure than v8.x
- Consider rate limiting for authenticated endpoints
- May need to handle CAPTCHA or anti-bot measures on Community
