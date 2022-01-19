
class CreateSchemas():
    def __init__(self):
        self.SQL_sentences = []
    
    def add_sql_sentence_sales_order_header(self, row):
        sql_sentence = f"INSERT INTO SALES_ORDER_HEADER (ExternalSalesId, CustomerAccount, PaymentMethod, Company) VALUES ('{row['ExternalSalesId']}' , '{row['CustomerAccount']}' , '{row['PaymentMethod']}','{row['Company']}')\n"
        self.SQL_sentences.append(sql_sentence)
        
    def add_sql_sentences_sales_order_lines(self, row):
        sql_sentence = f"INSERT INTO SALES_ORDER_LINES (ExternalSalesId, ItemNumber, SoldQuantity, PricePerUnit, Linenum) VALUES ('{row['ExternalSalesId']}' , '{row['ItemNumber']}' , '{row['SoldQuantity']}' , '{row['PricePerUnit']}','{row['Linenum']}')\n"
        self.SQL_sentences.append(sql_sentence)
        
    def print_sentences(self):
        for s in self.SQL_sentences:
            print(s)
            
    def get_sentences(self):
        ret = ""
        for s in self.SQL_sentences:
            ret = ret + s
        return ret
            
    def get_create_table_sentences(self):
        
        sentences = []
        
        sentences.append("""
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SALES_ORDER_HEADER]') AND type in (N'U'))
DROP TABLE [dbo].[SALES_ORDER_HEADER]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SALES_ORDER_HEADER](
    [ExternalSalesId] [varchar](20) NOT NULL,
    [CustomerAccount] [varchar](20) NOT NULL,
    [PaymentMethod] [varchar](12) NOT NULL,
    [Company] [varchar](4) NOT NULL
) ON [PRIMARY]
GO
            """)
        
        sentences.append("""
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SALES_ORDER_LINES]') AND type in (N'U'))
DROP TABLE [dbo].[SALES_ORDER_LINES]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SALES_ORDER_LINES](
    [ItemNumber] [varchar](20) NOT NULL,
    [SoldQuantity] [varchar](20) NOT NULL,
    [PricePerUnit] [float] NOT NULL,
    [Linenum] [int] NOT NULL,
    [ExternalSalesId] [varchar](20) NOT NULL
) ON [PRIMARY]
GO
            """)
        ret = ""
        for s in sentences:
            ret = ret + s
            
        return ret