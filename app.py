import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide',page_title='Startup Analysis')
df=pd.read_csv("startup_cleaned.csv")
df["date"]=pd.to_datetime(df["date"],errors="coerce")
df["month"]=df["date"].dt.month
df["year"]=df["date"].dt.year



def load_overall_analysis():
    st.title("Overall Analysis")

    #total invested amount
    total=round(df["amount"].sum())
    #Maximum funding infused in startup
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    #Average ticket size
    avg_funding=df.groupby("startup")["amount"].sum().mean()
    #no. of funded startups
    num_startups=df["startup"].nunique()


# creating ticket size
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total",str(total)+'Cr')
    with col2:
        st.metric("Max",str(max_funding)+'Cr')
    with col3:
        st.metric("Avg",str(round(avg_funding))+'Cr')
    with col4:
        st.metric("Funded Startups",num_startups)

#creating MoM Graph of investments.
    col1,col2=st.columns(2)

    with col1:
        st.header("MoM Graph")
        selected_option=st.selectbox("select Type",["Total","Count"])
        if selected_option=="Total":
            temp_df=df.groupby(["year", "month"])["amount"].sum().reset_index()
        else:
            temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

        temp_df['x_axis']=temp_df["year"].astype("str")+ "-"+temp_df["month"].astype("str")
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df["x_axis"], temp_df["amount"])
        st.pyplot(fig5)

    with col2:
        # sector wise analysis
        st.header("Sector Analysis")
        selected_option=st.selectbox("select Type",["Analysis on the basis of Number of sector","Analysis on the basis of Total money invested in each sector"])
        if selected_option=="Analysis on the basis of Number of sector":
            temp_series = df.groupby("vertical")["startup"].count().sort_values(ascending=False).head()
        else:
            temp_series = df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head()

        fig6, ax6 = plt.subplots()
        ax6.pie(temp_series,labels=temp_series.index,autopct="%0.01f%%")
        st.pyplot(fig6)

    col1, col2 = st.columns(2)
    with col1:
        #Funding Analysis
        st.header("Types of funding Analysis")
        selected_option=st.selectbox("select Type",["Count","Total"])
        if selected_option=="Count":
            temp_series=df.groupby("round")["startup"].count().sort_values(ascending=False).head()
        else:
            temp_series=df.groupby("round")["amount"].sum().sort_values(ascending=False).head()
        fig7, ax7 = plt.subplots()
        ax7.pie(temp_series, labels=temp_series.index, autopct="%0.01f%%")
        st.pyplot(fig7)

    with col2:
        # City wise Analysis
        st.header("City wise Analysis")
        selected_option = st.selectbox("select Type", ["city which have the highest investment", "Total Amount invested in each city"])
        if selected_option == "city which have the highest investment":
            temp_series = df.groupby("city")["startup"].count().sort_values(ascending=False).head()
        else:
            temp_series = df.groupby("city")["amount"].sum().sort_values(ascending=False).head()
        fig8, ax8 = plt.subplots()
        ax8.pie(temp_series, labels=temp_series.index, autopct="%0.01f%%")
        st.pyplot(fig8)

    col1,col2=st.columns(2)
    with col1:
        #top investors overall and  yearwise
        st.header("Top5 Investors")
        selected_option=st.selectbox("select Type",["Yearwise","Overall"])
        if selected_option=="Yearwise":
            top_inves=df.groupby(["investors","year"])["amount"].sum().reset_index().sort_values(["year", "amount"],ascending=[True,False]).groupby("year").apply(lambda x: x.head(1)).reset_index(drop=True)
            top_inves['amount'] = top_inves['amount'].apply(lambda x: '{:.2f}'.format(x))
            top_inves_list = top_inves.to_dict(orient='records')
            st.table(top_inves_list)
        else:
            top_investor_overall = df.groupby(["investors", "year"])["amount"].sum().reset_index().sort_values(["year", "amount"], ascending=[True, False]).sort_values(by="amount",ascending=False).head().reset_index(drop=True)
            top_investor_overall['amount'] = top_investor_overall['amount'].apply(lambda x: '{:.2f}'.format(x))
            top_investor_overall_list = top_investor_overall.to_dict(orient='records')
            st.table(top_investor_overall_list)

    with col2:
        #top startups overall and yearwise
        st.header("Top5 Startups")
        selected_option=st.selectbox("select Type",["Yearwise Top Startups","Overall Top Startups"])
        if selected_option=="Overall Top Startups":
            top_startup_overall = df.groupby(["startup", "year"])["amount"].sum().reset_index().sort_values(['year', 'amount'], ascending=[True, False]).sort_values(by='amount', ascending=False).head(5).reset_index(drop=True)
            top_startup_overall['amount']= top_startup_overall['amount'].apply(lambda x: '{:.2f}'.format(x))
            top_startup_overall_list = top_investor_overall.to_dict(orient='records')
            st.table(top_startup_overall_list)
        else:
            top_startup_yearwise=df.groupby(["startup","year"])["amount"].sum().reset_index().sort_values(by=['year','amount'],ascending=[True,False]).groupby('year').apply(lambda x: x.head(1)).reset_index(drop=True)
            top_startup_yearwise['amount'] = top_startup_yearwise['amount'].apply(lambda x: '{:.2f}'.format(x))
            top_startup_yearwise_list = top_startup_yearwise.to_dict(orient='records')
            st.table(top_startup_yearwise_list)

    #Funding Heatmap
    temp_df = df.groupby(["startup", "year"])["amount"].sum().sort_values(ascending=False).head(15).unstack().fillna(0).sort_index(axis=1)
    st.subheader("Funding Heatmap")
    #sns.heatmap(temp_df, annot=True, linewidth=0.5, cmap="autumn", fmt=".0f")
    st.write("Heatmap:")
    fig9, ax9 = plt.subplots()
    sns.heatmap(temp_df, annot=True, cmap='autumn', ax=ax9, linewidth=0.5, fmt=".0f")
    st.pyplot(fig9)



def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments detail of the investor

    last5_df=df[df["investors"].str.contains(investor)].head()[["date", "startup", "vertical", "city", "round", "amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)


    col1,col2=st.columns(2)
    with col1:
        #Biggest investments
        big_series=df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
       #verticals in which they invested most
       vertical_series=df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum().sort_values(ascending=False).head()
       st.subheader("Sectors Invested in")
       fig1, ax1=plt.subplots()
       ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
       st.pyplot(fig1)


    col1,col2=st.columns(2)
    with col1:
        #the rounds in which they invested most
        round_series=df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Types of Investments they invested most")
        fig2, ax2=plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col2:
        #the city in which they invested most
        city_series=df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Cities they invested most")
        fig3, ax3=plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    print(df.info())

    df["year"] = df["date"].dt.year
    year_series=df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("YoY Investments")
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)

def load_startup_details(startup):
    st.title("startup")
    def unique_values(series):
        unique_items = series.unique()
        non_nan_items = [str(item) for item in unique_items if not pd.isna(item)]
        return ', '.join(non_nan_items)
    st.subheader("Startup basic Detail")
    filtered_data = df[df["startup"].str.contains(startup, case=False, na=False)]
    startup_info = filtered_data.groupby("startup").agg({'vertical': unique_values, 'subvertical': unique_values,'city':unique_values})
    # Display the result in a DataFrame format using Streamlit
    if not startup_info.empty:
        st.dataframe(startup_info)
    else:
        st.write(f"No information found for {startup}.")


    def unique_vals(series1):
        unique_items1 = series1.unique()
        non_nan_items1 = [str(item) for item in unique_items1 if not pd.isna(item)]
        return ', '.join(non_nan_items1)
    st.subheader("Startup Investing Detail")
    filtered_data1 = df[df["startup"].str.contains(startup, case=False, na=False)]
    startup_info1 = filtered_data1.groupby("startup").agg({'investors': unique_vals, 'round': unique_vals,'amount':unique_vals})
    # Display the result in a DataFrame format using Streamlit
    if not startup_info.empty:
        st.dataframe(startup_info1)
    else:
        st.write(f"No information found for {startup}.")



st.sidebar.title('Startup Funding Analysis')
st.session_state.option=st.sidebar.selectbox("select one",["Overall Analysis","Startup","Investor"],key="analysis")
option=st.session_state.option
if option=="Overall Analysis":
        load_overall_analysis()

elif option=="Startup":
    selected_startup=st.sidebar.selectbox("select Startup",sorted(df["startup"].unique().tolist()))
    btn1=st.sidebar.button("Find Startup details")
    #st.title("Startup Analysis")
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor=st.sidebar.selectbox("select Investor",sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor details")
    if btn2:
        load_investor_details(selected_investor)



