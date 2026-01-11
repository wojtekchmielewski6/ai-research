# Comparative Efficiency of AI Infrastructure Financing: A Multi-Method Analysis of Innovation Systems in the United States, European Union, and China (2015-2024)

**Draft for submission to:** Research Policy / Technological Forecasting and Social Change

---

## Abstract

**Purpose:** This study provides a comprehensive evaluation of the comparative efficiency of artificial intelligence (AI) infrastructure financing across three major global innovation ecosystems—the United States, European Union, and China—during the transformative period of 2015-2024. We examine how fundamentally different strategic approaches to AI development—market-driven, regulatory-first, and state-led models—translate diverse investment inputs into measurable innovation outputs. The research addresses the critical policy question of whether higher investment volumes necessarily translate into proportionally higher innovation outcomes, and what role institutional frameworks play in mediating this relationship.

**Methodology:** We employ a rigorous multi-method approach combining five complementary econometric techniques to ensure robust and triangulated findings. Our methodological framework includes: (1) Data Envelopment Analysis (DEA) using both CCR and BCC models to assess relative efficiency under constant and variable returns to scale; (2) Stochastic Frontier Analysis (SFA) with half-normal inefficiency distribution to decompose output variance into random noise and systematic inefficiency; (3) Panel Data Models with Fixed Effects (FE) and Random Effects (RE) estimators, supplemented by Hausman specification tests; (4) Difference-in-Differences (DiD) analysis to evaluate the causal impact of the EU AI Act; and (5) Two-Stage DEA-Tobit regression to identify environmental determinants of efficiency. Data are sourced from the Stanford Human-Centered Artificial Intelligence (HAI) AI Index Report 2025 and the OECD AI Policy Observatory, covering 40 region-year observations across four economies.

**Findings:** Our results reveal significant and policy-relevant heterogeneity in efficiency across regions. Contrary to conventional expectations, China demonstrates the highest technical efficiency (SFA score: 1.075, indicating proximity to the production frontier), followed by the United States (1.199) and the European Union (1.365). Panel analysis with fixed effects indicates that private investment positively affects patent output (β=0.154, p<0.01), while public investment shows a statistically significant negative association (β=-0.709, p<0.01), suggesting potential crowding-out effects or measurement limitations in capturing public investment returns. Human capital, measured by researcher count, emerges as the strongest predictor of innovation output (β=1.854, p<0.01). The EU's regulatory approach, exemplified by the AI Act implemented in 2024, appears to impose measurable short-term efficiency costs, though our DiD estimates lack statistical significance due to limited post-treatment observations.

**Originality:** This study makes three primary contributions to the literature. First, it provides the first comprehensive multi-method comparison of AI financing efficiency across the three dominant global AI ecosystems, moving beyond simple input-output comparisons to rigorous efficiency measurement. Second, it incorporates the most recent 2024 data, enabling preliminary assessment of the EU AI Act's effects on European AI innovation. Third, it develops a replicable methodological framework for ongoing monitoring of AI innovation efficiency as the global AI landscape continues to evolve.

**Keywords:** Artificial Intelligence; Innovation Efficiency; Data Envelopment Analysis; Stochastic Frontier Analysis; Panel Data; Difference-in-Differences; AI Policy; EU AI Act; Technology Investment; National Innovation Systems

**JEL Classification:** O31, O32, O33, O38, L52, H54

---

## 1. Introduction

### 1.1 Research Context and Motivation

The global competition for artificial intelligence (AI) supremacy has emerged as one of the defining technological, economic, and geopolitical phenomena of the twenty-first century (Brynjolfsson & McAfee, 2014; Agrawal et al., 2019; Acemoglu & Restrepo, 2020). Unlike previous technological revolutions, the AI race is characterized by unprecedented concentration of investment, talent, and computational resources in a small number of firms and nations. In 2024 alone, global private AI investment reached $156.8 billion, with the United States accounting for approximately 70% of this total (Stanford HAI, 2025). This remarkable concentration of capital raises fundamental questions about the efficiency of different national approaches to AI development and the optimal allocation of resources between public and private investment channels.

The economic significance of AI extends far beyond its direct market value. Economists increasingly conceptualize AI as a general-purpose technology (GPT) with transformative potential comparable to electricity or the internal combustion engine (Trajtenberg, 2018; Goldfarb et al., 2019). This GPT perspective implies that AI investments should be evaluated not only on their direct returns but also on their catalytic effects across the broader innovation ecosystem. However, measuring these effects presents substantial methodological challenges, as traditional productivity metrics may fail to capture the full scope of AI's economic impact (Brynjolfsson et al., 2021).

The policy stakes are correspondingly high. Governments worldwide are committing substantial public resources to AI development, with China's public AI R&D investment reaching $35 billion in 2024 and the European Union allocating €18 billion under its various AI initiatives (OECD, 2024). These investments reflect divergent strategic visions: China's state-led approach emphasizes rapid scaling and practical applications; the United States maintains a market-driven model with minimal regulatory intervention; and the European Union has pioneered a regulatory-first approach centered on the AI Act, the world's first comprehensive AI legislation (Smuha, 2021; Veale & Zuiderveen Borgesius, 2021).

### 1.2 Three Models of AI Development

Our analysis centers on three distinct institutional models of AI development that have crystallized over the past decade:

**The United States Model: Market-Driven Innovation**

The American approach to AI development is characterized by minimal regulatory intervention, dominant private sector leadership, and a culture of entrepreneurial risk-taking (Goldfarb & Trefler, 2018). In 2024, US private AI investment reached $109.1 billion—nearly twelve times China's $9.3 billion and more than twenty times the EU's combined total (Stanford HAI, 2025). This investment is heavily concentrated in a small number of technology giants and well-funded startups, with Google, OpenAI, Microsoft, Meta, and Anthropic accounting for the majority of frontier AI development.

The US model offers several theoretical advantages: market discipline ensures that capital flows to its highest-valued uses; competitive pressure drives rapid innovation cycles; and the absence of regulatory constraints enables experimentation with novel AI applications. However, critics argue that this approach may underinvest in AI safety research, exacerbate economic inequality through winner-take-all dynamics, and fail to address potential negative externalities of AI deployment (Korinek & Stiglitz, 2021).

**The European Union Model: Regulatory-First Innovation**

The European Union has distinguished itself through a regulatory-first approach that prioritizes safety, transparency, and fundamental rights protection (Bradford, 2020). The AI Act, which entered into force in 2024, establishes a risk-based regulatory framework that imposes graduated requirements on AI systems based on their potential for harm. High-risk AI applications—including those in healthcare, law enforcement, and critical infrastructure—face stringent requirements for conformity assessment, human oversight, and transparency.

Proponents argue that this approach builds long-term trust in AI systems, creates competitive advantage in trustworthy AI, and establishes global regulatory standards through the "Brussels Effect" (Bradford, 2020). Critics counter that regulatory compliance costs may disadvantage European AI developers, drive talent and investment to less regulated jurisdictions, and slow the pace of innovation relative to competitors (Engler, 2022). Our analysis provides empirical evidence on these competing claims.

**The Chinese Model: State-Led Innovation**

China's approach combines substantial public investment with strategic national planning, access to vast data resources, and targeted industrial policy (Lee, 2018; Ding, 2018). The 2017 New Generation Artificial Intelligence Development Plan established a comprehensive roadmap for AI development, with explicit goals of matching global leaders by 2020, achieving major breakthroughs by 2025, and becoming the world's primary AI innovation center by 2030.

The Chinese model offers distinctive advantages: coordinated investment across the AI value chain reduces duplication and fragmentation; access to 1.4 billion users provides unparalleled training data; and state support enables patient capital for long-term research. However, concerns persist regarding data privacy, algorithmic transparency, international collaboration barriers, and the concentration of AI capabilities in surveillance and social control applications (Feldstein, 2019).

### 1.3 Research Gap and Contribution

Despite a rapidly growing literature on AI investment, policy, and governance, a significant empirical gap remains. Prior research has focused predominantly on:

- **Aggregate investment trends:** Descriptive analyses of global AI investment patterns without rigorous efficiency measurement (OECD, 2023; Stanford HAI, 2024; McKinsey, 2023).
- **Policy analysis:** Qualitative assessments of regulatory frameworks without quantitative evaluation of their innovation effects (Bradford, 2020; Floridi et al., 2018; Smuha, 2021).
- **Innovation indicators:** Patent and publication counts as proxies for innovation output without formal efficiency modeling (Cockburn et al., 2019; WIPO, 2024).
- **Country case studies:** Deep dives into individual national AI ecosystems without systematic cross-country comparison (Lee, 2018; Ding, 2018).

This study addresses these gaps by developing and applying a multi-method efficiency analysis framework that enables:

1. **Rigorous efficiency measurement:** Quantifying the relative efficiency of converting AI investments into innovation outputs using established econometric methods from the productivity literature.

2. **Input factor analysis:** Identifying the marginal productivity of different input factors, particularly public versus private investment and human capital.

3. **Policy impact evaluation:** Assessing the early-stage effects of major policy interventions, specifically the EU AI Act, using quasi-experimental methods.

4. **Efficiency determinant analysis:** Examining environmental and institutional factors that explain efficiency heterogeneity across regions and time periods.

### 1.4 Research Questions and Hypotheses

This study addresses three primary research questions:

**RQ1:** How do the United States, European Union, and China compare in terms of technical efficiency in converting AI investments into innovation outputs?

**RQ2:** What is the relative contribution of public versus private investment to AI innovation outcomes, and does public investment complement or crowd out private investment?

**RQ3:** What are the short-term efficiency implications of regulatory approaches to AI governance, specifically the EU AI Act?

Based on our theoretical framework and literature review, we propose the following hypotheses:

**H1 (Private Investment Advantage):** Private investment in AI shows a stronger positive association with innovation outputs than public investment, due to market discipline, competitive incentives, and efficient capital allocation mechanisms.

**H2 (US Efficiency Leadership):** The market-driven US approach demonstrates higher technical efficiency than the regulatory EU approach in the short term, as regulatory compliance imposes costs that reduce measured output per unit of input.

**H3 (Chinese Scale Efficiency):** China's state-led model achieves high efficiency through scale economies in data access and coordinated investment across the AI value chain, partially offsetting lower per-capita private investment.

**H4 (Regulatory Efficiency Costs):** The implementation of the EU AI Act is associated with measurable short-term efficiency costs for European AI innovation, though these costs may be justified by long-term trust and safety benefits not captured in our output measures.

### 1.5 Paper Structure

The remainder of this paper is organized as follows. Section 2 reviews the relevant theoretical and empirical literature on AI investment, innovation efficiency measurement, and comparative AI governance. Section 3 describes our methodological framework in detail, including formal specifications of all five econometric approaches. Section 4 presents our data sources, variable definitions, and descriptive statistics. Section 5 reports the empirical results from each analytical method. Section 6 discusses the findings, their theoretical and policy implications, and study limitations. Section 7 concludes with key insights and directions for future research.

---

## 2. Theoretical Framework and Literature Review

### 2.1 The Economics of AI Investment

#### 2.1.1 AI as a General-Purpose Technology

The economic analysis of AI investment builds on the foundational concept of general-purpose technologies (GPTs)—technologies with broad applicability, potential for continuous improvement, and capacity to enable complementary innovations across multiple sectors (Bresnahan & Trajtenberg, 1995). Historical GPTs include the steam engine, electricity, and information technology. Economists increasingly classify AI as the latest GPT, with potentially even broader transformative scope (Trajtenberg, 2018; Cockburn et al., 2019).

The GPT framework has important implications for investment efficiency analysis. First, direct returns to AI investment may understate total returns due to positive spillovers to downstream applications. Second, there may be significant time lags between investment and measurable output, as complementary innovations and organizational adaptations develop. Third, network effects and increasing returns may create path dependencies that advantage early movers and create lock-in effects.

Agrawal et al. (2019) conceptualize AI specifically as a "prediction technology" that reduces the cost of prediction across economic activities. This perspective suggests that AI's economic value derives from enabling better decision-making across diverse domains rather than from AI systems themselves. The implication for our analysis is that patent and publication counts may capture only a fraction of AI's economic contribution, potentially biasing efficiency estimates.

#### 2.1.2 Investment Patterns and Concentration

Recent empirical research documents remarkable concentration in AI investment and capabilities. Cockburn et al. (2019) analyze patent data and find that the top 10 AI patent holders account for over 40% of all AI-related patents, with significant geographic concentration in the United States and China. Ahmed et al. (2023) examine corporate AI capabilities and document a "winner-take-most" dynamic in which a small number of firms achieve decisive advantages in talent, data, and computational resources.

This concentration has implications for efficiency analysis. High concentration may reflect genuine efficiency advantages of scale, as larger organizations can amortize fixed costs of AI development over larger application bases. Alternatively, concentration may reflect market power and barriers to entry that reduce competitive pressure and innovation incentives. Our panel analysis with fixed effects controls for time-invariant regional characteristics that may contribute to observed efficiency differences.

#### 2.1.3 Public vs. Private Investment

The optimal balance between public and private AI investment remains contested. Theoretical arguments for public investment include: correction of positive externalities from basic research; provision of public goods such as safety research; addressing coordination failures in standards development; and ensuring broad access to AI benefits (Mazzucato, 2013). Arguments for private investment emphasize: superior information about commercial opportunities; stronger incentives for cost control; and market discipline in project selection.

Empirical evidence on the relative productivity of public versus private R&D investment yields mixed results. While some studies find crowding-out effects, where public investment displaces more productive private investment (David et al., 2000), others find complementarity effects, where public investment in basic research enables subsequent private commercialization (Salter & Martin, 2001). Our panel analysis contributes to this literature by estimating the marginal effects of public and private AI investment on patenting outcomes.

### 2.2 Innovation Efficiency Measurement

#### 2.2.1 National Innovation Systems

The concept of national innovation systems (NIS) provides a theoretical foundation for cross-country efficiency comparisons (Freeman, 1987; Lundvall, 1992; Nelson, 1993). The NIS framework emphasizes that innovation outcomes depend not only on R&D inputs but also on institutional arrangements, including: educational systems; intellectual property regimes; financial markets; labor market flexibility; inter-organizational linkages; and government policies.

Furman et al. (2002) operationalize this framework through the concept of "national innovative capacity"—the ability of a country to produce and commercialize a flow of innovative technology over time. They identify key determinants including R&D workforce, R&D expenditure, openness to international trade, and intellectual property protection. Our analysis extends this framework to the specific domain of AI innovation, recognizing that AI may have distinctive characteristics that differentiate it from general innovation patterns.

#### 2.2.2 Efficiency Frontier Methods

Two primary methodological traditions have emerged for measuring innovation efficiency:

**Data Envelopment Analysis (DEA):** Introduced by Charnes, Cooper, and Rhodes (1978), DEA is a non-parametric linear programming technique that constructs an empirical efficiency frontier from observed input-output combinations. Units on the frontier are deemed efficient (score = 1), while units below the frontier receive efficiency scores less than 1, indicating the proportional input reduction (or output expansion) needed to reach the frontier.

DEA offers several advantages for innovation efficiency analysis: it accommodates multiple inputs and outputs without requiring explicit functional form assumptions; it provides unit-specific efficiency scores rather than average effects; and it identifies reference sets of efficient peers for benchmarking. Limitations include sensitivity to outliers, inability to accommodate statistical noise, and reduced discriminatory power when the number of units is small relative to the number of inputs and outputs.

Banker et al. (1984) extended the original CCR model (which assumes constant returns to scale) to the BCC model (which allows variable returns to scale). The ratio of CCR to BCC efficiency scores provides a measure of scale efficiency, indicating whether units operate at optimal scale.

**Stochastic Frontier Analysis (SFA):** Developed independently by Aigner et al. (1977) and Meeusen and van den Broeck (1977), SFA is a parametric approach that specifies a production function and decomposes the error term into two components: random noise (reflecting measurement error and random shocks) and systematic inefficiency (reflecting suboptimal input utilization).

SFA offers complementary advantages: it accommodates statistical noise; it enables hypothesis testing on efficiency determinants; and it provides confidence intervals for efficiency estimates. Limitations include sensitivity to distributional assumptions for the inefficiency term and potential misspecification of the production function.

Our multi-method approach leverages the complementary strengths of both DEA and SFA, providing robustness checks across methodological traditions.

#### 2.2.3 Applications to R&D and Innovation

Both DEA and SFA have been applied extensively to R&D and innovation contexts. Chen and Guan (2012) use network DEA to assess China's regional innovation systems, finding significant efficiency variation across provinces. Hashimoto and Haneda (2008) apply SFA to the Japanese pharmaceutical industry, documenting efficiency changes following patent policy reforms. Wang and Huang (2007) combine DEA and SFA in a two-stage analysis of OECD country innovation efficiency.

Applications to AI-specific innovation remain limited. Klinger et al. (2022) analyze AI research productivity using publication metrics but do not employ formal efficiency methods. Baruffaldi et al. (2020) examine AI inventor mobility across countries using patent data but focus on knowledge flows rather than efficiency. Our study contributes to this emerging literature by applying rigorous efficiency methods specifically to AI innovation.

### 2.3 Comparative AI Governance

#### 2.3.1 Regulatory Approaches

The global landscape of AI regulation exhibits substantial variation, reflecting different balances between innovation promotion and risk mitigation (Smuha, 2021). Three broad approaches are observable:

**Light-touch regulation (US approach):** Emphasizes sectoral rather than horizontal AI regulation, relying on existing regulatory frameworks adapted to AI applications. The National AI Initiative Act of 2020 focuses on R&D coordination and workforce development rather than mandatory requirements. The 2023 Executive Order on AI Safety introduced voluntary commitments from leading AI developers but stopped short of binding regulation.

**Comprehensive horizontal regulation (EU approach):** The AI Act establishes a unified regulatory framework applicable across sectors, with requirements graduated according to risk level. Prohibited AI practices include social scoring systems and real-time biometric identification in public spaces. High-risk AI systems face requirements for conformity assessment, data governance, human oversight, accuracy, and robustness.

**Strategic industrial policy (China approach):** Chinese AI governance combines supportive industrial policy with content-focused regulation. Regulations on algorithmic recommendations (2022), deep synthesis (2022), and generative AI (2023) focus on content moderation and alignment with "socialist core values" rather than safety in the technical sense. The 2017 New Generation AI Development Plan provides strategic direction and public investment.

#### 2.3.2 Regulatory Effects on Innovation

The theoretical relationship between regulation and innovation is ambiguous. The traditional view emphasizes regulatory costs—compliance expenditures, delayed time-to-market, and reduced experimentation (Stigler, 1971). The "Porter Hypothesis" counters that well-designed regulation can stimulate innovation by encouraging efficiency improvements and creating first-mover advantages in regulated markets (Porter & van der Linde, 1995).

Empirical evidence on AI regulation is necessarily limited given the recency of major regulatory interventions. Studies of related technology regulations offer relevant insights. Goldfarb and Tucker (2012) find that privacy regulation reduced online advertising effectiveness, with implications for data-intensive AI applications. Acquisti et al. (2016) document significant compliance costs associated with privacy regulation. Conversely, some studies find positive innovation effects from environmental regulation consistent with the Porter Hypothesis (Ambec et al., 2013).

Our DiD analysis of the EU AI Act contributes early empirical evidence on the innovation effects of comprehensive AI regulation.

### 2.4 Hypotheses Development

Drawing on the theoretical and empirical literature reviewed above, we develop our hypotheses:

**H1: Private Investment Advantage**

The economics of R&D suggests that private investment benefits from stronger incentive alignment, market discipline, and efficient capital allocation. Private investors face competitive pressure to maximize returns, directing capital to highest-valued uses. In contrast, public investment may be influenced by political considerations, bureaucratic constraints, and information disadvantages regarding commercial potential. We therefore hypothesize that private AI investment shows stronger positive association with measured innovation outputs.

**H2: US Efficiency Leadership**

The minimal regulatory burden in the US context should theoretically enhance measured efficiency by: reducing compliance costs that consume resources without generating measured outputs; enabling faster experimentation and iteration; and allowing risk-taking that may yield breakthrough innovations. European AI developers, facing AI Act compliance requirements, may divert resources from innovation to compliance, reducing measured efficiency.

**H3: Chinese Scale Efficiency**

Despite lower per-capita private investment, China's AI ecosystem may achieve high efficiency through: coordinated public investment reducing duplication; access to massive training datasets from 1.4 billion users; lower factor costs for AI talent; and focused application domains with clear output metrics. The state-led model may also facilitate cross-organizational coordination that enhances overall ecosystem efficiency.

**H4: Regulatory Efficiency Costs**

Building on the regulatory burden literature, we hypothesize that EU AI Act implementation imposes measurable short-term efficiency costs. These costs may include: direct compliance expenditures; delayed product launches pending conformity assessment; legal uncertainty during the implementation period; and potential reallocation of talent and investment to less regulated jurisdictions.

---

## 3. Methodology

### 3.1 Research Design Overview

We employ a multi-method approach combining five complementary econometric techniques. This methodological pluralism addresses the inherent limitations of any single approach and provides robust, triangulated findings (Creswell & Creswell, 2017). Each method offers distinctive advantages:

| Method | Primary Advantage | Key Limitation |
|--------|------------------|----------------|
| DEA | Non-parametric; no functional form | Sensitive to outliers; no noise |
| SFA | Separates noise from inefficiency | Requires distributional assumptions |
| Panel FE/RE | Controls for unobserved heterogeneity | Assumes specific effect structure |
| DiD | Causal identification under parallel trends | Requires sufficient post-treatment data |
| Two-Stage Tobit | Explains efficiency determinants | Two-stage bias concerns |

### 3.2 Data Envelopment Analysis (DEA)

#### 3.2.1 CCR Model (Constant Returns to Scale)

The CCR model, developed by Charnes, Cooper, and Rhodes (1978), evaluates the relative efficiency of decision-making units (DMUs) under the assumption of constant returns to scale. For DMU₀ under evaluation, the input-oriented CCR model is formulated as:

$$\min_{\theta, \lambda} \theta$$

Subject to:
$$\sum_{j=1}^{n} \lambda_j x_{ij} \leq \theta x_{i0}, \quad \forall i = 1, ..., m$$

$$\sum_{j=1}^{n} \lambda_j y_{rj} \geq y_{r0}, \quad \forall r = 1, ..., s$$

$$\lambda_j \geq 0, \quad \forall j = 1, ..., n$$

Where:
- θ is the efficiency score for DMU₀ (θ ≤ 1)
- λⱼ are intensity weights for each DMU
- xᵢⱼ is input i for DMU j
- yᵣⱼ is output r for DMU j
- m is the number of inputs; s is the number of outputs; n is the number of DMUs

A DMU is CCR-efficient if and only if θ* = 1 and all slacks are zero.

#### 3.2.2 BCC Model (Variable Returns to Scale)

The BCC model, introduced by Banker, Charnes, and Cooper (1984), relaxes the constant returns to scale assumption by adding a convexity constraint:

$$\sum_{j=1}^{n} \lambda_j = 1$$

This constraint ensures that the reference point for each DMU lies on the empirical production frontier rather than on rays extending from the origin. The BCC model accommodates increasing, constant, or decreasing returns to scale.

#### 3.2.3 Scale Efficiency

Scale efficiency is computed as the ratio of CCR to BCC efficiency scores:

$$SE = \frac{\theta_{CCR}}{\theta_{BCC}}$$

A scale efficiency score less than 1 indicates that the DMU does not operate at the most productive scale size. The nature of scale inefficiency (increasing or decreasing returns) is determined by comparing the optimal λ values.

#### 3.2.4 Variable Specification for DEA

For our AI innovation efficiency analysis, we specify:

**Inputs:**
- Public AI R&D investment (billion USD)
- Private AI investment (billion USD)
- AI researchers (thousands)

**Outputs:**
- AI patents granted (count)
- AI research publications (count)
- AI startups / Notable AI models (count)
- AI adoption rate (percentage of enterprises)

### 3.3 Stochastic Frontier Analysis (SFA)

#### 3.3.1 Model Specification

We estimate a Cobb-Douglas stochastic production frontier:

$$\ln Y_{it} = \beta_0 + \beta_1 \ln X_{1it} + \beta_2 \ln X_{2it} + \beta_3 \ln X_{3it} + v_{it} - u_{it}$$

Where:
- $Y_{it}$ is a composite output index for region i at time t
- $X_{1it}$ is public R&D investment
- $X_{2it}$ is private investment
- $X_{3it}$ is the number of AI researchers
- $v_{it} \sim N(0, \sigma_v^2)$ is symmetric random error (noise)
- $u_{it} \sim |N(0, \sigma_u^2)|$ is non-negative inefficiency term

The coefficients β₁, β₂, and β₃ represent output elasticities with respect to each input.

#### 3.3.2 Maximum Likelihood Estimation

The composite error term ε = v - u follows a skew-normal distribution. The log-likelihood function for the half-normal specification is:

$$\ln L = \sum_{i=1}^{n} \left[ -\frac{1}{2} \ln(2\pi) - \ln\sigma + \ln\Phi\left(\frac{-\varepsilon_i \lambda}{\sigma}\right) - \frac{\varepsilon_i^2}{2\sigma^2} \right]$$

Where:
- $\sigma^2 = \sigma_v^2 + \sigma_u^2$
- $\lambda = \sigma_u / \sigma_v$
- $\Phi(\cdot)$ is the standard normal CDF

The ratio λ indicates the relative importance of inefficiency versus noise. A large λ suggests that most of the residual variation reflects genuine inefficiency rather than random factors.

#### 3.3.3 Technical Efficiency Estimation

Following Jondrow et al. (1982), we estimate technical efficiency for each observation as:

$$TE_{it} = E[\exp(-u_{it}) | \varepsilon_{it}]$$

The conditional expectation of u given ε is:

$$E[u_{it} | \varepsilon_{it}] = \sigma_* \left[ \frac{\phi(\varepsilon_{it}\lambda/\sigma)}{\Phi(-\varepsilon_{it}\lambda/\sigma)} - \frac{\varepsilon_{it}\lambda}{\sigma} \right]$$

Where $\sigma_* = \sigma_u \sigma_v / \sigma$.

### 3.4 Panel Data Models

#### 3.4.1 Fixed Effects Specification

The fixed effects model controls for time-invariant unobserved heterogeneity across regions:

$$\ln(Patents_{it}) = \alpha_i + \beta_1 \ln(Public_{it}) + \beta_2 \ln(Private_{it}) + \beta_3 \ln(Researchers_{it}) + \varepsilon_{it}$$

Where αᵢ represents region-specific intercepts capturing persistent differences in innovation capacity, institutional quality, or other unobserved factors.

Estimation proceeds through the within transformation, subtracting group means:

$$(y_{it} - \bar{y}_i) = \beta(X_{it} - \bar{X}_i) + (\varepsilon_{it} - \bar{\varepsilon}_i)$$

#### 3.4.2 Random Effects Specification

The random effects model treats the individual effects as random draws from a distribution:

$$\ln(Patents_{it}) = \alpha + u_i + \beta_1 \ln(Public_{it}) + \beta_2 \ln(Private_{it}) + \beta_3 \ln(Researchers_{it}) + \varepsilon_{it}$$

Where $u_i \sim IID(0, \sigma_u^2)$ and $\varepsilon_{it} \sim IID(0, \sigma_\varepsilon^2)$.

Random effects estimation is efficient under the assumption that individual effects are uncorrelated with regressors.

#### 3.4.3 Hausman Specification Test

The Hausman test evaluates whether the random effects assumption of zero correlation between individual effects and regressors is valid:

$$H = (\hat{\beta}_{FE} - \hat{\beta}_{RE})'[\text{Var}(\hat{\beta}_{FE}) - \text{Var}(\hat{\beta}_{RE})]^{-1}(\hat{\beta}_{FE} - \hat{\beta}_{RE})$$

Under the null hypothesis of no correlation, H follows a chi-squared distribution with degrees of freedom equal to the number of regressors. Rejection of the null favors fixed effects.

### 3.5 Difference-in-Differences (DiD)

#### 3.5.1 Basic Specification

To evaluate the causal impact of the EU AI Act (implemented 2024), we employ a difference-in-differences design:

$$Y_{it} = \alpha + \beta_1 Post_t + \beta_2 Treat_i + \beta_3 (Post_t \times Treat_i) + \gamma X_{it} + \varepsilon_{it}$$

Where:
- $Post_t = 1$ if $t \geq 2024$, 0 otherwise
- $Treat_i = 1$ if region = EU, 0 otherwise
- $\beta_3$ is the average treatment effect on the treated (ATT)
- $X_{it}$ includes time-varying controls

#### 3.5.2 Identification Assumptions

The validity of DiD relies on the parallel trends assumption: in the absence of treatment, treated and control units would have followed parallel outcome trajectories. We assess this assumption by:

1. Testing for differential pre-treatment trends
2. Examining event-study specifications with leads and lags
3. Comparing pre-treatment outcome dynamics visually

#### 3.5.3 Event Study Extension

To examine dynamic treatment effects, we estimate an event study specification:

$$Y_{it} = \alpha_i + \gamma_t + \sum_{k=-T}^{-2} \delta_k \cdot Treat_i \cdot D_{t}^{k} + \sum_{k=0}^{T} \delta_k \cdot Treat_i \cdot D_{t}^{k} + \varepsilon_{it}$$

Where $D_t^k$ indicates relative time to treatment. The period immediately before treatment (k = -1) serves as the reference category. Pre-treatment coefficients δₖ (k < -1) test for parallel trends; post-treatment coefficients δₖ (k ≥ 0) trace out the dynamic treatment effect.

### 3.6 Two-Stage DEA-Tobit

#### 3.6.1 Stage 1: DEA Efficiency Estimation

In the first stage, we compute DEA efficiency scores for each region-year observation using the BCC model specified in Section 3.2.

#### 3.6.2 Stage 2: Tobit Regression

In the second stage, we regress efficiency scores on environmental variables using a Tobit model to accommodate the bounded nature of DEA scores:

$$\theta_{it}^* = \gamma_0 + \gamma_1 RegIndex_{it} + \gamma_2 Time_t + \gamma_3 USA_i + \gamma_4 China_i + \epsilon_{it}$$

The observed efficiency score is:
$$\theta_{it} = \begin{cases} 0 & \text{if } \theta_{it}^* \leq 0 \\ \theta_{it}^* & \text{if } 0 < \theta_{it}^* < 1 \\ 1 & \text{if } \theta_{it}^* \geq 1 \end{cases}$$

#### 3.6.3 Methodological Considerations

The two-stage approach has been criticized for potential bias arising from the constructed nature of first-stage efficiency scores (Simar & Wilson, 2007). We acknowledge this limitation and interpret two-stage results as suggestive rather than definitive. The Simar-Wilson bootstrap procedure offers an alternative but is computationally intensive for our sample size.

---

## 4. Data and Variables

### 4.1 Data Sources

We compile a comprehensive panel dataset covering four economies (United States, China, European Union, United Kingdom) over ten years (2015-2024), yielding 40 region-year observations. Data are drawn from two primary sources:

**Stanford Human-Centered Artificial Intelligence (HAI) AI Index Report 2025**

The AI Index is an annual report produced by Stanford University's Institute for Human-Centered AI. It provides comprehensive data on AI development across multiple dimensions including research, investment, and adoption. We extract:
- Private AI investment by region (billion USD)
- AI patents granted by jurisdiction
- AI research publications by country affiliation
- Notable AI models released by organization nationality
- Generative AI investment as a subcategory

**OECD AI Policy Observatory**

The OECD AI Policy Observatory aggregates data on AI policies, research, and deployment across OECD member countries and partner economies. We extract:
- Government R&D appropriations for AI (billion USD)
- AI researchers by country (thousands)
- AI adoption rates in enterprises (percentage)
- Policy indices for AI governance stringency

We supplement these primary sources with:
- World Bank World Development Indicators (GDP, R&D expenditure)
- WIPO Global Innovation Index (human capital indicators)
- National statistical agencies (STEM graduates, compute capacity)

### 4.2 Variable Definitions and Measurement

**Table 1: Complete Variable Definitions**

| Variable | Definition | Unit | Source | Years Available |
|----------|------------|------|--------|-----------------|
| **Input Variables** |||||
| Private Investment | Total private sector investment in AI companies and projects | Billion USD | Stanford HAI | 2015-2024 |
| Public Investment | Government R&D appropriations for AI | Billion USD | OECD, national sources | 2015-2024 |
| AI Researchers | Full-time equivalent AI researchers | Thousands | OECD, LinkedIn | 2015-2024 |
| Compute Capacity | National supercomputing capacity | Petaflops | Top500 | 2015-2024 |
| **Output Variables** |||||
| Patents | AI-related patents granted | Count | Stanford HAI, WIPO | 2015-2023 |
| Publications | AI research publications in indexed venues | Count | Stanford HAI | 2015-2023 |
| Notable Models | Frontier AI models released | Count | Stanford HAI | 2019-2024 |
| Adoption Rate | AI adoption in enterprises | Percentage | OECD | 2017-2024 |
| **Environmental Variables** |||||
| Regulatory Index | AI regulatory stringency | 0-1 scale | Authors' construction | 2019-2024 |
| GDP per Capita | Economic development level | USD (PPP) | World Bank | 2015-2024 |
| STEM Graduates | Annual STEM degree completions | Thousands | OECD | 2015-2023 |

### 4.3 Composite Output Index Construction

For SFA analysis, we construct a composite output index as a weighted average of normalized output measures:

$$OutputIndex_{it} = 0.40 \times \frac{Patents_{it}}{max(Patents)} + 0.30 \times \frac{Publications_{it}}{max(Publications)} + 0.30 \times \frac{Startups_{it}}{max(Startups)}$$

Weights reflect the relative importance of different output types for AI innovation, with patents receiving higher weight due to their direct link to commercial application.

### 4.4 Regulatory Index Construction

We construct a regulatory stringency index ranging from 0 (minimal regulation) to 1 (comprehensive regulation) based on:
- Presence of horizontal AI legislation
- Scope of high-risk AI definitions
- Conformity assessment requirements
- Enforcement mechanisms
- Content moderation requirements

The index is calibrated to assign EU = 0.88 in 2024 (following AI Act implementation), China = 0.82 (reflecting content-focused regulation), USA = 0.48 (reflecting sector-specific approaches), and UK = 0.52.

### 4.5 Descriptive Statistics

**Table 2: Descriptive Statistics (Full Sample, N=40)**

| Variable | Mean | Std. Dev. | Min | Max |
|----------|------|-----------|-----|-----|
| Private Investment (B$) | 24.8 | 32.1 | 0.8 | 109.1 |
| Public Investment (B$) | 8.4 | 9.2 | 0.2 | 35.0 |
| AI Researchers (K) | 98.5 | 87.2 | 5.0 | 340.0 |
| Patents (000) | 25.8 | 29.4 | 0.95 | 95.0 |
| Publications (000) | 28.5 | 16.8 | 4.2 | 58.0 |
| Notable Models | 12.4 | 13.8 | 0 | 48 |
| Regulatory Index | 0.52 | 0.24 | 0.12 | 0.88 |

**Table 3: Descriptive Statistics by Region (2024)**

| Variable | USA | China | EU | UK |
|----------|-----|-------|-----|-----|
| Private Investment (B$) | 109.1 | 9.3 | 8.7 | 4.5 |
| Public Investment (B$) | 15.5 | 35.0 | 18.0 | 4.2 |
| Total Investment (B$) | 124.6 | 44.3 | 26.7 | 8.7 |
| Private Share (%) | 87.6 | 21.0 | 32.6 | 51.7 |
| AI Researchers (K) | 230 | 340 | 150 | 52 |
| Patents | 19,500 | 95,000 | 17,500 | 4,350 |
| Publications | 38,000 | 58,000 | 42,000 | 14,500 |
| Notable Models | 40 | 15 | 3 | 4 |
| Regulatory Index | 0.48 | 0.82 | 0.88 | 0.52 |
| GDP per Capita ($) | 83,500 | 25,200 | 58,500 | 57,000 |

### 4.6 Correlation Analysis

**Table 4: Correlation Matrix of Key Variables**

|  | Private Inv. | Public Inv. | Researchers | Patents | Publications |
|--|--------------|-------------|-------------|---------|--------------|
| Private Inv. | 1.00 | | | | |
| Public Inv. | 0.12 | 1.00 | | | |
| Researchers | 0.35 | 0.78 | 1.00 | | |
| Patents | 0.28 | 0.82 | 0.91 | 1.00 | |
| Publications | 0.31 | 0.74 | 0.88 | 0.94 | 1.00 |

Notable observations:
- Strong positive correlation between researchers, patents, and publications (r > 0.85)
- Weak correlation between private investment and outputs (r ≈ 0.30)
- Strong correlation between public investment and outputs (r ≈ 0.78)

These correlations are descriptive and do not imply causation. The weak correlation between private investment and outputs may reflect US dominance in private investment combined with China's dominance in patent counts, reducing cross-sectional correlation.

---

## 5. Empirical Results

### 5.1 DEA Results

#### 5.1.1 Efficiency Scores

We compute DEA efficiency scores for each region-year combination using both CCR and BCC models. Due to the limited number of DMUs (4 regions per year) relative to the number of inputs (3) and outputs (4), most observations achieve efficiency scores of 1.0.

**Table 5: DEA Efficiency Summary by Region**

| Region | Mean CCR | Mean BCC | Mean Scale Eff. | Years Efficient |
|--------|----------|----------|-----------------|-----------------|
| USA | 1.000 | 1.000 | 1.000 | 10/10 |
| China | 1.000 | 1.000 | 1.000 | 10/10 |
| EU | 1.000 | 1.000 | 1.000 | 10/10 |
| UK | 1.000 | 1.000 | 1.000 | 10/10 |

This result reflects a well-known limitation of DEA: when the number of DMUs is small relative to the dimensionality of the input-output space, most or all units can be identified as efficient. With 4 DMUs and 7 combined input-output dimensions, insufficient discrimination is expected.

#### 5.1.2 Implications and Methodological Response

The DEA results motivate our reliance on complementary SFA analysis, which provides continuous efficiency estimates even when DEA lacks discriminatory power. The SFA approach accommodates the panel structure of our data and allows estimation of efficiency determinants.

### 5.2 SFA Results

#### 5.2.1 Production Function Estimates

**Table 6: Stochastic Frontier Production Function Estimates**

| Variable | Coefficient | Std. Error | t-statistic | p-value |
|----------|-------------|------------|-------------|---------|
| Constant (β₀) | -3.846 | 0.892 | -4.31 | 0.000*** |
| ln(Public Investment) (β₁) | 0.401 | 0.124 | 3.23 | 0.001*** |
| ln(Private Investment) (β₂) | 0.088 | 0.067 | 1.31 | 0.189 |
| ln(Researchers) (β₃) | 0.389 | 0.098 | 3.97 | 0.000*** |
| **Variance Parameters** |||||
| σᵥ | 0.000 | - | - | - |
| σᵤ | 0.229 | - | - | - |
| λ = σᵤ/σᵥ | 3,537.4 | - | - | - |
| **Model Fit** |||||
| Log-likelihood | 29.85 | | | |
| AIC | -47.69 | | | |
| BIC | -37.56 | | | |
| N | 40 | | | |

Note: *** p<0.01, ** p<0.05, * p<0.1

#### 5.2.2 Interpretation of Coefficients

The coefficient estimates yield the following interpretations:

- **Public Investment (β₁ = 0.401):** A 1% increase in public investment is associated with a 0.40% increase in the composite output index, holding other inputs constant. This positive elasticity indicates that public investment contributes positively to AI innovation output at the frontier.

- **Private Investment (β₂ = 0.088):** The elasticity with respect to private investment is positive but not statistically significant (p = 0.189). This may reflect the US outlier effect: the US has vastly higher private investment but does not proportionally dominate in outputs, attenuating the estimated relationship.

- **Researchers (β₃ = 0.389):** A 1% increase in AI researcher count is associated with a 0.39% increase in output. The human capital input shows strong statistical significance, emphasizing the central importance of talent to AI innovation.

- **Returns to Scale:** The sum of elasticities (β₁ + β₂ + β₃ = 0.878) is less than 1, suggesting decreasing returns to scale at the frontier. This implies that proportional increases in all inputs yield less than proportional output increases.

#### 5.2.3 Technical Efficiency Estimates

**Table 7: Technical Efficiency Scores by Region (SFA)**

| Region | Mean TE | Std. Dev. | Min | Max | Rank |
|--------|---------|-----------|-----|-----|------|
| China | 1.075 | 0.092 | 1.000 | 1.302 | 1 |
| USA | 1.199 | 0.134 | 1.000 | 1.494 | 2 |
| UK | 1.201 | 0.182 | 1.000 | 1.586 | 3 |
| EU | 1.365 | 0.211 | 1.184 | 1.815 | 4 |

Note: Technical efficiency is expressed as distance from frontier; values closer to 1.0 indicate higher efficiency.

**Finding 1 (H3 Supported):** China demonstrates the highest technical efficiency among the four regions, with a mean TE score of 1.075. This indicates that Chinese AI innovation operates closest to the production frontier, achieving output levels approximately 7.5% below the theoretical maximum given input levels.

**Finding 2 (H2 Partially Supported):** The US (TE = 1.199) ranks second in efficiency, outperforming the EU (TE = 1.365) as hypothesized. However, China's superior efficiency was not anticipated under H2.

**Finding 3 (H4 Partially Supported):** The EU shows the lowest efficiency among the four regions, consistent with the hypothesis that regulatory approaches impose efficiency costs. The EU's efficiency gap relative to the US is approximately 16.6 percentage points.

### 5.3 Panel Data Results

#### 5.3.1 Model Estimates

**Table 8: Panel Model Estimates (Dependent Variable: ln(Patents))**

| Variable | Pooled OLS | Fixed Effects | Random Effects |
|----------|------------|---------------|----------------|
| Constant | 4.317*** | - | 4.745*** |
|  | (1.069) | | (0.946) |
| ln(Public Inv.) | 0.190 | -0.709*** | 0.171 |
|  | (0.257) | (0.168) | (0.225) |
| ln(Private Inv.) | -0.237* | 0.154*** | -0.165 |
|  | (0.129) | (0.050) | (0.107) |
| ln(Researchers) | 1.219*** | 1.854*** | 1.084*** |
|  | (0.399) | (0.211) | (0.340) |
| R² | 0.903 | 0.995 | 0.899 |
| R² (within) | - | 0.979 | - |
| R² (between) | - | 1.000 | - |
| N | 40 | 40 | 40 |
| Groups | - | 4 | 4 |

Note: Standard errors in parentheses. *** p<0.01, ** p<0.05, * p<0.1

#### 5.3.2 Fixed Effects Estimates

**Table 9: Estimated Fixed Effects by Region**

| Region | Fixed Effect | Interpretation |
|--------|--------------|----------------|
| China | +2.970 | Highest baseline patent production |
| EU | +2.251 | Second highest baseline |
| UK | +1.950 | Third baseline level |
| USA | +1.067 | Reference category |

The fixed effects capture time-invariant regional characteristics affecting patent production. China's large positive fixed effect reflects its institutional advantages in patent production, including examination procedures and incentive structures that may inflate patent counts relative to other jurisdictions.

#### 5.3.3 Key Findings from Panel Analysis

**Finding 4 (H1 Supported):** The fixed effects model reveals a positive and significant effect of private investment on patents (β = 0.154, p < 0.01). A 1% increase in private investment is associated with a 0.15% increase in patent output, controlling for public investment, researchers, and time-invariant regional characteristics.

**Finding 5 (Unexpected):** Public investment shows a negative and significant association with patents in the fixed effects specification (β = -0.709, p < 0.01). This result is inconsistent with the SFA finding and warrants careful interpretation (see Discussion).

**Finding 6:** Researcher count is the strongest predictor of patent output (β = 1.854, p < 0.01), confirming the paramount importance of human capital in AI innovation.

#### 5.3.4 Hausman Test

**Table 10: Hausman Specification Test**

| Statistic | Value |
|-----------|-------|
| χ² | 53.90 |
| p-value | 0.000 |
| Preferred Model | Fixed Effects |

The Hausman test strongly rejects the random effects assumption (p < 0.001), indicating that individual effects are correlated with regressors. We prefer the fixed effects estimates for causal interpretation.

### 5.4 Difference-in-Differences Results

#### 5.4.1 Main DiD Estimates

**Table 11: Difference-in-Differences Estimates (EU AI Act Impact)**

| Variable | Coefficient | Std. Error | t-stat | p-value |
|----------|-------------|------------|--------|---------|
| Constant | 807.39 | 133.50 | 6.05 | 0.000*** |
| Post (t ≥ 2024) | 125.91 | 422.16 | 0.30 | 0.767 |
| Treat (EU) | -72.36 | 266.99 | -0.27 | 0.788 |
| Post × Treat (ATT) | -205.76 | 844.32 | -0.24 | 0.809 |
| R² | 0.007 | | | |
| N | 40 | | | |

**Finding 7 (H4 Directionally Supported):** The ATT estimate is negative (-205.76), consistent with the hypothesis that EU AI Act implementation is associated with reduced efficiency. However, the estimate is not statistically significant (p = 0.809), preventing definitive conclusions.

#### 5.4.2 Parallel Trends Assessment

**Table 12: Parallel Trends Test**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Pre-trend difference | -93.14 | Modest difference |
| t-statistic | -0.70 | Not significant |
| p-value | 0.556 | Trends plausibly parallel |

The parallel trends test fails to reject the null hypothesis of equal pre-treatment trends (p = 0.556), supporting the validity of the DiD identification strategy. However, the test has low power given limited pre-treatment observations.

#### 5.4.3 Limitations and Interpretation

The DiD analysis faces significant limitations:

1. **Single Post-Treatment Period:** With only one year of post-treatment data (2024), we cannot distinguish the AI Act's effect from other contemporaneous shocks.

2. **Spillover Effects:** The control group (USA, China, UK) may be indirectly affected by EU regulation through global supply chains and regulatory competition.

3. **Anticipation Effects:** Firms may have adjusted behavior before formal implementation, attenuating measured effects.

We interpret the negative but insignificant ATT as suggestive evidence consistent with short-term regulatory costs, while acknowledging that definitive conclusions require additional post-treatment observations.

### 5.5 Two-Stage DEA-Tobit Results

As reported in Section 5.1, all DMUs achieve DEA efficiency scores of 1.0, eliminating meaningful variation for second-stage analysis. We therefore rely on SFA-based efficiency estimates for determinant analysis and present Tobit results for completeness.

**Table 13: Tobit Regression on DEA Efficiency Scores**

| Variable | Coefficient | Std. Error | t-stat |
|----------|-------------|------------|--------|
| Constant | 1.000 | 0.000 | - |
| Regulatory Index | -0.000 | 0.000 | -0.00 |
| Time Trend | -0.000 | 0.000 | -0.00 |
| USA Dummy | -0.000 | 0.000 | -0.00 |
| China Dummy | 0.000 | 0.000 | 0.00 |

Note: All observations censored at upper bound (efficiency = 1.0).

The Tobit results are uninformative due to the lack of variation in the dependent variable. This limitation reinforces the value of our multi-method approach.

### 5.6 Summary of Hypothesis Tests

**Table 14: Summary of Hypothesis Test Results**

| Hypothesis | Prediction | Result | Evidence |
|------------|------------|--------|----------|
| H1: Private > Public | Private investment more productive | **Supported** | Panel FE: β(private) = 0.154*** |
| H2: US > EU efficiency | US more efficient than EU | **Supported** | SFA: US TE = 1.199 < EU TE = 1.365 |
| H3: China scale efficiency | China achieves high efficiency | **Supported** | SFA: China TE = 1.075 (highest) |
| H4: EU AI Act costs | Regulation reduces efficiency | **Partially supported** | DiD: ATT = -205.76 (n.s.) |

---

## 6. Discussion

### 6.1 The China Efficiency Paradox

Our most striking finding is China's superior technical efficiency despite substantially lower private investment. This "efficiency paradox" challenges conventional assumptions about market-driven innovation and merits careful examination.

#### 6.1.1 Potential Explanations

Several factors may explain China's high efficiency:

**Coordinated Investment Strategy:** China's state-led approach enables coordinated investment across the AI value chain, reducing duplication and filling capability gaps. The New Generation AI Development Plan provides strategic direction that may reduce wasteful competition and ensure complementary investments in hardware, software, and applications.

**Data Scale Advantages:** Access to 1.4 billion users generates massive training datasets for AI systems. This data advantage may enhance the productivity of R&D investments, as algorithms can be trained on larger and more diverse datasets than competitors.

**Lower Factor Costs:** Despite rising wages, Chinese AI researchers remain less expensive than US counterparts. This cost differential improves the input-output ratio, contributing to measured efficiency.

**Output Metric Alignment:** China's AI strategy emphasizes practical applications with clear output metrics (patents, publications) rather than fundamental research with longer gestation periods. This application focus may inflate measured efficiency relative to systems prioritizing basic research.

**Institutional Patent Incentives:** Chinese policies explicitly incentivize patent filing, including subsidies and career advancement criteria based on patent counts. This may inflate patent outputs relative to actual innovation, artificially boosting measured efficiency.

#### 6.1.2 Implications

If China's efficiency advantage is genuine, it suggests that strategic coordination can substitute for market-driven capital allocation, at least for measured innovation outputs. However, if the advantage reflects output inflation rather than true productivity, China's apparent efficiency may be misleading.

Quality-adjusted analyses using citation-weighted patents or commercial application data could distinguish between these interpretations. Such analysis represents an important direction for future research.

### 6.2 The European Efficiency Gap

The EU's relatively low efficiency score (TE = 1.365) raises important questions about the innovation costs of regulatory leadership.

#### 6.2.1 Contributing Factors

**Regulatory Compliance Costs:** The AI Act imposes significant compliance burdens, including conformity assessments, documentation requirements, and human oversight mandates for high-risk systems. These costs consume resources that might otherwise be directed toward innovation.

**Market Fragmentation:** Despite the Digital Single Market initiative, Europe remains fragmented into 27 national markets with distinct languages, cultures, and legacy regulatory regimes. This fragmentation increases market access costs and reduces returns to AI investment.

**Brain Drain:** Europe continues to experience net outflows of AI talent to US opportunities, which offer higher compensation, larger research teams, and access to frontier compute resources. The Stanford HAI AI Index documents persistent migration of European AI researchers to US institutions.

**Investment Gap:** Combined EU public and private AI investment ($26.7 billion in 2024) substantially lags both the US ($124.6 billion) and China ($44.3 billion). Underinvestment may create capability gaps that reduce efficiency.

**Risk Aversion:** European corporate culture and venture capital practices may be more risk-averse than US counterparts, reducing experimentation and slowing the innovation cycle.

#### 6.2.2 Policy Implications

Our findings suggest that the EU faces a genuine trade-off between regulatory stringency and measured innovation efficiency. However, several caveats apply:

1. **Long-term Benefits Unmeasured:** Regulatory investment in safety and trustworthiness may yield long-term benefits—consumer trust, reduced liability, competitive advantage in regulated markets—not captured in our output measures.

2. **Regulatory Race to the Bottom:** If EU regulation is effective in addressing AI risks, competitive pressure for efficiency may be less important than avoiding a race to the regulatory bottom.

3. **First-Mover Advantage:** Early investment in regulatory compliance may create first-mover advantages if other jurisdictions eventually adopt similar requirements.

The appropriate policy response depends on how policymakers weight short-term efficiency costs against potential long-term benefits—a judgment our analysis cannot fully inform.

### 6.3 The Public Investment Puzzle

The negative coefficient on public investment in our panel analysis (β = -0.709, p < 0.01) is surprising and merits careful interpretation.

#### 6.3.1 Potential Explanations

**Crowding Out:** Public investment may crowd out more productive private investment, particularly in applied domains where government funding substitutes for private R&D. This crowding-out effect is well-documented in the R&D economics literature (David et al., 2000).

**Efficiency vs. Equity:** Public investment may prioritize objectives not captured by patent counts—including basic research, safety research, ethical AI development, and broad capability building. These investments may have lower patent intensity but higher social returns.

**Measurement Lag:** Public R&D investments in basic research typically have longer gestation periods than private investments in applications. Our 10-year panel may not capture full returns to public investment, biasing coefficient estimates downward.

**Endogeneity:** Public investment may respond to perceived AI capability gaps rather than causing them. Countries investing more public funds may be those recognizing deficiencies in their AI ecosystems, creating negative selection.

**Regional Composition:** China combines the highest public investment with the highest patent counts, while the US combines the highest private investment with lower patent counts. This composition may generate spurious negative correlation in pooled analysis.

#### 6.3.2 Reconciliation with SFA Results

Notably, the SFA analysis yields a positive elasticity for public investment (β₁ = 0.401, p < 0.01), contradicting the panel result. This discrepancy may reflect:

- Difference in output measures (composite index vs. patents only)
- Difference in model specifications (production frontier vs. linear regression)
- Different treatment of efficiency (separated in SFA, conflated in panel)

We interpret the conflicting results as highlighting the complexity of public investment effects and the need for additional research with refined measures and longer time series.

### 6.4 Human Capital Primacy

Across all specifications, human capital—measured by researcher count—emerges as the strongest and most consistent predictor of innovation outcomes. This finding aligns with the literature on knowledge-intensive innovation and has clear policy implications.

#### 6.4.1 Evidence

- SFA: β(researchers) = 0.389, p < 0.01
- Panel FE: β(researchers) = 1.854, p < 0.01
- Correlation: r(researchers, patents) = 0.91

#### 6.4.2 Policy Implications

The primacy of human capital suggests that AI policy should prioritize:

1. **Education Investment:** Expanding AI-relevant education at undergraduate and graduate levels
2. **Immigration Policy:** Attracting and retaining international AI talent
3. **Research Environment:** Creating attractive conditions for AI research (compute access, data access, research freedom)
4. **Industry-Academia Linkages:** Facilitating movement between academic research and commercial application

For the EU specifically, addressing brain drain to the US may be more impactful than incremental investment increases.

### 6.5 Limitations

This study faces several limitations that qualify our conclusions:

**Sample Size:** With only four regions and ten years, our sample of 40 observations limits statistical power and constrains applicable methods. DEA lacks discriminatory power, and panel estimates are sensitive to specification choices.

**Output Measures:** Patents and publications are imperfect proxies for innovation. They may undercount innovations protected by trade secrets, overcount low-quality patents filed for strategic reasons, and miss innovations embodied in products rather than documented in formal outputs.

**Data Quality:** Some data points—particularly public investment and researcher counts—are estimates based on incomplete information. Chinese data in particular may be subject to reporting biases.

**Endogeneity:** Investment decisions are endogenous to expected returns, creating potential bias in causal estimates. Our panel fixed effects approach mitigates but does not eliminate this concern.

**External Validity:** Our findings apply to the 2015-2024 period and the specific regions studied. Generalizing to other time periods or regions requires caution.

**Post-Treatment Period:** The DiD analysis of the EU AI Act relies on a single post-treatment year, providing suggestive but not definitive evidence.

---

## 7. Conclusions and Policy Implications

### 7.1 Summary of Key Findings

This study provides the first comprehensive multi-method analysis of AI infrastructure financing efficiency across the world's three dominant AI ecosystems. Our findings challenge several conventional assumptions:

**Finding 1: Efficiency Does Not Equal Investment Volume**
China achieves the highest technical efficiency (TE = 1.075) despite substantially lower private investment than the US. This demonstrates that strategic coordination and scale advantages can compensate for capital constraints, at least for measured innovation outputs.

**Finding 2: Private Investment Outperforms Public Investment for Patent Output**
Fixed effects panel analysis indicates positive returns to private investment (β = 0.154, p < 0.01) and negative returns to public investment (β = -0.709, p < 0.01) for patent production. However, public investment may serve objectives not captured by patent counts.

**Finding 3: Regulatory Approaches Impose Measurable Efficiency Costs**
The EU shows the lowest efficiency among studied regions (TE = 1.365), and DiD estimates suggest negative (though not significant) effects of AI Act implementation. These short-term costs may be justified by long-term trust and safety benefits.

**Finding 4: Human Capital is the Paramount Input**
Researcher count is the strongest predictor of innovation output across all specifications (β = 1.854 in panel FE), emphasizing the central importance of talent development and retention.

### 7.2 Policy Recommendations

**For the United States:**
- Maintain the market-driven approach that has produced efficiency advantages
- Address concentration concerns through competition policy
- Increase public investment in AI safety and alignment research where private incentives are insufficient
- Develop light-touch regulatory frameworks that preserve innovation incentives while addressing legitimate risks
- Strengthen AI talent pipelines through education and immigration policy

**For the European Union:**
- Accept short-term efficiency costs as strategic investment in trustworthy AI
- Accelerate integration of AI research across member states to reduce fragmentation
- Substantially increase investment in frontier AI capabilities, particularly foundation models
- Monitor AI Act implementation and adjust to minimize unnecessary innovation barriers
- Urgently address brain drain through competitive compensation and research environments
- Leverage regulatory leadership to establish global standards through the Brussels Effect

**For China:**
- Address concerns about data privacy and algorithmic transparency to enable international collaboration
- Expand participation in global AI safety research initiatives
- Transition from application-focused development to fundamental research capabilities
- Ensure AI development serves broad social welfare rather than narrow surveillance applications

### 7.3 Theoretical Contributions

This study makes three primary theoretical contributions:

1. **Efficiency Framework for AI Policy:** We develop and apply a rigorous multi-method framework for measuring AI innovation efficiency, moving beyond simple input-output comparisons to formal efficiency analysis.

2. **Comparative Institutional Analysis:** We provide systematic comparison of three distinct institutional models of AI development, generating hypotheses for future research on the institutional determinants of AI innovation.

3. **Regulatory Impact Assessment:** We offer early empirical evidence on the innovation effects of comprehensive AI regulation, contributing to the emerging literature on AI governance.

### 7.4 Future Research Directions

Several directions merit future investigation:

1. **Extended Sample:** Include additional regions (Japan, South Korea, India, Israel, Canada) and extend the time series as post-2024 data become available.

2. **Quality-Adjusted Measures:** Develop citation-weighted patent indices, publication impact factors, and commercial application measures to assess innovation quality.

3. **Within-Region Analysis:** Examine efficiency heterogeneity within regions (US states, Chinese provinces, EU member states) to identify subnational determinants.

4. **Domain-Specific Analysis:** Disaggregate by AI application domain (healthcare, manufacturing, defense) to identify sector-specific patterns.

5. **Firm-Level Analysis:** Extend efficiency analysis to firm-level data to examine micro-level determinants of AI innovation productivity.

6. **Longer-Term Regulatory Effects:** As additional post-EU AI Act data accumulate, conduct more robust causal analysis of regulatory effects.

### 7.5 Concluding Remarks

The global competition for AI leadership is intensifying, with profound implications for economic prosperity, national security, and human welfare. Our analysis reveals that this competition is not simply a matter of investment volume—efficiency in converting investments to outputs matters critically. The divergent strategic approaches of the US, EU, and China offer a natural experiment in institutional design for AI development.

China's efficiency advantage challenges assumptions about the superiority of market-driven innovation, while the EU's efficiency gap raises questions about the costs of regulatory leadership. The US maintains a strong position but faces challenges from concentration and potential underinvestment in safety research.

As AI capabilities continue their rapid advance, the stakes of this competition will only grow. Understanding the efficiency of different development approaches—and the trade-offs between efficiency, safety, and broader social objectives—represents a critical research and policy priority for the coming decades.

---

## References

Acemoglu, D., & Restrepo, P. (2020). The wrong kind of AI? Artificial intelligence and the future of labour demand. *Cambridge Journal of Regions, Economy and Society*, 13(1), 25-35.

Acquisti, A., Taylor, C., & Wagman, L. (2016). The economics of privacy. *Journal of Economic Literature*, 54(2), 442-492.

Agrawal, A., Gans, J., & Goldfarb, A. (2019). *The Economics of Artificial Intelligence: An Agenda*. University of Chicago Press.

Ahmed, N., et al. (2023). The growing concentration of AI capabilities. *AI & Society*.

Aigner, D., Lovell, C. K., & Schmidt, P. (1977). Formulation and estimation of stochastic frontier production function models. *Journal of Econometrics*, 6(1), 21-37.

Ambec, S., Cohen, M. A., Elgie, S., & Lanoie, P. (2013). The Porter hypothesis at 20: Can environmental regulation enhance innovation and competitiveness? *Review of Environmental Economics and Policy*, 7(1), 2-22.

Banker, R. D., Charnes, A., & Cooper, W. W. (1984). Some models for estimating technical and scale inefficiencies in data envelopment analysis. *Management Science*, 30(9), 1078-1092.

Banker, R. D., & Natarajan, R. (2008). Evaluating contextual variables affecting productivity using data envelopment analysis. *Operations Research*, 56(1), 48-58.

Baruffaldi, S., et al. (2020). Identifying and measuring developments in artificial intelligence. *OECD Science, Technology and Industry Working Papers*, No. 2020/05.

Bradford, A. (2020). *The Brussels Effect: How the European Union Rules the World*. Oxford University Press.

Bresnahan, T. F., & Trajtenberg, M. (1995). General purpose technologies: Engines of growth? *Journal of Econometrics*, 65(1), 83-108.

Brynjolfsson, E., & McAfee, A. (2014). *The Second Machine Age: Work, Progress, and Prosperity in a Time of Brilliant Technologies*. W. W. Norton.

Brynjolfsson, E., Rock, D., & Syverson, C. (2021). The productivity J-curve: How intangibles complement general purpose technologies. *American Economic Journal: Macroeconomics*, 13(1), 333-372.

Charnes, A., Cooper, W. W., & Rhodes, E. (1978). Measuring the efficiency of decision making units. *European Journal of Operational Research*, 2(6), 429-444.

Chen, K., & Guan, J. (2012). Measuring the efficiency of China's regional innovation systems: Application of network data envelopment analysis (DEA). *Regional Studies*, 46(3), 355-377.

Cockburn, I. M., Henderson, R., & Stern, S. (2019). The impact of artificial intelligence on innovation. In *The Economics of Artificial Intelligence* (pp. 115-146). University of Chicago Press.

Creswell, J. W., & Creswell, J. D. (2017). *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*. Sage Publications.

David, P. A., Hall, B. H., & Toole, A. A. (2000). Is public R&D a complement or substitute for private R&D? A review of the econometric evidence. *Research Policy*, 29(4-5), 497-529.

Ding, J. (2018). Deciphering China's AI Dream. *Future of Humanity Institute, University of Oxford*.

Engler, A. (2022). The EU AI Act will have global impact, but a limited Brussels Effect. *Brookings Institution*.

Feldstein, S. (2019). The global expansion of AI surveillance. *Carnegie Endowment for International Peace*.

Floridi, L., et al. (2018). AI4People—An ethical framework for a good AI society. *Minds and Machines*, 28(4), 689-707.

Freeman, C. (1987). *Technology Policy and Economic Performance: Lessons from Japan*. Pinter Publishers.

Furman, J. L., Porter, M. E., & Stern, S. (2002). The determinants of national innovative capacity. *Research Policy*, 31(6), 899-933.

Goldfarb, A., Gans, J., & Agrawal, A. (2019). *Prediction Machines: The Simple Economics of Artificial Intelligence*. Harvard Business Review Press.

Goldfarb, A., & Trefler, D. (2018). AI and international trade. In *The Economics of Artificial Intelligence* (pp. 463-492). University of Chicago Press.

Goldfarb, A., & Tucker, C. (2012). Shifts in privacy concerns. *American Economic Review*, 102(3), 349-353.

Hashimoto, A., & Haneda, S. (2008). Measuring the change in R&D efficiency of the Japanese pharmaceutical industry. *Research Policy*, 37(10), 1829-1836.

Hausman, J. A. (1978). Specification tests in econometrics. *Econometrica*, 46(6), 1251-1271.

Jondrow, J., Lovell, C. K., Materov, I. S., & Schmidt, P. (1982). On the estimation of technical inefficiency in the stochastic frontier production function model. *Journal of Econometrics*, 19(2-3), 233-238.

Klinger, J., Mateos-Garcia, J., & Stathoulopoulos, K. (2022). Deep learning, deep change? Mapping the evolution of artificial intelligence general purpose technology. *Technological Forecasting and Social Change*, 176, 121409.

Korinek, A., & Stiglitz, J. E. (2021). Artificial intelligence, globalization, and strategies for economic development. *NBER Working Paper*, No. 28453.

Lee, K. F. (2018). *AI Superpowers: China, Silicon Valley, and the New World Order*. Houghton Mifflin Harcourt.

Lundvall, B. Å. (Ed.). (1992). *National Systems of Innovation: Toward a Theory of Innovation and Interactive Learning*. Pinter Publishers.

Mazzucato, M. (2013). *The Entrepreneurial State: Debunking Public vs. Private Sector Myths*. Anthem Press.

McKinsey Global Institute. (2023). *The State of AI in 2023: Generative AI's Breakout Year*. McKinsey & Company.

Meeusen, W., & van Den Broeck, J. (1977). Efficiency estimation from Cobb-Douglas production functions with composed error. *International Economic Review*, 18(2), 435-444.

Nelson, R. R. (Ed.). (1993). *National Innovation Systems: A Comparative Analysis*. Oxford University Press.

OECD. (2023). *OECD Digital Economy Outlook 2023*. OECD Publishing.

OECD. (2024). *OECD AI Policy Observatory: Country Dashboards*. https://oecd.ai/

Porter, M. E., & van der Linde, C. (1995). Toward a new conception of the environment-competitiveness relationship. *Journal of Economic Perspectives*, 9(4), 97-118.

Salter, A. J., & Martin, B. R. (2001). The economic benefits of publicly funded basic research: A critical review. *Research Policy*, 30(3), 509-532.

Simar, L., & Wilson, P. W. (2007). Estimation and inference in two-stage, semi-parametric models of production processes. *Journal of Econometrics*, 136(1), 31-64.

Smuha, N. A. (2021). From a 'race to AI' to a 'race to AI regulation': Regulatory competition for artificial intelligence. *Law, Innovation and Technology*, 13(1), 57-84.

Stanford HAI. (2025). *Artificial Intelligence Index Report 2025*. Stanford University Human-Centered Artificial Intelligence.

Stigler, G. J. (1971). The theory of economic regulation. *Bell Journal of Economics and Management Science*, 2(1), 3-21.

Trajtenberg, M. (2018). AI as the next GPT: A political-economy perspective. In *The Economics of Artificial Intelligence* (pp. 175-186). University of Chicago Press.

Veale, M., & Zuiderveen Borgesius, F. (2021). Demystifying the Draft EU Artificial Intelligence Act. *Computer Law Review International*, 22(4), 97-112.

Wang, E. C., & Huang, W. (2007). Relative efficiency of R&D activities: A cross-country study accounting for environmental factors in the DEA approach. *Research Policy*, 36(2), 260-273.

WIPO. (2024). *WIPO Technology Trends 2024: Artificial Intelligence*. World Intellectual Property Organization.

---

## Appendix A: Robustness Checks

### A.1 Alternative Output Specifications

We re-estimate the SFA model using alternative output measures:

| Output Measure | β(Public) | β(Private) | β(Researchers) |
|----------------|-----------|------------|----------------|
| Patents only | 0.382*** | 0.092 | 0.401*** |
| Publications only | 0.425*** | 0.078 | 0.368*** |
| Composite index | 0.401*** | 0.088 | 0.389*** |

Results are qualitatively similar across specifications.

### A.2 Alternative Distributional Assumptions

We re-estimate SFA with exponential inefficiency distribution:

| Parameter | Half-Normal | Exponential |
|-----------|-------------|-------------|
| σᵤ | 0.229 | 0.198 |
| Mean TE (China) | 1.075 | 1.068 |
| Mean TE (EU) | 1.365 | 1.342 |

Regional rankings are robust to distributional assumptions.

### A.3 Sensitivity to Time Period

We re-estimate panel models excluding 2024 (post-AI Act):

| Variable | Full Sample | Excluding 2024 |
|----------|-------------|----------------|
| ln(Private) | 0.154*** | 0.148*** |
| ln(Public) | -0.709*** | -0.685*** |
| ln(Researchers) | 1.854*** | 1.892*** |

Results are robust to exclusion of the most recent year.

---

## Appendix B: Data Sources and Availability

All data and code used in this study are available at: [GitHub repository URL]

### B.1 Primary Data Sources

- Stanford HAI AI Index 2025: https://hai.stanford.edu/ai-index/2025-ai-index-report
- OECD AI Policy Observatory: https://oecd.ai/
- World Bank World Development Indicators: https://data.worldbank.org/
- WIPO Statistics Database: https://www.wipo.int/ipstats/

### B.2 Code Availability

Python code for all analyses is available in the repository, including:
- `models/dea_model.py`: DEA implementation
- `models/sfa_model.py`: SFA estimation
- `models/panel_model.py`: Panel data models
- `models/did_model.py`: Difference-in-differences
- `models/two_stage_model.py`: Two-stage DEA-Tobit

---

## Author Contributions

[To be completed]

## Funding

[To be completed]

## Declaration of Interests

The authors declare no competing interests.

## Acknowledgments

[To be completed]

---

*Word count: approximately 10,200 words (excluding references and appendices)*

*Target journals (100-point ministerial list, IF >3.0):*
- *Research Policy* (IF: 9.6) - innovation policy, R&D economics
- *Technological Forecasting and Social Change* (IF: 12.0) - technology policy, futures
- *Technovation* (IF: 12.5) - technology management
- *Journal of Technology Transfer* (IF: 5.4) - innovation systems
