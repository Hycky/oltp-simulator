"""
Stream: inserção e atualização contínua e realista de eventos.
Modelo realista: sem deletes, apenas INSERT e UPDATE.
"""

import logging
import os
import random
import signal
import time
from datetime import datetime, timedelta

import psycopg2
from dotenv import load_dotenv

from scripts.data_gen import (
    generate_paciente,
    generate_consulta,
    generate_exame,
    generate_internacao,
)
from scripts.db_init import load_env, create_connection, test_connection
from scripts.validators import Validators

logger = logging.getLogger(__name__)

should_stop = False


def handle_signal(signum, frame):
    """Handler para SIGINT/SIGTERM."""
    global should_stop
    logger.info("Sinal de parada recebido. Finalizando...")
    should_stop = True


def load_config() -> dict:
    """Carrega configurações do .env."""
    load_dotenv()
    return {
        "interval": int(os.getenv("STREAM_INTERVAL_SECONDS", 2)),
        "batch_size": int(os.getenv("BATCH_SIZE", 50)),
        "max_jitter_ms": int(os.getenv("MAX_JITTER_MS", 400)),
    }


def insert_paciente(conn: psycopg2.extensions.connection, validators) -> bool:
    """Insere um novo paciente."""
    try:
        paciente = generate_paciente()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO pacientes
            (nome, nascimento, cpf, telefone, endereco, data_cadastro)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                paciente["nome"],
                paciente["nascimento"],
                paciente["cpf"],
                paciente["telefone"],
                paciente["endereco"],
                paciente["data_cadastro"],
            ),
        )
        cur.close()
        conn.commit()
        validators.clear_cache()
        return True
    except psycopg2.IntegrityError as e:
        conn.rollback()
        logger.debug(f"IntegrityError ao inserir paciente: {e}")
        return False
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inserir paciente: {e}")
        return False


def update_paciente(conn: psycopg2.extensions.connection, validators) -> bool:
    """Atualiza dados de um paciente."""
    try:
        paciente_id = validators.get_random_paciente_id()
        if not paciente_id:
            return False
        
        from faker import Faker
        fake = Faker("pt_BR")
        
        if random.choice([True, False]):
            novo_telefone = fake.phone_number()
            cur = conn.cursor()
            cur.execute("UPDATE pacientes SET telefone = %s WHERE id = %s", (novo_telefone, paciente_id))
        else:
            novo_endereco = fake.address().replace("\n", " ")
            cur = conn.cursor()
            cur.execute("UPDATE pacientes SET endereco = %s WHERE id = %s", (novo_endereco, paciente_id))
        
        cur.close()
        conn.commit()
        validators.clear_cache()
        return True
    except Exception:
        conn.rollback()
        return False


def insert_consulta(conn: psycopg2.extensions.connection, validators) -> bool:
    """Insere uma nova consulta."""
    try:
        paciente_id = validators.get_random_paciente_id()
        if not paciente_id:
            logger.debug("Nenhum paciente disponível para consulta")
            return False
        
        medico_id = validators.get_random_medico_id()
        if not medico_id:
            logger.debug("Nenhum médico disponível para consulta")
            return False
        
        consulta = generate_consulta(paciente_id, medico_id)
        
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO consultas (paciente_id, medico_id, data, motivo, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (paciente_id, medico_id, consulta["data"], consulta["motivo"], consulta["status"]),
        )
        cur.close()
        conn.commit()
        return True
    except psycopg2.IntegrityError as e:
        conn.rollback()
        logger.debug(f"IntegrityError ao inserir consulta: {e}")
        return False
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inserir consulta: {e}")
        return False


def update_consulta(conn: psycopg2.extensions.connection) -> bool:
    """Atualiza status de uma consulta."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM consultas WHERE status = 'agendada' ORDER BY RANDOM() LIMIT 1")
        result = cur.fetchone()
        
        if not result:
            cur.close()
            return False
        
        consulta_id = result[0]
        novo_status = random.choice(["realizada", "cancelada", "faltou"])
        
        cur.execute("UPDATE consultas SET status = %s WHERE id = %s", (novo_status, consulta_id))
        cur.close()
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def insert_exame(conn: psycopg2.extensions.connection, validators) -> bool:
    """Insere um novo exame."""
    try:
        paciente_id = validators.get_random_paciente_id()
        if not paciente_id:
            logger.debug("Nenhum paciente disponível para exame")
            return False
        
        exame = generate_exame(paciente_id)
        
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO exames (paciente_id, tipo_exame, data, resultado)
            VALUES (%s, %s, %s, %s)
            """,
            (paciente_id, exame["tipo_exame"], exame["data"], exame["resultado"]),
        )
        cur.close()
        conn.commit()
        return True
    except psycopg2.IntegrityError as e:
        conn.rollback()
        logger.debug(f"IntegrityError ao inserir exame: {e}")
        return False
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inserir exame: {e}")
        return False


def update_exame(conn: psycopg2.extensions.connection) -> bool:
    """Atualiza resultado de um exame."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM exames WHERE resultado IS NULL ORDER BY RANDOM() LIMIT 1")
        result = cur.fetchone()
        
        if not result:
            cur.close()
            return False
        
        exame_id = result[0]
        novo_resultado = random.choice(["Normal", "Alterado", "Positivo", "Negativo", "Pendente"])
        
        cur.execute("UPDATE exames SET resultado = %s WHERE id = %s", (novo_resultado, exame_id))
        cur.close()
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def insert_internacao(conn: psycopg2.extensions.connection, validators) -> bool:
    """Insere uma nova internação."""
    try:
        paciente_id = validators.get_random_paciente_id()
        if not paciente_id:
            logger.debug("Nenhum paciente disponível para internação")
            return False
        
        internacao = generate_internacao(paciente_id)
        
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO internacoes (paciente_id, data_entrada, data_saida, motivo, quarto)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (paciente_id, internacao["data_entrada"], internacao["data_saida"], internacao["motivo"], internacao["quarto"]),
        )
        cur.close()
        conn.commit()
        return True
    except psycopg2.IntegrityError as e:
        conn.rollback()
        logger.debug(f"IntegrityError ao inserir internação: {e}")
        return False
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inserir internação: {e}")
        return False


def update_internacao(conn: psycopg2.extensions.connection) -> bool:
    """Marca alta de internação."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM internacoes WHERE data_saida IS NULL ORDER BY RANDOM() LIMIT 1")
        result = cur.fetchone()
        
        if not result:
            cur.close()
            return False
        
        internacao_id = result[0]
        data_saida = datetime.now() - timedelta(days=random.randint(1, 10))
        
        cur.execute("UPDATE internacoes SET data_saida = %s WHERE id = %s", (data_saida, internacao_id))
        cur.close()
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def stream_loop(conn: psycopg2.extensions.connection, interval: int, max_jitter_ms: int):
    """Loop principal de stream contínuo com INSERT e UPDATE."""
    global should_stop
    
    validators = Validators(conn)
    counters = {
        "insert_paciente": 0,
        "insert_consulta": 0,
        "insert_exame": 0,
        "insert_internacao": 0,
        "update_paciente": 0,
        "update_consulta": 0,
        "update_exame": 0,
        "update_internacao": 0,
    }
    
    weights = [5, 30, 15, 20, 8, 10, 7, 5]
    events = [
        "insert_paciente", "insert_consulta", "insert_exame", "insert_internacao",
        "update_paciente", "update_consulta", "update_exame", "update_internacao",
    ]
    
    logger.info(f"Iniciando stream com intervalo {interval}s e jitter até {max_jitter_ms}ms")
    logger.info("Modelo realista: INSERT (70%) e UPDATE (30%)")
    
    cycle = 0
    while not should_stop:
        try:
            cycle += 1
            jitter = random.randint(0, max_jitter_ms) / 1000
            
            event = random.choices(events, weights=weights)[0]
            
            if event == "insert_paciente":
                insert_paciente(conn, validators)
            elif event == "insert_consulta":
                insert_consulta(conn, validators)
            elif event == "insert_exame":
                insert_exame(conn, validators)
            elif event == "insert_internacao":
                insert_internacao(conn, validators)
            elif event == "update_paciente":
                update_paciente(conn, validators)
            elif event == "update_consulta":
                update_consulta(conn)
            elif event == "update_exame":
                update_exame(conn)
            elif event == "update_internacao":
                update_internacao(conn)
            
            counters[event] += 1
            
            # Determinar tipo (INSERT ou UPDATE)
            op_type = "INSERT" if event.startswith("insert_") else "UPDATE"
            table = event.replace("insert_", "").replace("update_", "")
            
            ins = sum(v for k, v in counters.items() if k.startswith("insert_"))
            upd = sum(v for k, v in counters.items() if k.startswith("update_"))
            
            logger.info(f"[{cycle:>5}] {op_type:>6} {table:>12} | INSERT: {ins:>4} | UPDATE: {upd:>4}")
            
            sleep_time = interval + jitter
            time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            logger.info("Interrupção detectada.")
            should_stop = True
        except psycopg2.OperationalError:
            logger.error("Conexão perdida. Tentando reconectar...")
            try:
                conn.close()
            except Exception:
                pass
            
            for attempt in range(1, 6):
                try:
                    time.sleep(2 ** (attempt - 1))
                    conn = create_connection(load_env())
                    if test_connection(conn):
                        logger.info("Reconectado com sucesso.")
                        validators = Validators(conn)
                        break
                except Exception:
                    if attempt == 5:
                        logger.error("Falha permanente de conexão.")
                        should_stop = True
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            time.sleep(interval)
    
    total_ops = sum(counters.values())
    ins_total = sum(v for k, v in counters.items() if k.startswith("insert_"))
    upd_total = sum(v for k, v in counters.items() if k.startswith("update_"))
    logger.info(f"Stream encerrado: {cycle} ciclos, {total_ops} operações (INSERT: {ins_total}, UPDATE: {upd_total})")


def main(interval: int = None, batch_size: int = None):
    """Função principal de stream."""
    config = load_config()
    
    if interval is None:
        interval = config["interval"]
    if batch_size is None:
        batch_size = config["batch_size"]
    
    env_vars = load_env()
    
    conn = create_connection(env_vars)
    if not test_connection(conn):
        logger.error("Falha ao testar conexão com o banco.")
        conn.close()
        return
    
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    try:
        stream_loop(conn, interval, config["max_jitter_ms"])
    finally:
        try:
            logger.info("Fechando conexão...")
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
