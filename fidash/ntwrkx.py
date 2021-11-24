
import warnings
import pandas as pd
import numpy as np
import networkx as nx
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# init_notebook_mode(connected=True)
warnings.filterwarnings("ignore")
# from IPython.core.display import display, HTML


def log_ret_df(df):
    log_returns_df = pd.DataFrame()
    for col in df.columns:
        log_returns_df[col] = np.log(df[col]/df[col].shift(1)).dropna()
    # print(log_returns_df.head())
    return log_returns_df


def corr_matrix(log_returns_df):
    correlation_matrix = log_returns_df.corr()
    # print(correlation_matrix.head())
    return correlation_matrix


# def heatmap_html(correlation_matrix, f_name):
#     """HTML rendered visualization of a clustered heatmap for a correlation matrix"""
#     # display(HTML("<h3>Clustered Heatmap: Correlations between asset price returns</h3>"))
#     sns.clustermap(correlation_matrix, cmap="RdYlGn")
#     plt.show()
#     plt.savefig(f'charts/{f_name}_heatmap.png')


def get_edge_list(correlation_matrix):
    """Make a list of edges from a correlation matrix and rename the columns."""
    edges = correlation_matrix.stack().reset_index()
    edges.columns = ['asset_1', 'asset_2', 'correlation']

    # remove self-referential correlations from the df
    edges = edges.loc[edges['asset_1'] != edges['asset_2']].copy()
    # print(edges.head())
    return edges


def undirected_graph(edges):
    """
    Create an undirected graph from an edge list.
    The weights correspond to the degree of correlation.
    """
    G0 = nx.from_pandas_edgelist(
        edges, 'asset_1', 'asset_2', edge_attr=['correlation'])
    # N of nodes and degrees (should all should have degree = 38, i.e. average degree = 38)
    print(nx.info(G0))
    return G0


# def demo_layouts(G0):
#     """Demonstrate various graph layouts."""
#     fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 20))

#     nx.draw(G0, with_labels=True, node_size=700, node_color="#e1575c",
#             edge_color='#363847',  pos=nx.circular_layout(G0), ax=ax[0, 0])
#     ax[0, 0].set_title("Circular layout")

#     nx.draw(G0, with_labels=True, node_size=700, node_color="#e1575c",
#             edge_color='#363847',  pos=nx.random_layout(G0), ax=ax[0, 1])
#     ax[0, 1].set_title("Random layout")

#     nx.draw(G0, with_labels=True, node_size=700, node_color="#e1575c",
#             edge_color='#363847',  pos=nx.spring_layout(G0), ax=ax[1, 0])
#     ax[1, 0].set_title("Spring layout")

#     nx.draw(G0, with_labels=True, node_size=700, node_color="#e1575c",
#             edge_color='#363847',  pos=nx.spectral_layout(G0), ax=ax[1, 1])
#     ax[1, 1].set_title("Spectral layout")

    # return plt.show()


def set_corr_threshold(edges, threshold=0.5):
    """Set the minimum correlation threshold to reduce number of graph edges (for clarity)."""

    # Create new graph based on edge list
    Gx = nx.from_pandas_edgelist(
        edges, 'asset_1', 'asset_2', edge_attr=['correlation'])

    # Remove edges for correlations below the threshold
    remove = []
    for asset_1, asset_2 in Gx.edges():
        corr = Gx[asset_1][asset_2]['correlation']
        if abs(corr) < threshold:
            remove.append((asset_1, asset_2))
    Gx.remove_edges_from(remove)

    print(str(len(remove)) + " edges removed")
    return Gx


def assign_colour(correlation):
    if correlation <= 0:
        # return "#ffa09b"  # red
        return "#DCBBA6"  # skin
    else:
        # return "#9eccb7"  # green
        return "#64646F"  # grey


def assign_node_colour(correlation):
    if correlation <= 0:
        # return "#ffa09b"  # red
        return "#64646F"  # grey
    else:
        # return "#9eccb7"  # green
        return "#DCBBA6"  # skin


def assign_thickness(correlation, benchmark_thickness=2, scaling_factor=3):
    return benchmark_thickness * abs(correlation)**scaling_factor


def assign_node_size(degree, scaling_factor=50):
    return degree * scaling_factor


def format_edges(Gx):
    """
    Format colour, dependent on sign of correlation (+ or -).
    Format edge thickness, dependent on degree of correlation.
    Format node sizes, dependent on number of connections.
    """
    edge_colours = []
    edge_width = []
    for key, value in nx.get_edge_attributes(Gx, 'correlation').items():
        edge_colours.append(assign_colour(value))
        edge_width.append(assign_thickness(value))

    node_size = []
    for key, value in dict(Gx.degree).items():
        node_size.append(assign_node_size(value))

    return edge_colours, edge_width, node_size


# def plt_cor_net(Gx, edge_colours, edge_width, node_size, node_color="#DCBBA6CC", figsize=(9, 9), fontsize=18, font='Roboto', savefig=False, f_name=None):
#     """Plot correlation network graph with matplotlib."""
#     sns.set(rc={'figure.figsize': figsize})
#     font_dict = {'fontsize': fontsize, 'family': font}

#     nx.draw(Gx, pos=nx.circular_layout(Gx), with_labels=True,
#             node_size=node_size, node_color=node_color, edge_color=edge_colours,
#             width=edge_width)
#     plt.title("Asset price correlations", fontdict=font_dict)
#     if savefig:
#         plt.savefig(f'charts/{f_name}_network-graph.png')
#     return plt.show()


# def fruchterman_reingold(Gx, edge_colours, edge_width, node_size, node_color="#DCBBA6CC", figsize=(9, 9), fontsize=18, font='Roboto', savefig=False, f_name=None):
#     """Plot correlation Fruchterman Reingold graph with matplotlib."""
#     sns.set(rc={'figure.figsize': figsize})
#     font_dict = {'fontsize': fontsize, 'family': font}

#     nx.draw(Gx, pos=nx.fruchterman_reingold_layout(Gx), with_labels=True,
#             node_size=node_size, node_color=node_color, edge_color=edge_colours,
#             width=edge_width)
#     plt.title(
#         "Asset price correlations network - Fruchterman-Reingold graph", fontdict=font_dict)
#     plt.show()
#     if savefig:
#         plt.savefig(f'charts/{f_name}_Fruchterman-Reingold.png')


def create_mst(Gx):
    """Create a minimum spanning tree layout."""
    mst = nx.minimum_spanning_tree(Gx)
    return mst

def ass_edge_colours(mst, edge_colours):
    """Assign colours to edges."""
    for key, value in nx.get_edge_attributes(mst, 'correlation').items():
        edge_colours.append(assign_colour(value))
    return edge_colours

def graph_mst(mst, edge_colours, node_color="#DCBBA6CC"):
    """Graph minimum spanning tree and set constants for node size and width."""
    return nx.draw(mst, with_labels=True, pos=nx.fruchterman_reingold_layout(mst),
            node_size=200, node_color=node_color, edge_color=edge_colours,
            width=1.2)

# def plt_mst(mst, figsize=(9, 9), fontsize=18, font='Roboto', savefig=False, f_name=None):
#     """Plot a minimum spanning tree with matplotlib."""
#     sns.set(rc={'figure.figsize': figsize})
#     font_dict = {'fontsize': fontsize, 'family': font}

#     plt.title("Asset Price Correlations - Minimum Spanning Tree",
#               fontdict=font_dict)
#     plt.show()
#     if savefig:
#         plt.savefig(f'charts/{f_name}_MST.png')


def convert_rankings_to_string(ranking):
    """
    Concatenates list of node and correlation into a single string which is the 
    preferred format for the plotly tooltip.
    Inserts html "<br>" inbetween each item in order to add a new line in the tooltip
    """
    s = ''
    for r in ranking:
        s += r + "<br>"
    return s

# def downside_risk(returns, rfr=0, trading_periods=252):
#     adj_returns = returns - rfr
#     sqr_downside = np.square(np.clip(adj_returns, np.NINF, 0))
#     return np.sqrt(np.nanmean(sqr_downside) * trading_periods)


# def sortino(returns, rfr=0, trading_periods=252):
#     adj_returns = returns - rfr
#     ds_risk = downside_risk(adj_returns)

#     if ds_risk == 0:
#         return np.nan

#     sort_ratio = (np.nanmean(adj_returns) * np.sqrt(trading_periods)) / ds_risk
#     return sort_ratio

def calc_sharpe(returns, rfr=0, trading_periods=252):
    vol = returns.std()*np.sqrt(trading_periods)
    avg_ann = (((1 + returns.mean())**trading_periods)-1) - rfr
    sharpe = avg_ann / vol
    return sharpe


def downside_risk(returns, trading_periods=252):
    returns = returns[~np.isnan(returns)]
    downside = returns.where(returns < 0, 0)
    # downside_sq = np.square(downside)
    # return np.sqrt(np.nanmean(downside_sq))
    return downside.std() * np.sqrt(trading_periods)


def calc_sortino(returns, rfr=0, trading_periods=252):
    # returns = returns[~np.isnan(returns)]
    adj_returns = returns - rfr
    annual_returns = ((1 + adj_returns.mean())**trading_periods)-1
    ds_risk = downside_risk(adj_returns, trading_periods=trading_periods)

    if ds_risk == 0:
        return np.nan

    sort_ratio = (annual_returns / ds_risk)
    return sort_ratio


def calculate_stats(df, log_returns_df, ann_factor=252):
    """calculate annualised log returns, volatility, Sharpe ratios and Sortino ratios.

    Returns the annualised returns and vol as a list of floats (used for node colours
    and sizes), and a list of formatted strings for tool tips.    
    """
    returns = log_returns_df
    ann_returns = list(np.mean(returns)*ann_factor*100)

    ann_vol = [np.std(returns[col]*100)*(ann_factor**0.5)
               for col in list(returns.columns)]

    sharpe = (np.mean(returns)*ann_factor*100)/([np.std(returns[col]*100)*(ann_factor**0.5)
                                                 for col in list(returns.columns)])

    # sortino = [(((df[col][-1]/df[col][0])-1)**(ann_factor/(df[col].count())) - 1)/(downside_risk(df[col].pct_change(), trading_periods=ann_factor))
    #                          for col in list(returns.columns)]

    sortino = [(np.mean(returns[col])*ann_factor)/(downside_risk(df[col].pct_change(), trading_periods=ann_factor))
               for col in list(returns.columns)]

    # create string for tooltip
    ann_vol_2dp = ["Annualized Volatility: ""%.1f" % r + "%" for r in ann_vol]
    ann_returns_2dp = ["Annualized Log Returns: ""%.1f" %
                       r + "%" for r in ann_returns]
    sharpe_2dp = ["Sharpe Ratio: ""%.2f" % r for r in sharpe]
    sortino_2dp = ["Sortino Ratio: ""%.2f" % r for r in sortino]

    return ann_returns, ann_vol, sharpe, sortino, ann_returns_2dp, ann_vol_2dp, sharpe_2dp, sortino_2dp


def get_top_and_bottom_three(correlation_matrix):
    """
    For each node, return a list of the names and values for the 3 most/least correlated securities. 
    """

    df = correlation_matrix
    top_3_list = []
    bottom_3_list = []

    for col in df.columns:

        # exclude self correlation #reverse order of the list returned
        top_3 = list(np.argsort(abs(df[col]))[-4:-1][::-1])
        # bottom 3 list is returned in correct order
        bottom_3 = list(np.argsort(abs(df[col]))[:3])

        # get column index
        col_index = df.columns.get_loc(col)

        # find values based on index locations
        top_3_values = [df.index[x] + ": %.2f" %
                        df.iloc[x, col_index] for x in top_3]
        bottom_3_values = [df.index[x] + ": %.2f" %
                           df.iloc[x, col_index] for x in bottom_3]

        top_3_list.append(convert_rankings_to_string(top_3_values))
        bottom_3_list.append(convert_rankings_to_string(bottom_3_values))

    return top_3_list, bottom_3_list


def get_coordinates(mst):
    """Returns the positions of nodes and edges in a format for Plotly to draw the network"""
    # Node positions
    pos = nx.fruchterman_reingold_layout(mst)

    Xnodes = [pos[n][0] for n in mst.nodes()]
    Ynodes = [pos[n][1] for n in mst.nodes()]

    Xedges = []
    Yedges = []
    for e in mst.edges():
        # x coordinates of nodes for each edge
        Xedges.extend([pos[e[0]][0], pos[e[1]][0], None])
        # y coordinates of nodes for each edge
        Yedges.extend([pos[e[0]][1], pos[e[1]][1], None])

    return Xnodes, Ynodes, Xedges, Yedges


def tooltip_stats(mst, df, log_returns_df, correlation_matrix, ann_factor=252):
    """Get stats for tooltip."""
    # make list of node labels.
    node_label = list(mst.nodes())
    # calculate annualised returns, annualised volatility, Sharpe, and Sortino, rounded to 2 decimals.
    ann_returns, ann_vol, sharpe, sortino, ann_returns_2dp, ann_vol_2dp, sharpe_2dp, sortino_2dp = calculate_stats(df, log_returns_df, ann_factor=ann_factor)
    # get the 3 highest and lowest correlations for each node
    top_3_corrs, bottom_3_corrs = get_top_and_bottom_three(correlation_matrix)

    # create tooltip string by concatenating statistics
    description = [f"<b>{node}</b>" +
                   "<br>" + ann_returns_2dp[index] +
                   "<br>" + ann_vol_2dp[index] +
                   "<br>" + sharpe_2dp[index] +
                   "<br>" + sortino_2dp[index] +
                   "<br><br>Strongly correlated with: " +
                   "<br>" + top_3_corrs[index] +
                   "<br>Weakly correlated with: "
                   "<br>" + bottom_3_corrs[index]
                   for index, node in enumerate(node_label)]

    return ann_returns, node_label, description


def assign_color_and_size(ann_returns, factor=10):
    """Assign node colour and size formatting dependent on returns."""
    node_colour = [assign_node_colour(i) for i in ann_returns]
    # assign node size based on annualised returns size (scaled by a factor)
    node_size = [abs(x)**0.5*factor for x in ann_returns]
    return node_colour, node_size


def plot_mst(df, ann_factor=252, corr_threshold=0.5, node_size_factor=10, savefig=False):
    """Plot a Minimum Spanning Tree with Plotly."""

    start_date = df.index.min()
    end_date = df.index.max()
    log_returns_df = log_ret_df(df)
    correlation_matrix = corr_matrix(log_returns_df)
    edges = get_edge_list(correlation_matrix)
    G0 = undirected_graph(edges)
    Gx = set_corr_threshold(edges, threshold=corr_threshold)
    edge_colours, edge_width, node_size = format_edges(Gx)
    mst = create_mst(Gx)
    edge_colours = ass_edge_colours(mst, edge_colours)
    # graph_mst(mst, edge_colours, node_color="#DCBBA6CC")
    ann_returns, node_label, description = tooltip_stats(mst, df, log_returns_df, correlation_matrix, ann_factor=ann_factor)
    Xnodes, Ynodes, Xedges, Yedges = get_coordinates(mst)
    node_colour, node_size = assign_color_and_size(ann_returns, factor=node_size_factor)

    # edges
    tracer = go.Scatter(x=Xedges, y=Yedges,
                        mode='lines',
                        line=dict(color='#DCDCDC', width=1),
                        hoverinfo='none',
                        showlegend=False)

    # nodes
    tracer_marker = go.Scatter(x=Xnodes, y=Ynodes,
                               mode='markers+text',
                               textposition='top center',
                               marker=dict(size=node_size,
                                           line=dict(width=1),
                                           color=node_colour),
                               hoverinfo='text',
                               hovertext=description,
                               text=node_label,
                               textfont=dict(size=7),
                               showlegend=False)

    axis_style = dict(title='',
                      titlefont=dict(size=20),
                      showgrid=False,
                      zeroline=False,
                      showline=False,
                      ticks='',
                      showticklabels=False)

    layout = dict(title='Correlations - Minimum Spanning Tree',
                #   width=400,
                #   height=620,
                  autosize=True,
                  showlegend=False,
                  xaxis=axis_style,
                  yaxis=axis_style,
                  hovermode='closest',
                  plot_bgcolor='#fff',
                  font_family="Roboto",
                  font_color='#58595b',
                  title_font_family="Roboto",
                  title_font_color='#a5a5a5')

    fig = go.Figure(dict(data=[tracer, tracer_marker], layout=layout))

    # display(HTML(f"""<p style="font-family:roboto; "font-size:100%;">Node size is proportional to annualised returns.<br>
    #                 Node color signify positive or negative cumulative returns between {start_date} to {end_date}.</p> """))

    if savefig:
        mst_name = f'/charts/Eurekahedge_Minimum_Spanning_Tree_{end_date}'
        fig.write_html(f'.{mst_name}.html')

    return fig


# log_returns_df = log_ret_df(df)
# correlation_matrix = corr_matrix(log_returns_df)  
# edges = get_edge_list(correlation_matrix)
# G0 = undirected_graph(edges)
# Gx = set_corr_threshold(edges, threshold=0.05)
# edge_colours, edge_width, node_size = format_edges(Gx)
# # node_color="#DCBBA6CC"
# mst = create_mst(Gx)
# edge_colours = ass_edge_colours(mst, edge_colours)
# Xnodes, Ynodes, Xedges, Yedges = get_coordinates(mst)
# ann_returns, node_label, description = tooltip_stats(mst, df, log_returns_df, correlation_matrix, ann_factor=252)
# node_colour, node_size = assign_color_and_size(ann_returns, factor=10)

# plot_mst(df, ann_factor=252, corr_threshold=0.05, node_size_factor=10, savefig=True)