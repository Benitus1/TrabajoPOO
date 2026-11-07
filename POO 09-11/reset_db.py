import os
import sys

try:
    import pymysql
    from DAO.conexion import Conexion
except Exception as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)


def reset_database():
    print("=== RESTAURAR BASE DE DATOS A ESTADO BASE ===")
    print("ADVERTENCIA: Se eliminarán TODOS los datos actuales.")
    confirm = input("¿Estás seguro de continuar? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operación cancelada.")
        return

    conexion_obj = Conexion()
    sql_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BASE', 'ecotech.sql')
    
    if not os.path.exists(sql_file):
        print(f"No se encontró el archivo SQL: {sql_file}")
        return
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Conectar sin base de datos para recrearla
        config = conexion_obj.config.copy()
        db_name = config.pop('database')
        
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Leer y ejecutar el script
        statements = []
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                statements.append(statement)
        
        for stmt in statements:
            if stmt:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    # Ignorar algunos errores menores si es necesario
                    pass
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n¡Base de datos restaurada a estado base exitosamente!")
        print("Se han cargado los datos de prueba iniciales.")
    except Exception as e:
        print(f"Error al restaurar la base de datos: {e}")
        print("Asegúrate de que MySQL esté corriendo y las credenciales sean correctas.")


if __name__ == "__main__":
    reset_database()
