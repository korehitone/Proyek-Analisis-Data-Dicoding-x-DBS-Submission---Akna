from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import MaxNLocator
sns.set(style='dark')

month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
            7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"}


# Helper function
def create_monthly_revenue_df(df):
    monthly_revenue_df = df.groupby(
        by=df["order_purchase_timestamp"].dt.month
    ).price.sum().reset_index()
    monthly_revenue_df = monthly_revenue_df.rename(columns={
        "order_purchase_timestamp": "month",
        "price": "revenue"
    })
    monthly_revenue_df["month"] = monthly_revenue_df["month"].map(month_names)

    return monthly_revenue_df


def create_sum_category_df(df):
    sum_category_df = df.groupby(
        by="product_category_name_english"
    ).order_id.count().reset_index()
    sum_category_df = sum_category_df.rename(columns={"order_id": "item_count"})

    return sum_category_df


# Load data
all_df = pd.read_csv(Path(__file__).parent / "main_data.csv")

datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Komponen filter
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.header("Filter")

    # Mengambil start_date & end_date dari date_input
    date_range = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# date_input mengembalikan 1 tanggal selama tanggal akhir belum dipilih
if len(date_range) != 2:
    st.info("Pilih tanggal awal dan tanggal akhir.")
    st.stop()

start_date, end_date = date_range

main_df = all_df[
    (all_df["order_purchase_timestamp"].dt.date >= start_date) &
    (all_df["order_purchase_timestamp"].dt.date <= end_date)
]

monthly_revenue_df = create_monthly_revenue_df(main_df)
sum_category_df = create_sum_category_df(main_df)

# Header
st.header("E-Commerce Dashboard :sparkles:")
st.caption("Order berstatus delivered. Revenue = jumlah price (tanpa ongkir). "
           "Jumlah item = jumlah baris order_items.")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Revenue", value=f"{main_df['price'].sum():,.2f}")

with col2:
    st.metric("Total Item Terjual", value=f"{len(main_df):,}")

# Pertanyaan 1: revenue per bulan
st.subheader("Total Revenue per Bulan")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    monthly_revenue_df["month"],
    monthly_revenue_df["revenue"],
    marker="o",
    linewidth=2,
    color="#72BCD4"
)

# Tandai bulan tertinggi dan terendah
imax = monthly_revenue_df["revenue"].idxmax()
imin = monthly_revenue_df["revenue"].idxmin()
ax.scatter(
    monthly_revenue_df["month"][[imax, imin]],
    monthly_revenue_df["revenue"][[imax, imin]],
    color="#D9534F",
    s=100,
    zorder=3
)

ax.set_title("Total Revenue per Bulan (Order Delivered, 2017)", loc="center", fontsize=20)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Revenue", fontsize=12)
ax.ticklabel_format(style="plain", axis="y")
ax.set_ylim(bottom=0)
ax.grid(axis="y", alpha=0.3)

st.pyplot(fig)

# Pertanyaan 2: kategori terlaris dan paling sedikit terjual
st.subheader("Best & Worst Performing Category")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="item_count",
    y="product_category_name_english",
    data=sum_category_df.sort_values(by="item_count", ascending=False).head(5),
    hue="product_category_name_english",
    palette=colors,
    legend=False,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Item Terjual", fontsize=30)
ax[0].set_title("Best Performing Category", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=30)
ax[0].tick_params(axis="x", labelsize=30)

sns.barplot(
    x="item_count",
    y="product_category_name_english",
    data=sum_category_df.sort_values(by="item_count", ascending=True).head(5),
    hue="product_category_name_english",
    palette=colors,
    legend=False,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Item Terjual", fontsize=30)
ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))  # sumbu bilangan bulat
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=30)
ax[1].tick_params(axis="x", labelsize=30)

fig.suptitle("Best and Worst Performing Category by Number of Items Sold (2017)", fontsize=50)
fig.tight_layout(rect=[0, 0, 1, 0.93])

st.pyplot(fig)

st.caption("Data: Olist Brazilian E-Commerce Public Dataset")