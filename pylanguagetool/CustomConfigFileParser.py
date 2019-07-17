from configargparse import DefaultConfigFileParser


class CustomConfigFileParser(DefaultConfigFileParser):
    def get_syntax_description(self):
        """
        Overwrite string to avoid printing goo.gl URL
        """
        msg = ("Config file syntax allows: key=value, flag=true, stuff=[a,b,c] "
               "(for details, see syntax at https://pypi.org/project/ConfigArgParse/).")
        return msg
