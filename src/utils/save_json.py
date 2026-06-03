import json
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession

class SaveJson:
    def __init__(self):
        # Ruta directa del Volume (Unity Catalog)
        self.base_volume = "/Volumes/workspace/formula_1/formula_1"
        # Instanciar dbutils dentro de la clase
        self.spark = SparkSession.builder.getOrCreate()
        self.dbutils = DBUtils(self.spark)

    def save(self, data, entity, year, month, filename):
        # 1. Construir la ruta (Usamos month:02d para que sea 03 en vez de 3)
        partition_path = f"{self.base_volume}/{entity}/year={year}/month={month:02d}"
        
        # 2. Asegurar que el directorio existe (Nativo de Databricks)
        self.dbutils.fs.mkdirs(partition_path)
        
        # 3. RUTA DIRECTA (Sin /dbfs)
        # Los Volumes en Unity Catalog ya están mapeados al sistema de archivos local del cluster
        full_path = f"{partition_path}/{filename}"
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Guardado exitoso: {full_path}")
        except Exception as e:
            print(f"❌ Error al guardar {filename}: {e}")
            
            # 4. ÚLTIMO RECURSO: Si falla lo anterior, intentar con /dbfs explícito
            # (Solo para clusters antiguos o configuraciones específicas)
            try:
                alt_path = f"/dbfs{full_path}"
                with open(alt_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"✅ Guardado (usando /dbfs): {alt_path}")
            except Exception as alt_e:
                print(f"❌ Fallo total en {filename}: {alt_e}")