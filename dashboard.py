import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Social Media Analytics",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("engagement_analysis.csv")
    df["post_date"] = pd.to_datetime(df["post_date"])
    return df


@st.cache_data
def load_source_data():
    return pd.read_csv("social_media_data.csv")


df = load_data()
source_df = load_source_data()

# DASHBOARD TITLE
st.title("📊 Social Media Engagement Analysis")
st.write("Analyze social media performance using Python.")

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

platforms = st.sidebar.multiselect(
    "Select Platform",
    options=sorted(source_df["platform"].dropna().unique()),
    default=sorted(source_df["platform"].dropna().unique())
)

content_types = st.sidebar.multiselect(
    "Select Content Type",
    options=sorted(source_df["content_type"].dropna().unique()),
    default=sorted(source_df["content_type"].dropna().unique())
)

# APPLY FILTERS
filtered_df = df[
    (df["platform"].isin(platforms)) &
    (df["content_type"].isin(content_types))
].copy()

quality_df = source_df.drop_duplicates(
    subset="post_id",
    keep="first"
).copy()
quality_df["views"] = pd.to_numeric(
    quality_df["views"],
    errors="coerce"
)
quality_df = quality_df[
    quality_df["platform"].isin(platforms) &
    quality_df["content_type"].isin(content_types)
].copy()

deleted_posts = quality_df[quality_df["status"] == "Deleted"]
active_quality_df = quality_df[quality_df["status"] != "Deleted"].copy()
zero_view_posts = active_quality_df[active_quality_df["views"] == 0]

positive_views = active_quality_df.loc[
    active_quality_df["views"] > 0,
    "views"
]
quartile_1 = positive_views.quantile(0.25)
quartile_3 = positive_views.quantile(0.75)
outlier_limit = quartile_3 + 1.5 * (quartile_3 - quartile_1)
active_quality_df["viral_outlier"] = (
    active_quality_df["views"] > outlier_limit
)
viral_outliers = active_quality_df[active_quality_df["viral_outlier"]]

# KPI CALCULATIONS
total_posts = len(filtered_df)
total_views = filtered_df["views"].sum()
total_likes = filtered_df["likes"].sum()

average_er = filtered_df["engagement_rate"].mean()

# DISPLAY KPI CARDS
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Posts", f"{total_posts:,}")
col2.metric("Total Views", f"{total_views:,}")
col3.metric("Total Likes", f"{total_likes:,}")

if pd.notna(average_er):
    col4.metric("Average Engagement Rate", f"{average_er:.2f}%")
else:
    col4.metric("Average Engagement Rate", "N/A")

# DATA QUALITY CHECKS
st.subheader("Data Quality Checks")
st.caption(
    "Counts and post lists follow the selected platform and content-type filters."
)

quality_col1, quality_col2, quality_col3 = st.columns(3)
quality_col1.metric("Zero-View Posts", f"{len(zero_view_posts):,}")
quality_col2.metric("Deleted Posts", f"{len(deleted_posts):,}")
quality_col3.metric("Viral Outlier Posts", f"{len(viral_outliers):,}")

zero_tab, deleted_tab, outlier_tab = st.tabs(
    ["Zero-View Posts", "Deleted Posts", "Viral Outliers"]
)
quality_columns = [
    "post_id", "platform", "content_type", "post_date", "views", "status"
]

with zero_tab:
    if zero_view_posts.empty:
        st.info("No zero-view posts match these filters.")
    else:
        st.dataframe(
            zero_view_posts[quality_columns],
            use_container_width=True
        )

with deleted_tab:
    if deleted_posts.empty:
        st.info("No deleted posts match these filters.")
    else:
        st.dataframe(
            deleted_posts[quality_columns],
            use_container_width=True
        )

with outlier_tab:
    if viral_outliers.empty:
        st.info("No viral outlier posts match these filters.")
    else:
        st.write(f"IQR upper limit: {outlier_limit:,.2f} views")
        st.dataframe(
            viral_outliers[quality_columns],
            use_container_width=True
        )

# PREPARE ANALYSIS
filtered_df["posting_day"] = (
    filtered_df["post_date"].dt.day_name()
)

filtered_df["posting_hour"] = (
    filtered_df["post_date"].dt.hour
)

# CONTENT TYPE ANALYSIS
st.subheader("Content Type Performance")

content_data = (
    filtered_df.groupby("content_type")["engagement_rate"]
    .mean()
    .reset_index()
    .sort_values("engagement_rate", ascending=False)
)

if not content_data.empty:
    fig1 = px.bar(
        content_data,
        x="content_type",
        y="engagement_rate",
        title="Average Engagement by Content Type",
        labels={
            "content_type": "Content Type",
            "engagement_rate": "Engagement Rate (%)"
        }
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.write(
        "Best Content Type:",
        content_data.iloc[0]["content_type"]
    )
else:
    st.info("No valid engagement data for these filters.")

# POSTING DAY ANALYSIS
st.subheader("Best Posting Day")

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

day_data = (
    filtered_df.groupby("posting_day")["engagement_rate"]
    .mean()
    .reindex(day_order)
    .dropna()
    .reset_index()
)

if not day_data.empty:
    fig2 = px.bar(
        day_data,
        x="posting_day",
        y="engagement_rate",
        title="Average Engagement by Day"
    )
    st.plotly_chart(fig2, use_container_width=True)

    best_day = day_data.loc[
        day_data["engagement_rate"].idxmax(), "posting_day"
    ]
    st.write("Best Posting Day:", best_day)
else:
    st.info("No valid posting-day data available.")

# POSTING HOUR ANALYSIS
st.subheader("Best Posting Hour")

hour_data = (
    filtered_df.groupby("posting_hour")["engagement_rate"]
    .mean()
    .dropna()
    .reset_index()
)

if not hour_data.empty:
    fig3 = px.bar(
        hour_data,
        x="posting_hour",
        y="engagement_rate",
        title="Average Engagement by Hour",
        labels={"posting_hour": "Hour (24-hour format)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    best_hour = hour_data.loc[
        hour_data["engagement_rate"].idxmax(), "posting_hour"
    ]
    st.write("Best Posting Hour:", f"{int(best_hour):02d}:00")
else:
    st.info("No valid posting-hour data available.")

# VIEWS VS LIKES
st.subheader("Views vs Likes Analysis")

fig4 = px.scatter(
    filtered_df,
    x="views",
    y="likes",
    color="content_type",
    hover_data=["post_id", "platform"],
    title="Relationship Between Views and Likes"
)

st.plotly_chart(fig4, use_container_width=True)

# DATA TABLE
st.subheader("Social Media Post Details")

st.dataframe(filtered_df, use_container_width=True)

# DOWNLOAD BUTTON
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="social_media_analysis.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
