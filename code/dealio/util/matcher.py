from difflib import SequenceMatcher

def find_nik_value(row_string:str):
  row_list = row_string.split(" ")
  for word in row_list:
    seq = SequenceMatcher(None, "NIK", word)
    if seq.ratio() >= 0.7:
      return row_list[-1]
  return

def find_name_value(row_string:str):
  row_list = row_string.split(" ")
  for word in row_list:
    seq = SequenceMatcher(None, "Nama", word)
    if seq.ratio() >= 0.7:
      result = " "
      return result.join(row_list[1:])
  return

def find_gender_value(row_string:str):
  row_list = row_string.split(" ")
  for word in row_list:
    seq = SequenceMatcher(None, "Jenis", word)
    if seq.ratio() >= 0.7:
      for inner_word in row_list:
        male_seq = SequenceMatcher(None, "LAKI-LAKI", inner_word)
        female_seq = SequenceMatcher(None, "PEREMPUAN", inner_word)
        if male_seq.ratio() >= 0.7 or female_seq.ratio() >= 0.7:
          if male_seq.ratio() >= female_seq.ratio():
            return "male"
          else:
            return "female"
      return row_list[2]
  return

def find_dob_value(row_string:str):
  row_list = row_string.split(" ")
  for word in row_list:
    seq = SequenceMatcher(None, "Tempat/Tgl", word)
    if seq.ratio() >= 0.7:
      return row_list[-1]
  return