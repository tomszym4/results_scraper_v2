

def writing_in_results(my_db, temp_pair):
    """Adds a new row in results table for every pair of teams"""
    cursor = my_db.cursor()
    print("Only updating in DB")
    minutes_as_string = ''.join(temp_pair.goals)
    sql = "INSERT INTO results (result, result_ht, result_ft," \
          "goals, date, postponed, url, url_active, pair_id)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (temp_pair.result, temp_pair.result_ht, temp_pair.result_ft,
                         minutes_as_string, temp_pair.date_of_match,
                         temp_pair.match_postponed, temp_pair.url,
                         temp_pair.url_active, temp_pair.pair_id))
    my_db.commit()

    #  TODO deleting upcoming_matches entry
    print(temp_pair.upcoming_id)
    deleting_entry(my_db, temp_pair.upcoming_id)


def deleting_entry(my_db, id_of_entry):
    cursor = my_db.cursor()
    sql = f"DELETE FROM upcoming_matches WHERE upcoming_id = {id_of_entry}"
    cursor.execute(sql)
    my_db.commit()
