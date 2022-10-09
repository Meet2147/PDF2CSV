import streamlit as st
import pandas as pd
import tabula
import streamlit.components.v1 as components
import plotly.express as px

st.title("PDF2CSV")
st.subheader("Convert your PDF files to CSV")

def main():
    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        
        if uploaded_file is not None:       
            tabula.convert_into(uploaded_file,"result.csv",pages="all",output_format="csv")
            with open("result.csv", "rb") as f:
                st.download_button(
                        label="Download data as CSV",
                        data=f,
                        file_name='result.csv',
                        mime='text/csv',
                        )
        df = pd.read_csv("result.csv")
    
        df.drop(df[df['Debit'] == 'Debit'].index, inplace = True)
        df['Debit'] = df['Debit'].str.replace(',','').astype('float')
        df['Credit'] = df['Credit'].str.replace(',','').astype('float')
        df['Credit'] = df['Credit'].fillna(0)
        df['Debit'] = df['Debit'].fillna(0)
        df2 = df.drop(df.columns[[1, 3]],axis = 1)
        st.dataframe(df2)
        menu = ['Reports','Charts']
        options = st.selectbox("Menu",menu)
        if options == "Charts":
            x_axis_val = st.selectbox('Select X-Axis Value', options=df2.columns)
            Y_axis_val = st.selectbox('Select Y-Axis Value', options=df2.columns)
            hist = px.histogram(df2, x=x_axis_val, y=Y_axis_val,nbins=150)
            line = px.line(df2, x=x_axis_val, y=Y_axis_val)
            pie = px.pie(df2, names=x_axis_val, values=Y_axis_val)
            density = px.density_heatmap(df2, x=x_axis_val, y=Y_axis_val)
            st.plotly_chart(hist)
            st.plotly_chart(line)
            st.plotly_chart(pie)
            st.plotly_chart(density)
    components.html("""<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="learnapplybuild" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>""", 
                            height=200)
if __name__ == '__main__':
    main()