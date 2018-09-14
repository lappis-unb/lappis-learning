import pickle


class Storage:

    def save(self, file_path, data):
        with open(file_path, 'wb') as output_file:
            pickle.dump(data, output_file, pickle.DEFAULT_PROTOCOL)


    def load(self, file_path, on_error_callback = None):
        try:
            with open(file_path, 'rb') as input_file:
                loaded_object = pickle.load(input_file)

            return loaded_object

        except:
            if on_error_callback:
                on_error_callback()
