# It's a Statistical Analysis script to perform basic data analysis on the fetched NASA data.

import pymannkendall as mk
import numpy as np

def analyze_trend(data_array):
    """
    1D Data Array/List par Mann-Kendall Test perform karta hai.
    
    Parameters:
        data_array (list or np.ndarray): Time-series 1D numeric data.
        
    Returns:
        dict: Trend direction, p-value, slope aur statistical significance detail.
    """
    # 1. Mann-Kendall test execute karna
    result = mk.original_test(data_array)
    
    # 2. Trend direction classify karna
    if result.trend == 'increasing':
        trend_direction = "Increasing"
    elif result.trend == 'decreasing':
        trend_direction = "Decreasing"
    else:
        trend_direction = "No Trend"
        
    # 3. Output structure ready karna
    output = {
        "trend": trend_direction,
        "p_value": result.p,
        "is_significant": result.h,  # True agar p-value < 0.05
        "slope": result.slope        # Sen's slope (rate of change)
    }
    
    return output

# --- Example Testing / Usage ---
if __name__ == "__main__":
    # Test Data 1: Clear Increasing Trend
    sample_data_1 = [12, 14, 15, 18, 21, 24, 27, 30]
    
    # Test Data 2: Random Noise (No Clear Trend)
    sample_data_2 = [10, 15, 11, 14, 10, 13, 12, 11]

    print("--- Test 1 Analysis ---")
    res1 = analyze_trend(sample_data_1)
    print(f"Trend Direction: {res1['trend']}")
    print(f"p-value: {res1['p_value']:.4f}")
    print(f"Statistically Significant: {res1['is_significant']}")
    print(f"Slope: {res1['slope']:.4f}\n")

    print("--- Test 2 Analysis ---")
    res2 = analyze_trend(sample_data_2)
    print(f"Trend Direction: {res2['trend']}")
    print(f"p-value: {res2['p_value']:.4f}")
    print(f"Statistically Significant: {res2['is_significant']}")
    print(f"Slope: {res2['slope']:.4f}")