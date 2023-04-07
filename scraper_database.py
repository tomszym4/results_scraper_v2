def writing_in_results(my_db, temp_pair):
    """Adds a new row in results table for every pair of teams"""
    cursor = my_db.cursor()
    print("Only updating in DB")
    sql = "INSERT INTO results (result, result_ht, result_ft, " \
          "goals, date, url, url_active, pair_id, is_result_bot, " \
          "is_ht_late, is_ft_late, is_late) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (temp_pair.result, temp_pair.result_ht, temp_pair.result_ft,
                         temp_pair.goals, temp_pair.date_of_match, temp_pair.url,
                         temp_pair.url_active, temp_pair.pair_id, True,
                         temp_pair.is_ht_late, temp_pair.is_ft_late, temp_pair.is_late))
    my_db.commit()
    # TODO Change also pairs if it's not updated elsewhere with total_matches etc.

    print(temp_pair.upcoming_id)
    deleting_entry(my_db, temp_pair.upcoming_id)


def deleting_entry(my_db, id_of_entry):
    cursor = my_db.cursor()
    sql = f"DELETE FROM upcoming_matches WHERE upcoming_id = {id_of_entry}"
    cursor.execute(sql)
    my_db.commit()
