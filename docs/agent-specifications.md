# FinanceBot Agent Specifications

This document provides detailed specifications for each financial agent in the FinanceBot system, including required inputs, expected outputs, and multi-agent collaboration workflows.

---

## Table of Contents

1. [Financial Planning Agent](#1-financial-planning-agent)
2. [Tax Planning Agent](#2-tax-planning-agent)
3. [Investment Advisor Agent](#3-investment-advisor-agent)
4. [Budget Coach Agent](#4-budget-coach-agent)
5. [Financial Research Agent](#5-financial-research-agent)
6. [Financial Guru Agent](#6-financial-guru-agent)
7. [Multi-Agent Research System](#multi-agent-research-system)

---

## 1. Financial Planning Agent

### Purpose
Creates comprehensive, personalized financial plans to guide users toward their long-term financial objectives.

### Required Inputs

#### Personal Information
- Full name, age, gender
- Marital status and spouse details (if applicable)
- Number and ages of dependents
- Health status (for medical expense projections)
- Future life plans (marriage, childbirth, education, retirement timing)

#### Financial Goals
- Short-term goals (< 3 years): Emergency fund, vacation, wedding
- Medium-term goals (3-10 years): Home down payment, child's education
- Long-term goals (10+ years): Retirement, estate planning
- Goal priority ranking

#### Current Financial Situation
- **Income Sources:**
  - Monthly salary/wages
  - Bonus/commissions
  - Freelance/gig income
  - Rental income
  - Other passive income
  
- **Assets:**
  - Bank account balances
  - Investment portfolios (stocks, bonds, mutual funds)
  - Real estate holdings
  - Retirement accounts (PF, NPS, PPF)
  - Other assets
  
- **Liabilities:**
  - Home loan/mortgage details
  - Personal loans
  - Credit card debt
  - Education loans
  - Auto loans
  
- **Monthly Expenses:**
  - Housing costs
  - Utilities
  - Food and groceries
  - Transportation
  - Insurance premiums
  - Debt repayments

#### Risk Profile
- Risk tolerance (conservative/moderate/aggressive)
- Time horizon for each goal
- Financial capacity to absorb losses

#### Existing Coverage
- Life insurance policies
- Health insurance coverage
- Disability insurance
- Property insurance

### Expected Output: Comprehensive Financial Plan Report

#### Executive Summary
- Client financial snapshot
- Key goals and priorities
- Current financial health score
- Top 3 recommendations

#### Detailed Analysis

**1. Net Worth Statement**
- Total assets breakdown
- Total liabilities breakdown
- Current net worth calculation
- Net worth projection (5, 10, 20 years)

**2. Cash Flow Analysis**
- Monthly income vs. expenses
- Savings rate calculation
- Cash flow trends
- Recommendations for optimization

**3. Goal-Based Financial Roadmap**
For each goal:
- Target amount required
- Current savings toward goal
- Monthly contribution needed
- Recommended investment vehicles
- Timeline to achieve goal
- Progress tracking metrics

**4. Investment Strategy**
- Recommended asset allocation based on risk profile
- Specific investment product recommendations
- Expected returns (conservative estimates)
- Rebalancing schedule

**5. Risk Management Plan**
- Life insurance gap analysis
- Recommended coverage amount
- Specific policy recommendations
- Health insurance adequacy assessment
- Emergency fund target (typically 6-12 months expenses)

**6. Tax Optimization Suggestions**
- Tax-saving investment recommendations (80C, 80D, etc.)
- Tax-efficient withdrawal strategies
- Estimated tax liability reduction

**7. Retirement Planning**
- Retirement age target
- Post-retirement income needs
- Retirement corpus required
- Current retirement savings
- Additional monthly savings needed
- Social security/pension considerations

**8. Estate Planning Basics**
- Will and nomination recommendations
- Succession planning for assets
- Trust recommendations (if applicable)

**9. Action Steps**
- Prioritized checklist of immediate actions
- Timeline for implementation
- Follow-up schedule (6-month, annual reviews)

### Handoff to Other Agents
- **Tax Planning Agent**: Sends detailed income and deduction data for tax optimization
- **Investment Advisor Agent**: Sends risk profile and asset allocation targets
- **Budget Coach Agent**: Sends expense patterns for budget creation

---

## 2. Tax Planning Agent

### Purpose
Provides tax-saving strategies and deduction guidance to minimize tax liability while maximizing compliance.

### Required Inputs

#### Personal & Demographic Information
- Full name, PAN number
- Date of birth, age
- Marital status
- Number of dependents (children, elderly parents)
- Residential status (resident/non-resident)
- Employment status (salaried/self-employed/business owner)

#### Income Information
- **Employment Income:**
  - Form 16/salary slips
  - Basic salary, HRA, allowances breakdown
  - Bonuses, commissions
  
- **Business/Professional Income:**
  - Profit & loss statements
  - GST returns
  - Business receipts and expenses
  
- **Investment Income:**
  - Interest from savings accounts, FDs
  - Dividend income
  - Capital gains (short-term, long-term)
  
- **Other Income:**
  - Rental income
  - Agricultural income
  - Income from other sources
  
- **Previous Year Tax Returns** (2-3 years)

#### Deductions & Expenses
- **Section 80C Investments:**
  - PPF contributions
  - ELSS mutual funds
  - Life insurance premiums
  - NSC, tax-saving FDs
  - Home loan principal repayment
  - Tuition fees
  
- **Section 80D:**
  - Health insurance premiums (self, family, parents)
  - Preventive health checkup expenses
  
- **Home Loan:**
  - Interest paid on home loan (Section 24)
  - Form 16B
  
- **Charitable Donations:**
  - 80G eligible donations
  - Receipts with donor details
  
- **Business Expenses** (if applicable):
  - Office rent, utilities
  - Employee salaries
  - Depreciation on assets
  - Professional fees

#### Assets & Liabilities
- Investment account statements
- Property ownership documents
- Loan statements
- Previous capital gains/losses carried forward

### Expected Output: Tax Savings Recommendations Report

#### Executive Summary
- Current tax liability estimate
- Potential tax savings identified
- Top 3 actionable recommendations
- Implementation deadline (financial year-end)

#### Current Tax Situation Analysis
- Income classification and breakdown
- Current tax bracket
- Available deductions already claimed
- Missed opportunities from previous years

#### Tax-Saving Strategies

**1. Income Management**
- Salary restructuring recommendations (HRA, LTA optimization)
- Deferring income or accelerating deductions (for businesses)
- Long-term vs. short-term capital gains planning
- Tax-loss harvesting opportunities

**2. Deduction Maximization**

| Section | Strategy | Eligible Amount | Estimated Savings |
|---------|----------|-----------------|-------------------|
| 80C | Increase PPF/ELSS contributions | Up to ₹1.5L | ₹46,800 (31.2% bracket) |
| 80D | Health insurance for parents (senior citizens) | ₹50,000 | ₹15,600 |
| 24(b) | Home loan interest | Up to ₹2L | ₹62,400 |
| 80G | Strategic charitable giving | Variable | Variable |

**3. Investment Recommendations**
- Tax-free bonds
- NPS (additional ₹50,000 u/s 80CCD(1B))
- Equity investments (for LTCG tax benefit)
- Municipal bonds (tax-exempt interest)

**4. Business-Specific Strategies** (if applicable)
- Optimal business structure (proprietorship vs. LLP vs. Pvt Ltd)
- Timing of capital expenditures
- Bonus depreciation opportunities
- Presumptive taxation scheme (Section 44AD/44ADA)

**5. Retirement Planning Tax Benefits**
- Maximizing employer PF contributions
- NPS tax benefits
- Annuity/pension plans

#### Year-End Tax Checklist
- [ ] Complete 80C investments before March 31
- [ ] Pay health insurance premium
- [ ] Submit investment proofs to employer
- [ ] Make advance tax payments (if applicable)
- [ ] Donate to eligible charities
- [ ] Review capital gains and harvest losses

#### Projected Tax Impact
- Current estimated tax: ₹X
- After implementing recommendations: ₹Y
- **Total tax savings: ₹Z**

#### Compliance Notes
- Important deadlines (ITR filing, advance tax dates)
- Document checklist for ITR filing
- Recommended documentation practices

### Handoff to Other Agents
- **Investment Advisor Agent**: Sends tax-efficient investment requirements
- **Financial Planning Agent**: Feeds back tax savings for goal planning

---

## 3. Investment Advisor Agent

### Purpose
Provides personalized investment portfolio recommendations based on risk profile, goals, and market analysis.

### Required Inputs

#### Client Profile
- Age and investment time horizon
- Financial goals (from Financial Planning Agent)
- Investment experience level
- Current investment holdings

#### Risk Assessment
- **Risk Tolerance:** Psychological comfort with market volatility
- **Risk Capacity:** Financial ability to absorb losses
  - Emergency fund status
  - Stable income sources
  - Debt obligations
  - Liquidity needs
- **Risk Requirement:** Returns needed to achieve goals
- Overall risk profile: Conservative / Moderate / Aggressive

#### Financial Situation
- Total investable amount
- Monthly investment capacity (SIP amount)
- Existing portfolio breakdown
- Income stability
- Upcoming large expenses (next 3-5 years)

#### Preferences & Constraints
- ESG (Environmental, Social, Governance) preferences
- Sectors to avoid (ethical/religious considerations)
- Investment platform preferences
- Tax status and requirements

### Expected Output: Investment Portfolio Recommendation Report

#### Executive Summary
- Recommended asset allocation
- Expected returns (conservative/realistic/optimistic)
- Risk-adjusted return potential
- Key investment themes

#### Risk Profile Analysis
- **Risk Tolerance Score:** 6/10 (Moderate-Aggressive)
- **Risk Capacity:** High (emergency fund in place, stable income)
- **Risk Requirement:** Medium (8-10% CAGR needed for goals)
- **Overall Profile:** Moderate-Aggressive

#### Strategic Asset Allocation

**Recommended Portfolio Mix:**

| Asset Class | Allocation | Rationale |
|-------------|------------|-----------|
| **Equity** | 65% | Long-term growth, inflation protection |
| Large Cap | 30% | Stability, consistent returns |
| Mid/Small Cap | 20% | Higher growth potential |
| International | 15% | Diversification, currency hedge |
| **Fixed Income** | 25% | Stability, regular income |
| Debt Mutual Funds | 15% | Tax efficiency, moderate returns |
| FDs/Bonds | 10% | Capital preservation |
| **Gold** | 5% | Hedge against inflation, crisis protection |
| **Cash/Liquid** | 5% | Emergency access, opportunities |

#### Specific Product Recommendations

**Equity Investments:**
1. **NIFTY 50 Index Fund** - 15% allocation
   - Low cost, market-cap weighted, diversified
   - Fund: ABC Nifty Index Fund
   - Expense ratio: 0.1%
   - 10Y CAGR: 12.5%

2. **Flexi-cap Active Fund** - 15% allocation
   - Fund: XYZ Flexi Cap Fund
   - 5Y CAGR: 14.2%
   - Consistency: High

3. **Mid/Small Cap Fund** - 20% allocation
   - Fund: DEF Mid Cap Growth Fund
   - Higher volatility, higher potential
   - 5Y CAGR: 16.8%

4. **International Equity** - 15% allocation
   - Fund: Global Tech ETF / S&P 500 Index Fund
   - Currency diversification
   - Exposure to global giants

**Debt Investments:**
- Short-term debt funds (for liquidity)
- Corporate bond funds (higher yield)
- 5-year fixed deposits (guaranteed returns)

**Gold:**
- Gold ETF or Sovereign Gold Bonds

#### Investment Strategy

**For Lumpsum Amount:**
- Systematic Transfer Plan (STP) over 6 months
- Reduces market timing risk
- Invest lumpsum in liquid fund, transfer weekly to equity

**For Monthly Investments:**
- SIP (Systematic Investment Plan) on 1st of each month
- Auto-debit setup for discipline
- Recommended SIP: ₹X/month

#### Portfolio Rebalancing
- **Frequency:** Annual (or when allocation deviates >5%)
- **Process:**
  1. Review current allocation
  2. Sell overperforming assets
  3. Buy underperforming assets
  4. Restore target allocation
- **Tax Consideration:** Use LTCG exemption limits

#### Performance Monitoring
- **Review Schedule:** Quarterly portfolio review
- **Key Metrics to Track:**
  - Absolute returns
  - Returns vs. benchmark
  - Portfolio volatility
  - Expense ratios
- **Red Flags:**
  - Fund underperforming benchmark for 3+ years
  - Change in fund manager
  - Drift in fund mandate

#### Expected Returns & Scenarios

| Scenario | 1 Year | 3 Years | 5 Years | 10 Years |
|----------|--------|---------|---------|----------|
| Conservative | 6% | 7% | 8% | 9% |
| Realistic | 9% | 10% | 11% | 12% |
| Optimistic | 13% | 14% | 15% | 16% |

#### Risk Warnings
- Market volatility can cause short-term losses
- Past performance is not indicative of future returns
- Stay invested for recommended time horizon
- Avoid panic selling during market corrections

#### Next Steps
1. Open investment accounts (Demat/mutual fund)
2. Complete KYC process
3. Set up auto-debit for SIPs
4. Review and sign off on recommendations
5. Execute investments
6. Schedule first review in 3 months

### Handoff to Other Agents
- **Tax Planning Agent**: Requests tax-efficient investment structures
- **Financial Research Agent**: Requests deep research on specific funds/stocks

---

## 4. Budget Coach Agent

### Purpose
Helps users create realistic monthly budgets, track expenses, and develop healthy spending habits.

### Required Inputs

#### Income Information
- **Regular Income:**
  - Monthly salary (take-home)
  - Freelance/gig income (average)
  - Rental income
  - Other passive income
  
- **Variable Income:**
  - Bonuses (annual average)
  - Commissions
  - Seasonal income

#### Expense Data (Past 3-6 Months)
- Bank statements (all accounts)
- Credit card statements
- Digital wallet transactions
- Cash expenses (estimated)

#### Financial Obligations
- Loan EMIs (home, car, personal)
- Credit card minimum payments
- Insurance premiums
- Rent/mortgage
- Subscription services

#### Financial Goals
- Emergency fund target
- Short-term savings goals
- Debt payoff targets
- Monthly investment amount

#### Personal Preferences
- Lifestyle priorities
- Non-negotiable expenses
- Areas willing to cut back
- Spending triggers/patterns

### Expected Output: Personalized Budget Plan

#### Executive Summary
- Total monthly income: ₹X
- Total current expenses: ₹Y
- Current savings rate: Z%
- **Target savings rate: Z+10%**
- Potential monthly savings increase: ₹A

#### Income Breakdown

| Income Source | Amount | % of Total |
|---------------|--------|------------|
| Salary | ₹50,000 | 80% |
| Freelance | ₹10,000 | 16% |
| Rental | ₹2,500 | 4% |
| **Total** | **₹62,500** | **100%** |

#### Expense Analysis (Current vs. Recommended)

**Fixed Expenses (Non-Negotiable):**

| Category | Current | Recommended | Notes |
|----------|---------|-------------|-------|
| Rent/Mortgage | ₹15,000 | ₹15,000 | 24% of income (ideal) |
| Utilities | ₹2,500 | ₹2,500 | - |
| Loan EMIs | ₹8,000 | ₹8,000 | - |
| Insurance | ₹2,000 | ₹2,000 | - |
| **Subtotal** | **₹27,500** | **₹27,500** | **44%** |

**Variable Expenses (Controllable):**

| Category | Current | Recommended | Savings | Action |
|----------|---------|-------------|---------|--------|
| Groceries | ₹8,000 | ₹7,000 | ₹1,000 | Meal planning, bulk buying |
| Dining Out | ₹5,000 | ₹3,000 | ₹2,000 | Limit to 2x/week |
| Transportation | ₹3,000 | ₹2,500 | ₹500 | Use public transport 2x/week |
| Entertainment | ₹4,000 | ₹2,500 | ₹1,500 | Cancel unused subscriptions |
| Shopping | ₹6,000 | ₹3,000 | ₹3,000 | 30-day rule for non-essentials |
| Personal Care | ₹2,000 | ₹1,500 | ₹500 | DIY treatments, fewer salon visits |
| Miscellaneous | ₹3,000 | ₹2,000 | ₹1,000 | Track and minimize |
| **Subtotal** | **₹31,000** | **₹21,500** | **₹9,500** | - |

**Savings & Investments:**

| Category | Current | Recommended | Change |
|----------|---------|-------------|--------|
| Emergency Fund | ₹0 | ₹3,000 | +₹3,000 |
| Investments (SIP) | ₹2,000 | ₹7,000 | +₹5,000 |
| Goal Savings | ₹2,000 | ₹3,500 | +₹1,500 |
| **Subtotal** | **₹4,000** | **₹13,500** | **+₹9,500** |

#### Budget Allocation (50/30/20 Rule)

- **50% Needs** (Essential): ₹31,250 → Current: ₹27,500 ✓
- **30% Wants** (Discretionary): ₹18,750 → Target: ₹21,500
- **20% Savings** (Future): ₹12,500 → Target: ₹13,500 ✓

#### Expense Category Guidelines

**Housing (25-30% of income):**
- Includes rent/mortgage, utilities, maintenance
- Current: 28% ✓ Within ideal range

**Food (10-15%):**
- Groceries: 11%
- Dining out: 5%
- Total: 16% → Reduce to 13%

**Transportation (10-15%):**
- Current: 5% → Low, good!

**Debt Repayment (< 20%):**
- Current: 13% → Acceptable, focus on early repayment

**Savings (Minimum 20%):**
- Current: 6% → **Priority: Increase to 20%+**

#### Behavioral Change Strategies

**1. Immediate Actions (This Week):**
- [ ] Set up separate savings account (auto-transfer on salary day)
- [ ] Cancel 2 unused subscriptions (identify: streaming, gym, etc.)
- [ ] Link all accounts to expense tracking app
- [ ] Set spending limit alerts on credit/debit cards

**2. Monthly Habits:**
- **Meal Planning Sunday:** Plan week's meals, grocery list
- **No-Spend Challenge:** One week/month with zero discretionary spending
- **Cash Envelope System:** Allocate cash for categories prone to overspending
- **Monthly Budget Review:** 1st of every month

**3. Spending Triggers:**
- **Identified pattern:** High weekend spending on dining/entertainment
- **Solution:** Plan free/low-cost weekend activities, cook special meals at home
- **Reward System:** For every ₹5,000 saved, allocate ₹500 for guilt-free spending

#### Emergency Fund Roadmap
- **Target:** 6 months expenses = ₹(27,500 + 21,500) × 6 = ₹2,94,000
- **Monthly contribution:** ₹3,000
- **Time to goal:** ~8 years → Accelerate with windfalls (bonus, tax refund)

#### Debt Payoff Strategy
**Loan 1:** Personal Loan (₹80,000 @ 12%)
- Minimum EMI: ₹5,000
- **Recommended:** ₹7,000 (+₹2,000)
- Payoff accelerated by 8 months, save ₹5,000 in interest

#### Progress Tracking

**Weekly:**
- Log all expenses in app
- Check spending vs. budget

**Monthly:**
- Review category-wise spending
- Adjust next month's budget
- Celebrate wins (e.g., under-budget categories)

**Quarterly:**
- Analyze expense trends
- Update financial goals
- Revise budget for life changes

#### Tools & Resources
- **Recommended Apps:**
  - Money Manager (expense tracking)
  - Walnut (auto-synced expenses)
  - ET Money (budget + investments)
  
- **Spreadsheet Template:** [Link to Google Sheets budget template]

#### Accountability System
- **Monthly Check-in:** Voice call with Budget Coach Agent
- **Accountability Partner:** Share goals with trusted friend/family
- **Milestone Rewards:**
  - 3 months on track → ₹1,000 treat
  - 6 months → Weekend getaway (budgeted)

### Handoff to Other Agents
- **Financial Planning Agent**: Sends savings capacity for goal planning
- **Investment Advisor Agent**: Sends monthly SIP amount recommendations

---

## 5. Financial Research Agent

### Purpose
Conducts deep market research, product comparisons, and data analysis to support other agents' recommendations.

### Required Inputs

#### Research Request
- **Request Type:**
  - Insurance product comparison
  - Investment fund analysis
  - Loan product research
  - Market trend analysis
  - Government scheme eligibility
  
- **Specific Parameters:**
  - Client risk profile
  - Budget constraints
  - Coverage requirements
  - Investment goals

#### Client Context
- Age, location, occupation
- Financial goals and timeline
- Risk tolerance
- Current holdings

### Expected Output: Research Report

#### Insurance Product Comparison

**Life Insurance:**

| Provider | Product | Type | Coverage | Premium (Annual) | Features | Rating |
|----------|---------|------|----------|------------------|----------|--------|
| HDFC Life | Click 2 Protect | Term | ₹1 Cr | ₹12,000 | Riders available, online discount | 4.5/5 |
| ICICI Pru | iProtect Smart | Term | ₹1 Cr | ₹11,500 | Return of premium option | 4.3/5 |
| Max Life | Smart Secure | Term | ₹1 Cr | ₹12,500 | Flexible coverage, premium waiver | 4.4/5 |

**Recommendation:** ICICI Prudential iProtect Smart
- Best value for money
- Strong claim settlement ratio (98.5%)
- Flexible premium payment options

**Health Insurance:**

| Provider | Product | Sum Insured | Premium (Annual) | Co-payment | Network Hospitals | Key Benefits |
|----------|---------|-------------|------------------|------------|-------------------|--------------|
| Star Health | Super Surplus | ₹10 L | ₹18,000 | No | 12,000+ | Unlimited restoration |
| Care Health | Platinum | ₹10 L | ₹17,500 | No | 18,000+ | International coverage |
| Niva Bupa | ReAssure | ₹10 L | ₹19,000 | No | 10,000+ | Preventive care |

**Recommendation:** Care Health Platinum
- Widest hospital network
- Comprehensive coverage including maternity
- Good claim settlement record

#### Investment Fund Analysis

**Equity Mutual Fund Deep Dive:**

**Fund Name:** ABC Flexi Cap Fund

- **Category:** Large & Mid Cap / Flexi Cap
- **AUM:** ₹15,000 Cr
- **Expense Ratio:** 0.85%
- **Fund Manager:** John Doe (10 years experience)
- **Minimum Investment:** ₹500 SIP / ₹5,000 lumpsum

**Performance:**

| Period | Fund Returns | Benchmark | Outperformance |
|--------|--------------|-----------|----------------|
| 1 Year | 18.5% | 15.2% | +3.3% |
| 3 Year | 14.8% | 12.1% | +2.7% |
| 5 Year | 13.2% | 11.5% | +1.7% |
| 10 Year | 15.1% | 12.8% | +2.3% |

**Risk Metrics:**
- Standard Deviation: 14.5% (Moderate)
- Sharpe Ratio: 1.2 (Good risk-adjusted returns)
- Beta: 0.95 (Slightly less volatile than market)
- Max Drawdown: -22% (March 2020)

**Portfolio Composition:**
- Large Cap: 55%
- Mid Cap: 30%
- Small Cap: 15%

**Top Holdings:**
1. Reliance Industries - 8%
2. HDFC Bank - 7%
3. Infosys - 6%
4. TCS - 5%
5. Bharti Airtel - 4%

**Sector Allocation:**
- Financial Services: 25%
- IT: 20%
- Consumer Goods: 15%
- Healthcare: 10%
- Others: 30%

**Strengths:**
- Consistent performance across market cycles
- Experienced fund manager
- Diversified portfolio

**Weaknesses:**
- Expense ratio slightly higher than category average
- Recent high exposure to IT sector (concentration risk)

**Recommendation:** BUY for long-term (7+ years)

#### Government Scheme Eligibility Check

**Schemes for Client Profile:**

1. **Pradhan Mantri Vaya Vandana Yojana (PMVVY)**
   - Eligibility: ✓ (Age 60+)
   - Benefit: Guaranteed 7.4% return for 10 years
   - Action: Invest ₹1.5L before scheme closes

2. **Atal Pension Yojana (APY)**
   - Eligibility: ✓ (Age 18-40)
   - Benefit: Guaranteed pension ₹5,000/month
   - Action: Enroll, contribute ₹210/month

3. **Sukanya Samriddhi Yojana**
   - Eligibility: ✗ (No girl child under 10)
   - N/A

#### Market Trend Analysis

**Current Market Outlook:**
- NIFTY 50: 22,500 (+12% YTD)
- Market Phase: Mid-cycle expansion
- Interest Rate Trend: Neutral (likely hold for 6 months)
- Inflation: 5.2% (within RBI target)

**Sector Recommendations:**
- **Overweight:** IT, Pharma, Consumption
- **Underweight:** Real Estate, Metals
- **Neutral:** Banking, Auto

### Handoff to Other Agents
- **Investment Advisor Agent**: Sends research for portfolio construction
- **Financial Planning Agent**: Sends insurance product recommendations
- **Tax Planning Agent**: Sends tax-saving scheme analysis

---

## 6. Financial Guru Agent

### Purpose
Provides financial education, explains concepts, and offers best practices guidance to improve financial literacy.

### Required Inputs

#### User Profile
- Current financial literacy level (beginner/intermediate/advanced)
- Specific knowledge gaps
- Learning preferences (examples, videos, step-by-step)

#### Specific Query
- Topic of interest (e.g., "What is compound interest?")
- Context (why they're asking)

### Expected Output: Educational Content

#### Concept Explanation

**Example: Understanding Mutual Funds**

**What is a Mutual Fund?**
A mutual fund is like a basket where many people pool their money together. A professional fund manager then invests this money in stocks, bonds, or other securities on behalf of all investors.

**Simple Analogy:**
Imagine you and 99 friends want to buy fruits in bulk to get a discount, but individually nobody has enough money. So, you all pool money, buy in bulk, and share the fruits proportionally. That's how a mutual fund works!

**How Does It Work?**

1. **You invest:** ₹1,000/month via SIP
2. **Fund manager:** Invests pooled money in 50+ stocks
3. **NAV (Unit price):** You get units based on daily NAV
4. **Returns:** If stocks go up, your units' value increases

**Types of Mutual Funds:**

| Type | Risk | Returns | Suitable For |
|------|------|---------|--------------|
| Equity | High | 12-15% | Long-term goals (7+ years) |
| Debt | Low | 6-8% | Short-term, stability |
| Hybrid | Medium | 9-11% | Balanced approach |

**Why Invest in Mutual Funds?**

✅ **Professional management** - Experts select stocks
✅ **Diversification** - Risk spread across many stocks
✅ **Low minimum** - Start with just ₹500
✅ **Liquidity** - Redeem anytime (with some funds)
✅ **Tax benefits** - ELSS funds get 80C deduction

**Common Mistakes to Avoid:**

❌ Investing based on past returns alone
❌ Frequent switching between funds
❌ Redeeming during market falls (panic selling)
❌ Ignoring expense ratio
❌ Not aligning with financial goals

**Best Practices:**

1. **Start early:** Power of compounding
2. **SIP over lumpsum:** Rupee-cost averaging
3. **Stay invested:** Minimum 5-7 years for equity
4. **Diversify:** Don't put all eggs in one basket
5. **Review annually:** Rebalance if needed

**Example Calculation:**

₹5,000 SIP for 20 years @ 12% return
- Total invested: ₹12 lakhs
- **Corpus at maturity: ₹49.95 lakhs**
- Profit: ₹37.95 lakhs!

**Next Steps:**
1. Complete your KYC
2. Choose fund category based on goal
3. Start small SIP (₹500-1,000)
4. Increase annually by 10%
5. Review every 6 months

**FAQs:**

**Q: Is my money safe?**
A: Regulated by SEBI. But market-linked, so value can fluctuate.

**Q: Can I lose money?**
A: Yes, in short term. But historically, equity funds deliver positive returns over 7+ years.

**Q: How to choose a fund?**
A: Check 5Y returns, consistency, expense ratio, and fund manager experience.

**Resources:**
- [Video] Mutual Funds Explained in 5 Minutes
- [Calculator] SIP Return Calculator
- [Article] How to Pick Your First Mutual Fund

### Handoff to Other Agents
- **Budget Coach Agent**: Sends educational content on expense management
- **Investment Advisor Agent**: Sends foundational knowledge for investment discussions

---

## Multi-Agent Research System

### Architecture Overview - Independent Agent Model

> **Key Principle:** Agents operate **independently**, not in sequence. Based on user preference from the initial call, **ONE specific agent** is selected to handle the entire conversation and generate a complete report. The Deep Research system supports that selected agent with data gathering.

```
                              ┌─────────────────────────┐
                              │   Initial Intake Call   │
                              │    (Pixpoc.ai)          │
                              │  Collects user info +   │
                              │  Identifies need        │
                              └───────────┬─────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │  Agent Router/Selector  │
                              │  Picks ONE agent based  │
                              │  on user preference     │
                              └───────────┬─────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
        ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
        │ Financial         │ │ Tax Planning      │ │ Investment        │
        │ Planning Agent    │ │ Agent             │ │ Advisor Agent     │
        │                   │ │                   │ │                   │
        │ [SELECTED]        │ │                   │ │                   │
        └─────────┬─────────┘ └───────────────────┘ └───────────────────┘
                  │
                  │ OR           OR                      OR
                  ▼                     ▼                     ▼
        ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
        │ Budget Coach      │ │ Financial Guru    │ │ Financial Research│
        │ Agent             │ │ Agent             │ │ Agent             │
        └─────────┬─────────┘ └───────────────────┘ └───────────────────┘
                  │
                  │ Only ONE agent is activated
                  ▼
        ┌─────────────────────────────┐
        │   Specialized Agent Call    │
        │     (Pixpoc.ai)             │
        │  - Collects ALL data needed │
        │  - Asks targeted questions  │
        │  - Provides guidance        │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Deep Research Agent System  │
        │  (Supports selected agent)   │
        │                              │
        │  ┌────────────────────────┐  │
        │  │  Web Search Agent      │  │
        │  │  Data Analysis Agent   │  │
        │  │  Financial Research    │  │
        │  │  Report Generator      │  │
        │  └────────────────────────┘  │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌─────────────────────────────┐
        │   Complete Report Generated │
        │   (Specific to agent type)  │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌─────────────────────────────┐
        │   WhatsApp Delivery         │
        │   - Personalized report     │
        │   - Actionable insights     │
        └─────────────────────────────┘
```

### Workflow Phases

#### Phase 1: Initial Intake (Pixpoc.ai Call)

**Objective:** Identify which ONE agent the user needs

**Process:**
1. User calls designated number
2. Initial Intake Agent (via Pixpoc.ai) greets and collects:
   - Name, age, gender, location
   - Occupation and income bracket
   - **Primary need** (ONE selection: planning/tax/investment/budgeting/education)
   - Preferred language
   - Availability for callback

**Output:** User profile + **single agent selection**

**Callback to System:**
```json
{
  "user_id": "USER_12345",
  "name": "Rahul Kumar",
  "phone": "+91XXXXXXXXXX",
  "age": 32,
  "occupation": "Gig worker - Food delivery",
  "income_bracket": "₹15,000-25,000/month",
  "primary_need": "budget_coaching",  // Only ONE need selected
  "urgency": "high",
  "language": "Hindi",
  "availability": "Evenings 6-8 PM"
}
```

#### Phase 2: Agent Selection

**Agent Router Logic:**

```python
def select_single_agent(primary_need, user_profile):
    """
    Returns EXACTLY ONE agent based on user's primary need.
    No chaining or sequential workflow.
    """
    
    agent_mapping = {
        "financial_planning": "Financial Planning Agent",
        "tax_saving": "Tax Planning Agent",
        "investment_advice": "Investment Advisor Agent",
        "budget_help": "Budget Coach Agent",
        "financial_education": "Financial Guru Agent",
        "product_research": "Financial Research Agent"
    }
    
    selected_agent = agent_mapping.get(primary_need, "Financial Guru Agent")
    
    print(f"Selected Agent: {selected_agent}")
    print(f"This agent will handle the ENTIRE workflow independently")
    
    return selected_agent
```

**Example:**
- User says: "I need help with budgeting" → **Budget Coach Agent** (and ONLY this agent)
- User says: "I want to save tax" → **Tax Planning Agent** (and ONLY this agent)
- User says: "I want to invest" → **Investment Advisor Agent** (and ONLY this agent)

#### Phase 3: Specialized Agent Call (Complete Data Collection)

**Objective:** Selected agent collects ALL data it needs for its report

**Process:**
1. System triggers Pixpoc.ai API for outbound call to **selected agent only**
2. Selected agent conducts comprehensive conversation:
   - Explains purpose of call
   - Asks **ALL** targeted questions needed for its specific report
   - Collects complete dataset (income, expenses, goals, preferences)
   - Provides initial guidance
   - Sets expectations for report delivery

**Example: Budget Coach Agent (Independent Workflow)**

**Conversation Script:**

> "Hello Rahul! This is your Budget Coach from FinanceBot. I'll help you create a complete monthly budget plan. I need to ask you about:
> 1. Your income sources
> 2. All your expenses (fixed and variable)
> 3. Your savings goals
> 4. Any debts or loans
> 
> This will take about 15 minutes. Ready to start?"

**Data Collected by Budget Coach Agent:**
```json
{
  "call_id": "CALL_67890",
  "user_id": "USER_12345",
  "agent_type": "Budget Coach Agent",
  "duration_minutes": 15,
  "transcript": "...",
  "complete_data": {
    "income": {
      "salary": 18000,
      "side_gig": 2000,
      "total": 20000
    },
    "fixed_expenses": {
      "rent": 5000,
      "loan_emi": 2000,
      "insurance": 500,
      "utilities": 800
    },
    "variable_expenses": {
      "food": 6000,
      "transport": 3000,
      "entertainment": 2000,
      "personal_care": 1000,
      "miscellaneous": 1500
    },
    "current_savings": 200,
    "debts": [
      {"type": "personal_loan", "outstanding": 50000, "emi": 2000}
    ],
    "goals": {
      "emergency_fund": true,
      "target_monthly_savings": 3000,
      "debt_payoff_priority": "high"
    }
  },
  "sentiment": "positive",
  "engagement_score": 8.5
}
```

**Key Point:** The Budget Coach Agent collects **everything** it needs. No handoff to other agents.

#### Phase 4: Deep Research (Supporting the Selected Agent)

**Objective:** Provide data/research to support the **one selected agent's** recommendations

**Deep Research Agent supports the selected agent only:**

**For Budget Coach Agent Example:**

```python
# Deep Research Agent receives request from Budget Coach Agent
research_request = {
    "requesting_agent": "Budget Coach Agent",
    "user_profile": {...},
    "research_needed": [
        "best_budget_apps",
        "savings_schemes_for_gig_workers", 
        "expense_optimization_strategies"
    ]
}

# Deep Research activates sub-agents in parallel:
research_tasks = [
    {
        "agent": "Web Search Agent",
        "task": "Find best budget tracking apps for gig workers (Hindi support)",
        "priority": "medium"
    },
    {
        "agent": "Financial Research Agent",
        "task": "Compare micro-savings schemes: RD, PPF, Post Office schemes",
        "priority": "high"
    },
    {
        "agent": "Data Analysis Agent",
        "task": "Analyze Rahul's expense pattern and identify savings opportunities",
        "priority": "high"
    }
]
```

**Research Output (returned to Budget Coach Agent only):**
```json
{
  "research_summary": {
    "recommended_app": "Walnut App (Hindi, auto-tracking, free)",
    "best_savings_scheme": {
      "name": "Post Office Recurring Deposit",
      "interest": "7.2% p.a.",
      "min_investment": "₹100/month",
      "liquidity": "Partial withdrawal after 1 year"
    },
    "expense_optimization": {
      "food": {
        "current": 6000,
        "recommended": 4500,
        "savings": 1500,
        "strategy": "Meal planning, bulk buying groceries"
      },
      "transport": {
        "current": 3000,
        "recommended": 2500,
        "savings": 500,
        "strategy": "Use shared auto 3x/week instead of solo"
      },
      "entertainment": {
        "current": 2000,
        "recommended": 1000,
        "savings": 1000,
        "strategy": "Free weekend activities, home cooking"
      }
    },
    "government_schemes": [
      {
        "name": "PM-SYM (Shram Yogi Maandhan)",
        "eligibility": "Yes (gig worker, age 32)",
        "benefit": "₹3,000/month pension after 60",
        "contribution": "₹100-200/month"
      }
    ]
  }
}
```

#### Phase 5: Report Generation (By Selected Agent)

**Budget Coach Agent generates its complete report:**

**Inputs:**
- User profile (Phase 1)
- Complete conversation data (Phase 3)
- Research findings from Deep Research Agent (Phase 4)

**Process:**
1. Budget Coach Agent selects its own template
2. Populates with personalized budget data
3. Generates visual charts (income/expense breakdown, savings projection)
4. Adds actionable recommendations
5. Translates to Hindi (user preference)

**Output:** **Complete Budget Plan Report** (as documented in section 4)

#### Phase 6: Report Delivery (WhatsApp)

**WhatsApp Integration:**

Send **Budget Coach Agent's report only** via WhatsApp Business API

**Message:**

> नमस्ते राहुल! 🎉
> 
> आपकी **बजट योजना** तैयार है!
> 
> ✅ आपकी मासिक आय: ₹20,000
> ✅ खर्चों का विश्लेषण
> ✅ **₹3,000/महीने** बचत का तरीका
> ✅ 6 महीने में इमरजेंसी फंड
> ✅ कर्ज जल्दी चुकाने की योजना
> 
> रिपोर्ट डाउनलोड करें 👇
> [बजट_योजना_राहुल.pdf]
> 
> सवाल? रिप्लाई करें! 💬

---

### Independent Agent Collaboration Model

**Important:** Agents do NOT chain together or hand off to each other. Each agent works independently.

#### Pattern: Single Agent Workflow

**Standard flow for ANY agent:**

```
User Request
    ↓
Initial Intake (identify ONE need)
    ↓
Agent Selection (pick ONE agent)
    ↓
Selected Agent Call (collect ALL data)
    ↓
Deep Research (support selected agent)
    ↓
Report Generation (by selected agent)
    ↓
WhatsApp Delivery
```

**Example Scenarios:**

**Scenario 1: User Needs Budget Help**
```
User: "I need help managing my expenses"
    ↓
Budget Coach Agent selected
    ↓
Budget Coach Agent collects: income, expenses, goals
    ↓
Deep Research finds: budget apps, savings schemes, optimization tips
    ↓
Budget Coach Agent generates: Complete Budget Plan
    ↓
Report sent via WhatsApp
```

**Scenario 2: User Needs Tax Advice**
```
User: "I want to save tax"
    ↓
Tax Planning Agent selected
    ↓
Tax Planning Agent collects: income, investments, deductions
    ↓
Deep Research finds: tax-saving schemes, investment options
    ↓
Tax Planning Agent generates: Complete Tax Savings Report
    ↓
Report sent via WhatsApp
```

**Scenario 3: User Needs Investment Advice**
```
User: "I want to invest ₹10,000/month"
    ↓
Investment Advisor Agent selected
    ↓
Investment Advisor Agent collects: risk profile, goals, time horizon
    ↓
Deep Research finds: fund analysis, portfolio recommendations
    ↓
Investment Advisor Agent generates: Complete Investment Portfolio Report
    ↓
Report sent via WhatsApp
```

#### Deep Research Agent: Universal Support System

**Role:** Supports whichever specialized agent is selected

**Capabilities:**
- Web Search Agent: Online research, product comparisons
- Data Analysis Agent: Pattern analysis, calculations, projections
- Financial Research Agent: Fund analysis, insurance comparison
- Report Generator Agent: Template selection, PDF generation

**Key Point:** Deep Research agents are **helpers** that work in the background. They don't interact with users directly.

### Data Flow & Security

**Data Storage:**
- User profile: Encrypted database
- Conversation transcripts: Encrypted, auto-delete after 90 days
- Generated reports: Encrypted cloud storage, user-accessible via secure link

**Access Control:**
- Each agent accesses only required data fields
- Personally Identifiable Information (PII) masked for analytics agents
- Audit logs for all data access

**Handoff Protocol:**

```json
{
  "from_agent": "Financial Planning Agent",
  "to_agent": "Tax Planning Agent",
  "data_shared": {
    "income": 500000,
    "existing_80C_investments": 50000,
    "loan_interest": 150000
  },
  "data_excluded": {
    "phone_number": "MASKED",
    "address": "MASKED"
  },
  "timestamp": "2025-11-25T00:15:00Z",
  "consent": true
}
```

### Performance Metrics

**Agent Collaboration Efficiency:**
- Average research time: < 5 minutes (target)
- Report generation time: < 2 minutes
- End-to-end (call to WhatsApp delivery): < 30 minutes

**Quality Metrics:**
- User satisfaction score: > 4.5/5
- Report accuracy: > 95%
- Recommendation acceptance rate: > 70%

---

## Conclusion

This multi-agent system enables **scalable, personalized, and comprehensive financial assistance** for underserved populations. Each agent is specialized yet collaborative, ensuring users receive expert-level guidance across all aspects of their financial lives.

**Next Steps:**
1. Implement agent prompts and conversation flows
2. Build Deep Research Agent orchestration logic
3. Integrate Pixpoc.ai APIs
4. Set up WhatsApp Business API
5. Create report templates for each agent type
6. Test end-to-end workflow with pilot users
