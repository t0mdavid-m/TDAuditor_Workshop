import matplotlib.pyplot as plt

from matplotlib.patches import Patch


def create_boxplot(data, quartile_cols, title, ylabel, grouped=False, filter_engine=None, figsize=(12, 6)):
    """
    Create boxplots from quartile data.
    
    Parameters:
    - data: DataFrame with the data
    - quartile_cols: List of 5 columns [min, q1, q2, q3, max]
    - title: Plot title
    - ylabel: Y-axis label
    - grouped: If True, group by DeconvolutionEngine
    - filter_engine: If provided, filter to this engine only
    - figsize: Figure size tuple
    """
    
    # Filter data if engine specified
    if filter_engine:
        plot_data = data[data['DeconvolutionEngine'] == filter_engine].copy()
    else:
        plot_data = data.copy()
    
    _, ax = plt.subplots(figsize=figsize)
    
    box_stats = []
    positions = []
    colors = ['#66c2a5', '#fc8d62', '#8da0cb']  # Set2 palette colors
    
    if grouped:
        # Grouped boxplots by deconvolution engine
        engines = plot_data['DeconvolutionEngine'].unique()
        source_files = plot_data['SourceFile'].unique()

        # Prepare data for injection into matplotlib
        pos = 1
        for source in source_files:
            for engine in engines:
                row_data = plot_data[(plot_data['SourceFile'] == source) & (plot_data['DeconvolutionEngine'] == engine)]
                if not row_data.empty:
                    row = row_data.iloc[0]
                    stats = {
                        'med': row[quartile_cols[2]],  # median (Q2)
                        'q1': row[quartile_cols[1]],   # first quartile
                        'q3': row[quartile_cols[3]],   # third quartile
                        'whislo': row[quartile_cols[0]],  # lower whisker (min)
                        'whishi': row[quartile_cols[4]],  # upper whisker (max)
                        'fliers': []
                    }
                    box_stats.append(stats)
                    positions.append(pos)
                pos += 1
            pos += 1  # Add space between source files
        
        # Create boxplot
        bp = ax.bxp(box_stats, positions=positions, patch_artist=True, widths=0.8,
                    medianprops=dict(color="black", linewidth=2, linestyle="-"))
        
        # Color boxes by engine
        for i, patch in enumerate(bp['boxes']):
            engine_idx = i % len(engines)
            patch.set_facecolor(colors[engine_idx])
        
        # Set x-axis labels for grouped
        tick_positions = [2 + i*4 for i in range(len(source_files))]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(source_files, rotation=45, ha='right')
        
        # Create legend
        legend_elements = [Patch(facecolor=colors[i], label=engine) for i, engine in enumerate(engines)]
        ax.legend(handles=legend_elements, title='Deconvolution Engine', bbox_to_anchor=(1.05, 1), loc='upper left')
        
    else:
        # Single boxplots
        pos = 1
        for idx, row in plot_data.iterrows():
            stats = {
                'med': row[quartile_cols[2]],  # median (Q2)
                'q1': row[quartile_cols[1]],   # first quartile
                'q3': row[quartile_cols[3]],   # third quartile
                'whislo': row[quartile_cols[0]],  # lower whisker (min)
                'whishi': row[quartile_cols[4]],  # upper whisker (max)
                'fliers': []
            }
            box_stats.append(stats)
            positions.append(pos)
            pos += 1
        
        # Create boxplot
        bp = ax.bxp(box_stats, positions=positions, patch_artist=True, widths=0.8,
                    medianprops=dict(color="black", linewidth=2, linestyle="-"))
        
        # Set x-axis labels for single
        ax.set_xticks(range(1, len(plot_data) + 1))
        ax.set_xticklabels(plot_data['SourceFile'], rotation=45, ha='right')
    
    ax.set_xlabel('Source File')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=14)
    
    plt.tight_layout()
    plt.show()


