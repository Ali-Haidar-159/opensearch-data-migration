from sqlalchemy.dialects.postgresql import insert
from config.db.connection import get_opensearch_client, get_postgres_engine
from config.db.models import users as users_table, address as address_table, activity as activity_table


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

    print(f"Fetched documents from '{index}'")
    return all_docs


def migrate():
    os_client = get_opensearch_client()
    engine    = get_postgres_engine()

    users_docs      = fetch_all_documents(os_client, "user")
    activities_docs = fetch_all_documents(os_client, "activity")

    location_map = {}
    for act in activities_docs:
        uid = act["user_id"]
        if uid not in location_map:
            location_map[uid] = []
        location_map[uid].append(act.get("location", ""))

    print("\nInserting into users table...")
    user_rows = [
        {
            "id": u["id"],
            "name": u["name"],
            "email": u["email"],
            "age": u["age"],
        }
        for u in users_docs
    ]

    with engine.begin() as conn:
        if user_rows:
            stmt = insert(users_table).values(user_rows).on_conflict_do_nothing(index_elements=["id"])
            conn.execute(stmt)

    print(f"users data inserted")


    print("\nInserting into address table...")
    address_rows = []
    for u in users_docs:
        addr      = u.get("address", {})
        locations = location_map.get(u["id"], [""])  # default empty if no activity

        for loc in locations:
            address_rows.append(
                {
                    "user_id": u["id"],
                    "street": addr.get("street"),
                    "city": addr.get("city"),
                    "country": addr.get("country"),
                    "activity_location": loc,
                }
            )

    with engine.begin() as conn:
        if address_rows:
            conn.execute(address_table.insert(), address_rows)

    print(f"address data inserted")

    print("\nInserting into activity table...")
    activity_rows = [
        {
            "id": act["id"],
            "user_id": act["user_id"],
            "action": act["action"],
            "timestamp": act["timestamp"],
            "ip_address": act["ip_address"],
        }
        for act in activities_docs
    ]

    with engine.begin() as conn:
        if activity_rows:
            stmt = insert(activity_table).values(activity_rows).on_conflict_do_nothing(index_elements=["id"])
            conn.execute(stmt)

    print(f"activities data inserted")
    
    print("\n daya migration complete")


if __name__ == "__main__":
    migrate()
