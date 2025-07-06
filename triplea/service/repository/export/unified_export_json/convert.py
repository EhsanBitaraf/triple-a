import click
from triplea.utils.general import safe_csv


class Converter:
    list_uni_model = []
    one_to_many = []
    one_to_one = []
    # Main Part of filename
    mf = "main"

    def _get_field_info(self):
        # Get first information for uni_model_fields
        d = self.list_uni_model[0]
        keys = d.keys()
        for k in keys:
            if isinstance(d[k], str):
                self.one_to_one.append(k)
            elif isinstance(d[k], int):
                self.one_to_one.append(k)
            elif isinstance(d[k], list):
                dic = {"Table": k}
                self.one_to_many.append(dic)
            elif d[k] is None:
                value = click.prompt(
                    f"""What is type of column {k}?
    (str, int, list)""",
                    type=str,
                )
                if value == "str":
                    self.one_to_one.append(k)
                elif value == "int":
                    self.one_to_one.append(k)
                elif value == "list":
                    dic = {"Table": k}
                    self.one_to_many.append(dic)
                else:
                    print("value is out of range.")
                    exit()
            else:
                print(type(d[k]))
                raise NotImplementedError

    def _create_header_one_to_one(self):
        # Create Header of main csv file - for one_to_one fields
        main = ""
        main = "ID,"
        for i in self.one_to_one:
            main = main + i + ","
        main = main[0: len(main) - 1] + "\n"
        with open(f"{self.mf}.csv", "w", encoding="utf-8") as file1:
            file1.write(main)
        file1.close()

    def _get_row_number_of_not_null_field(self, field_name):
        # value = self.list_uni_model[1][field_name]
        n = 0
        value_is_null = True
        while value_is_null:
            n = n + 1
            if n > len(self.list_uni_model):
                print("n is out of range")
                return None
            if field_name in self.list_uni_model[n]:
                value = self.list_uni_model[n][field_name]
            else:
                value = None

            if value is None:
                value_is_null = True
            else:
                if isinstance(value, list):
                    if len(value) == 0:
                        value_is_null = True
                    else:
                        value_is_null = False
                else:
                    value_is_null = False
        return n

    def _generate_sub_fields_of_field(self, field_name, one_row_of_unified_model):
        # Check Value of one to many field for detect sub fields(keys)
        value = one_row_of_unified_model[field_name]
        keys = []
        if isinstance(value, list):
            # Usually is list Because is one to many
            if len(value) == 0:
                # print(f"3) Value of {field_name} is None.")
                n = self._get_row_number_of_not_null_field(field_name)
                keys = self._generate_sub_fields_of_field(
                    field_name, self.list_uni_model[n]
                )
            else:
                one_value = value[0]
                if isinstance(one_value, dict):
                    keys = list(one_value.keys())
                elif isinstance(one_value, str):
                    keys = [field_name]
                else:
                    print(
                        f"""3) One value of {field_name} is not dict. {
                                field_name} is {type(one_value)}"""
                    )
                    print(value[0])

        elif value is None:
            # print(f"3) Value of {field_name} is None.")
            n = self._get_row_number_of_not_null_field(field_name)
            keys = self._generate_sub_fields_of_field(
                field_name, self.list_uni_model[n]
            )
        else:
            print(f"{field_name} is not list. {field_name} is {type(value)}")

        return keys

    def _complete_info_of_one_to_many_fields(self):
        # print_pretty_dict(one_to_many)
        num = 0
        while num < len(self.one_to_many):
            field_name = self.one_to_many[num]["Table"]
            # Check Type of Value
            keys = self._generate_sub_fields_of_field(
                field_name, self.list_uni_model[0]
            )
            self.one_to_many[num]["keys"] = keys
            num = num + 1

    def _create_header_one_to_many(self):
        # In This state one_to_many is complete
        for j in range(0, len(self.one_to_many)):
            field_name = self.one_to_many[j]["Table"]
            field_sub_fields = self.one_to_many[j]["keys"]
            file = open(f"{self.mf}_{field_name}.csv", "w", encoding="utf-8")
            header = ""
            header = "ID,"
            for f in field_sub_fields:
                header = header + f + ","
            header = header[0: len(header) - 1] + "\n"
            file.write(header)
            file.close()

    def _create_data_one_to_one(self, row_num):
        data = self.list_uni_model[row_num]
        # Write Value in main Table
        f_main = open(f"{self.mf}.csv", "a", encoding="utf-8")
        main = ""
        main = f"{row_num},"
        for col_name in self.one_to_one:
            col_value = ""
            if col_name in data:
                if data[col_name] is None:
                    col_value = ""
                else:
                    col_value = safe_csv(data[col_name])
            else:
                col_value = ""
            main = main + str(col_value) + ","
        main = main[0: len(main) - 1] + "\n"
        f_main.write(main)
        f_main.close()

    def _get_keys_from_one_to_many(self, field_name):
        for i in self.one_to_many:
            if i["Table"] == field_name:
                return i["keys"]

    def _get_chunk_of_csv_from_dict_value(self, col_name, value):
        main = ""
        if col_name in value:
            if isinstance(value[col_name], list):
                pass
                print("_get_chunk_of_csv_from_dict_value")
                print(f"    Not Implement. {col_name} Table in sub Table")
            elif isinstance(value[col_name], str):
                col_value = safe_csv(value[col_name])
                main = str(col_value) + ","
            elif isinstance(value[col_name], int):
                col_value = value[col_name]
                main = str(col_value) + ","
            elif isinstance(value[col_name], float):
                col_value = value[col_name]
                main = str(col_value) + ","
            elif value[col_name] is None:
                main = "" + ","
            else:
                print(type(value[col_name]))
                raise NotImplementedError
        else:
            main = "" + ","

        return main

    def _create_csv_row(self, field_name, list_value, row_num):
        # Value is list befor this state we checked
        if list_value is None:
            return
        for value in list_value:
            file = open(f"{self.mf}_{field_name}.csv", "a", encoding="utf-8")
            main = ""
            main = f"{row_num},"
            if isinstance(value, dict):
                keys = self._get_keys_from_one_to_many(field_name)
                for col_name in keys:
                    main = main + self._get_chunk_of_csv_from_dict_value(
                        col_name, value
                    )
            elif isinstance(value, str):
                col_value = safe_csv(value)
                main = main + str(col_value) + ","
            elif value is None:
                main = main + "" + ","
            else:
                pass
                print(
                    f"""_create_csv_row. value is not expected type. value is {
                        type(value)
                        }."""
                )
            main = main[0: len(main) - 1] + "\n"
            file.write(main)
            file.close()

    def _create_data_one_to_many(self, row_num):
        data = self.list_uni_model[row_num]
        for j in range(0, len(self.one_to_many)):
            field_name = self.one_to_many[j]["Table"]
            # Each field in one_to_many create new Table in seperate File
            if field_name in data:
                value = data[field_name]
            else:
                value = None
            # value must be list in one_to_many
            if isinstance(value, list):
                if len(value) == 0:
                    # Is Null
                    self._create_csv_row(field_name, None, row_num)
                else:
                    self._create_csv_row(field_name, value, row_num)
            elif value is None:
                # Is Null
                self._create_csv_row(field_name, None, row_num)
            else:
                print(
                    f"""_create_data_one_to_many. value is not expected type.
 value is {type(value)} = {value}."""
                )   # noqa: E501

    def convert_unified2csv_dynamically(self, list_output):
        self.list_uni_model = list_output
        self._get_field_info()

        # ---------------------Create Header of all csv files----------------------
        self._create_header_one_to_one()

        self._complete_info_of_one_to_many_fields()

        self._create_header_one_to_many()
        # ---------------------Create Header of all csv files----------------------

        # ---------------------Create Data of all csv files------------------------
        for i in range(0, len(self.list_uni_model)):
            self._create_data_one_to_one(i)

            self._create_data_one_to_many(i)
        # ---------------------Create Data of all csv files------------------------
