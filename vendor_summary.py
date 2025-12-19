import pandas as pd
import logging
import psycopg2
# import import_ipynb
# from ingestion_db import load_all_csvs
from sqlalchemy import create_engine

logging.basicConfig(
    filename="logs/vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s -%(message)s",
    filemode="w"
)

def create_vendor_summary(engine):
    '''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary=pd.read_sql(""" WITH FreightSummary AS(
    Select "VendorNumber",
    Sum("Freight") AS FreightCost   
    from vendor_invoice
    Group BY "VendorNumber"
),

PurchaseSummary AS (
        Select 
            p."VendorName",
            p."VendorNumber",
            p."Brand",
            P."Description",
            p."PurchasePrice",
            pp."Volume",
            pp."Price" as ActualPrice,
            sum(p."Quantity") as TotalPurchaseQuantity,
            sum(p."Dollars") as TotalPurchaseDollars
            from purchases p
            join purchase_prices pp on
            p."Brand"=pp."Brand"
            where p."PurchasePrice" > 0
            Group BY p."VendorNumber", p."VendorName", p."Brand",p."Description", p."PurchasePrice", pp."Volume", pp."Price"
),

SalesSummary As(
    Select
            "VendorNo",
            "Brand",
            SUM("SalesDollars") as TotalSalesDollars,
            SUM("SalesPrice") as TotalSalesPrice,
            SUM("SalesQuantity") as TotalSalesQuantity,
            SUM("ExciseTax") as TotalExciseTax
            from sales
            Group by "VendorNo", "Brand"
)
Select 
    ps."VendorNumber",
    ps."VendorName",
    ps."Brand",
    ps."Description",
    ps."PurchasePrice",
    ps.Actualprice,
    ps."Volume",
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost 
    from PurchaseSummary ps
    left join SalesSummary ss
    on ss."VendorNo"=ps."VendorNumber"
    AND ss."Brand"=ps."Brand"
    left join FreightSummary fs
    on ps."VendorNumber" = fs."VendorNumber"
    Order by ps.TotalPurchaseDollars desc""",engine)
    
    #Return the datafrmae
    return vendor_sales_summary
    

def clean_data(df):
    '''this function will clean the data'''
     
    #  Filling missing value with 0
    df.fillna(0,inplace=True)
    
    # Removing spaces from the categorical column
    df['VendorName']=df['VendorName'].str.strip()
    df['Description']=df['Description'].str.strip()
    
    # Creating new columns for better analysis
    df['GrossProfit'] = df['totalsalesdollars'] - df['totalpurchasedollars']
    df['Profitmargin'] = (df['GrossProfit'] / df['totalsalesdollars']) * 100
    df['StockTurnover'] = df['totalsalesquantity'] / df['totalpurchasequantity']
    df['SalestoPurchaseRatio'] = df['totalsalesdollars'] / df['totalpurchasedollars']
    
    return df

def load_all_csvs(df, table_name, conn):
    """Load a DataFrame into PostgreSQL with correct column types if table does not exist."""
    cur = conn.cursor()

    # Check if table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s
        );
    """, (table_name,))
    
    exists = cur.fetchone()[0]

    if exists:
        print(f"⚠️ Table '{table_name}' already exists. Skipping ingestion to avoid duplicates.")
        logging.info(f"Table '{table_name}' already exists. Skipping ingestion.")
    else:
        # Columns that should be numeric
        numeric_cols = {
            "VendorNumber", "Brand",
            "PurchasePrice", "actualprice", "Volume", "totalpurchasequantity",
            "totalpurchasedollars", "totalsalesquantity", "totalsalesdollars",
            "totalsalesprice", "totalexcisetax", "freightcost",
            "GrossProfit", "Profitmargin", "StockTurnover", "SalestoPurchaseRatio"
        }

        # Build CREATE TABLE query with correct types
        cols = []
        for col in df.columns:
            if col in numeric_cols:
                cols.append(f'"{col}" NUMERIC')  # Store as numeric
            else:
                cols.append(f'"{col}" TEXT')  # Keep as text
        col_defs = ", ".join(cols)

        cur.execute(f'CREATE TABLE "{table_name}" ({col_defs});')

        # Insert data row by row (convert NaN to None for SQL NULL)
        for _, row in df.iterrows():
            values = []
            for col in df.columns:
                val = row[col]
                if pd.isna(val):
                    values.append(None)
                elif col in numeric_cols:
                    try:
                        values.append(float(val))  # enforce numeric
                    except:
                        values.append(None)
                else:
                    values.append(str(val))
            
            placeholders = ", ".join(["%s"] * len(values))
            cur.execute(
                f'INSERT INTO "{table_name}" VALUES ({placeholders});',
                values
            )

        conn.commit()
        print(f"✅ Data inserted into new table: {table_name}")
        logging.info(f"Data inserted into new table: {table_name}")


if __name__=='__main__':
    # creating database connection
    # conn = psycopg2.connect(
    # dbname="inventory",
    # user="postgres",
    # password="Rpsingh123",
    # host="localhost",
    # port="5432"
    # )
    engine = create_engine("postgresql+psycopg2://postgres:Rpsingh123@localhost:5432/inventory")
    conn = psycopg2.connect(
        dbname="inventory",
        user="postgres",
        password="Rpsingh123",
        host="localhost",
        port="5432"
    )
   
    logging.info('Creating vendor summary table......')
    summary_df=create_vendor_summary(engine)
    logging.info(summary_df.head())
    
    logging.info('Cleaning Data.....')
    clean_df=clean_data(summary_df)
    logging.info(clean_df.head())
    
    logging.info('Ingesting Data.....')
    load_all_csvs(clean_df,'vendor_sales_summary', conn)
    logging.info('Completed')
