import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('有名米国株可視化アプリ')

st.sidebar.write("""
# オプション欄
以下より表示日数や株価の範囲指定が可能です。
""")
#はタイトルh2,やh3のようなもの

st.sidebar.write("""
## ①表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** の株価を表示します。
""")

st.write(
    """選択できる企業は以下となります。
    """
)

st.write(
    "google, apple, amazon, facebook(meta), microsoft, netflix, tesla, トヨタ自動車, NTT(日本電信電話), ソフトバンク"
)

def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## ②株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        50.0, 500.0, (50.0, 500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook(meta)': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN',
        'tesla': 'TSLA',
        'トヨタ自動車': 'TM',

    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '企業名を選択してください。',
        list(df.index),
        ['google', 'amazon', 'facebook(meta)', 'apple']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    print(e.__class__.__name__) # ZeroDivisionError
    print(e.args) # ('division by zero',)
    print(e) # division by zero
    print(f"{e.__class__.__name__}: {e}") # ZeroDivisionError: division by zero
    st.error(
        "エラーが起きているようです！"
    )