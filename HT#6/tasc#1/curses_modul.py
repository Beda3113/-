def test_modul(courses, mentors):
       all_list = []
       for m in mentors:
           all_list.extend(m)
       
       all_names_list = [mentor.split()[0] for mentor in all_list]
       unique_names = set(all_names_list)
       all_names_sorted = sorted(unique_names)
       
       return all_names_sorted

