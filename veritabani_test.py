from sqlalchemy import create_engine, text

# SSMS ve ODBC ekranımda teyit ettiğim bilgiler
SERVER = r'LAPTOP-NUKOQIM7\MSSQLSERVER02' 
DATABASE = 'master'                       
DRIVER = 'ODBC Driver 17 for SQL Server'  

# Windows Authentication ile bağlantı cümlesi
connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver={DRIVER}&trusted_connection=yes"

# Engine oluşturma
engine = create_engine(connection_string)

# Bağlantıyı test etme
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT @@VERSION"))
        
        print("✅ Bağlantı Başarılı!")
        print("-" * 50)
        print("SQL Server Bilgisi:\n", result.scalar())
        
except Exception as e:
    print("❌ Bağlantı hatası oluştu!")
    print("Hata detayı:", e)