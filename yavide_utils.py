class YavideUtils():
    @staticmethod
    def file_extension_to_programming_language(extension):
        if (extension == '.c' or extension == '.cpp' or extension == '.cc' or
            extension == '.h' or extension == '.hpp'):
            return 'Cxx'
        elif (extension == '.java'):
            return 'Java'
        else:
            return ''

    @staticmethod
    def programming_language_to_extension(programming_language):
        if (programming_language == 'Cxx'):
            return ['.c', '.cpp', '.cc', '.h', '.hpp']
        elif (programming_language == 'Java'):
            return ['.java']
        else:
            return ''

