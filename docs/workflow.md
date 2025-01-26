# Health Economic Impact Analysis Workflow

```mermaid
graph TD
    A[Intervention Input] --> B[Initial LLM Analysis]
    
    subgraph "1. Impact Identification"
        B --> C[Generate Health Benefits List]
        C --> D[Categorize by Impact Type]
        D --> |Direct Health| E1[QALY Impacts]
        D --> |Economic| E2[Cost Savings]
        D --> |Societal| E3[GDP Effects]
    end
    
    subgraph "2. Model Development"
        E1 --> F1[Define QALY Equations]
        E2 --> F2[Define Cost Equations]
        E3 --> F3[Define GDP Equations]
        F1 & F2 & F3 --> G[Parameter Identification]
        G --> H[Model Validation by Expert]
    end
    
    subgraph "3. Evidence Collection"
        H --> I[Systematic Literature Search]
        I --> J[Web Search for Recent Data]
        I --> K[Meta-analyses Review]
        J & K --> L[Data Extraction & Validation]
        L --> M[Parameter Range Definition]
    end
    
    subgraph "4. Analysis & Validation"
        M --> N[Parameter Sensitivity Testing]
        N --> O[Monte Carlo Simulation]
        O --> P[Uncertainty Quantification]
        P --> Q[Expert Review of Results]
    end
    
    subgraph "5. Report Generation"
        Q --> R[LLM Report Draft]
        R --> S[Citation Integration]
        S --> T[Methodology Documentation]
        T --> U[Limitations Analysis]
        U --> V[Final Report Generation]
    end

```


## Key Improvements Over Basic Workflow

1. **Rigorous Validation**
   - Expert review at multiple stages
   - Systematic literature review process
   - Quality assessment of evidence

2. **Better Uncertainty Handling**
   - Monte Carlo simulation
   - Parameter range definition
   - Confidence interval calculation

3. **Enhanced Documentation**
   - Methodology transparency
   - Assumption documentation
   - Limitation acknowledgment

4. **Quality Standards**
   - PRISMA guidelines for literature review
   - CHEERS guidelines for reporting
   - Standardized quality assessment tools

5. **Comprehensive Review**
   - Multiple data sources
   - Expert validation
   - Cross-reference with existing models

## Implementation Notes

1. **Automation Opportunities**
   - Literature search and data extraction
   - Parameter range calculation
   - Report template generation
   - Visualization creation

2. **Quality Control Points**
   - Expert review stages
   - Data validation checks
   - Cross-reference verification
   - Result plausibility checks

3. **Documentation Requirements**
   - Methodology description
   - Data source tracking
   - Assumption listing
   - Limitation documentation

4. **Tool Integration**
   - Literature database APIs
   - Statistical analysis packages
   - Visualization libraries
   - Report generation tools 