from DAO.conexion import Conexion

def test():
    conexion_obj = Conexion()
    try:
        conn = conexion_obj.conectar()
        print(">>> Conexion exitosa! :D <<<")
        conn.close()
    except Exception as e:
        print(f">>> Error de conexion: {e} <<<")

if __name__ == "__main__":
    test()
