from flask import Flask, jsonify
import redis
import requests
import mysql.connector
import time

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379, decode_responses=True)

DB_HOST = 'db'
DB_USER = 'root'
DB_PASSWORD = 'example'
DB_DATABASE = 'ecommerce'

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
            )
            print("Conexão com o MySQL estabelecida com sucesso!")
            return db
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")
            retries -= 1
            print(f"Tentando novamente em 5 segundos... ({retries} retentativas restantes)")
            time.sleep(5)
    raise Exception("Não foi possível conectar ao MySQL após várias tentativas.")

@app.route('/order')
def create_order():
    cached_products = cache.get('products_list')
    products_data = None

    if cached_products:
        print("Produtos obtidos do cache Redis.")
        products_data = eval(cached_products)
    else:
        print("Produtos não encontrados no cache. Buscando da API de Produtos.")
        try:
            r = requests.get('http://products:3000/products')
            r.raise_for_status()
            products_data = r.json()['produtos']
            cache.setex('products_list', 60, str(products_data))
            print("Produtos armazenados no cache Redis.")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar à API de Produtos: {e}")
            return jsonify({"error": "Falha ao obter produtos da API de Produtos"}), 500
        except KeyError:
            print("Formato de resposta inesperado da API de Produtos.")
            return jsonify({"error": "Formato de resposta inválido da API de Produtos"}), 500

    if not products_data:
        return jsonify({"error": "Nenhum produto disponível"}), 500
    
    if not isinstance(products_data, list) or not products_data:
        return jsonify({"error": "Formato de produtos inválido ou lista vazia"}), 500

    product = products_data[0]

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                quantity INT,
                total_price INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

        quantity = 2
        total_price = product['price'] * quantity
        cursor.execute(
            "INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s)",
            (product['id'], quantity, total_price)
        )
        db.commit()
        order_id = cursor.lastrowid
        print(f"Pedido {order_id} salvo no MySQL.")

        return jsonify({
            "order_id": order_id,
            "product_id": product['id'],
            "quantity": quantity,
            "total_price": total_price
        })
    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return jsonify({"error": f"Erro no banco de dados: {err}"}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)