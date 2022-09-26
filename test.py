import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

from GUI import CustomButton
from GUI import Input
from GUI import LabelTag
from GUI import RandomExcursionTestItem
from GUI import TestItem
from Tools import Tools

from ApproximateEntropy import ApproximateEntropy as aet
from Complexity import ComplexityTest as ct
from CumulativeSum import CumulativeSums as cst
from FrequencyTest import FrequencyTest as ft
from Matrix import Matrix as mt
from RandomExcursions import RandomExcursions as ret
from RunTest import RunTest as rt
from Serial import Serial as serial
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut

class Main(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):

        self._test_type = ['01. Monobit Frequency Test',
                            '02. Frequency within a Block Test',
                            '03. Runs Test',
                            '04. Longest Run of ones in a Block',
                            '05. Binary Matrix Rank Test',
                            '06. Discrete Fourier Transform Test',
                            '07. Non-Overlapping Template Matching Test',
                            '08. Overlapping Template Matching Test',
                            '09. Maurer\'s Universal Stat Test',
                            '10. Linear Complexity Test',
                            '11. Serial Test',
                            '12. Approximate Entropy Test',
                            '13. Cumulative Sums Test',
                            '14. Random Excursions Test',
                            '15. Random Excursions Variant Test']


        self.__test_function = {
            0:ft.monobit_test,
            1:ft.block_frequency,
            2:rt.run_test,
            3:rt.longest_one_block_test,
            4:mt.binary_matrix_rank_text,
            5:st.spectral_test,
            6:tm.non_overlapping_test,
            7:tm.overlapping_patterns,
            8:ut.statistical_test,
            9:ct.linear_complexity_test,
            10:serial.serial_test,
            11:aet.approximate_entropy_test,
            12:cst.cumulative_sums_test,
            13:ret.random_excursions_test,
            14:ret.variant_test
        }

        self._test_result = []
        self._test_string = []

    def init_window(self):
        frame_title = 'NTU Randomness Testing System'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)
        input_label_frame = LabelFrame(self.master, text="Input Stream")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0)
        input_label_frame.place(x=20, y=30, width=1260, height=125)
        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 5)
        self.__binary_data_file_input = Input(input_label_frame, 'Binary Data File', 10, 35, True,
                                              self.select_binary_file, button_xcoor=1060, button_width=160)


        self._stest_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self._stest_selection_label_frame.config(font=("Calibri", 14))
        self._stest_selection_label_frame.place(x=20, y=155, width=1240, height=450)

        test_type_label_01 = LabelTag(self._stest_selection_label_frame, 'Test Type', 10, 5, 250, 10, border=2,
                                   relief="groove")
        p_value_label_01 = LabelTag(self._stest_selection_label_frame, 'P-Value', 265, 5, 235, 10, border=2,
                                 relief="groove")
        result_label_01 = LabelTag(self._stest_selection_label_frame, 'Result', 505, 5, 110, 10, border=2,
                                relief="groove")

        test_type_label_02 = LabelTag(self._stest_selection_label_frame, 'Test Type', 620, 5, 250, 10, border=2,
                                      relief="groove")
        p_value_label_02 = LabelTag(self._stest_selection_label_frame, 'P-Value', 875, 5, 235, 10, border=2,
                                    relief="groove")
        result_label_02 = LabelTag(self._stest_selection_label_frame, 'Result', 1115, 5, 110, 10, border=2,
                                   relief="groove")

        self._test = []

        self._monobit = TestItem(self._stest_selection_label_frame, self._test_type[0], 10, 35, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._monobit)

        self._block = TestItem(self._stest_selection_label_frame, self._test_type[1], 620, 35, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._block)

        self._run = TestItem(self._stest_selection_label_frame, self._test_type[2], 10, 60, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._run)

        self._long_run = TestItem(self._stest_selection_label_frame, self._test_type[3], 620, 60, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._long_run)

        self._rank = TestItem(self._stest_selection_label_frame, self._test_type[4], 10, 85, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._rank)

        self._spectral = TestItem(self._stest_selection_label_frame, self._test_type[5], 620, 85, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._spectral)

        self._non_overlappong = TestItem(self._stest_selection_label_frame, self._test_type[6], 10, 110, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._non_overlappong)

        self._overlapping = TestItem(self._stest_selection_label_frame, self._test_type[7], 620, 110, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._overlapping)

        self._universal = TestItem(self._stest_selection_label_frame, self._test_type[8], 10, 135, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._universal)

        self._linear = TestItem(self._stest_selection_label_frame, self._test_type[9], 620, 135, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._linear)

        self._serial = TestItem(self._stest_selection_label_frame, self._test_type[10], 10, 160, serial=True, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11, two_columns=True)
        self._test.append(self._serial)

        self._entropy = TestItem(self._stest_selection_label_frame, self._test_type[11], 10, 185, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._entropy)

        self._cusum_f = TestItem(self._stest_selection_label_frame, self._test_type[12], 10, 210, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._cusum_f)

        self._excursion = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[13], 10, 235,
                                                   ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4'], font_size=11)
        self._test.append(self._excursion)

        self._variant = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[14], 10, 325,
                                                 ['-9.0', '-8.0', '-7.0', '-6.0', '-5.0', '-4.0', '-3.0', '-2.0',
                                                  '-1.0',
                                                  '+1.0', '+2.0', '+3.0', '+4.0', '+5.0', '+6.0', '+7.0', '+8.0',
                                                  '+9.0'], variant=True, font_size=11)
        self._test.append(self._variant)

        self._result_field = [
            self._monobit,
            self._block,
            self._run,
            self._long_run,
            self._rank,
            self._spectral,
            self._non_overlappong,
            self._overlapping,
            self._universal,
            self._linear,
            self._serial,
            self._entropy,
            self._cusum_f,
        ]

        select_all_button = CustomButton(self.master, 'All Tests', 20, 615, 100, self.select_all)
        execute_button = CustomButton(self.master, 'Execute Test', 150, 615, 100, self.execute)
        save_button = CustomButton(self.master, 'Save as Text File', 285, 615, 100, self.save_result_to_file)

    def select_binary_file(self):
        print('Select Binary File')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data(self.__file_name)
            #self.__string_data_file_input.set_data('')
            self.__is_binary_file = True
            self.__is_data_file = False

    def select_data_file(self):
        print('Select Data File')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Data File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data('')
            self.__string_data_file_input.set_data(self.__file_name)
            self.__is_binary_file = False
            self.__is_data_file = True



    def select_all(self):

        print('Select All Test')
        for item in self._test:
            item.set_check_box_value(1)

    def execute(self):
        print('Execute')

        if len(self.__binary_input.get_data().strip().rstrip()) == 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) == 0:
            messagebox.showwarning("Warning",
                                   'You must input the binary data or read the data from from the file.')
            return None
        elif len(self.__binary_input.get_data().strip().rstrip()) > 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) > 0:
            messagebox.showwarning("Warning",
                                   'You can either input the binary data or read the data from from the file.')
            return None

        input = []

        if not len(self.__binary_input.get_data()) == 0:
            input.append(self.__binary_input.get_data())
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            temp = []
            if self.__file_name:
                handle = open(self.__file_name)
            for data in handle:
                temp.append(data.strip().rstrip())
            test_data = ''.join(temp)
            input.append(test_data[:1000000])
        elif not len(self.__string_data_file_input.get_data()) == 0:
            data = []
            count = 1
            if self.__file_name:
                handle = open(self.__file_name)
            for item in handle:
                if item.startswith('http://'):
                    url = Tools.url_to_binary(item)
                    data.append(Tools.string_to_binary(url))
                else:
                    data.append(Tools.string_to_binary(item))
                count += 1
            print(data)
            input.append(''.join(data))

        for test_data in input:
            count = 0
            results = [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()]
            for item in self._test:
                if item.get_check_box_value() == 1:
                    print(self._test_type[count], ' selected. ', self.__test_function[count](test_data))

                    results[count] = self.__test_function[count](test_data)
                count += 1
            self._test_result.append(results)

        self.write_results(self._test_result[0])
        messagebox.showinfo("Execute", "Test Successful")

    def write_results(self, results):

        count = 0
        for result in results:
            if not len(result) == 0:
                if count == 10:
                    self._result_field[count].set_p_value(result[0][0])
                    self._result_field[count].set_result_value(self.get_result_string(result[0][1]))
                    self._result_field[count].set_p_value_02(result[1][0])
                    self._result_field[count].set_result_value_02(self.get_result_string(result[1][1]))
                elif count == 13:
                    print(result)
                    self._excursion.set_results(result)
                elif count == 14:
                    print(result)
                    self._variant.set_results(result)
                else:
                    self._result_field[count].set_p_value(result[0])
                    self._result_field[count].set_result_value(self.get_result_string(result[1]))


            count += 1

    def save_result_to_file(self):
        print('Save to File')
        print(self._test_result)
        if not len(self.__binary_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data:' + self.__binary_input.get_data() + '\n\n\n')
            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File save finished.  You can check the output file for complete result.")
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data File:' + self.__binary_data_file_input.get_data() + '\n\n\n')
            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File Saved.")

    def write_result_to_file(self, output_file, result):
        for count in range(15):
            if self._test[count].get_check_box_value() == 1:
                if count == 10:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][0][0]), self.get_result_string(result[count][0][1]))
                    output_file.write(output)
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][1][0]), self.get_result_string(result[count][1][1]))
                    output_file.write(output)
                    pass
                elif count == 13:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'Chi Squared', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                elif count == 14:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'COUNTS', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                else:
                    output = '%-50s\t%-20s\t%s\n' % (
                    self._test_type[count], str(result[count][0]), self.get_result_string(result[count][1]))
                    output_file.write(output)
            count += 1

    def get_result_string(self, result):
        if result == True:
            return 'Random'
        else:
            return 'Non-Random'

if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    root.geometry("%dx%d+0+0" % (1300, 650))
    title = 'NTU Randomness Testing System'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()