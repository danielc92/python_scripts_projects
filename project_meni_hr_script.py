#SCRIPT INPUTS

#values from old columns
old_id_list = ['90',
'91',
'92',
'93',
'94',
'95',
'96',
'97',
'98']

old_fte_list = ['5',
'6',
'4',
'3',
'5',
'6',
'4',
'6',
'5']

old_status_list = ['ongoing ',
'acting',
'ongoing ',
'acting',
' ongoing',
'acting',
'acting',
' ongoing',
'acting']

#values from new columns
new_id_list = ['91',
'92',
'93',
'94',
'95',
'96',
'97',
'98',
'99',
'100']

new_fte_list = ['6',
'4',
'6',
'5',
'2',
'4',
'6',
'5',
'3',
'1']

new_status_list = ['acting',
'ongoing ',
'acting',
'acting',
'ongoing ',
'acting',
' ongoing',
'acting',
'ongoing ',
'ongoing ']

#SCRIPT OUTPUTS


#trim and uppercase all elements from each lists

for n in range(len(old_id_list)):
    old_id_list[n] = str(old_id_list[n]).strip().upper()

for n in range(len(old_fte_list)):
    old_fte_list[n] = str(old_fte_list[n]).strip().upper()
    
for n in range(len(old_status_list)):
    old_status_list[n] = str(old_status_list[n]).strip().upper()

for n in range(len(new_id_list)):
    new_id_list[n] = str(new_id_list[n]).strip().upper()
    
for n in range(len(new_fte_list)):
    new_fte_list[n] = str(new_fte_list[n]).strip().upper()
    
for n in range(len(new_status_list)):
    new_status_list[n] = str(new_status_list[n]).strip().upper()
    


#check if all the lists in new are the same size, likewise for old.

len_old_id = len(old_id_list)
len_old_fte = len(old_fte_list)
len_old_status = len(old_status_list)
len_new_id = len(new_id_list)
len_new_fte = len(new_fte_list)
len_new_status = len(new_status_list)


if len_new_fte == len_new_id == len_new_status and len_old_fte == len_old_id == len_old_status:
    print("Number of items in all old lists are identical, number of items in all new lists are also identical. Script will continue.\n")

    # create new lists to store results
    new_id = []
    existing_id = []
    dropped_id = []
    existing_changed_id = []
    existing_changed_reason = []
    existing_unchanged_id = []

    # find dropped numbers
    for number in old_id_list:

        if number not in new_id_list:
            dropped_id.append(number)

    # find existing numbers
    for number in new_id_list:

        if number not in old_id_list:
            new_id.append(number)

        elif number in old_id_list:
            existing_id.append(number)

    for number in existing_id:

        old_index = old_id_list.index(number)
        new_index = new_id_list.index(number)

        old_fte_value = old_fte_list[old_index]
        old_status_value = old_status_list[old_index]

        new_fte_value = new_fte_list[new_index]
        new_status_value = new_status_list[new_index]

        if new_fte_value == old_fte_value and old_status_value == new_status_value:
            existing_unchanged_id.append(number)

        elif new_fte_value != old_fte_value and old_status_value == new_status_value:
            existing_changed_id.append(number)
            existing_changed_reason.append("FTE has changed from "  + str(old_fte_value) + " to " + str(new_fte_value) +".")

        elif new_fte_value == old_fte_value and old_status_value != new_status_value:
            existing_changed_id.append(number)
            existing_changed_reason.append("Status has changed from " + str(old_status_value) + " to " + str(new_status_value) + ".")

        elif new_fte_value != old_fte_value and old_status_value != new_status_value:
            existing_changed_id.append(number)
            existing_changed_reason.append("FTE has changed from "  + str(old_fte_value) + " to " + str(new_fte_value) +". Status has changed from " + str(old_status_value) + " to " + str(new_status_value) + ".")

    # print results
    print("\nNEW IDS: COUNT = " + str(len(new_id)))

    for number in new_id:
        print(number)

    print("\nDROPPED IDS: COUNT = " + str(len(dropped_id)))

    for number in dropped_id:
        print(number)

    print("\nPRE-EXISTING IDS (UNCHANGED): COUNT = " + str(len(existing_unchanged_id)))

    for number in existing_unchanged_id:
        print(number)

    print("\nPRE-EXISTING IDS (CHANGED): COUNT = " + str(len(existing_changed_id)))

    for n in range(len(existing_changed_id)):
        print(existing_changed_id[n] + ": " + existing_changed_reason[n])

else:
    print("Error: Not all old lists are same length. Please check old and new list lengths below:\n")
    print("Old lists:")
    print("Length of old_id list: " + str(len_old_id))
    print("Length of old_fte list: " + str(len_old_fte))
    print("Length of old_status list: " + str(len_old_status))
    print("New lists:")
    print("Length of new_id list: " + str(len_new_id))
    print("Length of new_fte list: " + str(len_new_fte))
    print("Length of new_status list: " + str(len_new_status))



