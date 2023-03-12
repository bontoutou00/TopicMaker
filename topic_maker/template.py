import re
from string import Template
from constants import DATA_PATH

class Templates:
    """Class of template"""
    def complete_template(self, data:dict):
        """
        The complete_template function takes a dictionary as an argument and returns the template.txt file with all of its placeholders replaced by the values in the dictionary.\n
        Args:
            data: dict: Pass the dictionary of data to the function\n
        Returns:
            A string
        """
        with open(f'{DATA_PATH}/template.txt', 'r', encoding='utf8') as f:
            src = Template(f.read())
            try:
                result = src.safe_substitute(data)
            except KeyError as error:
                print(error)
            else:
                result = re.sub(r'.*"None".*\n?',"", result)
                result = re.sub(r'(\$\w+)',"", result)
                return result
