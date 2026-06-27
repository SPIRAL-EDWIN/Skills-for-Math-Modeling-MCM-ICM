# AI Usage Log - Example Template

**Team Number**: 123456  
**Problem**: A  
**Competition**: MCM/ICM 2026

---

## Log Entry #1

**Time**: 2026-01-29 14:30  
**Tool/Model**: OpenAI ChatGPT GPT-4 (Web interface, chat.openai.com)  
**Type**: LLM  
**Purpose**: Polishing introduction paragraph for academic tone  
**Location**: Section 1 (Introduction), paragraph 2

### Query (Exact Wording)
```
Please polish the following paragraph for academic tone and clarity:

"Our model uses a SIR model to predict how the disease spreads. We think this is good because it's simple and works well. The model has three parts: S for people who can get sick, I for people who are sick, and R for people who got better."
```

### Output (Complete Response)
```
Here's a polished version with improved academic tone:

"Our approach employs a Susceptible-Infected-Recovered (SIR) compartmental model to simulate disease transmission dynamics. This model is particularly well-suited for our analysis due to its parsimony and empirical validation in epidemiological literature. The model partitions the population into three mutually exclusive compartments: Susceptible (S) individuals who are at risk of infection, Infected (I) individuals who are currently infectious, and Recovered (R) individuals who have acquired immunity."
```

### Verification and Revision
1. **Verified**: 
   - Confirmed that "parsimony" is appropriate terminology (checked against epidemiology textbooks)
   - Verified that SIR model is indeed validated in literature (cross-referenced with our citations [1, 2])
   - Checked that terminology matches our notation table

2. **Revised**: 
   - Changed "employs" back to "uses" for simplicity
   - Removed "mutually exclusive" as it's implied
   - Kept "compartmental model" terminology as it's standard
   - Simplified "empirical validation" to "well-established"

3. **Final Usage**: 
   - Used approximately 60% of AI output
   - Final paragraph is a blend of AI suggestions and our original wording
   - Specific phrase "transmission dynamics" was adopted from AI
   - Final version: "Our approach uses a Susceptible-Infected-Recovered (SIR) compartmental model to simulate disease transmission dynamics. This well-established model is particularly suited for our analysis. The model partitions the population into three compartments: Susceptible (S) individuals at risk of infection, Infected (I) individuals who are infectious, and Recovered (R) individuals with acquired immunity."

### Notes
This was our first use of ChatGPT. We were careful to verify terminology against our reference materials.

---

## Log Entry #2

**Time**: 2026-01-29 16:45  
**Tool/Model**: OpenAI ChatGPT GPT-4 (Web interface, chat.openai.com)  
**Type**: LLM  
**Purpose**: Generating Python code structure for data preprocessing  
**Location**: code/data_cleaner.py

### Query (Exact Wording)
```
Write a Python function that removes outliers from a pandas DataFrame using the IQR (Interquartile Range) method. The function should:
1. Take a DataFrame and column name as input
2. Calculate Q1, Q3, and IQR
3. Define outliers as values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
4. Return a new DataFrame with outliers removed
5. Print how many rows were removed
```

### Output (Complete Response)
```python
import pandas as pd

def remove_outliers_iqr(df, column_name):
    """
    Remove outliers from a DataFrame column using the IQR method.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    column_name (str): Name of the column to check for outliers
    
    Returns:
    pd.DataFrame: DataFrame with outliers removed
    """
    # Calculate Q1, Q3, and IQR
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter outliers
    df_filtered = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    
    # Print removed count
    removed_count = len(df) - len(df_filtered)
    print(f"Removed {removed_count} outliers from column '{column_name}'")
    
    return df_filtered

# Example usage
# df_clean = remove_outliers_iqr(df, 'price')
```

### Verification and Revision
1. **Verified**: 
   - Tested function on sample data with known outliers (5 data points manually identified as outliers)
   - Confirmed IQR formula is correct (1.5 * IQR is standard statistical practice)
   - Verified function returns correct DataFrame (compared output with manual calculation)
   - Checked that function handles edge cases (empty DataFrame, all values are outliers)

2. **Revised**: 
   - Added error handling for empty DataFrame:
     ```python
     if df.empty or column_name not in df.columns:
         raise ValueError(f"Invalid DataFrame or column name")
     ```
   - Added option to return both cleaned data and outliers:
     ```python
     return df_filtered, df_outliers
     ```
   - Changed variable names for clarity (df_filtered → df_clean)
   - Added logging instead of print for production use

3. **Final Usage**: 
   - Core logic (80%) is from ChatGPT
   - Error handling and logging (20%) is human-added
   - Final function is production-ready after modifications
   - Function is now part of our data_cleaner.py module (lines 23-58)

### Notes
ChatGPT was very helpful here. The suggested code was mostly correct, but we added robustness features for production use.

---

## Log Entry #3

**Time**: 2026-01-29 20:45  
**Tool/Model**: DeepL Translator (Web interface, deepl.com, accessed 2026-01-29)  
**Type**: Translation  
**Purpose**: Translate Chinese literature abstracts to English for literature review  
**Location**: Literature review notes (not directly in final paper)

### Query (Exact Wording)
```
[NOTE: For translation tools, full input text is NOT required per COMAP policy]

We translated 5 Chinese academic paper abstracts, approximately 2000 words total.

Source papers:
1. Zhang, L., Wang, H., & Liu, Y. (2023). 非线性规划方法在资源分配中的应用研究 [Application of Nonlinear Programming Methods in Resource Allocation]. 运筹学学报, 31(2), 45-58.

2. Li, M., Chen, X., & Wu, S. (2022). 基于遗传算法的多目标优化问题求解 [Multi-objective Optimization Problem Solving Based on Genetic Algorithm]. 系统工程理论与实践, 42(5), 1234-1245.

3. Wang, F., & Zhou, J. (2021). 传染病动力学模型的参数估计方法 [Parameter Estimation Methods for Epidemic Dynamics Models]. 应用数学学报, 44(3), 367-382.

4. Chen, Y., Liu, Q., & Zhang, W. (2023). 网络中心性分析及其在社交网络中的应用 [Network Centrality Analysis and Its Application in Social Networks]. 计算机学报, 46(1), 89-104.

5. Zhao, K., & Sun, L. (2022). 敏感性分析在数学建模中的应用 [Application of Sensitivity Analysis in Mathematical Modeling]. 数学建模及其应用, 11(4), 23-35.
```

### Output (Complete Response)
```
[NOTE: Full translation output is NOT required per COMAP policy]

DeepL provided English translations for all 5 abstracts.

Key translated terms:
- 非线性规划 → nonlinear programming
- 遗传算法 → genetic algorithm
- 多目标优化 → multi-objective optimization
- 传染病动力学 → epidemic dynamics
- 参数估计 → parameter estimation
- 网络中心性 → network centrality
- 敏感性分析 → sensitivity analysis
- 数学建模 → mathematical modeling
```

### Verification and Revision
1. **Verified**: 
   - Cross-checked technical terms against English-Chinese Mathematical Dictionary (Higher Education Press, 2018)
   - Confirmed translations match standard terminology in English literature
   - Verified logical consistency between Chinese and English versions by having bilingual team member read both
   - Checked that mathematical symbols and formulas were preserved correctly

2. **Revised**: 
   - Corrected "hereditary algorithm" to "genetic algorithm" (DeepL mistake with 遗传算法)
   - Adjusted sentence structure for better English flow in 3 abstracts
   - Clarified ambiguous pronoun references in translation
   - Ensured consistency of terminology across all 5 abstracts

3. **Final Usage**: 
   - Translations were used to understand prior work and identify relevant methodologies
   - Did NOT copy-paste translations into our paper
   - Used translations to inform our literature review section
   - Cited original Chinese papers with English translation of titles in our references
   - Example citation: Zhang, L., Wang, H., & Liu, Y. (2023). Application of nonlinear programming methods in resource allocation [非线性规划方法在资源分配中的应用研究]. Operations Research Transactions, 31(2), 45-58. (In Chinese)

### Notes
Translation quality was good overall, but technical terms required manual verification. DeepL sometimes uses literal translations that don't match standard mathematical terminology.

---

## Log Entry #4

**Time**: 2026-01-30 09:15  
**Tool/Model**: GitHub Copilot (VSCode extension, version 1.150.0)  
**Type**: Code Copilot  
**Purpose**: Auto-complete data preprocessing and visualization functions  
**Location**: code/data_cleaner.py (lines 23-45, 78-92), code/visualization.py (lines 34-67)

### Query (Exact Wording)
```
[NOTE: For code copilots, we describe the context rather than exact prompts, as Copilot works via auto-completion]

Context: We wrote function signatures and comments, and Copilot auto-completed the implementations.

Example 1 (data_cleaner.py, line 23):
# Function to normalize data using min-max scaling
def normalize_minmax(df, columns):
    # [Copilot auto-completed the rest]

Example 2 (visualization.py, line 34):
# Function to create a time series plot with confidence intervals
def plot_timeseries_ci(time, data, ci_lower, ci_upper):
    # [Copilot auto-completed the rest]
```

### Output (Complete Response)
```python
# Example 1: Copilot suggested for normalize_minmax
def normalize_minmax(df, columns):
    df_normalized = df.copy()
    for col in columns:
        min_val = df[col].min()
        max_val = df[col].max()
        df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
    return df_normalized

# Example 2: Copilot suggested for plot_timeseries_ci
def plot_timeseries_ci(time, data, ci_lower, ci_upper):
    plt.figure(figsize=(10, 6))
    plt.plot(time, data, 'b-', linewidth=2, label='Prediction')
    plt.fill_between(time, ci_lower, ci_upper, alpha=0.3, label='95% CI')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
```

### Verification and Revision
1. **Verified**: 
   - Tested all Copilot-generated functions with unit tests on sample data
   - Verified normalize_minmax handles edge cases (constant column, single value)
   - Confirmed plot_timeseries_ci produces correct visualization (compared with manual matplotlib code)
   - Checked that functions match our coding style and conventions

2. **Revised**: 
   - Added error handling for edge cases:
     ```python
     if max_val == min_val:
         df_normalized[col] = 0  # Handle constant column
     ```
   - Added comprehensive docstrings explaining parameters, return values, and edge cases
   - Modified plot_timeseries_ci to accept custom colors and labels
   - Added save_figure option to save plots to file
   - Renamed variables for clarity (df_normalized → df_scaled)
   - Added type hints for better code documentation

3. **Final Usage**: 
   - Across all files, approximately 60% human-written, 40% Copilot-assisted
   - All critical algorithms and model logic were designed by humans
   - Copilot primarily assisted with:
     - Boilerplate code (imports, basic data manipulation)
     - Standard visualization patterns (matplotlib setup)
     - Common data processing operations (normalization, filtering)
   - We rejected approximately 30% of Copilot suggestions that didn't fit our needs or contained logical errors
   - Final code passed all unit tests and integration tests

### Notes
GitHub Copilot was very helpful for speeding up implementation of standard functions. However, we always reviewed and tested suggestions before accepting them. We found that Copilot is best for well-established patterns, but human oversight is essential for domain-specific logic.

---

## Log Entry #5

**Time**: 2026-01-30 15:45  
**Tool/Model**: Claude 3.5 Sonnet (Web interface, claude.ai)  
**Type**: LLM  
**Purpose**: Debugging Python code for optimization model  
**Location**: code/optimizer.py, lines 156-203

### Query (Exact Wording)
```
I'm getting this error when running my optimization code:

ValueError: operands could not be broadcast together with shapes (100,) (99,) 

Here's the relevant code:

```python
def objective_function(x, data):
    predictions = model.predict(x)
    residuals = data - predictions
    return np.sum(residuals**2)

# Data setup
time_points = np.linspace(0, 10, 100)
observed_data = load_data()  # Returns array of length 99
initial_guess = [1.0, 2.0, 0.5]

# Optimization
result = scipy.optimize.minimize(
    objective_function,
    initial_guess,
    args=(observed_data,),
    method='Nelder-Mead'
)
```

The error occurs in the line `residuals = data - predictions`. Can you help me understand what's wrong and how to fix it?
```
```

### Output (Complete Response)
```
The error occurs because your `time_points` array has 100 elements, but your `observed_data` has only 99 elements. When you compute predictions using `model.predict(x)`, it likely generates 100 predictions (one for each time point), but you're trying to subtract an array of 99 observations from it.

Here are a few ways to fix this:

**Option 1: Ensure data and time points match**
```python
# Check lengths before optimization
assert len(time_points) == len(observed_data), \
    f"Length mismatch: {len(time_points)} time points vs {len(observed_data)} data points"

# Or adjust time_points to match data
time_points = np.linspace(0, 10, len(observed_data))
```

**Option 2: Slice predictions to match data length**
```python
def objective_function(x, data):
    predictions = model.predict(x)
    predictions = predictions[:len(data)]  # Slice to match data length
    residuals = data - predictions
    return np.sum(residuals**2)
```

**Option 3: Investigate why data is missing a point**
```python
# Check if data loading is correct
print(f"Expected data points: {len(time_points)}")
print(f"Actual data points: {len(observed_data)}")
# Perhaps there's a missing data point that should be handled
```

I recommend Option 1 (ensuring lengths match from the start) as it's the most robust approach. The mismatch likely indicates a data loading issue that should be investigated.
```

### Verification and Revision
1. **Verified**: 
   - Investigated data loading and found that `load_data()` was indeed returning 99 points (one missing data point at t=5.0)
   - Confirmed Claude's diagnosis was correct (shape mismatch between predictions and observations)
   - Tested all three suggested fixes on our actual data
   - Verified that fixing the length mismatch resolved the error

2. **Revised**: 
   - Chose Option 1 (ensure lengths match) as Claude recommended
   - Added data validation at the start of our script:
     ```python
     # Validate data before optimization
     if len(observed_data) != len(time_points):
         print(f"Warning: Data length mismatch. Adjusting time points.")
         time_points = time_points[:len(observed_data)]
     ```
   - Added better error messages for debugging
   - Documented the missing data point issue in our code comments

3. **Final Usage**: 
   - Claude's explanation helped us understand the root cause
   - We used Claude's Option 1 suggestion with minor modifications
   - Approximately 70% of the fix was based on Claude's suggestion
   - 30% was our own addition (better error handling and documentation)
   - The bug was resolved and optimization now runs successfully

### Notes
Claude was very helpful for debugging. The explanation was clear and the suggested fixes were practical. We always tested the suggestions before implementing them in our production code.

---

## Summary Statistics

**Total AI Interactions Logged**: 5 (as of 2026-01-30 16:00)

**Breakdown by Tool Type**:
- LLM (ChatGPT): 2 interactions
- LLM (Claude): 1 interaction
- Translation (DeepL): 1 interaction
- Code Copilot (GitHub Copilot): 1 interaction (multiple auto-completions)

**Breakdown by Purpose**:
- Text polishing: 1
- Code generation: 2
- Translation: 1
- Debugging: 1

**Total Time Spent Logging**: ~15 minutes (3 min per entry average)

**Verification Quality**: All interactions have specific verification notes with concrete actions taken.

---

**Notes for Final Report**:
- All prompts are exact (copy-pasted)
- All outputs are complete (not summarized, except translation per COMAP policy)
- All verification notes are specific and detailed
- No AI-generated citations were used (all citations were verified by humans)
- All critical decisions (model selection, interpretation) were made by humans
