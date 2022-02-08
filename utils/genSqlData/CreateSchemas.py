class CreateSchemas():
    def __init__(self):
        self.SQL_sentences = []
    
    def add_sql_sentence_sales_order_header(self, row, source_identifier):
        sql_sentence = f"INSERT INTO SALES_ORDER_HEADER (ExternalSalesId, CustomerAccount, PaymentMethod, Company, _IntegrationSourceBatchId) VALUES ('{row['ExternalSalesId']}' , '{row['CustomerAccount']}' , '{row['PaymentMethod']}','{row['Company']}','{source_identifier}')\n"
        self.SQL_sentences.append(sql_sentence)
        
    def add_sql_sentences_sales_order_lines(self, row, source_identifier):
        sql_sentence = f"INSERT INTO SALES_ORDER_LINES (ExternalSalesId, ItemNumber, SoldQuantity, PricePerUnit, Linenum, _IntegrationSourceBatchId) VALUES ('{row['ExternalSalesId']}' , '{row['ItemNumber']}' , '{row['SoldQuantity']}' , '{row['PricePerUnit']}','{row['Linenum']}','{source_identifier}')\n"
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

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SALES_ORDER_LINES]') AND type in (N'U'))
DROP TABLE [dbo].[SALES_ORDER_LINES]
GO                

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[INTEGRATION_STATUS_GROUP]') AND type in (N'U'))
DROP TABLE [dbo].[INTEGRATION_STATUS_GROUP]
GO
                         
                         """)
        
        sentences.append("""
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[INTEGRATION_STATUS_GROUP](
	[ID] [smallint] NOT NULL,
	[STATE] [varchar](50) NOT NULL,
 CONSTRAINT [PK_INTEGRATION_STATUS_GROUP] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO                                           
            
   
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (0, 'UNPROCESSED')
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (10, 'PROCESSED')
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (20, 'PROCESSING')
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (30, 'RETRYING')
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (35, 'MAX_RETRY')
INSERT INTO [dbo].[INTEGRATION_STATUS_GROUP]  ([ID] ,[STATE]) VALUES (40, 'IN_TARGET')

GO
            """)          
        
        sentences.append("""
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SALES_ORDER_HEADER](
	[ExternalSalesId] [varchar](20) NOT NULL,
	[CustomerAccount] [varchar](20) NOT NULL,
	[PaymentMethod] [varchar](12) NOT NULL,
	[Company] [varchar](4) NOT NULL,
	[_IntegrationRefId] [uniqueidentifier] NOT NULL DEFAULT (newid()),
	[_IntegrationState] [smallint] NOT NULL DEFAULT ((0)),
    [_IntegrationSourceBatchId] [uniqueidentifier] NOT NULL,
	[_IntegrationTargetBatchId] [uniqueidentifier] NULL,
	[_IntegrationTimestamp] [timestamp] NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[SALES_ORDER_HEADER]  WITH CHECK ADD  CONSTRAINT [FK_SALES_ORDER_HEADER_INTEGRATION_STATUS_GROUP] FOREIGN KEY([_IntegrationState])
REFERENCES [dbo].[INTEGRATION_STATUS_GROUP] ([ID])
GO

ALTER TABLE [dbo].[SALES_ORDER_HEADER] CHECK CONSTRAINT [FK_SALES_ORDER_HEADER_INTEGRATION_STATUS_GROUP]
GO


            """)
        
        sentences.append("""
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[SALES_ORDER_LINES](
    [ItemNumber] [varchar](20) NOT NULL,
    [SoldQuantity] [varchar](20) NOT NULL,
    [PricePerUnit] [float] NOT NULL,
    [Linenum] [int] NOT NULL,
    [ExternalSalesId] [varchar](20) NOT NULL,
	[_IntegrationRefId] [uniqueidentifier] NOT NULL DEFAULT (newid()),
	[_IntegrationState] [smallint] NOT NULL DEFAULT ((0)),
    [_IntegrationSourceBatchId] [uniqueidentifier] NOT NULL,
	[_IntegrationTargetBatchId] [uniqueidentifier] NULL,
	[_IntegrationTimestamp] [timestamp] NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[SALES_ORDER_LINES]  WITH CHECK ADD  CONSTRAINT [FK_SALES_ORDER_LINES_INTEGRATION_STATUS_GROUP] FOREIGN KEY([_IntegrationState])
REFERENCES [dbo].[INTEGRATION_STATUS_GROUP] ([ID])
GO

ALTER TABLE [dbo].[SALES_ORDER_LINES] CHECK CONSTRAINT [FK_SALES_ORDER_LINES_INTEGRATION_STATUS_GROUP]
GO

            """)
        ret = ""
        for s in sentences:
            ret = ret + s
            
        return ret