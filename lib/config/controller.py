import configparser
import os


class Controller(object):
    def __init__(self, section):
        """Create an instance of a config controller for getting and setting information
        :param section: The default section from and to which to get and set information 
        """

        self.path = os.path.dirname(os.path.realpath(__file__)) + 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.section_default = section

    def get(self, name, section='BunqAPI'):
        """Returns a value with a given name from the configuration file."""
        return self.config[section][name]

    def set(self, name, val, section='BunqAPI'):
        """Sets an entry in the default section of the config file to a specifieg value
        :param section: [Optional] The section in which an entry should be changed
        :param name: The entry whose value should be changed
        :param val: The new value for the specified entry
        :return: Nothing, but happiness
        """
        if section not in self.config.sections():
            self.config.add_section(section)

        self.config.set(section, name, val)
        self.save()

    def save(self):
        file = open(self.path, 'w')
        self.config.write(file)
        file.close()

