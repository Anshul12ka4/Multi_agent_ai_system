import sqlite3
import pandas as pd
import json

def load_logs_to_dataframe(db_path='memory.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, source, type, intent, timestamp, sender, conversation_id, fields FROM memory")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        base = {
            "id": row[0],
            "source": row[1],
            "type": row[2],
            "intent": row[3],
            "timestamp": row[4],
            "sender": row[5],
            "conversation_id": row[6],
        }

        try:
            fields = json.loads(row[7]) if row[7] else {}
        except json.JSONDecodeError:
            fields = {}

        # Flatten everything into a single dict
        data.append({**base, **fields})

    df = pd.DataFrame(data)

    # Convert unhashable types to strings to avoid TypeError in drop_duplicates
    for col in df.columns:
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

    df_deduped = df.drop_duplicates(subset=[col for col in df.columns if col not in ["id", "timestamp"]])

    return df_deduped

if __name__ == "__main__":
    df = load_logs_to_dataframe()
    df.to_csv("logs_output.csv", index=False)
    # print("Logs exported to logs_output.csv (duplicates removed)")
    print(df)