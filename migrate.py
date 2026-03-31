from connection import get_opensearch_client, get_postgres_conn


def fetch_all_documents(client, index):
    all_docs = []

    response  = client.search(
        index=index,
        body={"query": {"match_all": {}}},
        scroll="2m",   
        size=100      
    )
    scroll_id = response["_scroll_id"]
    hits      = response["hits"]["hits"]

    while hits:
        all_docs.extend([hit["_source"] for hit in hits])

        response  = client.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = response["_scroll_id"]
        hits      = response["hits"]["hits"]

    print(f"Fetched {len(all_docs)} documents from '{index}'")
    return all_docs


def migrate():
    os_client = get_opensearch_client()
    pg_conn   = get_postgres_conn()
    cur       = pg_conn.cursor()

    users      = fetch_all_documents(os_client, "user")
    activities = fetch_all_documents(os_client, "activity")

    location_map = {}
    for act in activities:
        uid = act["user_id"]
        if uid not in location_map:
            location_map[uid] = []
        location_map[uid].append(act.get("location", ""))

    print("\nInserting into users table...")
    user_insert_count = 0
    for u in users:
        cur.execute("""
            INSERT INTO users (id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            u["id"],
            u["name"],
            u["email"],
            u["age"]
        ))
        user_insert_count += 1

    print(f"{user_insert_count} users inserted")


    print("\nInserting into address table...")
    address_insert_count = 0
    for u in users:
        addr      = u.get("address", {})
        locations = location_map.get(u["id"], [""])  # default empty if no activity

        for loc in locations:
            cur.execute("""
                INSERT INTO address (user_id, street, city, country, activity_location)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                u["id"],
                addr.get("street"),
                addr.get("city"),
                addr.get("country"),
                loc
            ))
            address_insert_count += 1

    print(f"   {address_insert_count} address rows inserted")

    print("\nInserting into activity table...")
    activity_insert_count = 0
    for act in activities:
        cur.execute("""
            INSERT INTO activity (id, user_id, action, timestamp, ip_address)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            act["id"],
            act["user_id"],
            act["action"],
            act["timestamp"],
            act["ip_address"]
        ))
        activity_insert_count += 1

    print(f" {activity_insert_count} activities inserted")

    # Commit and close 
    pg_conn.commit()
    cur.close()
    pg_conn.close()
    print("\n Migration complete!")


if __name__ == "__main__":
    migrate()
