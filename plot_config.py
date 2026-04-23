"""
Academic style plotting configuration module
English-only version for reliable display
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import platform

# ==================== Font Configuration ====================

def setup_english_font():
    """Configure English fonts for reliable display"""
    system = platform.system()

    # Use standard English fonts
    if system == 'Windows':
        font_names = ['Arial', 'Times New Roman', 'DejaVu Sans']
    elif system == 'Darwin':
        font_names = ['Arial', 'Helvetica', 'Times New Roman', 'DejaVu Sans']
    else:
        font_names = ['DejaVu Sans', 'Arial', 'Liberation Sans']

    # Configure matplotlib - use sans-serif for reliability
    plt.rcParams.update({
        'font.family': ['sans-serif'],
        'font.sans-serif': font_names + plt.rcParams['font.sans-serif'],
        'axes.unicode_minus': False,
    })

    return font_names[0]

# ==================== Color Schemes ====================

# Academic paper style colors (based on plot-from-data skill)
COLORS = {
    # Primary colors
    'primary': '#3B6BB5',      # Main blue
    'secondary': '#3A8B3A',    # Main green
    'accent': '#C0392B',       # Accent red

    # Contrast colors
    'purple': '#5B0DAD',       # Deep purple
    'teal': '#5BBCCA',         # Teal
    'orange': '#E8845A',       # Medium orange

    # Neutral colors
    'dark_gray': '#707070',
    'medium_gray': '#A9A9A9',
    'light_gray': '#D3D3D3',
    'very_light_gray': '#EBEBEB',

    # Gradient groups
    'warm_gradient': ['#F5C5A3', '#E8845A', '#C0392B'],
    'cool_gradient': ['#B8D4E3', '#6BAED6', '#3182BD'],

    # Group comparison colors (SOE vs non-SOE)
    'soe': '#C0392B',          # SOE - red
    'nonsoe': '#3182BD',       # Non-SOE - blue
}

# Seaborn palettes
SEABORN_PALETTES = {
    'default': sns.color_palette([COLORS['primary'], COLORS['secondary'], COLORS['accent'],
                                   COLORS['purple'], COLORS['teal'], COLORS['orange']]),
    'coolwarm': sns.color_palette("vlag", as_cmap=True),
    'diverging': sns.diverging_palette(240, 10, as_cmap=True),
    'sequential': sns.color_palette("viridis", as_cmap=True),
}

# ==================== Plot Style Configuration ====================

def setup_academic_style():
    """Configure academic paper style"""
    english_font = setup_english_font()

    plt.rcParams.update({
        # Font sizes
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,

        # Lines
        'lines.linewidth': 2,
        'lines.markersize': 6,

        # Axes
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.linewidth': 0.9,

        # Ticks
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.top': False,
        'ytick.right': False,

        # Grid
        'axes.grid': False,

        # Legend
        'legend.frameon': True,
        'legend.framealpha': 1.0,
        'legend.edgecolor': '#7A7A7A',

        # Figure quality
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
    })

    return english_font

# ==================== Helper Functions ====================

def add_value_labels(ax, spacing=3, fontsize=9, color='#333333', fmt='.3f'):
    """Add value labels on top of bar plots"""
    for patch in ax.patches:
        value = patch.get_height()
        if not np.isnan(value) and np.isfinite(value):
            x = patch.get_x() + patch.get_width() / 2
            y = patch.get_height()
            ax.text(x, y + spacing, format(value, fmt),
                    ha='center', va='bottom', fontsize=fontsize, color=color)

def remove_top_right_spines(ax):
    """Remove top and right spines"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def set_spines_linewidth(ax, linewidth=0.9):
    """Set spine line width"""
    for spine in ax.spines.values():
        spine.set_linewidth(linewidth)

def styled_heatmap(corr_matrix, ax=None, cmap=None, **kwargs):
    """
    Styled heatmap

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Correlation matrix
    ax : matplotlib.axes.Axes, optional
        Axes object
    cmap : colormap, optional
        Colormap
    **kwargs : dict
        Additional parameters passed to sns.heatmap

    Returns
    -------
    matplotlib.axes.Axes
    """
    if cmap is None:
        cmap = sns.diverging_palette(240, 10, as_cmap=True)

    default_kwargs = {
        'annot': True,
        'fmt': '.3f',
        'cmap': cmap,
        'vmax': 1,
        'vmin': -1,
        'center': 0,
        'square': True,
        'linewidths': 0.5,
        'cbar_kws': {'shrink': 0.8},
        'annot_kws': {'size': 9},
    }
    default_kwargs.update(kwargs)

    ax = sns.heatmap(corr_matrix, ax=ax, **default_kwargs)

    # Apply colorbar styling after creation for broad matplotlib compatibility.
    colorbar = ax.collections[0].colorbar if ax.collections else None
    if colorbar is not None:
        colorbar.outline.set_edgecolor('#333333')
        colorbar.outline.set_linewidth(0.8)

    # Adjust label rotation
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    return ax

def styled_boxplot(data, x=None, y=None, hue=None, ax=None, palette=None, **kwargs):
    """
    Styled boxplot

    Parameters
    ----------
    data : pd.DataFrame
        Data
    x, y, hue : str, optional
        Column names
    ax : matplotlib.axes.Axes, optional
        Axes object
    palette : list, optional
        Color list
    **kwargs : dict
        Additional parameters passed to sns.boxplot

    Returns
    -------
    matplotlib.axes.Axes
    """
    if palette is None:
        palette = [COLORS['primary'], COLORS['secondary']]

    default_kwargs = {
        'palette': palette,
        'width': 0.6,
        'fliersize': 3,
        'linewidth': 1.2,
    }
    default_kwargs.update(kwargs)

    ax = sns.boxplot(data=data, x=x, y=y, hue=hue, ax=ax, **default_kwargs)
    remove_top_right_spines(ax)

    return ax

def styled_lineplot(data, x=None, y=None, hue=None, style=None, ax=None, palette=None, **kwargs):
    """
    Styled line plot

    Parameters
    ----------
    data : pd.DataFrame
        Data
    x, y, hue, style : str, optional
        Column names
    ax : matplotlib.axes.Axes, optional
        Axes object
    palette : list, optional
        Color list
    **kwargs : dict
        Additional parameters passed to sns.lineplot

    Returns
    -------
    matplotlib.axes.Axes
    """
    if palette is None:
        palette = [COLORS['nonsoe'], COLORS['soe']]

    default_kwargs = {
        'palette': palette,
        'linewidth': 2,
        'markers': True,
        'markersize': 7,
        'markeredgecolor': 'white',
        'markeredgewidth': 1,
    }
    default_kwargs.update(kwargs)

    ax = sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, ax=ax, **default_kwargs)
    remove_top_right_spines(ax)

    # Add light grid
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    return ax

def styled_barplot(data, x=None, y=None, hue=None, ax=None, palette=None, **kwargs):
    """
    Styled bar plot

    Parameters
    ----------
    data : pd.DataFrame
        Data
    x, y, hue : str, optional
        Column names
    ax : matplotlib.axes.Axes, optional
        Axes object
    palette : list, optional
        Color list
    **kwargs : dict
        Additional parameters passed to sns.barplot

    Returns
    -------
    matplotlib.axes.Axes
    """
    if palette is None:
        palette = COLORS['warm_gradient']

    default_kwargs = {
        'palette': palette,
        'edgecolor': 'white',
        'linewidth': 1,
    }
    default_kwargs.update(kwargs)

    ax = sns.barplot(data=data, x=x, y=y, hue=hue, ax=ax, **default_kwargs)
    remove_top_right_spines(ax)

    return ax

def save_figure(fig, filepath, **kwargs):
    """
    Save figure, automatically create directory

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object
    filepath : str
        Save path
    **kwargs : dict
        Additional parameters passed to fig.savefig
    """
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    default_kwargs = {
        'dpi': 300,
        'bbox_inches': 'tight',
        'pad_inches': 0.1,
    }
    default_kwargs.update(kwargs)

    fig.savefig(filepath, **default_kwargs)

# ==================== Initialization ====================

# Auto-initialize
_english_font = setup_academic_style()
print(f"Plot config initialized, English font: {_english_font}")
