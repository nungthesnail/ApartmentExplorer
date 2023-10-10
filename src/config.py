import json


day_length = 86400
update_rate = day_length / 2
result_avg_time_change = 7
result_apartment_view_count = 10

with open("env.json", "r") as f:
    env = json.load(f)
    bot_token = env["bot-token"]
    db_path = env["db-path"]
    avito_url = env["avito-url"]
    cian_url = env["cian-url"]
